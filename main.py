import json
import requests
from datetime import datetime, timedelta
from time import sleep


my_latitude = 37.45
my_longitude = -122.25
my_radius = 50

#Time variables
now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
two_hours = (datetime.utcnow() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

# palette for led's
mag_color = {'10':(255,0,0), '9':(228, 9, 55), '8':(228, 19, 109), '7':(228, 29, 158), '6':(228, 39, 203), '5':(211, 49, 228), '4':(175, 59, 227), '3':(143, 69, 227), '2':(115,79,227), '1':(92,89,227), '0':(0,52,255)}


#Linear Interpolation, for smoothing transition from one color to the next
def lerp(x, x0, x1, y0, y1):
    return y0 + (x-x0)*((y1-y0)/(x1-x0))

def mag_light(magnitude): #changes the color of a light depending on magnitude
    magnitude = (str(magnitude)[0])
    neopixel = mag_color[magnitude]
    print(neopixel)


def setup_quake_check():
    payload = {'format':'geojson','latitude':my_latitude, 'longitude':my_longitude, 'maxradiuskm':my_radius, 'starttime':two_hours, 'orderby':'time-asc'}
    r = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?', params = payload)
    response = r.json()

    response_count = response['metadata']['count']

    if response_count != 0:
        for hour_quake in response['features']:
            magnitude = hour_quake['properties']['mag']
            quake_time = datetime.utcfromtimestamp(int(str(hour_quake['properties']['time'])[:10]))
            last_quake = quake_time.strftime('%Y-%m-%d %H:%M:%S')
        sleep(20)
        return(last_quake)
    else:
        last_quake = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        sleep(20)
        return(last_quake)


#main program
def check_quake(last_quake):
    while True:
        payload = {'format':'geojson','latitude':my_latitude, 'longitude':my_longitude, 'maxradiuskm':my_radius, 'starttime':last_quake, 'orderby':'time-asc'}
        r = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?', params = payload)
        response = r.json()
        response_count = response['metadata']['count']

        if response_count != 0:
            for quake in response['features']:
                magnitude = quake['properties']['mag']
                location = hour_quake['properties']['place']
                last_quake = datetime.fromtimestamp(int(str(hour_quake['properties']['time'])[:10]))
                print(magnitude, location, last_quake)
                sleep(20)

        else:
            last_quake = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            print('Nothin shakin eggs n bacon')
            sleep(1800) #30 minutes

        sleep(10)


mag_light(1.27)

#recent_quake = setup_quake_check()
#check_quake(recent_quake)
