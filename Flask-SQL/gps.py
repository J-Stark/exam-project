import requests
import json

headers = {
    'Accept': 'application/json',
    'Authorization': 'key ttn-account-v2.AQx5q3qYsjMMTZotp3BDpX3ZRKZfRSSeY_vTIm--m-g',
}

response = requests.get('https://bicycle1.data.thethingsnetwork.org/api/v2/query?last=3h', headers=headers)
dat = json.loads(response.text)
gpsdata = (dat[1]["gps_1"])
data = (dat[1]["time"])
data = data.replace("T", " ")
gpsdata = gpsdata.replace("map[altitude:0 ", "")
gpsdata = gpsdata.replace("latitude:", "")
gpsdata = gpsdata.replace("longitude:", "")
gpsdata = gpsdata.replace("]", "")
gpsdata = gpsdata.split(" ")
print(dat[1]["device_id"])
print(gpsdata[0])
print(gpsdata[1])
print(data)
print(gpsdata[1])

def get():
    devID = dat[1]["device_id"]
    bike_id = devID.replace("bicycle", "")
    formattedData = {'x' : gpsdata[0], 'y': gpsdata[1], 'bike_id': bike_id, 'time': data}
    return formattedData
