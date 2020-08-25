###################################################################
#    ____ ___  ___  _____________  ____  ____ ____  _____
#   / __ `__ \/ _ \/ ___/ ___/ _ \/ __ \/ __ `/ _ \/ ___/
#  / / / / / /  __(__  |__  )  __/ / / / /_/ /  __/ /
# /_/ /_/ /_/\___/____/____/\___/_/ /_/\__, /\___/_/
#                                     /____/
###################################################################
# Title:        messenger
# Version:      2.5
# Description:  Enters MQTT messages from EdgeX into InfluxDB
# Author:       Jonas Werner
###################################################################
import paho.mqtt.client as mqtt
import time
import json
import argparse
from influxdb import InfluxDBClient
from datetime import datetime

# Set environment variables
# MQTTT authentication + port need to be set separately
# on line 92 and 95 if required
broker_address  = "<edgex ip>"
topic           = "edgex-tutorial"
dbhost          = "<edgex ip>"
dbport          = 8086
dbuser          = "root"
dbpassword      = "pass"
dbname          = "sensordata"


def influxDBconnect():

    """Instantiate a connection to the InfluxDB."""
    influxDBConnection = InfluxDBClient(dbhost, dbport, dbuser, dbpassword, dbname)

    return influxDBConnection



def influxDBwrite(device, sensorName, sensorValue):

    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    measurementData = [
        {
            "measurement": device,
            "tags": {
                "gateway": device,
                "location": "Tokyo"
            },
            "time": timestamp,
            "fields": {
                sensorName: sensorValue
            }
        }
    ]
    influxDBConnection.write_points(measurementData, time_precision='ms')



def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))

    # Create a dictionary and extract the current values
    obj = json.loads(m)
    # current date and time
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Extract the data from each sensor, even if the MQTT message contain multiple entries
    for entry in obj["readings"]:
        #print("Sensor: %s: Reading: %s" % (entry["name"], entry["value"]) )

        device      = entry["device"]
        sensorName  = entry["name"]
        sensorValue = entry["value"]

        # Write data to influxDB
        influxDBwrite(device, sensorName, sensorValue)




influxDBConnection = influxDBconnect()

print("Creating new instance ...")
client = mqtt.Client("sub1") #create new instance
client.on_message=on_message #attach function to callback
# client.username_pw_set("mqttUser", "mqttPass")

print("Connecting to broker ...")
client.connect(broker_address, 1883) #connect to broker
print("...done")

client.loop_start()



while True:
    client.subscribe(topic)
    time.sleep(1)

client.loop_stop()
