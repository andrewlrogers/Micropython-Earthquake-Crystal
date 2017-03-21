# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import network
from ntptime import settime
import utime

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Small Talk', 'preston3')
        while not wlan.isconnected():
            pass
    settime()
    print('network config:', wlan.ifconfig())
    print('time is:', utime.localtime())

#connect to local network
do_connect()
gc.collect()
