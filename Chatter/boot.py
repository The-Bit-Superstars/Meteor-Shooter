import network, time, gc
from Chatter import begin, display
begin()
display.text('boot.py 1.0.2', 64-len('boot.py 1.0.2')*4, 60, 65535)
display.commit()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print('Connected:',str(wlan.isconnected()))
gc.collect()
try:
    gc.collect()
    with open('wifi.txt', 'r') as f:
        ssid = f.readline().strip()
        pswd = f.readline().strip()
    gc.collect()
    if not wlan.isconnected():
        wlan.connect(ssid, pswd)
        time.sleep(5)
        display.fill(0)
    gc.collect()
    display.text(wlan.ifconfig()[0],0,0,65535)
    display.text(wlan.ifconfig()[1],0,8,65535)
    display.text(wlan.ifconfig()[2],0,16,65535)
    display.text(wlan.ifconfig()[3],0,24,65535)
    display.commit()
    time.sleep(2.5)
except Exception as e:
    gc.collect()
    display.fill(0)
    display.text(repr(e),0,0,65535)
    display.commit()
    time.sleep(2.5)
    gc.collect()
