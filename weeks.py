import csv
import math
import pandas as pd
import numpy
import datetime as dt
import matplotlib.pyplot as plt
import pylab
import sys


def run():
    df = pd.read_csv('out.csv', parse_dates=['timestamp'],
            header=0, skiprows=[1,2], index_col='timestamp')
    rm = pd.rolling_mean(df.resample("60Min", fill_method="ffill"), 
            window=3, min_periods=1)
    df['traffic'].plot()
    #rm['traffic'].plot()
    # pylab.ion()
    # pylab.show()

    import ipdb; ipdb.set_trace() # BREAKPOINT
    kw = lambda x: x.isocalendar()[1]
    by_week = df.groupby([df.index.map(kw)], sort=False)

    for each_week in xrange(0, 52):
        try:
            by_week.get_group(each_week).to_csv('out-week{0}.csv'.format(each_week), header=True, index=True)
            print('Created {0}'.format(each_week))
        except KeyError, e:
            pass
        except:
            raise

        
#    rm.to_csv('rec-center-hourly_out.csv', header=True, index=True)

    sys.exit(0)


    for idx in xrange(len(lines)):
        if not lines[idx][2]:
            lines_list.append(numpy.nan)
        else:
            lines_list.append(float(lines[idx][2]))
    import ipdb; ipdb.set_trace() # BREAKPOINT
    lines_array = numpy.array(lines_list)
    lines_interpolated = Series(lines_array).interpolate().values

    import ipdb; ipdb.set_trace() # BREAKPOINT
    rm = rolling_mean(lines_interpolated, window=3, min_periods=1)

    with open('f.out', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(["timestamp", "traffic"])
        writer.writerow(["datetime", "float"])
        writer.writerow(["", ""])

        for idx in xrange(len(lines)):
            writer.writerow([lines[idx][1], lines_interpolated[idx]])

if __name__ == "__main__":
    run()

