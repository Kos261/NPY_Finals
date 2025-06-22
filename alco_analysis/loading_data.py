import pandas as pd
import numpy as np
import unidecode, re



def cut_KPPSP_in_city_names(df):
    #Aleksandrów Kujawski i Różno Parcele są razem nie wiedzieć czemu ale dobra
    df["Miejscowość"] = df["Nazwa KP/M PSP"].apply(lambda x: " ".join(x.split()[2:]))
    df = df.drop(["Nazwa KP/M PSP","Nazwa KW PSP"], axis=1)
    return df

def clean_city_names(txt):
    """Zdejmuje polskie znaki, spacje, zamienia na lower-case
       i odcina dopiski w nawiasie."""
    txt = unidecode.unidecode(str(txt)).lower().strip()
    # np. "Adamów (siedleckie)" -> "adamow"
    return re.sub(r"\s*\(.*\)$", "", txt)

def norm_city(txt):
    return unidecode.unidecode(str(txt)).lower().strip()

def norm_woj(txt):
    return (str(txt)
            .replace("WOJ.", "")
            .replace("WOJ", "")
            .strip()
            .upper())

def split_cities(raw):
    # rozdziel po przecinku lub średniku
    parts = re.split(r'[;,]', str(raw))
    return [norm_city(p) for p in parts if p.strip()]

def take_first_city(df):
    tmp = df.copy()
    # print(tmp.head(5))
    tmp['city'] = tmp['city'].apply(lambda x: split_cities(x)[0])
    return tmp

def dms_to_decimal(coord):
    import re
    match = re.match(r"(\d+)°(\d+)'?([NSEW])", coord.strip())
    if not match:
        return None
    degrees, minutes, direction = match.groups()
    decimal = float(degrees) + float(minutes) / 60
    if direction in ['W', 'S']:
        decimal = -decimal
    decimal = round(decimal,4)
    return decimal



def load_cities(filepath_cities, debug=True):
    df_cities = pd.read_fwf(filepath_cities, 
                                header=None, 
                                colspecs=[(0, 24), (25, 39), (40, 50)],
                                names=["Miejscowość", "Długość", "Szerokość"],
                                skiprows=1)
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

def load_concession(filepath_conc, debug=True):
    df_conc = pd.read_csv(filepath_conc, usecols=['Miejscowość','Data ważności','Województwo'])
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

def load_events(filepath_events, debug=True):
    df_events = pd.read_csv(filepath_events)
    rows_before = df_events.shape[0]
    df_events = df_events.dropna()
    df_events = cut_KPPSP_in_city_names(df_events)
    df_events.rename(columns={"Miejscowość":"city"}, inplace=True)
    df_events['city'] = df_events['city'].apply(norm_city)

    rows_after = df_events.shape[0]
    rows_deleted = rows_before - rows_after

    if debug:
        print("\n###EVENTS DATAFRAME###\n")
        # print(df_events.head(5))
    if rows_deleted > 0:
        print(f"Deleted {rows_deleted} rows")
   
    return df_events

def load_data(filepath_conc, filepath_events, filepath_cities):
    df_conc = load_concession(filepath_conc)
    df_events = load_events(filepath_events)
    df_cities = load_cities(filepath_cities)

    return df_conc, df_events, df_cities # , df_conc_location     

