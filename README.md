Some personal ZNC IRC bouncer scripts.

### Channel Manager

Unfinished module.

This module maintains customized groups of channels for easy attaching/detaching. ZNC allows you to be connected to many channels at once, but 'detach' from any of them, which simply means ZNC disconnects them from your client while staying connected. So you can be connected to many channels at once, but have a group 'gaming', and attach to only the gaming channels with a command, automatically detaching from all others. It also maintains a list of favorite channels, so you can easily reconnect if you are disconnected.

### Mention Logger

Currently this module doesn't distinguish between different users on the same bouncer.

Add some words to log, and mention logger will keep a log of the messages that include that term until you clear it.
