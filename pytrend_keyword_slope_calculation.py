from pytrends.request import TrendReq
import pandas as pd
import os
import csv
import glob
from dateutil.relativedelta import relativedelta
import time
import datetime
from datetime import datetime, date, time


os.getcwd()
os.chdir('/home/karina/Documents/pyseo/kwsSlope/')

pytrend = TrendReq()
searchKeywords = []

for row in csv.reader(open('/home/karina/Documents/pyseo/kwsSlope/keywords.csv')):
	searchKeywords.append(row[0])

def chunks(items, chunkSize):
	for i in range(0, len(items), chunkSize):
		yield items[i:i+chunkSize]


print(list(chunks(searchKeywords, 5)))

# putting it all together (copying in calls to pytrends library to calculate interest_over_time)
for chunkIndex, chunk in enumerate(chunks(searchKeywords, 5)):
    print('%2d) getting google trends for %s...' % (chunkIndex+1, chunk), end='')
    chunkOutputFile="chunk%02d.csv" % (chunkIndex+1)
    pytrend.build_payload(kw_list=chunk, timeframe='today 5-y', geo='GB')
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df.to_csv(path_or_buf='/home/karina/Documents/pyseo/kwsSlope/chunks/' + chunkOutputFile)
    print('done, saved to %s' % chunkOutputFile)


path =r"/home/karina/Documents/pyseo/kwsSlope/chunks/"   # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
df_from_each_file = (pd.read_csv(f) for f in all_files)
#concatenated_df = pd.concat(df_from_each_file, axis=1, join_axes=[df.index])
concatenated_df = pd.concat(df_from_each_file, axis=1)
concatenated_df_clean = (concatenated_df.drop('date',1)).drop('isPartial',1)
concatenated_df_clean


#https://stackoverflow.com/questions/14941097/selecting-pandas-column-by-location
df_dates_file = pd.read_csv('/home/karina/Documents/pyseo/kwsSlope/chunks/chunk01.csv')
df_date_export = concatenated_df.iloc[:, 0]



#https://chrisalbon.com/python/data_wrangling/pandas_join_merge_dataframe/
final_result = pd.concat([df_date_export,concatenated_df_clean], axis=1)
final_result


#give me the current year and month
yearToday = datetime.now().strftime('%Y')
lastYear = (datetime.now() - relativedelta(years=1)).strftime('%Y')
prevYear = (datetime.now() - relativedelta(years=2)).strftime('%Y')

lastYearResults = final_result[(final_result['date'] > lastYear) & (final_result['date'] < yearToday)]
prevYearResults = final_result[(final_result['date'] > prevYear) & (final_result['date'] < lastYear)]

#https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers
keywords_to_check = list(final_result)

last_year_mean = lastYearResults[keywords_to_check].mean()
prev_year_mean = prevYearResults[keywords_to_check].mean()

xlast = last_year_mean 
xprev = prev_year_mean
ylast = int(lastYear)
yprev = int(prevYear)


def slope_formula(xlast,xprev,ylast,yprev):
	return (xlast-xprev)/(ylast-yprev)

keywordFinallist = ((slope_formula(xlast,xprev,ylast,yprev))).to_csv(path="/home/karina/Documents/pyseo/kwsSlope/trends_slope.csv", encoding="utf-8")