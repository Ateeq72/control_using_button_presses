import RPi.GPIO as GPIO
import time
import sys
import os
from time import sleep

sw_in = 26
LED = 18
file = open('/home/pi/PiraCast/status','r+w')
f = file.read()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sw_in,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(sw_in,GPIO.FALLING)
GPIO.setup(LED,GPIO.OUT)
GPIO.setwarnings(False)

def flashLED(speed, time):
        for x in range(0, time):
                GPIO.output(LED, GPIO.LOW)
                sleep(speed)
                GPIO.output(LED, GPIO.HIGH)
                sleep(speed)

flashLED(0.5, 5)

def triplePress():
       	flashLED(0.5, 3)
	print ("Pressed Thrice So! Switching to Piracast!")
	print ("Killing VNC Server as it may interfere!")
	os.system("sudo -u root vncserver -kill :0")
	os.system("sudo -u root vncserver -kill :1")
	os.system('echo "You pressed the button thrice!. So, Switching to Piracast" | festival --tts')
	if f[0] == "1":
	   print('Starting! Piracast')
           os.system('echo "suitable environment found!. So, switching to Piracast" | festival --tts')
	   os.system("sh /home/pi/runme_piracast.sh")
	elif f[0] == "0":
	   print('Changing file and rebooting')
	   os.system('echo "Sorry no suitable environment found!. Changing the file and rebooting!" | festival --tts')
	   os.system("echo 1 > /home/pi/PiraCast/status")
	   os.system("sh /home/pi/PiraCast/switch_to_piracast")

def doublePress():
	flashLED(0.5, 2)
        print ("Pressed Twice So! Kodi! Here We come! :D")
	os.system("sudo -u root vncserver -kill :0")
	os.system("sudo -u root vncserver -kill :1")
	os.system('echo "You pressed the button twice!. So, KODI here we come!" | festival --tts')
        if f[0] == "1":
	   print("Changing file and rebooting")
	   os.system('echo "Sorry! no suitable environment found!. Changing the file and rebooting" | festival --tts') 
	   os.system("echo 0 > /home/pi/PiraCast/status")
	   os.system("sh /home/pi/PiraCast/switch_to_normal")
        elif f[0] == "0" :
	   os.system('echo "suitable environment found!. So, Starting KODI!." | festival --tts')
	   print("Suitable situation found ! so starting")
	   os.system("sudo -u pi kodi-standalone")

def singlePress():
	flashLED(0.5, 1)
        print ("Pressed Once So! Home Automation!")
	os.system('echo "You pressed the button once!. So, Home Automation!" | festival --tts')
        if f[0] == "1":
	  print("Changing file and rebooting")
	  os.system('echo "Sorry! no suitable environment found!. Changing the file and rebooting" | festival --tts')
          os.system("echo 0 > /home/pi/PiraCast/status")
          os.system("sh /home/pi/PiraCast/switch_to_normal")
        elif f[0] == "0" :
	  print("Suitable situation found ! so starting")
	  os.system('echo "Suitable environment found ! so starting" | festival --tts')
	  os.system('echo "use this Address to control your electrical devices!" | festival --tts && hostname -I | festival --tts && echo " colon 8 0 9 0" | festival --tts')
	  os.system("sudo -u pi sh /home/pi/HomeAutomation/runme.sh")
        


while True:
 try:
   if GPIO.event_detected(sw_in):
      GPIO.remove_event_detect(sw_in)
      now = time.time()
      count = 1
      GPIO.add_event_detect(sw_in,GPIO.RISING)
      while time.time() < now + 1: # 1 second period
         if GPIO.event_detected(sw_in):
            count +=1
            time.sleep(.25) # debounce time
      #print count
      #performing required task!
      if count == 2:
	singlePress()
	GPIO.remove_event_detect(sw_in)
        GPIO.add_event_detect(sw_in,GPIO.FALLING)
	#break
      elif count == 3:
	doublePress()
	GPIO.remove_event_detect(sw_in)
	GPIO.add_event_detect(sw_in,GPIO.FALLING)
	#break
      elif count == 4:
	triplePress()
        GPIO.remove_event_detect(sw_in)
        GPIO.add_event_detect(sw_in,GPIO.FALLING)
	#break



 except KeyboardInterrupt:
        GPIO.cleanup()
        print "\n Terminated on request"
	sys.exit()
	file.close()

