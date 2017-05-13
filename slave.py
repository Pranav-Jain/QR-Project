from RPLCD import CharLCD
from RPi import GPIO
import subprocess
import serial
import time
import datetime
from lcd import *
import json
import codecs

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7
GPIO.setup(21, GPIO.OUT)

lcd_init()
ser = serial.Serial('/dev/ttyACM0', 2000000, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
ser.flushInput()
ser.flushOutput()
while True :
    
    data_raw = ser.readline()
    data_raw=str(data_raw,'utf-8')
    data_raw=data_raw[0:-1]
    qr_code = data_raw
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    lcd_string("Scan QR",LCD_LINE_1)
    GPIO.output(21, False)
    if(data_raw):
        try:
            f=open("output.txt", "a+")
        except IOError:
            f=open("output.txt", "w")
        ts= time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(data_raw,st)
        data_raw= data_raw +"   "+st+'\n' 
        f.write(data_raw)
        f.flush()
        
        
        qr_code = "/var/www/html/qpasslitesis/protected/./yiic interaccion interaccion --tipo=salida --qrcode=" + qr_code
        term_out = subprocess.check_output(qr_code,shell=True)
        str_term_out = term_out.decode('utf-8')
        term_out=json.loads(str_term_out)
        msg= term_out["message"]
        n = len(msg)
        status = term_out["status"]
        print(msg)
        if (status==1):
            if (n<16):
                lcd_string(msg,LCD_LINE_1)
                GPIO.output(21, True)
                #time.sleep(1)
            else:
                lcd_string(msg[:16],LCD_LINE_1)
                lcd_string(msg[16:],LCD_LINE_2)
                GPIO.output(21, True)
        else:
            if (n<16):
                lcd_string(msg,LCD_LINE_1)
            else:
                lcd_string(msg[:16],LCD_LINE_1)
                lcd_string(msg[16:],LCD_LINE_2)
            
            #time.sleep(1)
        f.close()


