#This script was made to copy the temperature.txt file over to the Temporary_Logs folder at end of the day
#There is a cronjob that runs this script everyday at 11:59 pm before temperature.txt gets erased by the erasetemp.py script at midnight
#To view the cronjob type crontab -l
#To change the cronjob settings type crontab -e and change the one corresponding to this file
#Use the website: https://crontab.guru/   to help when changing the time for the cron schedule
#For anything else cronjob related resort to this article:  https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/

import shutil                         #imports the shutil protocol used for copying files
from datetime import datetime         #imports datetime protocol used for finding date and time

now = datetime.now()                  #assigns the date and time to a variable called now
dt_string = now.strftime("%m_%d_%Y")  #takes the now variable and assigns it to dt_string variable with formatting %m=month %d=day %Y=year

print(dt_string) #placed this here for testing purposes to see how dt_string is formatted
original = r'/home/pi/temperature.txt'                             #assigns temperature.txt file location to variable original
target = r'/home/pi/Temperature_Logs/templog_' + dt_string + '.txt'#assigns the new location you want to copy orginal file over to. added dt_string to add date to end of file

print(target) #placed this here for testing the formatting on the copied file name

shutil.copyfile(original, target)    #This is where it tells it to copy the original file to the target file path
