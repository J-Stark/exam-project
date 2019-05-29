import requests
import json

headers = {
    'Accept': 'application/json',
    'Authorization': 'key ttn-account-v2.AQx5q3qYsjMMTZotp3BDpX3ZRKZfRSSeY_vTIm--m-g',
}


def request():
    response = requests.get('https://bicycle1.data.thethingsnetwork.org/api/v2/query?last=5h', headers=headers)
    return response

def checkData(my_response):
    try:
        object = json.loads(my_response.text)
    except ValueError as e:
        return False
    return True


def format(gpsdata):
    gpsData = gpsdata.split()
    gpsData.remove("map[altitude:0")
    gpsData[0] = gpsData[0].replace(']','')
    gpsData[1] = gpsData[1].replace(']','')
    for dat in gpsData:
        newDat = dat.split(':')
        if (newDat[0] == "longitude"):
            lng = newDat[1]
        else:
            lat = newDat[1]
    return lat, lng


def get():
    bike_id = 0
    listOfBikes = []
    if (checkData(request())):
        response = json.loads(request().text)
        for gps in response:
            lat, lng = format(response[bike_id]["gps_1"])
            bike_id += 1
            # send time
            formattedData = {'x': lat, 'y': lng, 'bike_id': bike_id}
            listOfBikes.append(formattedData)
        return listOfBikes
    else:
        print("No data sent in the last hour.")
