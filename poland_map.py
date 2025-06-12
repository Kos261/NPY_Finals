import folium
from folium.plugins import HeatMap
from pathlib import Path

from alco_analysis.stats import count_concession
from alco_analysis.loading_data import load_data


df_conc, df_events, df_cities, df_conc_location = load_data(args.file_conc,
                                                            args.file_fire,
                                                            args.file_cities)

df_conc = count_concession(df_conc)

POL_X , POL_Y = 52.1, 19.4

m = folium.Map(location=[POL_X, POL_Y], zoom_start=6, tiles='CartoDB positron')

# dane do heatmapy
heat_data = [
    [row["lat"] + POL_X, row["lon"] + POL_Y, float(row["Liczba_koncesji"])]
    for _, row in df_conc_location.iterrows()
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
