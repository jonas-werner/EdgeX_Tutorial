
import requests
import json
import random
import time


edgexip = '10.42.0.188'
humval = 40
tempval = 23

def generateSensorData(humval, tempval):

    humval = random.randint(humval-5,humval+5)
    tempval = random.randint(tempval-1, tempval+1)

    print("Sending values: Humidity %s, Temperature %sC" % (humval, tempval))

    return (humval, tempval)



if __name__ == "__main__":

    sensorTypes = ["temperature", "humidity"]

    while(1):

        (humval, tempval) = generateSensorData(humval, tempval)

        url = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/temperature' % edgexip
        payload = tempval
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        url = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/humidity' % edgexip
        payload = humval
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        time.sleep(5)
