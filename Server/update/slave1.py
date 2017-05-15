from RPLCD import CharLCD
from RPi import GPIO
import subprocess
import serial
import time
import datetime
from lcd import *
import json
import codecs

def make_log(string):
    try:
        Slave_log_file=open("Slave_Log.txt", "a+")
    except IOError:
        Slave_log_file = open("Slave_log.txt", "w")
    ts= time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data_raw= "[" + st + "]" + "  " + string+'\n' 
    Slave_log_file.write(data_raw)
    Slave_log_file.flush()

make_log("Slave Started")

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
make_log("LCD Initialised")
ser = serial.Serial('/dev/ttyACM0', 2000000, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
ser.flushInput()
ser.flushOutput()
make_log("Serial Initialised")
while True :
    
    data_raw = ser.readline()
    data_raw=str(data_raw,'utf-8')
    data_raw=data_raw[0:-1]
    qr_code = data_raw
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    lcd_string("Updated",LCD_LINE_1)
    GPIO.output(21, False)
    if(data_raw):
        make_log("Barcode Read")
        try:
            output_file = open("Output.txt", "a+")
        except:
            output_file = open("Output.txt", "w")
        ts= time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        data_raw= "[" + st + "]" + "  " + data_raw+'\n' 
        output_file.write(data_raw)
        output_file.flush()
        make_log("Information is Updated")
        
        qr_code = "/var/www/html/qpasslitesis/protected/./yiic interaccion interaccion --tipo=salida --qrcode=" + qr_code
        term_out = subprocess.check_output(qr_code,shell=True)
        str_term_out = term_out.decode('utf-8')
        make_log("Data checked with the database")
        term_out=json.loads(str_term_out)
        msg= term_out["message"]
        make_log("Output message is: " + str(msg))
        n = len(msg)
        status = term_out["status"]
        make_log("Output Status is: " + str(status))
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
        output_file.close()


