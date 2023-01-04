import pandas as pd
from os import listdir
from os.path import isfile, join

#This code is used to combined different .csv that were collected for different years or months.

years = [2017, 2018, 2019, 2020]

final_ticker_list = []
for yr in years:
    path = "data/%s/" % str(yr)

    list_files = [f for f in listdir(path) if isfile(join(path, f))]

    ticker_file = [file.split("_")[0] for file in list_files]
    final_ticker_list = final_ticker_list + ticker_file

final_ticker_list = list(set(final_ticker_list))
print(final_ticker_list)

for tick in final_ticker_list:
    df_ticker = pd.DataFrame()

    for yr in years:
        path_file = "data/" + str(yr) +"/" + tick + "_" + str(yr) + ".csv"
        try:
            df_year = pd.read_csv(path_file, low_memory=False, lineterminator='\n')
        except FileNotFoundError:
            df_year = pd.DataFrame()
        df_ticker = pd.concat([df_ticker, df_year], axis=0)
    print(tick, df_ticker.created_at.min(), df_ticker.created_at.max(), )
    path_file_cb = "data/combined/%s.csv" % tick 
    df_ticker.to_csv(path_file_cb)
