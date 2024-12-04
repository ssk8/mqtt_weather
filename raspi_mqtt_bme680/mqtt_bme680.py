#!/usr/bin/python

import paho.mqtt.publish as publish
import json
from time import sleep
import bme680

hostname = "tbox"
mqtt_base_topic = "weather"
device_name = "piedisp_BME680"
sleep_time = 300


try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)


sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

print('\n\nPolling:')
try:
    while True:
        payload = dict()
        if sensor.get_sensor_data():
            payload["temperature"] = round(sensor.data.temperature, 1)
            payload["pressure"] = round(sensor.data.pressure, 1)
            payload["humidity"] = round(sensor.data.humidity, 1)

            if sensor.data.heat_stable:
                #payload["gas_resistance"] = int(sensor.data.gas_resistance)
                ...
        if payload:
            try:
                publish.single(hostname=hostname, topic=f"{mqtt_base_topic}/{device_name}", payload=json.dumps(payload))
                print(payload)
                sleep(sleep_time)
            except TimeoutError as e:
                print(e)
        sleep(1)

except KeyboardInterrupt:
    print("\ngoodbye")
