import random
from machine import Pin, SPI, ADC
import st7789
import utime

import vga1_bold_16x32 as font

sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)



spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = st7789.ST7789(
    spi,
    135,
    240,
    reset=Pin(12, Pin.OUT),
    cs=Pin(9, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=1)

tft.init()
utime.sleep(0.5)
'''
tft.text(font,"Hello World!", 0,0)
#tft.rect(100, 100, 100, 10, st7789.RED)
tft.fill_rect(70, 40, 120,10, st7789.RED)

utime.sleep(2)
tft.fill(0)'''
#tft.fill_rect(60, 20, 120,10, st7789.RED)
#tft.fill_rect(60, 90, 120,10, st7789.YELLOW)
tft.fill_rect(0, 00, 240,20, st7789.RED)
tft.fill_rect(0, 90, 240,20, st7789.YELLOW)
tft.fill_rect(0, 110, 240,20, st7789.CYAN)


while True:
    
    reading = sensor_temp.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    
    tft.text(font, "TEMP:{:.2f}".format(temperature), 40,40)
    utime.sleep(1)
