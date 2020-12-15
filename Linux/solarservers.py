from configparser import ConfigParser

class ManageServers():
    def __init__(self, servername = "", serverip = ""):
        self.servername = servername
        self.serverip = serverip
        self.config = ConfigParser()

    def ServerSearch(self):
        with open('servers.solar', "r") as fp:
            config = ConfigParser()
            config.read_file(fp)
            self.serveraddresses = config.sections()
            return self.serveraddresses
    
    def GetServerDetails(self):
        with open("servers.solar", "r") as fp:
            config = ConfigParser()
            config.read_file(fp)
            self.serverdetails = config._sections[self.servername]
            return self.serverdetails

    def AddNewServer(self):
        with open('servers.solar', 'a') as configfile:
            if self.servername not in self.ServerSearch():
                self.config[self.servername] = {"ip": self.serverip}
                self.config.write(configfile)

manageservers = ManageServers()