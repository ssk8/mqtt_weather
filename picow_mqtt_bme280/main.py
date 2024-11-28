from machine import Pin, I2C
from time import sleep
import network
from umqtt.simple import MQTTClient
import json
import config
import lib.BME280 as BME280

mqtt_base_topic = "weather"
device_name = "picow12992"
sleep_time = 300

i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)
bme = BME280.BME280(i2c=i2c, addr=0x76)


def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    if wlan.status() != 3:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

def connect_mqtt():
    try:
        print("try mqtt")
        client = MQTTClient(client_id=device_name,
                            server=config.mqtt_server,
                            port=config.mqtt_port,
                            user=config.mqtt_username,
                            password=config.mqtt_password,
                            keepalive=7200)
        client.connect()
        print("dun mqtt connnect")
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback


try:
    if not initialize_wifi(config.wifi_ssid, config.wifi_password):
        print('Error connecting to the network... exiting program')
    else:
        client = connect_mqtt()
        while True:
            payload = {'temperature': bme.temperature[:-2], 'humidity': bme.humidity[:-2], 'pressure': bme.pressure[:-4]}
            print(f"{mqtt_base_topic}/{device_name}", json.dumps(payload))
            client.publish(f"{mqtt_base_topic}/{device_name}", json.dumps(payload))
            sleep(sleep_time)

except Exception as e:
    print('Error:', e)
