The scripts have been designed and coded in such a way that they are always functioning and would even work right after the system is rebooted.
This has been done using crontab. Additionally they can be updated over the air (OTA) by us.
#1 Open Terminal
#2 type in: sudo apt-get install crontab (It may ask for your password, type in your password)
#3 type: crontab -e (This would pop up the crontab file in nano)
#4 type: @reboot sleep 30 && cd /home/pi/qrproject (The path where you have saved the file) && python master_program.py
#5 Save the crontab file
#6 type: python register.py(Ensure that you are in the same directory)
#7type: sudo shutdown -r now
#8 Your system is ready to use

