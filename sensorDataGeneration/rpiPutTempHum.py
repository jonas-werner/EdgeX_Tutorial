#!/usr/bin/python

import sys, time, requests, json, Adafruit_DHT

edgexip = "<edgex ip>"

while True:

    rawHum, rawTmp = Adafruit_DHT.read_retry(11, 6)

    urlTemp = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/temperature' % edgexip
    urlHum  = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/humidity' % edgexip

    humval  = str(rawHum)
    tempval = str(rawTmp)

    headers = {'content-type': 'application/json'}

    if(float(humval) < 100):
        response = requests.post(urlTemp, data=json.dumps(int(rawTmp)), headers=headers,verify=False)
        response = requests.post(urlHum, data=json.dumps(int(rawHum)), headers=headers,verify=False)

        print('Temp: {} C, humidity: {} %').format(tempval, humval)


    time.sleep(2)
