#!/usr/bin/python
"""
Project: Pandora_Downloader_Transfer
Author: Jared R. Luellen
About: Automatically transfers songs from iPhone that were downloaded using Pandora Downloader to the users desktop.
"""

import os
from subprocess import check_output
import sys

class Pandora_Downloader_Transfer(object):
    def __init__(self):
        os.system("clear")
        print "\nThank you for choosing Pandora Downloader Automatic Transfer!\n"

    def main(self):
        while True:
            response = raw_input("Are you connected via iPhone HotSpot? (yes, no, or quit): ")
            if response == "Yes" or response == "yes":
                ip_addresses = self.get_ip_addresses(True)
                break
            elif response == "No" or response == "no":
                ip_addresses = self.get_ip_addresses(False)
                break
            elif response == "q" or response == "Q" or response == "quit" or response == "Quit":
                sys.exit()

        self.copy_mp3_files_to_home_desktop(ip_addresses)

    def copy_mp3_files_to_home_desktop(self, ip_addresses):
        local_ip_address = ip_addresses.get('local_ip_address')
        iphone_ip_address = ip_addresses.get('iphone_ip_address')
        try:
            local_username = check_output("whoami").rstrip()
            print "\nPlease provide ssh passwords for iPhone and local computer respectively\n"
            commands = " \'scp -r /User/Media/Pandora/ "+local_username+"@"+local_ip_address+":~/Desktop/; rm /User/Media/Pandora/*.mp3; exit\'"
            response = os.system("ssh -t root@"+iphone_ip_address+commands)
            if response == 256:
                print "\nThere aren't any songs to transfer, you should download some more!"
            else:
                print "\nYour songs have been successfully transfered and removed from your iPhone"
        except:
            print "\nTransfer failed, please ensure everything is configured correctly and try again"
        finally:
            print "\nThank you for using Pandora Downloader Automatic Transfer!!\n"

    def get_ip_addresses(self, hotspot_status):
        if hotspot_status == True:
            iphone_ip_address = check_output(["ipconfig", "getoption", "en0", "router"]).rstrip()
        elif hotspot_status == False:
            while True:
                response = raw_input("What's the iPhone IP Address?: ")
                try:
                    check_input_ip = check_output(["ping", "-c", "1", response]).rstrip()
                    iphone_ip_address = response
                    break
                except:
                    print "You've entered an incorrect IP address"
        local_ip_address = check_output(["ipconfig", "getifaddr", "en0"]).rstrip()

        return {'local_ip_address': local_ip_address, 'iphone_ip_address': iphone_ip_address}

if __name__ == "__main__":
    Pandora_Downloader_Transfer = Pandora_Downloader_Transfer()
    Pandora_Downloader_Transfer.main()