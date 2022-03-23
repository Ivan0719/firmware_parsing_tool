import requests
from bs4 import BeautifulSoup
import os
import json

firmware_dir = "moxa_firmware"
headers={
		'User-Agent'  :'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0'
}

def download_firmware(device_name,link):
    finded = False
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    trs = soup.find_all("tr", class_="border-table__tr filter_row js-showAll_item")
    for tr in trs:
        tds = tr.find_all("td", class_="border-table__td")
        for i,td in enumerate(tds):
            if i == 0 :
                divs = td.find_all("div",class_="flex-between")
                firmware_link_a = divs[0].find_all("a",class_="border-table__link record-download")
                firmware_link = firmware_link_a[0].get("href")
            if i == 1 and "Firmware" in td.string:
                finded = True
            if finded:
                break
        if finded:
            break
    if finded:
        device_name = device_name.replace('/','_')
        firmware_file = requests.get(firmware_link, headers=headers)
        print("Downloading "+firmware_link.split('/')[-1])
        if not os.path.exists(firmware_dir+"/"+device_name):
            os.mkdir(firmware_dir+"/"+device_name)
        with open(firmware_dir+"/"+device_name+"/"+firmware_link.split('/')[-1], "wb") as f:
            f.write(firmware_file.content)
        print("Success!!")
    else:
        print("Could not find "+device_name+" firmware !!")
if not os.path.exists(firmware_dir):
    os.mkdir(firmware_dir)
else:
    print("moxa_firmware/ exist, please remove and run again!!")
    exit





# Get device link
response = requests.get("https://www.moxa.com/en/support/product-support/software-and-documentation", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
devices  = soup.find_all("a", class_="search-dropdown__link")
total = len(devices)
print(total)
index = 0
for device in devices:
    index += 1
    print("Now : "+str(index*100/total)+" %")
    device_name = device.string
    device_link = "https://www.moxa.com/en/support/product-support/"+device.get("href")
    print(device_name)
    download_firmware(device_name,device_link)

