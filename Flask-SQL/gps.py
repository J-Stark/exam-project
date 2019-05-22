import requests
import json

headers = {
    'Accept': 'application/json',
    'Authorization': 'key ttn-account-v2.AQx5q3qYsjMMTZotp3BDpX3ZRKZfRSSeY_vTIm--m-g',
}


def request():
    response = requests.get('https://bicycle1.data.thethingsnetwork.org/api/v2/query?last=1h', headers=headers)
    return json.loads(response.text)


def format(gpsdata):
    gpsdata = gpsdata.replace("map[altitude:0 ", "")
    gpsdata = gpsdata.replace("latitude:", "")
    gpsdata = gpsdata.replace("longitude:", "")
    gpsdata = gpsdata.replace("]", "")
    gpsdata = gpsdata.split(" ")
    return gpsdata


def get():
    bike_id = 0
    listOfBikes = []
    for gps in request():
        gpsData = format(request()[bike_id]["gps_1"])
        time = request()[bike_id]["time"]
        time.replace("T", "")
        bike_id += 1
        formattedData = {'x': gpsData[0], 'y': gpsData[1], 'bike_id': bike_id, 'time': time}
        listOfBikes.append(formattedData)
    return listOfBikes
