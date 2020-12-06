# SOLAR LAUNCHER - UNOFFICIAL LAUNCHER FOR PLANET GAME (github.com/Jachdich/planet-client, github.com/Jachdich/planet-server)
# THIS VERSION ONLY WORKS ON LINUX

import tkinter as tk
import webbrowser as web
import urllib.request
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
import os
import configparser
from tkinter import messagebox
import feedparser
import subprocess

window = ThemedTk(theme = "equilux")

bgdefault = "#464646"
fgdefault = "#a6a6a6"

config = configparser.ConfigParser()
config['SETUP'] = {}

window.title("Solar Launcher")
window.geometry("400x350")
window.iconbitmap(os.getcwd() +"/icon.ico")

window.configure(bg = bgdefault)

menubar = tk.Menu(window)
window.config(menu = menubar)

def SetClientLocation():
    clientlocation = str(filedialog.askopenfilename())
    config['SETUP']['ClientLocation'] = clientlocation
    with open('solar.launchersettings', 'w') as configfile:
        config.write(configfile)
    if "planet-client" not in clientlocation:
        tk.messagebox.showwarning(title = "Solar Launcher - Warning", message = "This install location may be invalid. Proceed with caution.")
    return

def SetServerLocation():
    serverlocation = str(filedialog.askopenfilename())
    config['SETUP']['ServerLocation'] = serverlocation
    with open('solar.launchersettings', 'w') as configfile:
        config.write(configfile)
    return

def InstallLocationWarning():
    locationwarning = tk.messagebox.askyesno(title = 'Solar Launcher', message = 'Solar Launcher has detected an invalid or missing install location for planet-client. Would you like to set a new one now?')
    if locationwarning == True:
        SetClientLocation()
    return

def LoadUpdateFeed():
    feed = feedparser.parse('https://github.com/Jachdich/planet-client/commits/master.atom')
    feedtext = (feed['entries'][0]['title'])
    feedlabel.config(text = feedtext)
    updatetime = "at " +feed['entries'][0]['updated']
    updatelabel.config(text = updatetime)
    return

def LaunchClient():
    config.read('solar.launchersettings')
    clientsavedlocation = (config['SETUP']['clientlocation'])
    launchcommand = "./" +clientsavedlocation +" " +ipentry.get()
    print("Opening " +launchcommand)
    subprocess.call(launchcommand)
    window.destroy()

#About Menu
aboutmenu = tk.Menu(menubar)
menubar.add_cascade(label = "About", menu = aboutmenu)
aboutmenu.add_command(label = "planet-client on GitHub", command = (lambda l = "https://github.com/Jachdich/planet-client": web.open(l)))
aboutmenu.add_command(label = "planet-server on GitHub", command = (lambda l = "https://github.com/Jachdich/planet-server": web.open(l)))

#Setup Menu
setupmenu = tk.Menu(menubar)
menubar.add_cascade(label = "Setup", menu = setupmenu)
setupmenu.add_command(label = "Set planet-client install location", command = SetClientLocation)
setupmenu.add_command(label = "Set planet-server install location", command = SetServerLocation)

#Options Menu
optionsmenu = tk.Menu(menubar)
menubar.add_cascade(label = "Options", menu = optionsmenu)
optionsmenu.add_command(label = "Refresh commit updates", command = LoadUpdateFeed)

#Title
title = ttk.Label(text = "Solar Launcher", font = "GENISO 40").pack()
title2 = ttk.Label(text = "Unofficial launcher for Planet Game", font = "Helvetica 12").pack()
divider = ttk.Label(text = " ", font = "Unispace 10 bold").pack()

#Update Feed
updateframe = tk.Frame(window, highlightbackground = fgdefault, highlightthickness = 1, bg = bgdefault)
updateframe.pack()

feedtitle = ttk.Label(updateframe, text = "Most recent commit to planet-client master:", font = "Helvetica 10 bold").pack()
dividersmall = ttk.Label(updateframe, text = " ", font = "Unispace 2 bold").pack()

feed = feedparser.parse('https://github.com/Jachdich/planet-client/commits/master.atom')
feedtext = (feed['entries'][0]['title'])
feedlabel = ttk.Label(updateframe, text = feedtext)
feedlabel.pack()
updatetime = "at " +feed['entries'][0]['updated']
updatelabel = ttk.Label(updateframe, text = updatetime)
updatelabel.pack()

dividersmall = ttk.Label(updateframe, text = " ", font = "Unispace 2 bold").pack()

updatebutton = ttk.Button(updateframe, text = "Download new updates", command = (lambda l = "https://github.com/Jachdich/planet-client/commits": web.open(l))).pack()
divider = ttk.Label(text = " ", font = "Unispace 10 bold").pack()

#IP Input
iptext = ttk.Label(text = "Server Adress:").pack()
ipentry = ttk.Entry()
ipentry.pack()
divider = ttk.Label(text = " ", font = "Unispace 10 bold").pack()
ipaddress = str(ipentry.get)
launchbutton = ttk.Button(text = "Connect", command = LaunchClient).pack()

config.read('solar.launchersettings')
clientsavedlocation = (config['SETUP']['clientlocation'])
print(clientsavedlocation)
if "planet-client" not in str(clientsavedlocation):
    InstallLocationWarning()

window.mainloop()
