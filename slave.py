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
make_log("Serial Initialised")
while True :
    
    data_raw = ser.readline()
    make_log("Data read from serial")
    data_raw=str(data_raw,'utf-8')
    data_raw=data_raw[0:-1]
    qr_code = data_raw
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    lcd_string("Updated",LCD_LINE_1)
    GPIO.output(21, False)
    if(data_raw):
        try:
            f1 = open("Output.txt", "a+")
        except:
            f1 = open("Output.txt", "w")
        ts= time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        data_raw= st + "   " + string +'\n' 
        f.write(data_raw)
        f.flush()
        make_log("Information is Updated")
        
        qr_code = "/var/www/html/qpasslitesis/protected/./yiic interaccion interaccion --tipo=salida --qrcode=" + qr_code
        term_out = subprocess.check_output(qr_code,shell=True)
        str_term_out = term_out.decode('utf-8')
        make_log("Data checked with the database")
        term_out=json.loads(str_term_out)
        msg= term_out["message"]
        make_log("Output message is: " + msg)
        n = len(msg)
        status = term_out["status"]
        make_log("Output Status is: " + status)
        if (status==1):
            if (n<16):
                lcd_string(msg,LCD_LINE_1)
                GPIO.output(21, True)
                make_log("Relay ON")
                #time.sleep(1)
            else:
                lcd_string(msg[:16],LCD_LINE_1)
                lcd_string(msg[16:],LCD_LINE_2)
                GPIO.output(21, True)
                make_log("Relay ON")
        else:
            if (n<16):
                lcd_string(msg,LCD_LINE_1)
                make_log("Relay OFF")
            else:
                lcd_string(msg[:16],LCD_LINE_1)
                lcd_string(msg[16:],LCD_LINE_2)
                make_log("Relay OFF")
            #time.sleep(1)
        f.close()

def make_log(string):
    try:
        f=open("Slave_Log.txt", "a+")
    except IOError:
        f = open("Slave_log.txt", "w")
    ts= time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data_raw= "[" + st + "]" + "  " + string+'\n' 
    f.write(data_raw)
    f.flush()


