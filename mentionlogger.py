# mentionlogger.py

""" Logs mentions. Reads the log when you first log into znc,
 or by command. Currently doesn't distinguish between different users.
"""

import datetime
import znc

def get_timestamp():
    return datetime.datetime.now().strftime("[%m:%d:%Y %H:%M:%S]")

setting_splitter = ";~.`;"

class mentionlogger(znc.Module):
    module_types = [znc.CModInfo.NetworkModule]
    description = "Saves mention log"
    
    def load_settings(self):
        try:
            with open(self.dir + "/mlsettings") as f:
                settings = f.read()
        except IOError:
            settings = None
        except Exception as e:
            self.PutModule(str(e))
            raise
        if settings:
            self.settings = settings.split(setting_splitter)
        else:
            self.settings = []
    
    def save_settings(self):
        try:
            with open(self.dir + "/mlsettings", "w") as f:
                f.write(setting_splitter.join(list(set(self.settings))))
        except Exception as e:
            self.PutModule("Unable to save settings.")
            self.PutModule(str(e))
    
    def load_help(self):
        self.PutModule("'log' to show log.\n'del' to delete log.")
        self.PutModule("'add/rem <string>' to add or remove match entries.\n'list' to list match strings.")

    def OnLoad(self, args, message):
        self.dir = self.GetModDataDir()
        self.load_settings()
        self.load_help()
        return znc.CONTINUE

    def load_log(self, show_if_blank=True):
        if show_if_blank:
            self.PutModule('Log:')
        with open(self.dir + "/mentionlog") as f:
            for line in f.readlines():
                self.PutModule(line)

    def OnModCommand(self, command):
        cmd = command.lower()
        if cmd == "log" or cmd == "l":
            self.load_log()
        elif cmd == "firstlog":
            self.load_log(False)
        elif cmd == "del":
            self.PutModule("Deleting log.")
            with open(self.dir + "/mentionlog", "w+") as f:
                pass
        elif cmd[:4] == "add ":
            self.load_settings()
            self.settings.append(cmd[4:].strip())
            self.save_settings()
            self.PutModule(cmd[4:].strip() + " added.")
        elif cmd[:4] == "rem ":
            self.load_settings()
            try:
                self.settings.pop(self.settings.index(cmd[4:].strip()))
                self.save_settings()
                self.PutModule(cmd[4:].strip() + " removed.")
            except ValueError:
                self.PutModule(cmd[4:].strip() + " not in the list.")
        elif cmd == "list":
            self.load_settings()
            self.PutModule("Matched strings list: " + ",".join(self.settings))
        else:
            self.load_help()
        return znc.CONTINUE

    def OnPrivMsg(self, d, msg):
        with open(self.dir + "/mentionlog", "a+") as f:
            f.write(get_timestamp() + "PRIV: " + d.GetNick() + ": " + msg.s + "\n")
        return znc.CONTINUE

    def OnChanMsg(self, d, channel, message):
        if any([1 for x in self.settings if x in message.s.lower()]):
            with open(self.dir + "/mentionlog", "a+") as f:
                f.write(get_timestamp() + channel.GetName() + ": " + d.GetNick() + ": " + message.s + "\n")
        return znc.CONTINUE

    def OnClientLogin(self):
        self.OnModCommand("firstlog")
        return znc.CONTINUE
