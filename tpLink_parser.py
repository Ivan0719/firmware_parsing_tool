import requests
from bs4 import BeautifulSoup
import os

response = requests.get("https://www.tp-link.com/tw/support/download/")
soup = BeautifulSoup(response.text, "html.parser")
items  = soup.find_all("div", class_="item")
schedule = len(items)
now = -1
for item in items:
    now+=1
    if item.find("span", class_="tp-m-hide") is not None:
        li = list(str(item.find("span", class_="tp-m-hide").string))
        for i in range(len(li)):
            if(li[i]=='>'):
                li[i]='-'
            if(li[i]=='/'):
                li[i]=' '
        s = "".join(li)
        if not os.path.exists(s):
                os.mkdir(s)
        devices = item.find_all("a",class_="ga-click")
        if devices is not None:
            for device in devices:
                device_name = device.string
                link = device.get("href")
                response = requests.get("https://www.tp-link.com"+link+"/#Firmware")
                soup = BeautifulSoup(response.text, "html.parser")
                titles  = soup.find_all("table")
                if len(titles) !=0 :
                    if not os.path.exists(s+"/"+device_name):
                        os.mkdir(s+"/"+device_name)
                for title in titles :
                    downloadlink = title.find("tr",class_="basic-info")
                    if downloadlink is not None:
                        downloadlink = downloadlink.find("th")
                    if downloadlink is not None:
                        downloadlink = downloadlink.find("a",class_="download ga-click")
                        text = downloadlink.get("href")
                        if 'TP-LINK' not in text.split('/')[-1] and  'USB' not in text.split('/')[-1] \
                        and  'GPL' not in text.split('/')[-1] and  'gpl' not in text.split('/')[-1] \
                            and  'Easy' not in text.split('/')[-1] and  'bz2' not in text.split('/')[-1] \
                                and  'tar' not in text.split('/')[-1] and  'discovery' not in text.split('/')[-1] \
                                    and  'Discovery' not in text.split('/')[-1] and  'Win' not in text.split('/')[-1] \
                                        and  'Mac' not in text.split('/')[-1] and  'Linux' not in text.split('/')[-1] \
                                            and  '.zip' in text.split('/')[-1]:
                            file = requests.get(text)
                            print("Now : "+str(int(((now+1)/schedule)*100))+"%  Download : "+s+"/"+device_name+"/"+text.split('/')[-1])
                            with open(s+"/"+device_name+"/"+text.split('/')[-1], "wb") as f:
                                f.write(file.content)