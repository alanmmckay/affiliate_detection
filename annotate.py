from helper_functions import DataInterface, JsonInterface, SourceInterface
from annotation_appender import append_script
from urllib.parse import urlparse
import os
import sys

json_handler = JsonInterface()
info = json_handler.read_from_file('analysis_files/info.json')
db_handler = DataInterface("datadir/","/crawl-data.sqlite")

mode = input("Input Mode: ")

if not (mode == "ui" or mode =="manual"):
    print("Please enter valid input mode.")
    sys.exit()

inputStr = str()
quit = ['quit','Quit','QUIT']
cont = ['continue','Continue']
whitelist = ["rstyle.me","go.skimresources.com","click.linksynergy.com"]
inputStr = input("Input website URL: ")

while inputStr not in quit:

    url = inputStr

    hostname = urlparse(inputStr).hostname

    if hostname in info and inputStr in info[hostname]:

        local_page = db_handler.get_source_from_url(inputStr)

        for anchor in info[hostname][url]['anchors']:
            if urlparse(anchor).hostname in whitelist:
                info[hostname][url]['anchors'][anchor]['annotation'] = 'yes'
                print(str(anchor) + " annotation switched to yes")

        print("Local filename: " + local_page)

        if mode == "manual":
            os.system('firefox ' + 'datadir/sources/' + local_page + ' > /dev/null 2>&1 &')

            inputStr = input("Input anchor URL to annotate: ")
            while inputStr not in cont:

                anchor = inputStr
                if anchor in info[hostname][url]['anchors']:

                    inputStr = input("Annotation value: ")
                    if inputStr != None:

                        old_val = info[hostname][url]['anchors'][anchor]['annotation']
                        info[hostname][url]['anchors'][anchor]['annotation'] = inputStr
                        print(str(anchor) + " annotation switched from " + str(old_val) + " to " + inputStr)

                else:
                    print(" !!! Invalid anchor URL: ")
                    print(anchor)

                inputStr = input("Input anchor URL to annotate: ")

            json_handler.write_to_file('analysis_files/info.json',info)
            os.system('firefoxPID=$(pgrep firefox); kill $firefoxPID;')

        elif mode == "ui":
            append_script('datadir/sources/'+local_page, url, "links.txt", "temp.html")

            os.system('firefox temp.html > /dev/null 2>&1 &')

            inputStr = input("Input 'continue' once links have been selected: ")

            while inputStr != "continue":
                inputStr = input("Input 'continue' once links have been selected: ")


            f = open('links.txt','r')
            link_listing = f.readlines()
            f.close()

            for link in link_listing:
                anchor = link.split()[0]
                old_val = info[hostname][url]['anchors'][anchor]['annotation']
                info[hostname][url]['anchors'][anchor]['annotation'] = 'yes'
                print(str(anchor) + " annotation switched from " + str(old_val) + " to " + 'yes')

            json_handler.write_to_file('analysis_files/info.json',info)
            os.system('firefoxPID=$(pgrep firefox); kill $firefoxPID;')

    else:

        print(" !!! Invalid URL: ")
        print(inputStr)
        print("\n\n")

    inputStr = input("Input website URL: ")
