import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import astropy.time as mytm
import astropy.io.fits as fitsio
from matplotlib.dates import DateFormatter
from datetime import datetime
from sqlalchemy import create_engine
from TSI_PLOT_LIB_JTSIM_pandas import create_HKfig, create_Irradfig, plot_HK_1, plot_HK_2, plot_SCI_1 

# https://stackoverflow.com/questions/5734438/how-to-create-a-month-iterator
def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        year, month = divmod( ym, 12 )
        yield year, month+1

hk_plotPostFix = "HK_Plot_monthly.png"
rad_plotPostFix = "RAD_Plot_monthly.png"
save_folder = './plots/monthly/'

# hk_plotPostFix = "_HK_Plot.pdf"
# rad_plotPostFix = "_RAD_Plot.pdf"

version = " / 0.1"

conn_string = "mysql+mysqlconnector://dev:password@localhost:3306/test_db"
conn_string = "mysql+mysqlconnector://dara_dev:password@localhost:3306/dara"

engine = create_engine(
    conn_string
)

start_year = 2022
start_month = 6
end_year = 2023
end_month = 12

num_years = end_year - start_year
num_months = end_month - start_month # TODO fix this doesn't work if monrths go over new year
year = 2022
# for month in range(start_month, start_month + num_months + 1):
for year, month in month_year_iter(start_month, start_year, end_month, end_year):
    print(f'----- {year}-{month:02d} -----')
    housekeeping_query = f"SELECT * FROM housekeeping WHERE MONTH(timestamp) = {month} and YEAR(timestamp) = {year} order by timestamp;"
    df_housekeeping = pd.read_sql(housekeeping_query, con=engine)
    df_housekeeping.columns = map(str.lower, df_housekeeping.columns)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_housekeeping)}")

    calibration_query = f"SELECT * FROM calibration WHERE MONTH(timestamp) = {month} and YEAR(timestamp) = {year} order by timestamp;"
    df_calibration = pd.read_sql(calibration_query, con=engine)
    df_calibration.columns = map(str.lower, df_calibration.columns)
    print("Finish loading data from DB")
    print(f"Rows loaded {len(df_calibration)}")

    cavity_map = {"a": 1, "A": 1, "b": 2, "B": 2, "c": 3, "C":3, "none": 0, None: 0}
    df_calibration["nominal_cavity"] = df_calibration["nominal_cavity"].map(
        lambda x: cavity_map.get(x, 0)
    ).astype(np.uint8)
    df_calibration["reference_cavity"] = df_calibration["reference_cavity"].map(
        lambda x: cavity_map.get(x, 0)
    ).astype(np.uint8)
    df_calibration["backup_cavity_1"] = df_calibration["backup_cavity_1"].map(
        lambda x: cavity_map.get(x, 0)
    ).astype(np.uint8)


    plotname = '_'.join([str(year), f'{month:02d}', "01", hk_plotPostFix])
    print(f"plotname: {plotname}")
    # day_data = df_resampled[df_resampled["timestamp"].dt.date == day]
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
    plot_HK_1(df_housekeeping, ax, "month")
    fig.savefig(save_folder + plotname)
    plt.close(fig)
    
    plotname = '_'.join([str(year), f'{month:02d}', "02", hk_plotPostFix])
    print(f"plotname: {plotname}")
    fig, ax = create_HKfig("FY-3 JTSIM DARA HK " + plotname + version)
    plot_HK_2(df_housekeeping, ax, "month")
    fig.savefig(save_folder + plotname)
    plt.close(fig)
    # continue
    plotname = '_'.join([str(year), f'{month:02d}', "03", rad_plotPostFix])
    print(f"plotname: {plotname}")
    # fig, ax = create_HKfig("FY-3 JTSIM DARA RAD " + plotname + version)
    fig, ax = create_Irradfig("FY-3 JTSIM DARA RAD " + plotname + version)
    plot_SCI_1(df_calibration, ax, "month")
    fig.savefig(save_folder + plotname)
    plt.close(fig)

exit()