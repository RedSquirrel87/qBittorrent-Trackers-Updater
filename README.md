# What's it?
A very simple python script for [qBittorrent](https://www.qbittorrent.org/) which uses the WebUI API to automatically add new stable trackers (list downloaded from [newtrackon.com](https://newtrackon.com/list)) to existing torrents.

# Usage
`trackers.py [-h] [--ipv6] [--ipv4] [-d] [-s] [-t] [-p] [--cat CAT] [--tag TAG] [-c] [-v]`

Explanation of optional arguments:
* [-h, --help] show this help message and exit
* [--ipv6] include ipv6 only trackers in the list downloaded from newtrackon.com
* [--ipv4] include ipv4 only trackers in the list downloaded from newtrackon.com
* [-d, --downloading] add trackers only to torrents currently downloading
* [-s, --seeding] add trackers only to torrents currently seeding
* [-t, --stalled] add trackers only to torrents currently stalled
* [-p, --paused] add trackers only to torrents currently paused
* [--cat CAT] add trackers only to torrents with the given category
* [--tag TAG] add trackers only to torrents with the given tag
* [-c, --clear] also remove currently not working trackers from torrents
* [-v, --verbose] list all the not working trackers that will be removed (works only with -c)



**Note:** you can also use more filters at once, for example to filter *downloading* and *seeding* torrents with tag *my tag* just type:

`trackers.py -ds --tag "my tag"`

Also please note that with no arguments by default the trackers of all the torrents will be updated.

# Requirements 
* Python v3+
* qBittorrent v4.1+
