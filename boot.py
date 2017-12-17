# MC ESP8266 Clock Program

# This file is executed on every boot (including wake-boot from deepsleep)
# It establishes a network connection and sets the time with NTP.

import gc
import webrepl
import ntptime
import time
import utime
import network
import machine
import ssd1306

webrepl.start()
gc.collect()
gc.enable()  # Enables automatic garbage collection
machine.freq(160000000)  # boosts the speed to max

# Load your known wifi network credentials here
wifis = {
    'SSID1': 'password1',
    'SSID2': 'password2'
}

# -----------------------------OLED Methods---------------------------------


def initialize_screen():
    global i2c
    global oled
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
    oled = ssd1306.SSD1306_I2C(128, 32, i2c)
    oledclear()


def oledprint(x, y):
    oled.pixel(x, y, 1)
    oled.show()


def oledtext(text, indent, line):
    oled.text(text, indent, line)
    oled.show()


def oledclear():
    oled.fill(0)
    oled.show()


def welcomescreen():
    oledclear()
    oledtext('----------------', 0, 0)
    oledtext('MC Wifi Clock', 15, 13)
    oledtext('----------------', 0, 28)
    time.sleep(2)


# -------------------------------Networking Methods----------------------------


def wifi_scan():
    global wifi
    networks = wifi.scan()
    available = []
    for net in networks:
        available.append(net[0].decode())
    filtered = set(available)
    available_networks = list(filtered)
    return available_networks


def initialize_networking():
    global wifi
    global ap
    global session_ssid
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print('Scanning for known wifi networks...')
        oledclear()
        oledtext('Scanning Wifi', 0, 5)
        available_networks = wifi_scan()
        print(len(available_networks), 'networks found!')
        oledtext(str(len(available_networks)) + ' networks found!', 0, 17)
        connect_attempts = 0
        for each in available_networks:
            if each in wifis:
                print("Boom!", each, "is a known network, woot!")
                oledclear()
                oledtext('Boom!', 25, 0)
                oledtext(each, 25, 10)
                oledtext('is a known network', 0, 20)
                session_ssid = each
                session_pw = wifis[each]
                print("Connecting to", session_ssid)
                oledclear()
                oledtext('Connecting to', 0, 5)
                oledtext(session_ssid, 0, 15)
                wifi.connect(session_ssid, session_pw)
                while not wifi.isconnected():
                    time.sleep(0.5)
                    connect_attempts += 1
                if wifi.isconnected():
                    ipaddy, mask, gateway, xyz = wifi.ifconfig()
                    print('You are connected to', session_ssid, 'on', ipaddy)
                    oledclear()
                    oledtext('Connected to', 0, 0)
                    oledtext(session_ssid, 15, 10)
                    oledtext(str('at ' + ipaddy), 0, 20)
                    return
                elif connect_attempts > 5:
                    print("Cannot connect to", session_ssid)
                    pass
    elif wifi.isconnected():
        ipaddy, ssid, gateway, xyz = wifi.ifconfig()
        print('You are already connected on', ipaddy)
        oledclear()
        oledtext('Connected ', 0, 5)
        oledtext(str('on ' + ipaddy), 0, 15)
        time.sleep(2)
        return


initialize_screen()
welcomescreen()
initialize_networking()
ntptime.settime()
