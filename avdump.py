#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

                        __                       
        .---.-.--.--.--|  |.--.--.--------.-----.
        |  _  |  |  |  _  ||  |  |        |  _  |
        |___._|\___/|_____||_____|__|__|__|   __|
                                          |__|   

		avdump displays imvu profile information raw using
        the old and new api
		
		Version: 0.2
            + new api support
        Version: 0.1
            + initial version
		
		Written by Peter Bartels
        
        https://www.kangafoo.de
		
"""

import sys
import argparse
import os
import requests
import json


def clear():
    """
    
    clear() -> no return
    
    just clear screen for linux and windows
    
    """
	os.system("cls" if os.name == "nt" else "clear")	


def infoheader():
    """
    
    infoheader() -> no return
    
    prints header logo and avatar target name and CID
    
    """
    clear()
    print("                __                       ")
    print(".---.-.--.--.--|  |.--.--.--------.-----.")
    print("|  _  |  |  |  _  ||  |  |        |  _  |")
    print("|___._|\___/|_____||_____|__|__|__|   __|")
    print("                                  |__| \n") 
    print("-"*50)
    print("->>  Target: %s%s" %(options.cid,options.user))
    print("-"*50)


def printhelp():
    """
    
    printhelp() -> no return
    
    prints header logo and displays help parameters
    
    """
    clear();
    print("                __                       ")
    print(".---.-.--.--.--|  |.--.--.--------.-----.")
    print("|  _  |  |  |  _  ||  |  |        |  _  |")
    print("|___._|\___/|_____||_____|__|__|__|   __|")
    print("                                  |__| \n") 
    parser.print_help()
    
def getusercid(username):
    """
    
    getusercid(string) -> string
    
    tries to retrieve the CID of an avatar for a name to cid lookup
    
    """
    getuser = 'http://www.imvu.com/catalog/web_av_pic.php?av=%s' % (username)
    r = requests.get(getuser)
    link = r.url
    cid = link[link.index('avatars/')+len('avatars/'):link.index('_')]
    return cid
	
def dumpprofile(cid,way):
    """
    
    dumpprofile(string,integer) -> no return
    
    checks the online status of an avatar using inofficial imvu api and prints status
    
    """
    if (way == 1): #old api
        profile = 'http://client-dynamic.imvu.com/api/avatarcard.php?cid=%s&viewer_cid=%s' % (cid,cid)
    else: #new api
        profile = 'https://api.imvu.com/user/user-%s' % (cid) 
    response = requests.get(profile)
    dict = json.loads(response.content)
    print(json.dumps(dict, indent = 4, sort_keys=False))
		
if __name__=="__main__":
    parser = argparse.ArgumentParser("usage: %prog [options] arg1 arg2")
    parser.add_argument("-c", "--cid", dest="cid",default="",help="specify the cid of a user")
    parser.add_argument("-u", "--user", dest="user",default="",help="specify the username of a user")
    parser.add_argument("-p", "--profile", dest="prof",type=int,default=1,help="chose the profile api, 1 for old, 2 for new")
    options = parser.parse_args()
    if len(sys.argv) < 2:
        printhelp()
        quit()
    else:
        cid = options.cid
        prof = options.prof
        user = options.user
        infoheader()
        if options.cid:
            dumpprofile(cid,prof)
        elif options.user:
            usercid = getusercid(user)
            if usercid != 'default':
                dumpprofile(usercid,prof)
            else:
                print('User not found')