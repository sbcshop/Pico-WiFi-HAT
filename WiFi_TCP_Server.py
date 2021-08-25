# Use thonny ide to program pico
# Use Hercules SETUP utility for TCP server and client https://www.hw-group.com/software/hercules-setup-utility
# Make sure both WiFi HAT and TCP Server are connected on same network

from machine import UART, Pin
import utime,time

WiFi_SSID='WiFi_SSID'               # Enter Wifi SSID here
WiFi_password = 'WiFi_Password'     # Enter WiFi Password here
Port = '8080'                       # TCP Server Port

uart = UART(0, 115200)              # Default Baud rate of ESP8266

########  Function to send command  ###############

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

########  Function to send data  ###############

def sendData(ID,data):
    sendCMD('AT+CIPSEND='+str(ID)+','+str(len(data)),'>')
    uart.write(data)

########  Function to receive data  ###############

def ReceiveData():
    data=uart.read()
    if(data != None):
        data=data.decode()
        print(data)
        if(data.find('+IPD') >= 0):
            n1=data.find('+IPD,')
            n2=data.find(',',n1+5)
            ID=int(data[n1+5:n2])
            n3=data.find(':')
            data=data[n3+1:]
            return ID,data
    return None,None

uart.write('+++')
time.sleep(1)
if(uart.any()>0):uart.read()
sendCMD("AT","OK")
sendCMD("AT+CWMODE=3","OK")
sendCMD("AT+CWJAP=\""+WiFi_SSID+"\",\""+WiFi_password+"\"","OK",20000)
sendCMD("AT+CIPMUX=1","OK")
sendCMD("AT+CIPSERVER=1,"+Port,"OK")
sendCMD("AT+CIFSR","OK")

while True:
    Connection_ID,data=ReceiveData()
    if(Connection_ID != None):
        sendData(Connection_ID,data) #Send received data back to TCP Server
        print(data)   # Print Received data
