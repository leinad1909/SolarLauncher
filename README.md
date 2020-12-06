# SolarLauncher
Unofficial launcher for [Planet Game](https://github.com/Jachdich/planet-client/).
Still very much work in progress.

Solar Launcher is a program that provides a user interface to connecting to a server in Planet Game.

# Installation and Usage
Running from the .py file:
You will need the three files (icon.ico, solar.launchersettings and solarmain.py) to all be in the same directory. It should be as simple as ensuring you have the following includes and running the script:

 - tkinter (apt: python3-tk, should be preinstalled on Windows)
 - ttkthemes (pip: ttkthemes)
 - ConfigParser (pip: configparser)
 - feedparser (pip: feedparser)
 
 Executable releases for both Linux and Windows should be out at some point soon.
 
 If you want to change options (like the appearance style and Planet Game install location) you can use the text file "solar.launcherproperties". I am trying to make it so you don't actually need to go into the main code to change stuff, and am working towards making it so you can modify most things from the "solar.launcherproperties" file.
 
# Future Plans
- Add a "Saved Servers" menu where you can save a server with a name and IP
- Add a more fleshed out options menu with stuff like visual appearance/themes
- Online server browser that people can publically add their server to for other people to connect
 
 I don't really care what you do with the code, feel free to reuse it or change it however you want.
