import pandas as pd
import numpy as np
import pytest
import pathlib
from pathlib import Path
from tabulate import tabulate

from alco_analysis.io import (
    load_concession,
    load_events,
    load_cities,
    load_data,
    norm_city,
)


#There is no builtin function or method to save fwf files :(
def to_fwf(df, fname):
    content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
    open(fname, "w").write(content)

pd.DataFrame.to_fwf = to_fwf




@pytest.fixture
def tiny_files(tmp_path):
    conc_path = Path("tests","resources", "concession.csv")
    cities_path = Path("tests","resources", "cities.csv")
    events_path = Path("tests","resources", "events.csv")
    pop_path = Path("tests","resources", "rezydenci_2023.xlsx")
    
    #Concessions
    df_conc = pd.read_csv(conc_path).head(10).copy()
    df_conc.loc[0, "Miejscowość"] = np.nan
    df_conc.loc[1, "Miejscowość"] += ", " + df_conc.loc[1, "Miejscowość"]
    temp_conc_path = Path(tmp_path,"conc.csv")
    df_conc.to_csv(temp_conc_path, index=False, encoding='utf-8')

    #Events
    df_events = pd.read_csv(events_path).head(10).copy()
    df_events.loc[0, "Nazwa KP/M PSP"] = "KP PSP Cokolwiek " + df_events.loc[0, "Nazwa KP/M PSP"]
    temp_events_path = Path(tmp_path , "events.csv")
    df_events.to_csv(temp_events_path, index=False, encoding='utf-8')

    #Cities
    cols = [(0, 24), (25, 39), (40, 50)]
    df_cities = pd.read_fwf(cities_path, colspecs=cols, header=None,
                         names=["Miejscowość", "Długość", "Szerokość"]).head(10)
    df_cities.loc[1, "Miejscowość"] += " (testest)"
    df_cities.loc[2, "Długość"] = "1000"
    temp_cities_path = Path(tmp_path, "cities.fwf")
    df_cities.to_fwf(temp_cities_path)

    #Population
    temp_pop_path = Path(tmp_path , "rezydenci_2023.xlsx")
    df_pop = pd.read_excel(pop_path,sheet_name="województwa")
    df_pop.to_excel(temp_events_path, index=False)

    paths = {"conc":   temp_conc_path,
             "events": temp_events_path,
             "cities": temp_cities_path,
             "population": temp_pop_path}
    
    return paths


def test_load_concession_shape_and_columns(tiny_files):
    df = load_concession(tiny_files["conc"], debug=False)
    # Column names
    assert list(df.columns) == ["city", "date", "woj"]
    # NaN deleted
    assert df["city"].notna().all()
    # Normalised strings
    assert all(df["city"].map(lambda x: x == norm_city(x)))

    
def test_load_concession_first_city_split(tiny_files):
    df = load_concession(tiny_files["conc"], debug=False)
    # No comma "," -> split_cities works
    assert df["city"].str.contains(",").sum() == 0


def test_load_events_columns_no_kpps(tiny_files):
    df = load_events(tiny_files["events"], debug=False)
    # No KP/M or PSP
    assert "Nazwa KP/M PSP" not in df.columns
    assert "Nazwa KW PSP"   not in df.columns
    # Normalised strings
    assert df["city"].map(lambda x: x == norm_city(x)).all()


def test_load_cities_lon_lat_numeric(tiny_files):
    df = load_cities(tiny_files["cities"], debug=False)
    # columns 'lon' and 'lat' are numeric
    assert "lon" in df.columns and "lat" in df.columns
    assert df["lon"].dtype.kind in "fi" and df["lat"].dtype.kind in "fi"

def test_load_cities_unique_city_key(tiny_files):
    df = load_cities(tiny_files["cities"], debug=False)
    # po drop_duplicates nie powinno być duplikatów miasta+tag
    assert not df.duplicated(subset=["city", "tag"]).any()


def test_load_data_returns_three_df(tiny_files):
    df_conc, df_events, df_cities, df_pop = load_data(
        tiny_files["conc"],
        tiny_files["events"],
        tiny_files["cities"],
        tiny_files["population"]
    )
    assert isinstance(df_conc,  pd.DataFrame)
    assert isinstance(df_events,  pd.DataFrame)
    assert isinstance(df_cities, pd.DataFrame)
    assert isinstance(df_pop, pd.DataFrame)
    
    assert set(df_conc.columns)  >= {"city", "date", "woj"}
    assert "city" in df_events.columns
    assert set(df_cities.columns) >= {"city", "lon", "lat"}
    assert set(df_pop.columns) >= {'woj', 'n_pop'}