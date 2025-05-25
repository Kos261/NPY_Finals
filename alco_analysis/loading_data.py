import pandas as pd

def clean_city_names(df):
    #Aleksandrów Kujawski i Różno Parcele są razem nie wiedzieć czemu ale dobra
    df["Miejscowość"] = df["Nazwa KP/M PSP"].apply(lambda x: " ".join(x.split()[2:]))
    df = df.drop(["Nazwa KP/M PSP","Nazwa KW PSP"], axis=1)
    return df

def load_data(filepath_conc, filepath_fire):
    df_conc = pd.read_csv(filepath_conc)
    df_events = pd.read_csv(filepath_fire)

    df_events = clean_city_names(df_events)
    # col_names = df.column_name
    # print(df_conc.head(5))
    # print(df_events.head(5))

    return df_conc, df_events      

