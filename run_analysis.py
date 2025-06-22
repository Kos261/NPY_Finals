import argparse
from alco_analysis.io import load_data
from alco_analysis.agg import merge_conc_cities, count_conc
from alco_analysis.stats import summary, correlation
from alco_analysis.heat_map import create_heatmap
import cProfile
import re
# cProfile.run('re.compile("foo|bar")')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This is package for alcohol concesion data analysis in Poland")
    # parser.add_argument("--summary", help="Show short summary of data (mean, median etc.)")
    parser.add_argument('-f1',"--file_conc", help="Provide concesion data file path")
    parser.add_argument('-f2',"--file_fire", help="Provide fire incident data file path")
    parser.add_argument('-f3',"--file_cities", help="Provide city location data file path")

    args = parser.parse_args()

    if args.file_conc and args.file_fire:
        df_conc, df_events, df_cities = load_data(args.file_conc, 
                                                  args.file_fire,
                                                  args.file_cities)

    merged = merge_conc_cities(df_conc, df_cities)

    pearson = correlation(df_conc, df_cities, df_events)
    # print("Pearson =", round(pearson, 3))
    
    create_heatmap(merged)
    '''
    RUN $ python run_analysis.py -f1 data/concession.csv -f2 data/events.csv -f3 data/cities.csv
    
    STREAMLIT $streamlit run run_analysis.py -- \
    -f1 data/concession.csv \
    -f2 data/events.csv     \
    -f3 data/cities.csv
    PROFILE $ python -m cProfile -o temp.dat run_analysis.py -f1 data/concession.csv -f2 data/events.csv -f3 data/cities.csv

    SHOW PROFILE snakeviz temp.dat
    '''