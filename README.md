# RainLED
This is to be used with a Raspberry Pi in order to create an LED matrix of rain data. Useful as a decoration.
It is currently a work in progress. I have done limited testing, but in theory, it should 
work in other locations, whilst dynamically selecting the best weather station to represent each LED.

Specify the desired dimension (only takes odds, and will replace evens with odds) as an argument after main.py
Defaults to 5x5 if no dimension is specified
Dimension must be at least 3, or the program will go to the default of 5

The data is currently just outputted to the console every 15 minutes, along with a timestamp
If 'log' is passed as an argument, this program will log data to a logs.txt file every 15 minutes.

Configure your APIKey and coordinates in the specified variables in main.py

# You must use your own OpenWeatherMap API Key!
