import os

from dotenv import load_dotenv

from utils.mqtt import MQTT
from utils.sqlconnector import SQLConnector


def upload_temperature(temperature):
    db.upload_temperature(temperature)
    print(f"Temperature uploaded: {temperature}°C")


if __name__ == '__main__':
    load_dotenv()
    db = SQLConnector(os.getenv("SQL_DATABASE"), os.getenv("SQL_HOST"), os.getenv("SQL_USER"), os.getenv("SQL_PASSWORD"), os.getenv("SQL_PORT"))
    mqtt = MQTT("IOT3", os.getenv("MQTT_BROKER_URL"), int(os.getenv("MQTT_BROKER_PORT")), os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    mqtt.subscribe("temperature", lambda client, userdata, message: upload_temperature(message.payload.decode()))

    mqtt.client.loop_forever()
