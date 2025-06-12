import pandas as pd

def clean_city_names(df):
    #Aleksandrów Kujawski i Różno Parcele są razem nie wiedzieć czemu ale dobra
    df["Miejscowość"] = df["Nazwa KP/M PSP"].apply(lambda x: " ".join(x.split()[2:]))
    df = df.drop(["Nazwa KP/M PSP","Nazwa KW PSP"], axis=1)
    return df

def dms_to_decimal(coord):
    import re
    match = re.match(r"(\d+)°(\d+)'?([NSEW])", coord.strip())
    if not match:
        return None
    degrees, minutes, direction = match.groups()
    decimal = float(degrees) + float(minutes) / 60
    if direction in ['W', 'S']:
        decimal = -decimal
    return decimal

def load_cities(filepath_cities, debug=True):
    df_cities = pd.read_fwf(filepath_cities, 
                                header=None, 
                                colspecs=[(0, 24), (25, 39), (40, 50)],
                                names=["Miejscowość", "Długość", "Szerokość"],
                                skiprows=1)

    df_cities.columns = df_cities.columns.str.strip()
    df_cities["Miejscowość"] = df_cities["Miejscowość"].str.strip()
    # Miejscowość             Długość        Szerokość
    df_cities = df_cities.dropna(subset=["Miejscowość", "Długość", "Szerokość"])

    df_cities["lon"] = df_cities["Długość"].apply(dms_to_decimal)
    df_cities["lat"] = df_cities["Szerokość"].apply(dms_to_decimal)
    if debug:
        print("\n###CITIES DATAFRAME###\n")
        print(df_cities.head(5))

    return df_cities

def load_concession(filepath_conc, debug=True):
    df_conc = pd.read_csv(filepath_conc) #usecols=['Data ważności', 'Miejscowość']
    df_conc = df_conc.dropna()
    if debug:
        print("\n###CONCESSION DATAFRAME###\n")
        print(df_conc.head(5))
    
    return df_conc

def load_events(filepath_events, debug=True):
    df_events = pd.read_csv(filepath_events)
    df_events = df_events.dropna()
    df_events = clean_city_names(df_events)

    if debug:
        print("\n###EVENTS DATAFRAME###\n")
        print(df_events.head(5))
        
    return df_events

def load_data(filepath_conc, filepath_events, filepath_cities):
    df_conc = load_concession(filepath_conc)
    df_events = load_events(filepath_events)
    df_cities = load_cities(filepath_cities)

    df_conc_location = pd.merge(df_conc, df_cities, on="Miejscowość", how="inner")

    # col_names = df.column_name
    return df_conc, df_events, df_cities, df_conc_location     

