# This is a project I worked on while first getting to grips with programming. It may or may not work but I will not provide any support and will no longer be updated in its current form.

# Solar Launcher
Unofficial launcher for [Planet Game](https://github.com/Jachdich/planet-client/).
Still very much work in progress.

Solar Launcher is a program that provides a user interface to connecting to a server in Planet Game.

#### This project (probably) hasn't been abandoned. 
I don't commit to GitHub much, so if the last commit was a week or two ago, I'm probably still working on it but just haven't bothered committing it. I tend to commit in bursts when I have a lot of stuff ready to add.

## Installation and Usage
Running from the .py file:
You will need the files (icon.ico, solarservers.py, solarmain.py and all the .solar files) to all be in the same directory. It should be as simple as ensuring you have the following includes and running the script:

 - tkinter (apt: python3-tk, should be preinstalled on Windows)
 - ttkthemes (pip: ttkthemes)
 - ConfigParser (pip: configparser)
 - feedparser (pip: feedparser)
 
 Windows executables are released shortly after an update to the source. Linux executables may be available at some point.
 
 If you want to change options (like the appearance style and the Planet Game install location) you can use the text file "settings.solar". I am trying to make it so you don't actually need to go into the main code to change stuff, and am working towards making it so you can modify most things from the "settings.solar" file.
 
## Future Plans
- Online server browser that people can publically add their server to for other people to connect
- Texture pack switching and possibly online texture pack browser
 
 I don't really care what you do with the code, feel free to reuse it or change it however you want. Some credit is nice though.
