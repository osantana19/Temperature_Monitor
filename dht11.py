#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           dht11.py
#  Basic example script to read DHT11 sensor using 
#  Adafruit DHT library:
#  https://github.com/adafruit/Adafruit_Python_DHT
#
#  Based on examples by Tony DiCola
#
# Author : Matt Hawkins
# Date   : 04/09/2017
#
# http://www.raspberrypi-spy.co.uk/tag/dht11/
#
#--------------------------------------

#Didn't want to remove credit from the guy above who created the base of the code that I expanded on incase you guys want to check out the original

#Created this code to check the temperature and send out emails/text alerts when over a certain amount of degrees
#There is a cronjob that runs this script everyday at 5:01pm after everyone leaves for the day
#The script is designed to run for 23 hours and 58 minutes
#To view the cronjob type crontab -l
#To change the cronjob settings type crontab -e and change the one corresponding to this file
#Use the website: https://crontab.guru/   to help when changing the time for the cron schedule
#For anything else cronjob related resort to this article:  https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/

import os
import re
import Adafruit_DHT
import time
import threading
from datetime import datetime
import smtplib, ssl

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor = Adafruit_DHT.DHT22

# Set GPIO sensor is connected to.
gpio = 17

#Set date and time

now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

#method for opening and writing to a file
def tempfile():
    f = open("temperature.txt",'a+')
    for i in range (2):
        f.write(str)

SMTP_PORT = 587  # For SSL
SMTP_SERVER = "smtp.gmail.com"            # Enter type of email server run
GMAIL_USERNAME = "noreply@easternia.com"  # Enter your address
GMAIL_PASSWORD = "newaccount12"           # Enter your password
class Emailer:
    def sendmail(self, recipient, subject, content):
         
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
 
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
 
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
 
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit

# Sets up where to send Emails
sender = Emailer()
sendTo = 'it@easternia.com'      #It email chain
sendTo2 = '3392292459@vtext.com' #Oliver
sendTo3 = '3392224287@vtext.com' #Steve
sendTo4 = '6175195579@vtext.com' #Chris
sendTo5 = '7814241042@vtext.com' #Bob

# Sets up the email subject and contents
emailSubject = "Waltham Server Rooms Hot"    
emailContent = "This is a test of my Email of temperature alerts"  
emailSubject2 = "Temperature Gauge Offline!!"        
emailContent2 = "Temperature gauge has been knocked offline. Failed to get reading."

# Sets the maximum temperature for room before Alerts are sent out 
tempmax = (75.9)   #Change value to set temperature


# Creates a function called run_check to be called upon and executed to send the emails/texts out 
def run_check():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio) #Assigns humidty and temperature output to respective variables
    temperature = float(temperature * 1.8 + 32)      #Changes the temperature value from celsius to farenheit
    now = datetime.now()                             #Assigns the date and time to variable now
    dt_string = now.strftime("%m/%d/%Y %H:%M")       #Formats the now variable and assigns to a new variable dt_string
    if humidity is not None and temperature is not None:    #if statement to make sure sensor is working
        print('Temp={0:0.1f}  Humidity={1:0.1f}%  '.format(temperature, humidity),dt_string)        #Placed this here for testing purposes prints out if works
        if temperature > float(tempmax):      #If the temperature is over the amount set in tempmax it will send emails/texts
            
            # Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
            sender.sendmail(sendTo, emailSubject, emailContent)
            sender.sendmail(sendTo2, emailSubject, emailContent)
            sender.sendmail(sendTo3, emailSubject, emailContent)
            sender.sendmail(sendTo4, emailSubject, emailContent)
            sender.sendmail(sendTo5, emailSubject, emailContent)
            print ('fire sent')
        else:
            print ('ok')
    else:
        sender.sendmail(sendTo, emailSubject2, emailContent2)  #Sends out the notice that the reader is down to IT email
        print('Failed to get reading. Try again!')
    

#Sets the counter values for the loops
counter2 = (5)  #This counter is set to 29 because the counter2 if statement is triggered once it hits 30. it then takes an hour with this setup to trigger again
counter = (0)    #For the while loop so our main loop keeps going for 23 hrs and 58min because the sleep time is set to 2 minutes and runs 719 times

while counter < 143:
    #runs the runcheck command and sends out emails and texts alerts

    #Needed to run temperature check seperate to save it to temp1 variable
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    temperature = float(temperature * 1.8 + 32)
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M")
    #Saves Temperature to a variable
    temp1 = ('Temp={0:0.1f}  Humidity={1:0.1f}%  '.format(temperature, humidity),dt_string)
    #Turns temperature output into a string
    temp2 = (str(temp1))
    #expression to remove weird characters from string
    temp3 = re.sub("'|\(|\)|,", '', temp2)
    print(temp3)
    f = open("temperature.txt",'a+')
    f.write(temp3)
    f.write("\r\n")
    f.close()
    if temperature > float(tempmax):
        print('fire')
        counter2 = counter2 + 1
        counter = counter + 1              
    else:
        counter = counter + 1
    if counter2 >= (6):
        emailContent = "Waltham server room temperature is high, the current temp is: " + str(int(temperature)) + " degrees"
        run_check()
        counter2 = (0)
    else:
        print ('ok') 
    time.sleep(599)  #Amount of seconds before the code runs again
print ('finished')

#humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
         
# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.
#if humidity is not None and temperature is not None:
    #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
#else:
    #print('Failed to get reading. Try again!')
