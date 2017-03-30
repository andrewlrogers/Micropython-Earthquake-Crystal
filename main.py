import urequests, json
from utime import mktime, localtime
from time import sleep, ticks_ms
import machine, neopixel
from math import sin, pi

""" G L O B A L """
""" V A R I A B L E S """

my_latitude = 37.45
my_longitude = -122.25
my_radius = 50
neopixel_pin = 14
number_of_neopixels = 12

led0 = machine.Pin(0, machine.Pin.OUT) #onboard LED to track functionality.


""" N E O P I X E L S """
""" I N I T I A L I Z E """
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), number_of_neopixels)
np.fill((0,0,10)) #Set's the led's to off
np.write()

""" T I M E """
""" F U N C T I O N S """

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

""" L I G H T """
""" F U N C T I O N S """

# palette for led's
mag_color = {'10':(255,0,0), '9':(255, 0, 0), '8':(228, 19, 109), '7':(228, 29, 158), '6':(228, 39, 203), '5':(220, 2, 241), '4':(8, 236, 4), '3':(6,230,277), '2':(5, 234, 77), '1':(5,232,153), '0':(32,5,234)}


def mag_light(magnitude): #changes the color of a light depending on magnitude
    magnitude = (str(magnitude)[0])
    np.fill(mag_color[magnitude])
    np.write()

def lerp(x, x0, x1, y0, y1):
    return y0 + (x-x0)*((y1-y0)/(x1-x0))

def diminish(): #slowly diminishes color of led over time.
    COLOR_A = np[0]
    COLOR_B = (0,0,0)
    current = ticks_ms()
    x = sin(2.0 * pi * .001 * current)
    red = lerp(x, -1.0, 1.0, COLOR_A[0], COLOR_B[0])
    green = lerp(x, -1.0, 1.0, COLOR_A[1], COLOR_B[1])
    blue = lerp(x, -1.0, 1.0, COLOR_A[2], COLOR_B[2])
    np.fill((int(red), int(green), int(blue)))
    np.write()
    sleep(0.01)

def chase(magnitude): #quick spin
    COLOR_A = mag_color[(str(magnitude)[0])]
    for t in range (5):
        for pixel in range(number_of_neopixels):
            np.fill((0,0,0))
            np.write()
            np[pixel]= COLOR_A
            np.write()
            sleep(.01)
    np.fill(COLOR_A)
    np.write()

""" M A I N  Q U A K E """

def setup_quake_check(): #runs a broad check for the last quake based on current time
    try:
        request_payload = 'format=geojson'+'&'+'latitude=' + str(my_latitude) +'&'+ 'longitude=' + str(my_longitude) +'&'+ 'maxradiuskm=' + str(my_radius) +'&'+ 'starttime=' + get_time() +'&'+ 'orderby=time-asc'
        response = urequests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?' + request_payload).json()
        response_count = response['metadata']['count']

        if response_count != 0: #If there is a response do this.
            for setup_quake in response['features']:
                magnitude = setup_quake['properties']['mag']
                timestamp = (int(str(setup_quake['properties']['time'])[:10]))
                last_quake = epoch_convert(timestamp)
            chase(magnitude)
            return(last_quake)

        else:
            last_quake = convert_time(localtime())
            sleep(10)
            return(last_quake)
    except(OSError, MemoryError):
        print('Error, going to try again in a sec')
        last_quake = convert_time(localtime())
        sleep(10)
        return(last_quake)


#main program
def check_quake(last_quake):
    while True:
        try:
            request_payload = 'format=geojson'+'&'+'latitude=' + str(my_latitude) +'&'+ 'longitude=' + str(my_longitude) +'&'+ 'maxradiuskm=' + str(my_radius) +'&'+ 'starttime=' + last_quake +'&'+ 'orderby=time-asc'
            response = urequests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?' + request_payload).json()

            response_count = response['metadata']['count']

            if response_count != 0:
                for quake in response['features']:
                    chase(quake['properties']['mag'])
                    timestamp = (int(str(quake['properties']['time'])[:10]))
                    print(last_quake)
                    sleep(20)

            else:
                last_quake = convert_time(localtime())
                print('Nothin shakin eggs n bacon')
                diminish()
                sleep(60) #1800 is30 minutes

        except(OSError, MemoryError):
            last_quake = convert_time(localtime())
            print('Error, gonna try again real soon')
            sleep(60) #1800 is 30 minutes
            diminish()


sleep(5)
recent_quake = setup_quake_check()
check_quake(recent_quake)
