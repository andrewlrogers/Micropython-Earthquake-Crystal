import urequests, json
import utime
import machine, neopixel

my_latitude = 37.45
my_longitude = -122.25
my_radius = 50

def convert_time(time_tuple): #takes time as a tuple and returns it as %Y-%m-%d %H:%M:%S
    year = str(time_tuple[0])
    month = str(time_tuple[1])
    day = str(time_tuple[2])
    hour = str(time_tuple[3])
    minute = str(time_tuple[4])
    second = str(time_tuple[5])

    time_string = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second

    return(time_string)

#returns the current time in ('%Y-%m-%d %H:%M:%S') format
def get_time():
    currently = utime.localtime()
    utc_current = utime.mktime(currently)
    utc_two_hours = utc_current - 7200
    two_hours = utime.localtime(utc_two_hours)
    earlier_time = convert_time(two_hours)
    return(earlier_time)


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
    payload = {'format':'geojson','latitude':my_latitude, 'longitude':my_longitude, 'maxradiuskm':my_radius, 'starttime':get_time(), 'orderby':'time-asc'}
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



#mag_light(1.27)

recent_quake = setup_quake_check()
print(recent_quake)
#check_quake(recent_quake)
