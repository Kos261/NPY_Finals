import pandas as pd

def count_concession(df):
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




def different_correlations(df_sum):
    corr_pearson = df_sum["Liczba_koncesji"].corr(df_sum["RAZEM Pożar (P)"])
    print(f"Korelacja Pearsona między liczbą koncesji a łączną ilością pożarów: {corr_pearson:.3f}")



def summary(*args):
    for arg in args:
        print(arg.describe())
    