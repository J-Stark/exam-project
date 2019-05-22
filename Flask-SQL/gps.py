import requests
import json

headers = {
    'Accept': 'application/json',
    'Authorization': 'key ttn-account-v2.AQx5q3qYsjMMTZotp3BDpX3ZRKZfRSSeY_vTIm--m-g',
}


gpsdata = (dat[1]["gps_1"])
data = (dat[1]["time"])
data = data.replace("T", " ")
print(dat[1]["device_id"])
print(gpsdata[0])
print(gpsdata[1])
print(data)
print(gpsdata[1])

def request():
    response = requests.get('https://bicycle1.data.thethingsnetwork.org/api/v2/query?last=1h', headers=headers)
    return json.loads(response.text)


def get():
    count = 0
    for gps in request():
        print(request()[count])
        count += 1

    devID = dat[1]["device_id"]
    bike_id = devID.replace("bicycle", "")
    formattedData = {'x' : gpsdata[0], 'y': gpsdata[1], 'bike_id': bike_id, 'time': data}
    return formattedData


def format(gpsdata):
    gpsdata = gpsdata.replace("map[altitude:0 ", "")
    gpsdata = gpsdata.replace("latitude:", "")
    gpsdata = gpsdata.replace("longitude:", "")
    gpsdata = gpsdata.replace("]", "")
    gpsdata = gpsdata.split(" ")
    return gpsdata
