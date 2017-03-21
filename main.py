import urequests, json
from utime import mktime, localtime
from time import sleep
import machine, neopixel

my_latitude = 37.45
my_longitude = -122.25
my_radius = 50



def convert_time(time_tuple): #takes time as a tuple and returns it as %Y-%m-%d %H:%M:%S
    time_string = str(time_tuple[0]) + '-' + str(time_tuple[1]) + '-' + str(time_tuple[2]) + ' ' + str(time_tuple[3]) + ':' + str(time_tuple[4]) + ':' + str(time_tuple[5])
    return(time_string)

#returns the current time in ('%Y-%m-%d %H:%M:%S') format
def get_time():
    currently = localtime()
    utc_current = mktime(currently)
    utc_two_hours = utc_current - 7200 #7200 is two hours
    two_hours = localtime(utc_two_hours)
    earlier_time = convert_time(two_hours)
    return(earlier_time)

def epoch_convert(timestamp):
    time_diff = 946684800 #seconds between 1976 epoch and 2000 epoch
    last_quake = convert_time(localtime(timestamp - time_diff))
    return(last_quake)

# palette for led's
mag_color = {'10':(255,0,0), '9':(228, 9, 55), '8':(228, 19, 109), '7':(228, 29, 158), '6':(228, 39, 203), '5':(211, 49, 228), '4':(175, 59, 227), '3':(143, 69, 227), '2':(115,79,227), '1':(92,89,227), '0':(0,52,255)}

def mag_light(magnitude): #changes the color of a light depending on magnitude
    magnitude = (str(magnitude)[0])
    neopixel = mag_color[magnitude]
    print(neopixel)


def setup_quake_check():
    request_payload = 'format=geojson'+'&'+'latitude=' + str(my_latitude) +'&'+ 'longitude=' + str(my_longitude) +'&'+ 'maxradiuskm=' + str(my_radius) +'&'+ 'starttime=' + get_time() +'&'+ 'orderby=time-asc'
    response = urequests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?' + request_payload).json()

    response_count = response['metadata']['count']

    if response_count != 0:
        for setup_quake in response['features']:
            magnitude = setup_quake['properties']['mag']
            timestamp = (int(str(setup_quake['properties']['time'])[:10]))
            last_quake = epoch_convert(timestamp)
        sleep(20)
        mag_light(magnitude)
        return(last_quake)
    else:
        last_quake = convert_time(localtime())
        sleep(5)
        return(last_quake)


#main program
def check_quake(last_quake):
    while True:
        request_payload = 'format=geojson'+'&'+'latitude=' + str(my_latitude) +'&'+ 'longitude=' + str(my_longitude) +'&'+ 'maxradiuskm=' + str(my_radius) +'&'+ 'starttime=' + last_quake +'&'+ 'orderby=time-asc'
        response = urequests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?' + request_payload).json()

        response_count = response['metadata']['count']

        if response_count != 0:
            for quake in response['features']:
                mag_light(quake['properties']['mag'])
                timestamp = (int(str(quake['properties']['time'])[:10]))
                print(last_quake)
                sleep(20)

        else:
            last_quake = convert_time(localtime())
            print('Nothin shakin eggs n bacon')
            sleep(1800) #30 minutes

        sleep(10)



#mag_light(1.27)

recent_quake = setup_quake_check()
check_quake(recent_quake)
