import pandas as pd



def load_data(filepath_conc, filepath_fire):
    df1 = pd.read_csv(filepath_conc)
    df2 = pd.read_csv(filepath_fire)
    # saved_column = df.column_name
    print(df1.columns)
    print(df2.columns)

    return df1, df2      

