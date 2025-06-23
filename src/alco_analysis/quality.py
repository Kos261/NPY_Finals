import pandas as pd

def report(df_cities, df_conc, df_events) -> pd.DataFrame:
    df_missing = pd.DataFrame({
        "missing_lonlat": df_cities[['lon','lat']].isna().any(axis=1).sum(),
        "duplicate_city": df_cities.duplicated('city').sum(),
        "conc_without_city": df_conc['city'].isna().sum(),
        "events_without_city": df_events['city'].isna().sum(),
    }, index=[0])
    return df_missing