import pandas as pd

def count_concession(df):
    miasta = df.groupby('Miejscowość').size().reset_index(name='Liczba_koncesji')
    # print(miasta.max(axis=0))
    # print(miasta)
    return miasta

def merge_df_on_city(df1,df2):
    '''This function connects dataframes by cities'''
    df_sum = pd.merge(df1, df2, on="Miejscowość", how="inner")
    # df_sum = df_sum.size().reset_index(name='liczba_sklepów')
    return df_sum

def different_correlations(df_sum):
    korelacja = df_sum["Liczba_koncesji"].corr(df_sum["RAZEM Pożar (P)"])
    print(f"Korelacja Pearsona między liczbą koncesji a łączną ilością pożarów: {korelacja:.3f}")


def summary(*args):
    for arg in args:
        print(arg.describe())
    