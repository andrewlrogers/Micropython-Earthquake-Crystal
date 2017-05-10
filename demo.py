"""A way to demonstrate what the crystal SHOULD do"""

import urequests, json
from time import sleep, ticks_ms
import machine, neopixel
from math import sin, pi


""" G L O B A L """
""" V A R I A B L E S """

neopixel_pin = 14
number_of_neopixels = 12


""" N E O P I X E L S """
""" I N I T I A L I Z E """
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), number_of_neopixels)
np.fill((1,1,1)) #Set's the led's to off
np.write()


""" L I G H T """
""" F U N C T I O N S """

# palette for led's
mag_color = {'10':(255,0,0), '9':(255, 0, 0), '8':(228, 19, 109), '7':(228, 29, 158), '6':(228, 39, 203), '5':(220, 2, 241), '4':(8, 236, 4), '3':(6,230,277), '2':(5, 234, 77), '1':(5,232,153), '0':(32,5,234)}


def lerp(x, x0, x1, y0, y1):
    return y0 + (x-x0)*((y1-y0)/(x1-x0))

def blink(blinks): #blink's an LED to indicate that progam is running.
    for blink in range(blinks):
        COLOR_A = np[10]
        np[10] = (3, 3, 3)
        np.write()
        sleep(.25)
        np[10]=COLOR_A
        np.write()
        sleep(.75)

def diminish(): #slowly diminishes color of led over time.
    blink(1)
    COLOR_A = np[0]
    COLOR_B = (1,1,1)
    current = ticks_ms()
    x = sin(2.0 * pi * .001 * current)
    red = lerp(x, -1.0, 1.0, COLOR_A[0], COLOR_B[0])
    green = lerp(x, -1.0, 1.0, COLOR_A[1], COLOR_B[1])
    blue = lerp(x, -1.0, 1.0, COLOR_A[2], COLOR_B[2])
    np.fill((int(red), int(green), int(blue)))
    np.write()
    print((int(red), int(green), int(blue)))
    sleep(0.01)

def pulse(magnitude): #Pulses magnitude color with COLOR_B before setting to mag_color
    COLOR_A = mag_color[(str(magnitude)[0])]
    COLOR_B = (255,255,255)

    for m in range(200):
        current = ticks_ms()
        x = math.sin(2.0 * math.pi * .001 * current)
        red = lerp(x, -1.0, 1.0, COLOR_A[0], COLOR_B[0])
        green = lerp(x, -1.0, 1.0, COLOR_A[1], COLOR_B[1])
        blue = lerp(x, -1.0, 1.0, COLOR_A[2], COLOR_B[2])
        np.fill((int(red), int(green), int(blue)))
        np.write()
        sleep(0.01)
    np.fill(COLOR_A)
    np.write()

def chase(magnitude): #quick spin
    COLOR_A = mag_color[(str(magnitude)[0])]
    for t in range (5):
        for pixel in range(number_of_neopixels):
            np.fill((1,1,1))
            np.write()
            np[pixel]= COLOR_A
            np.write()
            sleep(.01)
    np.fill(COLOR_A)
    np.write()

""" M A I N  Q U A K E """



#main program

def demo(interval, demo_mag, iterations):
    blink(interval)
    pulse(demo_mag)
    for i in range(iterations):
        blink(interval)
        diminish()

demo(10, 3, 15)
