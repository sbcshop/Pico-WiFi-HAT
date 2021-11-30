# Use thonny ide to program pico
# Use Hercules SETUP utility for TCP server and client https://www.hw-group.com/software/hercules-setup-utility
# Make sure both server and WiFi HAT are connected on same network

from machine import UART, Pin,SPI
import utime,time
import st7789
import vga1_8x16 as font1
#import vga2_8x8 as font
import vga1_16x32 as font
import vga1_16x16 as font2


lst = []
#import vga1_8x16 as font
WiFi_SSID='SSID'  # Wifi_SSID
WiFi_password = 'PASSWORD'      # WiFi Password
TCP_ServerIP = 'IP ADDRESS OF YOUR PC'   # IP of Computer on which TCP server is running
Port = '8080'                    # TCP Server Port

uart = UART(0, 115200)           # Default Baud rate


#information
spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = st7789.ST7789(spi,135,240,reset=Pin(12, Pin.OUT),cs=Pin(9, Pin.OUT),dc=Pin(8, Pin.OUT),backlight=Pin(13, Pin.OUT),rotation=3)
    
def info():
    tft.init()
    utime.sleep(0.2)
    tft.text(font,"SB-COMPONENTS", 15,0)
    tft.fill_rect(15, 40, 210,10, st7789.RED)
    
    tft.text(font,"PICO WIFI HAT", 15,55,st7789.YELLOW)
    tft.fill_rect(15, 90, 210, 10, st7789.BLUE)
    time.sleep(2)
    tft.fill(0) #clear screen
    tft.text(font,"WAITING........", 15,55,st7789.YELLOW)
    
    
    
info()


######## Function to send or receive commands and data

def sendCMD(cmd,ack,timeout=2000):
    uart.write(cmd+'\r\n')
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode()
            lst.append(s)
            print(s)
            
            if(s.find(ack) >= 0):
                return True
    return False
#####################################################

uart.write('+++')
time.sleep(1)
if(uart.any()>0):uart.read()
sendCMD("AT","OK")
sendCMD("AT+CWMODE=3","OK")
sendCMD("AT+CWJAP=\""+WiFi_SSID+"\",\""+WiFi_password+"\"","OK",20000)
sendCMD("AT+CIFSR","OK")
sendCMD("AT+CIPSTART=\"TCP\",\""+TCP_ServerIP+"\","+Port,"OK",10000)
sendCMD("AT+CIPMODE=1","OK")
sendCMD("AT+CIPSEND",">")
tft.text(font,"WAITING........", 15,55,st7789.BLACK)
uart.write('Hello World !!!\r\n')  # Send data to TCP server
uart.write('ESP8266 TCP Client\r\n')
a = lst[4]
res = str(a)[1:-1]
x = res.split(",")
s = x[3].replace('"',"")
print(s)
tft.text(font2,"IP ADDRESS", 5,10)
tft.text(font2,"RECEIVER MODE:", 10,60)

tft.text(font2,s, 5,30)
tft.fill_rect(10, 50, 220,5, st7789.BLUE)

while True:
    s=uart.read()   # receive data from server
    if(s != None):
        s=s.decode()
        tft.text(font1,s, 10,80,st7789.YELLOW)
        time.sleep(2)
        tft.text(font1,"                            ", 10,80)
        print(s)    # Print received data

