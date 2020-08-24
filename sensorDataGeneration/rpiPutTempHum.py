# -*- coding: utf-8 -*-
#################################################################
#     ____  __  ________   ___      ______    __          _  __
#    / __ \/ / / /_  __/  |__ \    / ____/___/ /___ ____ | |/ /
#   / / / / /_/ / / /     __/ /   / __/ / __  / __ `/ _ \|   / 
#  / /_/ / __  / / /     / __/   / /___/ /_/ / /_/ /  __/   |  
# /_____/_/ /_/ /_/     /____/  /_____/\__,_/\__, /\___/_/|_|  
#                                           /____/             
#################################################################
#  Description: Script for capturing and sending DHT11 data from 
#               Raspberry Pi to EdgeX Foundry over REST
#  Version: 1.2
#  Author: Jonas Werner
#################################################################


import sys, time, requests, json, Adafruit_DHT

edgexip = "<edgex ip>"

while True:

    # Update to match DHT sensor type and GPIO pin
    # DHT11 and GPIO pin 6 used in example
    rawHum, rawTmp = Adafruit_DHT.read_retry(11, 6)

    urlTemp = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/temperature' % edgexip
    urlHum  = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/humidity' % edgexip

    humval  = str(rawHum)
    tempval = str(rawTmp)

    headers = {'content-type': 'application/json'}

    if(float(humval) < 100):
        response = requests.post(urlTemp, data=json.dumps(int(rawTmp)), headers=headers,verify=False)
        response = requests.post(urlHum, data=json.dumps(int(rawHum)), headers=headers,verify=False)

        print("Temp: %s\N{DEGREE SIGN}C, humidity: %s%%" % (tempval, humval))


    time.sleep(2)
