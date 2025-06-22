import pandas as pd
from scipy import stats
from alco_analysis.agg import merge_conc_cities, count_conc

def correlation(df_conc, df_cities, df_events):
    merged = merge_conc_cities(df_conc, df_cities, debug=True)
    df_conc_count = count_conc(merged)
    df_corr = (df_conc_count.merge(df_events, on='city', how='inner'))

    # print(df_conc_count)
    corr_pearson = df_corr[['n_conc', 'RAZEM Pożar (P)']].corr().iloc[0,1]
    return corr_pearson


def summary(*args):
    for arg in args:
        print(arg.describe())
    # Pareto-Lorenz??