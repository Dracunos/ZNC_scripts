# chanman.py

""" Channel Manager. It should manage favorite channels, disconnected
favorites, attach/detach groups.
"""

import json
import znc

AUTOADD_DEFAULT = True

class chanman(znc.Module):
    module_types = [znc.CModInfo.NetworkModule]
    description = "Channel Manager"
    
    def OnLoad(self, args, message):
        self.modcmds = {
            'help':             {'cmd_list': ['h', 'help'],
                                'func': self.load_help,
                                'has_args': False},
            'addfav':           {'cmd_list': ['addfav', 'af', 'addf'],
                                'func': self.add_fav,
                                'has_args': True},
            'rmfav':            {'cmd_list': ['rmfav', 'rf', 'rmf'],
                                'func': self.remove_fav,
                                'has_args': True},
            'listfavs':         {'cmd_list': ['listfavs', 'lf', 'listf'],
                                'func': self.list_favs,
                                'has_args': False},
            'autoadd':          {'cmd_list': ['autoadd'],
                                'func': self.toggle_autoadd,
                                'has_args': False},
            'addgroup':         {'cmd_list': ['addgroup', 'ag', 'addg'],
                                'func': self.add_group,
                                'has_args': True},
            'rmgroup':          {'cmd_list': ['rmgroup', 'rg', 'rmg'],
                                'func': self.remove_group,
                                'has_args': True},
            'setgroup':         {'cmd_list': ['setgroup', 'sg', 'setg'],
                                'func': self.set_group,
                                'has_args': True},
            'show':             {'cmd_list': ['show', 'showgroup', 'sh'],
                                'func': self.show_group,
                                'has_args': True},
            'listgroups':       {'cmd_list': ['listgroups', 'lg', 'listg'],
                                'func': self.list_groups,
                                'has_args': False},
            'group':            {'cmd_list': ['group', 'grp'],
                                'func': self.select_group,
                                'has_args': True},
            'debug':            {'cmd_list': ['debug'],
                                'func':self.toggle_debug,
                                'has_args': False}
        }
        self.sdir = self.GetModDataDir() + "/cmsettings"
        self.load_settings()
        self.load_help()
        return znc.CONTINUE
    
    def save_settings(self):
        try:
            with open(self.sdir, "w") as f:
                json.dump(self.settings, f)
        except Exception as e:
            self.PutModule("Unable to save to settings file at: " + self.sdir)
            self.PutModule(str(e))
    
    def load_settings(self):
        try:
            with open(self.sdir) as f:
                settings = json.load(f)
        except IOError:
            self.PutModule("Creating new settings file at: " + self.sdir)
            self.create_settings()
        except Exception as e:
            self.PutModule(str(e))
            raise
        self.settings = settings
    
    def create_settings(self):
        self.settings = {
            'favs': [],
            'groups': {},
            'autoadd': AUTOADD_DEFAULT,
            'debug': False
        }
        self.save_settings()
    
    def load_help(self):
        print_help(self.PutModule)
    
    def OnModCommand(self, command):
        cmd = command.lower().strip()
        command_function, command_args = self.find_command(cmd)
        if command_function:
            if command_args:
                command_function(command_args)
            else:
                command_function()
        return znc.CONTINUE
    
    def find_command(self, command):
        cmdlist = self.modcmds
        for cmd_key, cmd_dict in cmdlist.items():
            if cmd_dict['has_args']:
                match, cmd_length = check_cmd(command, cmd_dict['cmd_list'], True)
                if match:
                    return (cmd_dict['func'], command[cmd_length:])
            else:
                match, _ = check_cmd(command, cmd_dict['cmd_list'], False)
                if match:
                    return (cmd_dict['func'], False)
        return (False, False)
    
    def add_fav(self, cmd):
        
    
    def remove_fav(self, cmd):
        
    
    def list_favs(self):
        
    
    def add_group(self, cmd):
        
    
    def remove_group(self, cmd):
        
    
    def set_group(self, cmd):
        
    
    def show_group(self, cmd):
        
    
    def list_groups(self):
        
    
    def select_group(self, cmd):
        
    
    def disconnect_all(self):
        
    
    def connect_all(self):
        
    
    def toggle_autoadd(self):
        if self.settings['autoadd']:
            self.settings['autoadd'] = False
            self.PutModule("Auto add favorite channels DEACTIVATED.")
        else:
            self.settings['autoadd'] = True
            self.PutModule("Auto add favorite channels ACTIVATED.")
        
    
    def toggle_debug(self):
        if self.settings['debug']:
            self.settings['debug'] = False
            self.PutModule("Debug mode DEACTIVATED.")
        else:
            self.settings['debug'] = True
            self.PutModule("Debug mode ACTIVATED.")
    
    def OnClientLogin(self):
        return znc.CONTINUE


def check_cmd(cmd, cmdlist, has_args=False):
    for command in cmdlist:
        if not has_args:
            if command == cmd:
                return (True, None)
        else:
            if command + " " == cmd[:len(command)+1]:
                return (True, len(command) + 1)
    return (False, None)

def print_help(print_func):
    for line in help_list:
        print_func(line)


fmt = "{:15}|{:25}|{}"
help_list = [
    "This module allows you to save groups of channels into 'channel groups'. "
        "Select a group to attach to only those channels, while detaching from "
        "all others.",
    "[channels] argument: one or multiple channel names/number shortcuts. You "
        "may also use a group name to indicate all the channels in the group.",
    "Default groups (cannot be deleted):",
    "'all': every connected channel.",
    "'attached': currently attached channels.",
    "'detached': currently detached, but connected, channels.",
    "'favs': the channels currently in the favorites list.",
    "----------------------------------------------------------",
    fmt.format("Command", "[Arguments]", "Description (command shortcuts)"),
    fmt.format('help', '', "Help: Show the help text. (h)"),
    fmt.format('autoadd', '', "Toggle Autoadd: Channels are automatically added"
        " to favorites on join and when the module is first loaded. "
        "Adding/removing a favorite will automatically join or leave the "
        "channel. Currently: " + str(self.settings['autoadd'])),
    fmt.format('listfavs', '', "List Favorites: List favorite channels, "
        "connected channels, and show channel number shortcuts. (lf, listf)",
    fmt.format('addfav', '[channels]', "Add Favorite: Add favorite channels "
        "by channel name, number, or add all channels. If autoadd is enabled "
        "you can also simply join the channel. 'all' will add all currently "
        "connected channels. (af, addf)"),
    fmt.format('rmfav', '[channels]', "Remove Favorite: Remove favorite "
        "channels. (rf, rmf)"),
    fmt.format('addgroup', '[groupname] [channels]', "Add Group: Add to a "
        "group, or create new channel group. (ag, addg)"),
    fmt.format('rmgroup', '[groupname] [channels]', "Remove Group: Remove from "
        "a group. Removing 'all' will delete the group. (rg, rmg)"),
    fmt.format('setgroup', '[groupname] [channels]', "Set Group: Sets a group "
        "to contain only these channels. (sg, setg)"),
    fmt.format('show', '[groupname]', "Show Group: Shows the contents of a "
        "group. (sh)"),
    fmt.format('listgroups', '', "List all groups and channels. (lg, listg)"),
    fmt.format('group', '[groupname]', "Select Group: Attaches to only the "
        "channels in the group, detaches all others. Add the '{disconnect}' "
        "argument in curly braces to disconnect instead of detaching. (eg: "
        "group {disconnect} mygroupname) (grp)")
]











