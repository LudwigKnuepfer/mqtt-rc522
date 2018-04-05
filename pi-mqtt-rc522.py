#!/usr/bin/env python3

import sys
import time

from pirc522 import RFID
import paho.mqtt.client as mqtt

STATUS_TOPIC = 'rc522/status'
EVENT_TOPIC = 'rc522/events'
HOST = "localhost"
PORT = 1883

def LOG(msg):
    print(msg)

def mqtt_on_message(client, userdata, msg):
    LOG("mqtt got message")
    pass

def mqtt_on_connect(client, userdata, flags, rc):
    if rc == 0:
        LOG("mqtt connected")
        client.publish(
                STATUS_TOPIC, "rc522 up and running", qos=1, retain=True)
    else:
        LOG("mqtt connection failed")
        sys.exit(1)

def mqtt_init():
    protocol = mqtt.MQTTv311
    client_id = 'rc522'

    client = mqtt.Client(
            client_id=client_id, clean_session=False, protocol=protocol)

    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message

    return client

def rfid_read(reader):
    uid_str = None
    LOG("waiting for tag")
    reader.wait_for_tag()
    LOG("found")
    (error, data) = reader.request()
    if not error:
        LOG("Detected: " + format(data, "02x"))
        (error, uid) = reader.anticoll()
        if not error:
            uid_str = ".".join(str(e) for e in uid)
            LOG("Card read UID: " + uid_str)
        else:
            LOG("error in anticoll")
    else:
        LOG("error in request")

    return uid_str

def main():
    client = mqtt_init()
    try:
        client.connect(HOST, PORT, 60)
    except socket.error as err:
        LOG(err)
        sys.exit(1)

    client.loop_start()

    reader = RFID()

    try:
        last_uid_str = None
        last_time = 0
        while True:
            uid_str = rfid_read(reader)
            td = time.time() - last_time
            if uid_str:
                if (uid_str != last_uid_str) or (td > 1):
                    last_uid_str = uid_str
                    client.publish(
                        EVENT_TOPIC, uid_str, qos=1, retain=False)
                time.sleep(0.1)
                last_time = time.time()
    except KeyboardInterrupt:
        LOG("KeyboardInterrupt")
    finally:
        reader.cleanup()
        client.publish(
                STATUS_TOPIC, "rc522 dead", qos=1, retain=True)
        client.disconnect()

    sys.exit(0)

if __name__ == "__main__":
    main()
