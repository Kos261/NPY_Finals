import argparse
# from alco_analysis.stats import summary
from alco_analysis.loading_data import load_data

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This is package for alcohol concesion data analysis in Poland")
    # parser.add_argument("--summary", help="Show short summary of data (mean, median etc.)")
    parser.add_argument('-f1',"--file_conc", help="Provide concesion data file path")
    parser.add_argument('-f2',"--file_fire", help="Provide fire incident data file path")

    args = parser.parse_args()
    # print(args.filein)

    if args.file_conc and args.file_fire:
        df_conc, df_fire = load_data(args.file_conc, args.file_fire)

    # RUN $ python run_analysis.py -f1 data/alcohol_companies.csv -f2 data/incidents.csv