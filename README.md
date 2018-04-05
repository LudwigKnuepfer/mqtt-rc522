# mqtt-rc522
This is  a python script that reads RFID IDs from an RC522 and publishes them via MQTT

# Installation
Assuming you're on a raspberry pi running the latest (as of this time) raspbian distribution (Debian 9.4):
```sh
sudo cp pi-mqtt-rc522.py /usr/local/bin/pi_mqtt_rc522
sudo cp rc522-daemon.service /lib/systemd/system/
sudo systemctl enable rc522-daemon.service
sudo systemctl start rc522-daemon.service
```

# Installing Prerequisits
```sh
sudo pip3 install pi-rc522
sudo pip3 install paho-mqtt
```
