import pandas as pd
from alco_analysis.features import *
import io
from pathlib import Path
from charset_normalizer import from_bytes


def load_cities(filepath_cities, debug=False):
    df_cities = pd.read_fwf(filepath_cities, 
                                header=None, 
                                colspecs=[(0, 23), (24, 38), (39, 50)],
                                names=["Miejscowość", "Długość", "Szerokość"],
                                skiprows=1)
    # df_cities.name = filepath_cities[:-4]

    rows_before = df_cities.shape[0]

    df_cities.columns = df_cities.columns.str.strip()
    df_cities["Miejscowość"] = df_cities["Miejscowość"].str.strip()
    
    df_cities = df_cities.dropna(subset=["Miejscowość", "Długość", "Szerokość"])


    pat = r'^(.*?)\s*\((.*?)\)$'                 # "Adamów (siedleckie)"
    df_cities[['city', 'tag']] = df_cities['Miejscowość'].str.extract(pat)
    df_cities['city'] = df_cities['city'].fillna(df_cities['Miejscowość']) 
    # df_cities["woj"] = df_cities["tag"].map(tag2woj)


    df_cities["lon"] = df_cities["Długość"].apply(dms_to_decimal)
    df_cities["lat"] = df_cities["Szerokość"].apply(dms_to_decimal)

    df_cities = df_cities.drop(['Miejscowość'], axis=1)
    # new_order = ['city', 'tag','woj', 'Szerokość','Długość', 'lon', 'lat']
    new_order = ['city', 'tag','Szerokość','Długość', 'lon', 'lat']
    df_cities = df_cities[new_order] 

    df_cities['city'] = df_cities['city'].apply(norm_city)
    # df_cities['woj']  = df_cities['woj'].apply(norm_woj)

    rows_after = df_cities.shape[0]
    rows_deleted = rows_before - rows_after
    if debug:
        print("\n###CITIES DATAFRAME###\n")
        # print(df_cities.head(5))
    if rows_deleted > 0:
        print(f"Deleted {rows_deleted} rows")
        

    return df_cities

def load_concession(filepath_conc, debug=False):
    df_conc = pd.read_csv(filepath_conc)
    # print(df_conc)
    df_conc = df_conc[['Miejscowość','Data ważności','Województwo']]
    rows_before = df_conc.shape[0]
    df_conc = df_conc.dropna()
    
    df_conc["woj"]   = df_conc["Województwo"].str.replace(r"^WOJ\.\s*", "", regex=True).str.upper()
    df_conc = df_conc.drop(['Województwo'], axis=1)
    df_conc = df_conc.set_axis(['city', 'date', 'woj'], axis=1)

    df_conc['city'] = df_conc['city'].apply(norm_city)
    df_conc['woj']  = df_conc['woj'].apply(norm_woj)
    #Czasem koncesja jest do kilku miast naraz :( muszę wywalić te nadmiarowe
    df_conc = take_first_city(df_conc)

    rows_after = df_conc.shape[0]
    rows_deleted = rows_before - rows_after
    if debug:
        print("\n###CONCESSION DATAFRAME###\n")
        # print(df_conc.head(5))
    if rows_deleted > 0:
        print(f"Deleted {rows_deleted} rows")
        
    
    return df_conc

def load_events(filepath_events, debug=False):
    # enc = detect_encoding(filepath_events)
    df_events = pd.read_csv(filepath_events, encoding="iso-8859-2")
    # df_events = read_csv_clean(filepath_events,debug=True)
   

    rows_before = df_events.shape[0]
    df_events = df_events.dropna()
    df_events = cut_KPPSP_in_city_names(df_events)
    df_events.rename(columns={"Miejscowość":"city"}, inplace=True)
    df_events['city'] = df_events['city'].apply(norm_city)

    rows_after = df_events.shape[0]
    rows_deleted = rows_before - rows_after

    if debug:
        print("\n###EVENTS DATAFRAME###\n")
        print(df_events.head(5))
    if rows_deleted > 0:
        print(f"Deleted {rows_deleted} rows")
   
    return df_events

def load_population(filepath_pop, debug=False):
    xls = pd.ExcelFile(filepath_pop)
    df = xls.parse('województwa', skiprows=8, index_col=None, na_values=['NA'])

    #Powinno być 16 województw
    df_pop = df.iloc[:, :2].copy()
    df_pop.columns = ["woj", "n_pop"]
    df_pop["woj"] = df_pop["woj"].apply(norm_woj)
    # df_pop.name = filepath_pop[:-5]

    if debug:
        print("\n###POPULATION DATAFRAME###\n")
        print(df_pop.head(5))
    return df_pop

def load_data(filepath_conc, filepath_events, filepath_cities, filepath_pop, debug=False):
    df_conc = load_concession(filepath_conc, debug)
    df_events = load_events(filepath_events, debug)
    df_cities = load_cities(filepath_cities, debug)
    df_pop = load_population(filepath_pop, debug)

    return df_conc, df_events, df_cities, df_pop 

