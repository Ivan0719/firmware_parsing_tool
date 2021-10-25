import requests
from bs4 import BeautifulSoup
import os
import json

devices = []
dev_list = []
firmware_dir = "zyxel_firmware"

def download_firmware(name,link):
    response = requests.get("https://www.zyxel.com/support/SupportLandingSR.shtml?c=gb&l=en&kbid="+link+"&md="+name)
    soup = BeautifulSoup(response.text, "html.parser")
    tables  = soup.find_all("table", class_="blueTable table")
    for table in tables:
        tbodys = table.find_all("tbody")
        for tbody in tbodys:
            trs = tbody.find_all("tr")
            for tr in trs:
                if "Firmware" in str(tr):
                    firmwares = tr.find_all("option")
                    for firmware in firmwares:
                        print("Downloading... : "+name.replace('%20','_')+"_"+firmware.text)
                        if not os.path.exists(firmware_dir+"/"+name.replace('%20','_')):
                            os.mkdir(firmware_dir+"/"+name.replace('%20','_'))
                        print("https://download.zyxel.com/"+name.replace('%20','_')+"/firmware/"+name+"_"+firmware.text+".zip")
                        download_file = requests.get("https://download.zyxel.com/"+name.replace('%20','_')+"/firmware/"+name+"_"+firmware.text+".zip")
                        with open(firmware_dir+"/"+name.replace('%20','_')+"/"+name.replace('%20','_')+firmware.text+".zip", "wb") as f:
                                f.write(download_file.content)
                        f.close()


if not os.path.exists(firmware_dir):
    os.mkdir(firmware_dir)
else:
    print("zyxel_firmware/ exist, please remove and run again!!")
    exit

for c in range(ord('A'),ord('Z')+1):
    response = requests.get("https://www.zyxel.com/Dropdowns.shtml?ikey=support&c=gb&l=en&dataType=json&phrase="+chr(c))

    js = json.loads(response.text)
    for device in js:
        if device['title'] not in dev_list:
            dev_list.append(device['title'])
            temp_str = device['title'].replace(' ', '%20')
            devices.append({'name':temp_str, 'link':device['link']})

print("Find end!!")
print("Total number of devices :"+str(len(devices)))
total = len(devices)
i = 0
for device in devices:
    i+=1
    print("Now : "+str(i*100/total)+" %")
    download_firmware(device['name'],device['link'])


