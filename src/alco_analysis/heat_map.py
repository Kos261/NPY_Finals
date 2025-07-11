import folium
from folium.plugins import HeatMap
from pathlib import Path
from alco_analysis.agg import count_conc_city, merge_conc_cities

POL_X , POL_Y = 52.1, 19.4

def create_heatmap(df_conc, df_events, df_cities, output_folder):
    merged = merge_conc_cities(df_conc, df_cities)
    df_count = count_conc_city(merged)
    df_all = (df_count.merge(df_events, on='city', how='inner'))
    # This is for location of each concession

    m = folium.Map(location=[POL_X, POL_Y], zoom_start=6, tiles='CartoDB positron')

    heat_conc_data = [
        [row["lat"], row["lon"],
        float(row["n_conc"])] for _, row in df_all.iterrows()
    ]

    conc_map = HeatMap(
        heat_conc_data,
        radius=20,
        blur=15,
        max_zoom=13,
        min_opacity=0.4,
        gradient={0.4: 'blue', 0.6: 'lime', 0.8: 'orange', 1.0: 'red'},
        name="Heatmap of concessions"
    )
    conc_map.add_to(m)    


    heat_fire = HeatMap(
        data=df_all[['lat', 'lon', 'RAZEM Pożar (P)']].values.tolist(),
        name="Heatmap of fire events",
        radius=20, 
        blur=15, 
        max_zoom=13,
        min_opacity=0.4,
        gradient={0.4: 'purple', 0.6: 'violet', 0.8: 'magenta', 1.0: 'red'}
    )
    heat_fire.add_to(m)


    folium.LayerControl(collapsed=False).add_to(m)

    map_path = Path(output_folder,"mapa_koncesji.html")
    m.save(map_path)
    print("Mapa została zapisana jako 'mapa_koncesji.html'")

    return m

# def create_heatmap(merged):
#     st.map(merged)