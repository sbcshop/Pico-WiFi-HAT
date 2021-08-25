# Use thonny ide to program pico
# Use Hercules SETUP utility for TCP server and client https://www.hw-group.com/software/hercules-setup-utility

from machine import UART, Pin
import utime,time

WiFi_SSID='WiFi_SSID'  # Wifi_SSID
WiFi_password = 'WiFi_Password'      # WiFi Password
TCP_ServerIP = '192.168.1.22'   # IP of Computer on which TCP server is running
Port = '8080'                    # TCP Server Port

uart = UART(0, 115200)           # Default Baud rate


######## Function to send or receive commands and data

def sendCMD(cmd,ack,timeout=2000):
    uart.write(cmd+'\r\n')
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode()
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

uart.write('Hello World !!!\r\n')  # Send data to TCP server
uart.write('ESP8266 TCP Client\r\n')
while True:
    s=uart.read()   # receive data from server
    if(s != None):
        s=s.decode()
        print(s)    # Print received data
