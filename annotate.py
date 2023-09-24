from helper_functions import DataInterface, JsonInterface, SourceInterface
from urllib.parse import urlparse
import os

json_handler = JsonInterface()
info = json_handler.read_from_file('analysis_files/info.json')
db_handler = DataInterface("datadir/","/crawl-data.sqlite")

inputStr = str()
quit = ['quit','Quit','QUIT']
cont = ['continue','Continue']
inputStr = input("Input website URL: ")

while inputStr not in quit:

    url = inputStr

    hostname = urlparse(inputStr).hostname

    if hostname in info and inputStr in info[hostname]:

        local_page = db_handler.get_source_from_url(inputStr)

        os.system('firefox ' + 'datadir/sources/' + local_page + ' > /dev/null 2>&1 &')

        inputStr = input("Input anchor URL to annotate: ")

        while inputStr not in cont:

            anchor = inputStr

            if anchor in info[hostname][url]['anchors']:

                inputStr = input("Annotation value: ")

                if inputStr != None:
                    old_val = info[hostname][url]['anchors'][anchor]['annotation']
                    info[hostname][url]['anchors'][anchor]['annotation'] = inputStr
                    print(str(url) + " annotation switched from " + str(old_val) + " to " + inputStr)

            else:

                print(" !!! Invalid anchor URL: ")
                print(anchor)

            inputStr = input("Input anchor URL to annotate: ")


        json_handler.write_to_file('info.json',info)

        os.system('firefoxPID=$(pgrep firefox); kill $firefoxPID;')

    else:

        print(" !!! Invalid URL: ")
        print(inputStr)
        print("\n\n")

    inputStr = input("Input website URL: ")
