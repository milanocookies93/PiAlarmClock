# PiAlarmClock

## Inspiration
This Alarm Clock attempts to make your morning wakeup a better experience. This Alarm syncs up with your Google Calendar to wake you up at the correct time, gives you a mental challenge to help you wake up, and tells you the temperature when you wake up. 

## How it works
The project is essentially a python program is running on a Raspberry Pi hooked up to some electronics and connected to the internet. The program looks for the "Sleep" event in one's calendar, and sends some current through some speakers when it's over. After the user presses a push button to stop the alarm, we pull the local temperature from Yahoo Weather and sends it in binary to some LEDs. Since the temperature is in binary, the user will have to do some simple math to figure out the temperature, helping them focus and become more awake.

http://milandasgupta.com/redbirdsubmission.mp4
