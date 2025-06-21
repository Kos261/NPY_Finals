import pandas as pd


def correlation_fire(df_sum):
    corr_pearson = df_sum["Liczba_koncesji"].corr(df_sum["RAZEM Pożar (P)"])
    print(f"Korelacja Pearsona między liczbą koncesji a łączną ilością pożarów: {corr_pearson:.3f}")

def spatial_correlation(df_sum):
    pass
