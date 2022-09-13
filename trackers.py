###############################################################
##          Created by Red Squirrel (@redsquirrel87)         ##
##                 https://redsquirrel87.com                 ##
###############################################################
import requests
import sys
import json
import argparse

######################### Login data ##########################
##          Please edit the two following variables          ##
##     with your qBittorrent WebUI username and password     ##
###############################################################
user="username"
pswd="password"

####################### WebUI API URLs ########################
##       Please edit the following URLs by replacing         ##
##     localhost with the IP of your qBittorrent WebUI       ##
###############################################################
api_login="http://localhost:8080/api/v2/auth/login"
api_get_torrents="http://localhost:8080/api/v2/torrents/info"
api_get_trackers="http://localhost:8080/api/v2/torrents/trackers"
api_add_trackers="http://localhost:8080/api/v2/torrents/addTrackers"
api_rem_trackers="http://localhost:8080/api/v2/torrents/removeTrackers"
stable_trackers="https://newtrackon.com/api/stable"

################# DO NOT EDIT BELOW THIS LINE #################
parser=argparse.ArgumentParser(description="A very simple python script for qBittorrent which uses the WebUI API to automatically add new stable trackers (list downloaded from newtrackon.com) to existing torrents. Created by Red Squirrel (@redsquirrel87) - https://redsquirrel87.com
parser.add_argument("--ipv6",action='store_true',help="include ipv6 only trackers in the list downloaded from newtrackon.com")
parser.add_argument("--ipv4",action='store_true',help="include ipv4 only trackers in the list downloaded from newtrackon.com")
parser.add_argument("-d","--downloading",action='store_true',help="add trackers only to torrents currently downloading")
parser.add_argument("-s","--seeding",action='store_true',help="add trackers only to torrents currently seeding")
parser.add_argument("-t","--stalled",action='store_true',help="add trackers only to torrents currently stalled")
parser.add_argument("-p","--paused",action='store_true',help="add trackers only to torrents currently paused")
parser.add_argument("--cat",help="add trackers only to torrents with the given category")
parser.add_argument("--tag",help="add trackers only to torrents with the given tag")
parser.add_argument("-c","--clear",action='store_true',help="also remove currently not working trackers from torrents")
parser.add_argument("-v","--verbose",action='store_true',help="list all the not working trackers that will be removed (works only with -c)")
args=parser.parse_args()

print ("Downloading new list of stable trackers from newtrackon.com, please wait...",end=" ")
data={"include_ipv4_only_trackers":args.ipv4,"include_ipv6_only_trackers":args.ipv6}
req=requests.get(stable_trackers,data)
if req.status_code == 200 :
        print ("OK!")
else:
        print ("ERROR!")
        sys.exit(-1)
trackers=req.text

print ("")
print ("Logging in to your qBittorent WebUI...",end=" ")
data={"username":user,"password":pswd}
result=requests.post(api_login, data=data).text
if result.lower() == "ok." :
        print ("OK!")
else:
        print ("ERROR!")
        sys.exit(-2)

filter=[]
if args.seeding :
        filter.append("seeding")
if args.downloading :
        filter.append("downloading")
if args.stalled :
        filter.append("stalled")
if args.paused :
        filter.append("paused")
if args.cat :
        cat = args.cat
else:
        cat = ""
if args.tag :
        tag = args.tag
else:
        tag = ""
print ("Getting torrents list...",end=" ")
data={"filter":"&".join(filter),"category":cat,"tag":tag}
result=requests.get(api_get_torrents,data).text
json_data=json.loads(result)
torrents=len(json_data)
if torrents == 0 :
        print ("No torrents found with given filters, category or tag.")
        sys.exit(0)
else:
        print (str(torrents) + " torrent(s) found with given filters, category or tag.")
        cont=0
        for torrent in json_data :
                cont+=1
                print (str(cont) + ") " + torrent["name"])
                if args.clear :
                        print ("        Cleaning currently not working trackers...")
                        data={"hash":torrent["hash"]}
                        old_trackers=requests.get(api_get_trackers,data).text
                        json_trackers=json.loads(old_trackers)
                        rem_list=[]
                        for tracker in json_trackers :
                                status=tracker["status"]
                                if status == 4 :
                                        if args.verbose :
                                                print ("                - " + tracker["url"] + " flagged for removal.")
                                        rem_list.append(tracker["url"])
                        if len(rem_list) > 0 :
                                print ("        Removing flagged trackers...",end=" ")
                                data={"hash":torrent["hash"],"urls":"|".join(rem_list)}
                                remove_trackers=requests.get(api_rem_trackers,data).status_code
                                if remove_trackers == 200 :
                                        print (str(len(rem_list)) + " not working trackers removed successfully for this torrent.")
                print ("        Adding the new stable trackers to the torrent...",end=" ")
                data={"hash":torrent["hash"],"urls":trackers}
                add_trackers=requests.post(api_add_trackers,data).status_code
                if add_trackers == 200 :
                        print ("SUCCESS!")
print ("")
print ("Procedure completed, bye bye!")
                               
