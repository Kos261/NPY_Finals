import argparse
from alco_analysis.loading_data import load_data
from alco_analysis.stats import count_concession, summary, merge_df_on_city, different_correlations

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This is package for alcohol concesion data analysis in Poland")
    # parser.add_argument("--summary", help="Show short summary of data (mean, median etc.)")
    parser.add_argument('-f1',"--file_conc", help="Provide concesion data file path")
    parser.add_argument('-f2',"--file_fire", help="Provide fire incident data file path")

    args = parser.parse_args()
    # print(args.filein)

    if args.file_conc and args.file_fire:
        df_conc, df_events = load_data(args.file_conc, args.file_fire)

    # summary(df_conc, df_events)
    conc_num = count_concession(df=df_conc)

    # print(conc_num.head(5))
    # print(df_events.head(5))

    df_sum = merge_df_on_city(conc_num, df_events)
    print(df_sum.head(5))
    print(df_sum.columns)


    different_correlations(df_sum)
    # RUN $ python run_analysis.py -f1 data/concession.csv -f2 data/events.csv