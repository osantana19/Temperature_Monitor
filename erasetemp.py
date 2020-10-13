#This code was written to just erase whatever is inside the temperature.txt file
#It's purpose is because the dht11.py script appends the temperature output to the end of the temperature.txt
#So in order to keep the temperature.txt file from being an infinitely long save file
#This file was made so it would erase all the contents inside that file at the end of the day
#There is a cronjob that runs this script everyday at midnight
#To view the cronjob type crontab -l
#To change the cronjob settings type crontab -e and change the one corresponding to this file
#Use the website: https://crontab.guru/   to help when changing the time for the cron schedule
#For anything else cronjob related resort to this article:  https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/

file='/home/pi/temperature.txt'          #adds the file to a variable called file
with open(file, 'w') as filetowrite:     #opens the variable file and says overwrite file with the following
    filetowrite.write('')    #inside of the ('') is what gets written to the file example: filetowrite.write('cool') will overwrite all contents within file with just one word cool
