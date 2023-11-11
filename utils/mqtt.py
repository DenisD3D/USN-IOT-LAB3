import os

import paho.mqtt.client as paho
from dotenv import load_dotenv
from paho import mqtt


class MQTT:
    def __init__(self, project_name, host, port, username, password):
        self.project_name = project_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = paho.Client(protocol=paho.MQTTv5)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.host, self.port)

    def publish(self, topic, message= None):
        self.client.publish(f"{self.project_name}/{topic}", message)

    def subscribe(self, topic, callback):
        self.client.subscribe(f"{self.project_name}/{topic}")
        self.client.message_callback_add(f"{self.project_name}/{topic}", callback)


if __name__ == '__main__':
    load_dotenv()

    mqtt = MQTT("IOT3", os.getenv("MQTT_BROKER_URL"), int(os.getenv("MQTT_BROKER_PORT")), os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    mqtt.publish("test", "Hello World")

    mqtt.client.loop_forever()