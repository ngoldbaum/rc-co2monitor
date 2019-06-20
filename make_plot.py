import pandas
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

data = pandas.read_csv("co2data.csv")

time = pandas.to_datetime(data["Time"], unit="s")

concentration = data["Concentration"]

plt.plot(time, concentration, '.')

now = pandas.Timestamp.now()

begin = now - pandas.Timedelta('4 days')

day = pandas.Timedelta('1 days')

plt.xlim(begin, now)
plt.ylim(0, 3000)

plt.xticks([now - 4*day, now - 3*day, now - 2*day, now-1*day, now])

plt.grid()

plt.xlabel('Time')

plt.ylabel(r'$\rm{CO}_2$ Concentration (PPM)')

plt.savefig("co2.png")
