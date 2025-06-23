import pandas as pd
from scipy import stats
from alco_analysis.agg import (merge_conc_cities,
                               count_conc_city, 
                               count_conc_woj, 
                               merge_conc_population,
                               merge_pop_events)
import statsmodels.api as sm
import numpy as np
from pathlib import Path

DEFAULT_TARGETS = {
    "RAZEM Pożar (P)" : "Pożary (razem)",
    "Mały (P/M)" :"P - małe",
    "Średni (P/Ś)" : "P - średnie",
    "Duży (P/D)" : "P - duże",
    "Bardzo duży (P/BD)":"P - bardzo duże",
    "RAZEM Miejscowe zagrożenie (MZ)" : "Miejscowe zagrożenia (razem)",
    "Małe (MZ/M)" : "MZ - małe",
    "Średnie (MZ/Ś)" : "MZ - średnie",
    "Lokalne (MZ/L)" : "MZ - lokalne",
    "Gigantyczne lub klęska żywiołowa (MZ/K)" : "MZ - katastrofalne",
}


def correlation_conc_events(df_conc, df_cities, df_events, targets: list[str] | None = None) -> pd.DataFrame:
    """
    targets : list[str] | None
    Columns from df_events, from which we calculate corr.
    If None -> use DEFAULT_TARGETS.
    """
    targets = targets or list(DEFAULT_TARGETS.keys())

    merged = merge_conc_cities(df_conc, df_cities)
    df_conc_count = count_conc_city(merged)
    df_all = df_conc_count.merge(df_events, on="city", how="inner")

    records = []
    for col in targets:
        if col not in df_all:
            continue
        r = df_all[["n_conc", col]].corr(method="pearson").iloc[0, 1]
        records.append({"zdarzenie": DEFAULT_TARGETS.get(col, col) + " vs koncesja", "Pearson": r})

    return pd.DataFrame(records)


def correlation_conc_pop(df_conc, df_pop):

    conc_count_woj = count_conc_woj(df_conc)
    df_conc_pop = merge_conc_population(conc_count_woj, df_pop)
    corr_pop = df_conc_pop[["n_conc", "n_pop"]].corr(method="pearson").iloc[0, 1]

    return corr_pop


def correlation_pop_events(df_conc, df_events, df_pop):
    df_corr = merge_pop_events(df_conc, df_events, df_pop)
    corr_pop_eve = df_corr[['n_fire', 'n_pop']].corr(method='pearson').iloc[0,1]
    return corr_pop_eve


def summary(output_folder, *args):
    for i,arg in enumerate(args):
        desc = arg.describe(include="all").transpose() 
        file_path = Path(output_folder, f"summary_{i}.csv")
        desc.to_csv(file_path)