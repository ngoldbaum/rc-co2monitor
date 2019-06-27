# Recurse Center CO2 Monitor

## Installation

This makes use of the Python `co2meter` library available [on
github](https://github.com/vfilimonov/co2meter) and
[pypi](https://pypi.org/project/CO2meter/). I've only tested this on an Ubuntu
18.04 machine so other operating systems may have different setup instructions.


To get set up you will need to install a few packages:

```bash
$ sudo apt-get install libusb-1.0-0-dev libudev-dev
$ sudo pip install hidapi co2meter
```

You can additionally install pandas if you want to get the data as a pandas
dataframes. 

On linux you will also need to set rules for the device interface. Add the
following content to a file named `/etc/udev/rules.d/98-co2mon.rules`:

```
SUBSYSTEM=="usb", ATTRS{idVendor}=="04d9", ATTRS{idProduct}=="a052", GROUP="plugdev", MODE="0666"
KERNEL=="hidraw*", ATTRS{idVendor}=="04d9", ATTRS{idProduct}=="a052", GROUP="plugdev", MODE="0666"
```

And then reload the `udev` rules:

```bash
$ sudo udevadm control --reload-rules && udevadm trigger
```

To check that everything is working, do the following:

```bash
$ sudo python -c "import co2meter as co2;mon = co2.CO2monitor();print(mon.info)"
```

Assuming everything is working correctly, you should see output like this:

```
{'product_name': u'USB-zyTemp', 'vendor_id': 1241, 'serial_no': u'1.40', 'product_id': 41042, 'manufacturer': u'Holtek'}
```

Note that I'm using a CO2 meter from co2meter.com, specifically [this
one](https://www.co2meter.com/collections/desktop/products/co2mini-co2-indoor-air-quality-monitor).

## Starting the liveplotter

You can generate a running stream of measurements (one a minute by default) and
a liveplot by doing

```bash
$ sudo python3 gather_data.py
```

To serve the liveplot on a webpage via flask, do:

```bash
$ cd webapp
$ export FLASK_APP=webapp.py
$ flask run --host=0.0.0.0
```
