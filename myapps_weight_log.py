import os; import traceback; import os.path ; import platform; import sys; 
from matplotlib.dates import datestr2num
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# weight loss data :
#      date      weight(kg)  comment
log=[
     ('2023-5-9', 79.5, 'eless'), 
     ('2023-5-10', 79.4, '29+32'),
     ('2023-05-11', 78.1, 'eless,25'),
     ('2023-05-15', 77.8, '33+26'),
     ('2023-05-24', 78.2, 'eat too more'),
     ('2023-05-26', 77.3, '13+27'),
     ('2023-05-27', 77.5, '34+22'),
     ('2023-05-30', 77.1, ''),
     ('2023-05-31', 76.9, ''),
     ('2023-06-01', 76.8, '32+24'),
     ('2023-06-02', 76.6, '33+25'),
     ('2023-06-03', 76.2, ''),
     ('2023-06-03', 76.5, ''),
     ('2023-06-03', 76.5, ''),
     ('2023-06-11', 76.3, ''),
     ('2023-06-12', 76, ''),
     ('2023-06-13', 75.8, ''),
     ('2023-06-15', 75.6, ''),
     ('2023-06-16', 75.4, ''),
     ('2023-07-01', 74.7, ''),
     ('2023-07-03', 75.4, ''),
     ('2023-07-04', 74.8, ''),
     ('2023-07-10', 74.6, ''),
     ('2023-07-12', 74.1, ''),
     ('2023-07-16', 73.6, ''),
     ('2023-07-19', 73.8, ''),
     ('2023-8-1', 72, 'KEYSTONE'), #target weight in future
     ('2023-10-1', 68, 'KEYSTONE'),#target weight in future
     ('2023-12-1', 64, 'KEYSTONE'),#target weight in future
    ]

# 设置中文字体
plt.rcParams['font.family'] = ['SimHei']

dates = [datetime.strptime(record[0], '%Y-%m-%d') for record in log]
weights = [record[1]*2 for record in log]
comments = [record[2] for record in log]

# draw line of weight changes.
plt.plot(dates, weights)

# draw a line from start to end
plt.plot([dates[0], dates[-1]], [weights[0], weights[-1]], color='orange', linestyle='--')
# plt.plot([dates[0], dates[-1]], [weights[0] - 1, weights[-1] - 1], color='green', linestyle='--')

# Set the date format of the x-axis to month.day
date_formatter = DateFormatter('%m.%d')
plt.gca().xaxis.set_major_formatter(date_formatter)

# display comment in the plot
from datetime import datetime

#loop logs from end to start, break when found where coment != 'KEYSTONE'
for i in range(len(comments)-1,-1,-1):
    if comments[i] != 'KEYSTONE':
        idx = i+1
        weights_latest=weights[i]
        date_latest=dates[i]
        break

weights_start=weights[0]
date_start=dates[0]

#calc from weights_start/date_start and weights_latest/date_latest, get estimate weight at dates[-1]
days_diff_current = (date_latest - date_start).days
days_diff_totally = (dates[-1] - date_start).days
actual_weight_loss = weights_start - weights_latest

weight_loss_planned=weights_start - weights[-1]
# calc percent of weight_diff to weight_planned 
percent = (actual_weight_loss / weight_loss_planned) * 100.0
percent_days = (days_diff_current /days_diff_totally) * 100.0

actual_avg_weight_loss_per_day = 0.9 * actual_weight_loss / days_diff_current
target_avg_weight_loss_per_day = weight_loss_planned / days_diff_totally

# draw percent on plot
# add percent to lablel of plot
date_end = dates[-1]
estimate_weight = weights_latest - actual_avg_weight_loss_per_day * ((date_end) - date_latest).days
print("avg_weight_loss_per_day {}".format(actual_avg_weight_loss_per_day))
print("Estimated weight at {}: {}".format(date_end, round(estimate_weight, 2)))

# titles
title_est='Estimated weight at {}: {}'.format(date_end, round(estimate_weight, 1))
title_actual="Actual Statistic : Percent {:.2f}% daily:{:.2f} ".format(percent, actual_avg_weight_loss_per_day)
title_actual1='Actual total:(kg/2):{:.1f} monthly:{:.1f}'.format(actual_weight_loss, actual_avg_weight_loss_per_day*30)
title_plan='plan: target:{:.1f} monthly:{:.1f}'.format(weight_loss_planned, target_avg_weight_loss_per_day*30)
title_plan_time='times changes:  {:.2f}%  days:{} totaldays:{}'.format(percent_days, days_diff_current, days_diff_totally)
plt.title(f"{title_est}\n{title_actual}\n{title_actual1}\n{title_plan}\n{title_plan_time}")

#loop logs from end to start, break when found where coment != 'KEYSTONE'
for i in range(len(comments)-1,-1,-1):
    if comments[i] == 'KEYSTONE':
        days_diff_current = (dates[i] - date_latest).days
        estimate_weight=weights_latest - actual_avg_weight_loss_per_day * days_diff_current
        plt.plot(dates[i], estimate_weight, 'ro', markersize=6)
        plt.text(dates[i], estimate_weight, "{:.1f}".format(estimate_weight))

# display comment in the plot
for i in range(len(log)):
    x = dates[i]
    xd = dates[i]
    y = weights[i]
    comment = comments[i]

    if xd.day == 1:
        comment = "!"

    plt.text(x, y, comment)

# Draw a vertical line at the current date
current_date = datetime.now().date()
plt.axvline(x=current_date, color='red', linestyle='--')    

plt.text(date_latest, weights_latest, weights_latest, color='red', fontsize=12)

# Set horizontal axis label and vertical axis label
plt.xlabel('Date')
plt.ylabel('Weight (catty)')

# display graphics on screen
plt.show()