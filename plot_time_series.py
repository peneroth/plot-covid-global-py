
import csv
import numpy as np
import matplotlib.pyplot as plt

# https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv
csv_file = 'time_series_covid19_deaths_global_1218.csv'

# Determine data set size!
cvs_row_count = 0
cvs_column_width = 0
with open(csv_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        cvs_row_count += 1
        if len(row) > cvs_column_width:
            cvs_column_width = len(row)
rows = cvs_row_count-1
columns = cvs_column_width-4

print("columns = ", columns)

# Load data set
dead_acc = np.zeros((rows,columns))
country = []
region = []
with open(csv_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in readCSV:
        if line_count == 0:
            dates = row[4:cvs_column_width]
            line_count += 1
        else:
            country.append(row[1])
            region.append(row[0])
            dead_acc[line_count-1,:] = row[4:cvs_column_width]
            line_count += 1

# Remove the last days, due to delayed statistics
columns -= 0

# Calculate deaths per day, and smoothen the curve by averaging
dead_day = np.zeros((rows,columns))
dead_day[:,0] = dead_acc[:,0]
dead_day[:,1:columns] = dead_acc[:,1:columns] - dead_acc[:,0:columns-1]

win_len = 7 # must be an odd number
win_step = round((win_len-1)/2)
dead_mean = np.zeros((rows,columns-win_step))
for i in range(0,rows):
    for j in range(win_step,columns-win_step):
        dead_mean[i,j] = sum(dead_day[i,j-win_step:j+win_step])/win_len

# find selected contries
c1 = 'Sweden'
c2 = 'Italy'
c3 = 'Spain'
c4 = 'US'
c5 = 'France'
c6 = 'Brazil'
c7 = 'United Kingdom'
c8 = 'Denmark'
c9 = 'Germany'

index1 = country.index(c1)
index2 = country.index(c2)
index3 = country.index(c3)
index4 = country.index(c4)
index5 = country.index(c5)+10 # skip xxx
index6 = country.index(c6)
index7 = country.index(c7)+10 # skip Bermuda, Cayman Islands, Channel Islands, Gibraltar, Isle of Man, Montserrat + more
index8 = country.index(c8)+2 # skip xxx
index9 = country.index(c9)

y1 = dead_mean[index1,:]/10 * 10 # per 100000
y2 = dead_mean[index2,:]/60 * 10 # per 100000
y3 = dead_mean[index3,:]/47 * 10 # per 100000
y4 = dead_mean[index4,:]/328 * 10 # per 100000
y5 = dead_mean[index5,:]/67 * 10 # per 100000
y6 = dead_mean[index6,:]/210 * 10 # per 100000
y7 = dead_mean[index7,:]/67 * 10 # per 100000
y8 = dead_mean[index8,:]/5.8 * 10 # per 100000
y9 = dead_mean[index9,:]/83 * 10 # per 100000

x = np.linspace(1,len(y1),len(y1))
plt.plot(x,y1,label=c1)
plt.plot(x,y2,label=c2) # x+18
plt.plot(x,y3,label=c3) # x+10
plt.plot(x,y4,label=c4)
plt.plot(x,y5,label=c5)
plt.plot(x,y6,label=c6)
plt.plot(x,y7,label=c7)
plt.plot(x,y8,label=c8)
plt.plot(x,y9,label=c9)
plt.xlabel('days')
plt.ylabel('deaths per 100000 per day')
plt.title("Data set = " + csv_file)
plt.legend()
plt.show()

