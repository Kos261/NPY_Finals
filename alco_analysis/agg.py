import pandas as pd

def count_conc(df):
    df_conc_count = (
    df.groupby('city', as_index=False)
    .agg(n_conc = ('city', 'size'),    # liczba wierszy = liczba koncesji
         lon    = ('lon',  'first'),   # dowolna – i tak każda koncesja w mieście ma te same wsp.
         lat    = ('lat',  'first')))
    return df_conc_count

def merge_df_on_city(df1,df2):
    '''This function connects dataframes by cities'''
    df_sum = pd.merge(df1, df2, on="city", how="inner")
    # df_sum = df_sum.size().reset_index(name='liczba_sklepów')
    return df_sum

def merge_conc_cities(df_conc, df_cities, debug=False):
    merged = (df_conc.merge(df_cities, on=['city'], how='left', indicator=True)) 

    vc = merged['_merge'].value_counts()

    if debug:
        print("Dopasowane   :", vc.get('both', 0))
        print("Niedopasowane:", vc.get('left_only', 0))
        print("Nie­użyte     :", vc.get('right_only', 0))

    missing = merged.loc[merged['_merge'] == 'left_only', 'city']

    percent = vc.get('left_only', 0)/(vc.get('both', 0) + vc.get('left_only', 0))*100
    
    if debug:
        print("Koncesje bez lokalizacji przydzielonego miasta")
        print(missing.unique())
        print(f"\n\tDropping {vc.get('left_only', 0)} rows ({percent:.2f}% of data)")
    merged.dropna(subset=["lon", "lat"], inplace=True)

    return merged