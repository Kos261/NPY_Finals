import argparse
import cProfile
import re
from pathlib import Path

from alco_analysis.io import load_data
from alco_analysis.agg import merge_conc_cities, count_conc_city
from alco_analysis.stats import (summary, 
                                 correlation_conc_events,
                                 correlation_conc_pop,
                                 correlation_pop_events)

from alco_analysis.heat_map import create_heatmap

# cProfile.run('re.compile("foo|bar")')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This is package for alcohol concesion data analysis in Poland")
    # parser.add_argument("--summary", help="Show short summary of data (mean, median etc.)")
    parser.add_argument('-f1',"--file_conc", help="Provide concesion data file path")
    parser.add_argument('-f2',"--file_fire", help="Provide fire incident data file path")
    parser.add_argument('-f3',"--file_cities", help="Provide city location data file path")
    parser.add_argument('-f4',"--file_population", help="Provide population data file path")
    parser.add_argument('-o', "--output_folder", help="Provide path for statistical output file")

    args = parser.parse_args()
    output_folder = Path(args.output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    if args.file_conc and args.file_fire and args.file_cities and args.file_population:

        df_conc, df_events, df_cities, df_pop = load_data(args.file_conc, 
                                                          args.file_fire,
                                                          args.file_cities,
                                                          args.file_population)

    summary(output_folder, df_conc, df_events, df_pop)


    # Calculating correlation table

    df_corr = correlation_conc_events(df_conc, df_cities, df_events)
    df_corr

    corr_conc_pop = correlation_conc_pop(df_conc, df_pop)
    # print("Korelacja między populacją województwa ilością koncesji",corr_conc_pop)

    df_corr.loc[-1] = ["Populacja vs ilość koncesji", corr_conc_pop]
    df_corr.index = df_corr.index + 1  # shifting index
    df_corr = df_corr.sort_index() 


    corr_pop_ev = correlation_pop_events(df_conc, df_events, df_pop) 
    # print("Korelacja między populacją województwa a ilością pożarów",corr_conc_pop)

    df_corr.loc[-1] = ["Populacja vs liość pożarów (RAZEM)", corr_pop_ev]
    df_corr.index = df_corr.index + 1  # shifting index
    df_corr = df_corr.sort_index() 



    df_corr.to_csv(output_folder/"corr_notebook.csv")

    create_heatmap(df_conc, df_events, df_cities, output_folder)


    '''
    RUN $ python run_analysis.py    \
        -f1 data/concession.csv     \
        -f2 data/events.csv         \
        -f3 data/cities.csv         \
        -f4 data/rezydenci_2023.xlsx\
        -o output/
    

    STREAMLIT $streamlit run run_analysis.py -- \
    -f1 data/concession.csv         \
    -f2 data/events.csv             \
    -f3 data/cities.csv

    PROFILE $ python -m cProfile    \
        -o output/temp.dat          \
        run_analysis.py             \
        -f1 data/concession.csv     \
        -f2 data/events.csv         \
        -f3 data/cities.csv         \
        -f4 data/rezydenci_2023.xlsx\
        -o output/

    SHOW PROFILE snakeviz output/temp.dat
    '''