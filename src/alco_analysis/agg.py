import pandas as pd

def count_conc_city(df):
    has_lat = 'lat' in df.columns
    has_lon = 'lon' in df.columns

    if has_lat and has_lon:
        df_conc_count = (df.groupby('city', as_index=False)
        .agg(n_conc = ('city', 'size'),    # liczba wierszy = liczba koncesji
            lon    = ('lon',  'first'),   # dowolna, każda koncesja w mieście ma te same wsp.
            lat    = ('lat',  'first')))
    else:
        df_conc_count = (df.groupby('city', as_index=False).agg(n_conc = ('city', 'size')))
            
    return df_conc_count    

def count_conc_woj(df):
    df_conc_count_woj = df.groupby('woj', as_index=False).agg(n_conc = ('woj', 'size'))
    # liczba wierszy = liczba koncesji
            
    return df_conc_count_woj


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


def merge_conc_population(df_conc, df_pop, debug=False):
    merged = (df_conc.merge(df_pop, on=['woj'], how='left', indicator=True))
    return merged 

def merge_pop_events(df_conc, df_events, df_pop):
    city2woj = (df_conc[['city', 'woj']]
                .drop_duplicates()          
                .set_index('city')['woj']
                .to_dict())
    
    df_fire_woj = (df_events.assign(woj=lambda d: d['city'].map(city2woj)).dropna(subset=['woj']))

    fire_by_woj = (df_fire_woj.groupby('woj', as_index=False).agg(n_fire=('RAZEM Pożar (P)', 'sum')))
    
    df_corr = (fire_by_woj.merge(df_pop[['woj', 'n_pop']], on='woj', how='inner'))

    return df_corr