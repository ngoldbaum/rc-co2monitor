# -*- coding: utf-8 -*-

import time
import csv
import os
import pandas
import matplotlib
import numpy as np

matplotlib.use("agg")

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from palettable.cartocolors.qualitative import Antique_2 as cmap


def get_data():
    now = pandas.Timestamp.now()
    begin = now - pandas.Timedelta("4.5 days")
    files_to_read = [""]
    time = pandas.Series()
    concentration = pandas.Series()
    temperature = pandas.Series()
    for i in range(6):
        dtime = begin + pandas.Timedelta("{} days".format(i))
        fname = "{}-{}-{}.csv".format(dtime.year, dtime.month, dtime.day)
        if not os.path.exists(fname):
            continue
        data = pandas.read_csv(fname)
        time = time.append(data["Time"])
        concentration = concentration.append(data["Concentration"])
        temperature = temperature.append(data["Temperature"])
    time = pandas.to_datetime(time, unit="s")
    time = time.dt.tz_localize("UTC").dt.tz_convert("US/Eastern")
    concentration = np.array(concentration)
    temperature = np.array(temperature)
    return time, concentration, temperature


def make_plot():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax_c = ax2.twinx()

    now = pandas.Timestamp.now(tz="US/Eastern")

    today = pandas.Timestamp(
        year=now.year, month=now.month, day=now.day, tz="US/Eastern"
    )

    # handle bug in old pandas version on rpi
    try:
        today = today.tz_localize("US/Eastern")
    except TypeError:
        pass

    begin = now - pandas.Timedelta("4.5 days")

    day = pandas.Timedelta("1 days")

    time, concentration, temperature = get_data()

    ticks = [today - i * day for i in range(4, -2, -1)]
    minorticks = [today - day * (i + 0.5) for i in range(4, -2, -1)]

    ax1.set_xlim(begin, now + 0.5 * day)
    ax1.set_xlabel("Time")
    ax1.set_xticks(ticks)
    ax1.set_xticks(minorticks, minor=True)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%H"))

    ax2.set_xlim(begin, now + 0.5 * day)
    ax2.set_xlabel("Time")
    ax2.set_xticks(ticks)
    ax2.set_xticks(minorticks, minor=True)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%H"))

    ax1.plot(time, concentration, color=cmap.mpl_colors[0])
    ax1.set_ylim(0, 3000)
    ax1.set_ylabel(r"$\rm{CO}_2$ Concentration (PPM)")
    ax1.grid()

    flimits = [70, 80]
    climits = [21.11, 26.67]

    ax2.plot(
        time, 9 / 5 * temperature + 32, ".", markersize=0.4, color=cmap.mpl_colors[1]
    )
    ax2.set_ylim(flimits[0], flimits[1])
    ax2.set_ylabel(r"Temperature ($\circ\rm{F}$)")
    ax2.grid()

    ax_c.set_ylim(climits[0], climits[1])
    ax_c.set_ylabel(r"($\circ\rm{C}$)")

    plt.tight_layout()

    if not os.path.isdir("webapp/static"):
        os.mkdir("webapp/static")
    fig.savefig("webapp/static/co2.png", dpi=100)
    plt.close()


if __name__ == "__main__":
    import co2meter

    while True:
        tb = time.time()
        mon = co2meter.CO2monitor()
        now = pandas.Timestamp.now()
        output_filename = "{}-{}-{}.csv".format(now.year, now.month, now.day)
        if not os.path.exists(output_filename):
            with open(output_filename, "w") as f:
                f.write("Time,Concentration,Temperature\n")
        data = mon.read_data()
        t = time.mktime(data.index[0].timetuple())
        row = t, np.float64(data["co2"]), np.float64(data["temp"])
        print("{}, {} PPM, {} °C".format(*row))
        with open(output_filename, "a") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        make_plot()
        tsleep = 60 - (time.time() - tb)
        if tsleep > 0:
            time.sleep(tsleep)
