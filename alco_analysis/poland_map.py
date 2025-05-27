import regex as re
import pandas as pd
from stats import count_concession
import folium
from folium.plugins import HeatMap

def dms_to_decimal(coord):
    import re
    match = re.match(r"(\d+)°(\d+)'?([NSEW])", coord.strip())
    if not match:
        return None
    degrees, minutes, direction = match.groups()
    decimal = float(degrees) + float(minutes) / 60
    if direction in ['W', 'S']:
        decimal = -decimal
    return decimal


df = pd.read_csv("../data/concession.csv")
df.columns = df.columns.str.strip()
df["Miejscowość"] = df["Miejscowość"].str.strip()

df = count_concession(df)
# print(df.head(3))

df_cities = pd.read_fwf(
    "../data/miasta.csv", 
    header=None, 
    colspecs=[(0, 24), (25, 39), (40, 50)],
    names=["Miejscowość", "Długość", "Szerokość"],
    skiprows=1
)
# print(df_cities.columns)
df_cities.columns = df_cities.columns.str.strip()
df_cities["Miejscowość"] = df_cities["Miejscowość"].str.strip()

# print(df_cities.head(3))

df = df.merge(df_cities, on="Miejscowość", how="inner")
# print(df.head(3))


df["lon"] = df["Długość"].apply(dms_to_decimal)
df["lat"] = df["Szerokość"].apply(dms_to_decimal)


df_filtered = df.dropna(subset=["lat", "lon", "Liczba_koncesji"])

POL_X , POL_Y = 52.1, 19.4

m = folium.Map(location=[POL_X, POL_Y], zoom_start=6, tiles='CartoDB positron')

# dane do heatmapy
heat_data = [
    [row["lat"] + POL_X, row["lon"] + POL_Y, float(row["Liczba_koncesji"])]
    for _, row in df_filtered.iterrows()
]

HeatMap(
    heat_data,
    radius=20,
    blur=15,
    max_zoom=13,
    min_opacity=0.4,
    gradient={0.4: 'blue', 0.6: 'lime', 0.8: 'orange', 1.0: 'red'}
).add_to(m)


folium.LayerControl().add_to(m)

m.save("mapa_koncesji.html")
print("Mapa została zapisana jako mapa_koncesji.html")
