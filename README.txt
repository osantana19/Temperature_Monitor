# Temperature_Monitor
This read me is made to help explain the cronjobs used to setup the Temperature Sensor and how to use the scripts associated with them.

First to explain what a cronjob is it's basically Linux's version of Windows Task Scheduler.
In order to setup a cronjob (aka schedule a task) you need to open up the command line.

I've setup a few cronjobs for the multiple scripts I made and one cronjob has no script it's just a task 
setup to delete files to get erased 

To view the cronjob type crontab -l
What you will see is a list of the cronjobs available at the bottom.
Anything starting with # is just a comment so those do not run they are just notes.



The cronjobs will appear like this at the bottom of the command screen: 

	1 17 * * * python /home/pi/dht11.py &

	59 23 * * * python /home/pi/copyfiles.py &

	1 16 * * * /home/pi/Temperature_Logs/* -ctime +7 -exec rm {} \; 

	0 0 * * * python /home/pi/erasetemp.py &



To explain each job I will break it down by line. More descriptions on what each script does can be found in the comments
provided within each indivdual script



1) The first job is:

	1 17 * * * python /home/pi/dht11.py &

	This job makes is so that the dhty11.py script runs every day at 5:01 pm each day. This is the main sensor script which
	checks for temperature, logs the temperature in a file called temperature.txt, and sends out the email/text alerts
	when ever the temperature exceeds 75 degrees farenheit


2) The second job is:

	59 23 * * * python /home/pi/copyfiles.py &
	
	This job runs the copyfiles.py script everyday at 11:59 pm. It copies the temperature.txt file as a new file in to the
	Temperature_Logs folder as templog(todaysdate).txt. The temperature.txt file holds the temperature readings for the entire day.
	It needs to be copied over because the temperature.txt file gets erased and replaced at midnight to make room for the next days 
	temperature logs.


3)The third job is:

	1 16 * * * /home/pi/Temperature_Logs/* -ctime +7 -exec rm {} \; 

	This is the only job that doesn't run a script its a task that runs a regular expression to delete files within the 
	Temperature_Logs folder at 4:01pm. You can change the amount of days by changing the number after the +. From example 
	changing the ... -ctime +5 ... in the above script will delete files that are more than 5 days old.


4) The fourth and final job is:

	0 0 * * * python /home/pi/erasetemp.py &

	This job runs the erasetemp.py script everyday at midnight. This is the final piece of the code. It erases the contents 
	in temperature.txt file. It's designed to erase it every day at midnight after all the contents in temperature.txt  are copied 
	over into the Temperature_Logs folder as a new file. It prevents the temperature.txt file from being infinitely long and 
	it's also what makes sure the logs are kept for that day only. Think of the temperature.txt as a live log file for the day.
	


To Kill the pi running the temperature script for the day incase of emergencies first you need to type:
	
	ps aux | grep dht11.py

The command above will display the PID number for the command running. for example it will output something like this:

	pi         378  0.0  1.0  17384 10052 ?        S    02:40   0:01 python /home/pi/dht11.py
	            ^
	           PID#

In the example above the place where the 378 is stands for the PID number we need in order to kill the process. Once you have that number
enter it into the next command after the sudo kill -9 which is:

	sudo kill -9 378
		      ^
		     PID#

After you run the code you can run the ps aux | grep dht11.py to verify the task is gone.
If you see a command that looks like this:

pi        3517  0.0  0.0   7348   556 pts/0    R+   08:57   0:00 grep --color=auto dht11.py

Don't worry about it that's just the grep command we used to search for the dht11.py script so it's already gone.

	

To change the cronjob settings type crontab -e and change the one corresponding to the file you want
Use the website: https://crontab.guru/   to help when changing the time for the cron schedule
For anything else cronjob related resort to this article:  https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/
