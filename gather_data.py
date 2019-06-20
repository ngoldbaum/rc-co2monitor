# -*- coding: utf-8 -*-

import time
import csv
import co2meter
import os

if not os.path.exists('co2data.csv'):
    with open('co2data.csv') as f:
        f.write('Time,Concentration,Temperature')

while True:
    mon = co2meter.CO2monitor()
    data = mon.read_data()
    row = (time.mktime(data[0].timetuple()),) + data[1:]
    print("{}, {} PPM, {} °C".format(str(data[0]), data[1], data[2]))
    with open('co2data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    time.sleep(10)
