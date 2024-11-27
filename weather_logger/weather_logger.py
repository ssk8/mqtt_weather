from weather_db import session, DataPoint
import paho.mqtt.client as mqtt
import json

MQTT_HOST = "tbox"
MQTT_BASE_TOPIC = "weather"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected: {reason_code}")
    client.subscribe(f"{MQTT_BASE_TOPIC}/#")


def on_message(client, userdata, msg):
    datapoint = DataPoint(topic=str(msg.topic), **json.loads(msg.payload))
    print(datapoint)
    session.add(datapoint)
    session.commit()


if __name__ == "__main__":
    try:
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message

        mqttc.connect(MQTT_HOST, 1883, 60)

        mqttc.loop_forever()
        
    except KeyboardInterrupt:
        print(f"\ngoodbye\n")
