# SOLAR LAUNCHER - UNOFFICIAL LAUNCHER FOR PLANET GAME (github.com/Jachdich/planet-client, github.com/Jachdich/planet-server)
# THIS VERSION ONLY WORKS ON WINDOWS

SOLAR_VERSION = 1.1

import urllib.request, os, configparser, feedparser, sys, logging, datetime, re
from subprocess import call
import solarservers, solarthemes
import tkinter as tk
from tkinter import ttk, filedialog, font, messagebox
import webbrowser as web
from ttkthemes import ThemedTk

#Setting up logging
def LogFormat(text):
    now = datetime.datetime.now()
    current_time = now.strftime("%d/%m/%y, %H:%M:%S: ")
    logging.info(current_time +text)
    print(current_time +text)
logging.basicConfig(filename="log.solar", encoding="utf-8", level=logging.DEBUG)

#Translate theme names into actual stuff that can be used
config = configparser.ConfigParser()
with open("settings.solar", "r") as configfile:
    config.read_file(configfile)
    theme = config["STYLE"]["currenttheme"]
    getthemeinfo = solarthemes.Themes(theme)
    themedetails = getthemeinfo.ThemeInfo()
    ttktheme = themedetails[0]
    bgdefault = themedetails[1]
    fgdefault = themedetails[2]

#Configuring tkinter window
window = ThemedTk(theme = ttktheme)
window.title("Solar Launcher")
window.geometry("480x400")
icon = tk.PhotoImage(file = "icon.gif")
window.iconphoto(True, icon)
window.configure(bg = bgdefault)
menubar = tk.Menu(window)
window.config(menu = menubar)

class SetLocation:
    def __init__(self, serverclient):
        self.serverclient = serverclient

    def SetFileLocation(self):
        #Opens window to select planet-client location
        location = str(filedialog.askopenfilename())
        if self.serverclient == 'client':
            config["SETUP"]["ClientLocation"] = location
        else:
            config["SETUP"]["ServerLocation"] = location
        with open("settings.solar", "w") as configfile:
            config.write(configfile)
        if "planet" not in location:
            tk.messagebox.showwarning(title = "Solar Launcher - Warning", message = "This install location may be invalid. Proceed with caution.")

def InstallLocationWarning():
    with open("settings.solar", "r") as configfile:
        config.read_file(configfile)
        clientsavedlocation = (config["SETUP"]["clientlocation"])
    LogFormat("Install Location: " +clientsavedlocation)
    if "planet-client" not in str(clientsavedlocation):
        locationwarning = tk.messagebox.askyesno(title = "Solar Launcher", message = "Solar Launcher has detected an invalid or missing install location for planet-client. Would you like to set a new one now?")
        if locationwarning == True:
            setclientlocation.SetFileLocation()
    return

def LoadUpdateFeed():
    try:
        feed = feedparser.parse("https://github.com/Jachdich/planet-client/commits/master.atom")
        feedtext = (feed["entries"][0]["title"])
        updatetime = "at " +feed["entries"][0]["updated"]
        LogFormat("Commit feed updated successfully.")
    except urllib.error.URLError:
        feedtext = "Failed to connect to GitHub."
        updatetime = "Please check your internet connection."
        LogFormat("Cannot connect to GitHub. Will not update feed.")
    try:
        feedlabel.config(text = feedtext)
        updatelabel.config(text = updatetime)
        return
    except NameError:
        return feedtext, updatetime

def LaunchClient():
    #Launches planet-client with given install location and IP
    clientsavedlocation = (config["SETUP"]["clientlocation"])
    launchcommand = clientsavedlocation +" " +ipaddress.get()
    print("Opening " +launchcommand)
    try:
        subprocess.call(launchcommand)
        window.destroy()
    except FileNotFoundError or OSError:
        tk.messagebox.showerror(title = "Solar Launcher - Error", message = "No planet-client install location specified. Please set a location under the Setup menu tab.")

class OptionsMenu():
    def __init__(self):
        self.optionsmenu = tk.Toplevel(window, bg = bgdefault)
        self.optionsmenu.geometry("400x300")
        ttk.Label(self.optionsmenu, text = "Options", font = "Helvetica 20").pack()
        ttk.Label(self.optionsmenu, text = " ", font = "Unispace 10 bold").pack()
        ttk.Label(self.optionsmenu, text = "Appearance Settings", font = "Helvetica 10 underline").pack()
        ttk.Label(self.optionsmenu, text = "Theme: ").pack(anchor = tk.W, padx = 10, pady = 8)
        self.stylevariable = tk.StringVar()
        self.stylevariable.set(theme)
        ttk.Radiobutton(self.optionsmenu, text = "DARK", variable = self.stylevariable, value = "DARK", command = self.ChangeTheme).pack(anchor = tk.W, padx = 20, pady = 2)
        ttk.Radiobutton(self.optionsmenu, text = "LIGHT", variable = self.stylevariable, value = "LIGHT", command = self.ChangeTheme).pack(anchor = tk.W, padx = 20, pady = 2)

    def ChangeTheme(self):
        with open("settings.solar", "r") as configfile:
            config.read_file(configfile)
            config["STYLE"]["currenttheme"] = self.stylevariable.get()
        with open("settings.solar", "w") as configfile:
            config.write(configfile)
        tk.messagebox.showwarning(title = "Solar Launcher", message = "Please restart Solar Launcher for changes to take effect.")

class SavedServersMenu:
    def __init__(self, window):
        self.window = window
        try:
            self.servernames = solarservers.manageservers.ServerSearch()
            self.serverdetails = solarservers.manageservers
        except TypeError:
            self.servernames = {"None":""}
        self.windowopen = False
        self.selectedserver = tk.StringVar()

    def InsertSavedServer(self):
        self.solargetdetails = solarservers.ManageServers(self.selectedserver.get())
        ipaddress.set(self.solargetdetails.GetServerDetails()["ip"])

    def RemoveServer(self):
        self.solargetdetails = solarservers.ManageServers(self.selectedserver.get())
        self.solargetdetails.DeleteServer()

    def SaveServer(self):
        self.serversconfig = solarservers.ManageServers(self.newservernametext.get(), self.newserveriptext.get())
        self.serversconfig.AddNewServer()

    def CreateWindow(self):
        serversmenu = tk.Toplevel(self.window, bg = bgdefault)
        serversmenu.geometry("340x220")
        
        self.serverselectframe = tk.Frame(serversmenu, bg = bgdefault)

        self.serversselect = ttk.OptionMenu(self.serverselectframe, self.selectedserver, "Select a saved server...", *self.servernames)
        self.serversselect.pack(pady = 10, padx = 5, side = tk.LEFT)
        ttk.Button(self.serverselectframe, text = "Apply", command = self.InsertSavedServer).pack(side = tk.LEFT)
        ttk.Button(self.serverselectframe, text = "Delete", command = self.RemoveServer).pack(side = tk.LEFT)

        self.serverselectframe.pack(side = tk.TOP)

        ttk.Label(serversmenu, text = "Add a new saved server:").pack(pady = 10, padx = 5, anchor = tk.W)

        self.newservernameframe = tk.Frame(serversmenu, bg = bgdefault)
        self.newservernameframe.pack(pady = 5)
        ttk.Label(self.newservernameframe, text = "Server Name:").pack(padx = 10, pady = 5, side = tk.LEFT)
        self.newservernametext = tk.StringVar()
        self.newservername = ttk.Entry(self.newservernameframe, textvariable = self.newservernametext)
        self.newservername.pack(side = tk.RIGHT)

        self.newserveripframe = tk.Frame(serversmenu, bg = bgdefault)
        self.newserveripframe.pack(pady = 5)
        ttk.Label(self.newserveripframe, text = "Server Address:").pack(padx = 10, pady = 5, side = tk.LEFT)
        self.newserveriptext = tk.StringVar()
        self.newserverip = ttk.Entry(self.newserveripframe, textvariable = self.newserveriptext)
        self.newserverip.pack(side = tk.RIGHT)

        ttk.Button(serversmenu, text = "Save Server", command = self.SaveServer).pack(pady = 5)

        ttk.Label(serversmenu, text = "Any changes made here will update after launcher restart.").pack()


def UpdateCheck():
    try:
        releasefeed = feedparser.parse("https://github.com/NeptuniteDaniel/SolarLauncher/releases.atom")
        versionname = (releasefeed["entries"][0]["title"])
        versionnumber = re.findall("\d+\.\d+", versionname)
        latestversion = versionnumber[0]
        versioninfo = ("Current version: " +str(SOLAR_VERSION) +" Latest: " +str(latestversion))
        LogFormat(versioninfo)
        if float(latestversion) > float(SOLAR_VERSION):
            updatenotify = tk.messagebox.askyesno(title = "Solar Launcher - Update", message = ("There is a newer version of Solar Launcher available. Would you like to download it now?" +" (" +str(latestversion) +" > " + str(SOLAR_VERSION) +")"))
            if updatenotify == True:
                web.open("github.com/NeptuniteDaniel/SolarLauncher")
        return versioninfo
    except urllib.error.URLError or IndexError:
        LogFormat("Update checking could not find or connect to a version list.")
        return "Could not find or connect to a version list."

setclientlocation = SetLocation('client')
setserverlocation = SetLocation('server')

#About Menu
aboutmenu = tk.Menu(menubar)
menubar.add_cascade(label = "About", menu = aboutmenu)
aboutmenu.add_command(label = "planet-client on GitHub", command = (lambda l = "https://github.com/Jachdich/planet-client": web.open(l)))
aboutmenu.add_command(label = "planet-server on GitHub", command = (lambda l = "https://github.com/Jachdich/planet-server": web.open(l)))
aboutmenu.add_command(label = "Solar Launcher on GitHub", command = (lambda l = "https://github.com/NeptuniteDaniel/SolarLauncher": web.open(l)))

#Setup Menu
setupmenu = tk.Menu(menubar)
menubar.add_cascade(label = "Setup", menu = setupmenu)

setupmenu.add_command(label = "Set planet-client install location", command = setclientlocation.SetFileLocation)
setupmenu.add_command(label = "Set planet-server install location", command = setserverlocation.SetFileLocation)

#Options Menu
optionsmenu = tk.Menu(menubar)
menubar.add_cascade(label = "Options", menu = optionsmenu)
optionsopen = OptionsMenu
optionsmenu.add_command(label = "Options menu", command = optionsopen)

#Title
ttk.Label(text = "Solar Launcher", font = "GENISO 40").pack()
ttk.Label(text = "Unofficial launcher for Planet Game", font = "Helvetica 12").pack()

#Update Feed
updateframe = tk.Frame(window, highlightbackground = fgdefault, highlightthickness = 1, bg = bgdefault)
updateframe.pack(pady = 10)

ttk.Label(updateframe, text = "Most recent commit to planet-client master:", font = "Helvetica 10 bold").pack()
ttk.Label(updateframe, text = " ", font = "Unispace 2 bold").pack()

feedtext, updatetime = LoadUpdateFeed()

feedlabel = ttk.Label(updateframe, text = feedtext)
feedlabel.pack()
updatelabel = ttk.Label(updateframe, text = updatetime)
updatelabel.pack()
ttk.Button(updateframe, text = "Download new updates", command = (lambda l = "https://github.com/Jachdich/planet-client/commits": web.open(l))).pack(pady = 10)
optionsmenu.add_command(label = "Refresh commit updates", command = LoadUpdateFeed)

#IP Input
ttk.Label(text = "Server Address:").pack()
ipaddress = tk.StringVar()
ipentry = ttk.Entry(textvariable = ipaddress)
ipentry.pack(pady = 5)
versionlabel = ttk.Label(text = "Getting version...", font = 'Helvetica 8')
versionlabel.pack(side = tk.BOTTOM)
ttk.Button(text = "Connect", command = LaunchClient).pack(side = tk.BOTTOM, pady = 10)
createsavedservers = SavedServersMenu(window)
savedserversbutton = ttk.Button(text = "Saved Servers", command = (createsavedservers.CreateWindow))
savedserversbutton.pack(side = tk.TOP)

versionlabel.config(text = UpdateCheck())
InstallLocationWarning()

window.mainloop()