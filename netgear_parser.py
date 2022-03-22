import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options



def file_download(model_name, address):


    browser.get("https://www.netgear.com/support/download/")
    input = browser.find_element_by_id("MainContent_support_home_suggest")
    input.send_keys(model_name)

    time.sleep(2)

    input.send_keys(u'\ue007')
    input.send_keys(u'\ue007')
    
    time.sleep(2)

    soup = BeautifulSoup(browser.page_source, "html.parser")
    h4_list = soup.find_all("h4")
    add = address
    for h4 in h4_list:
        if("Firmware/Software" in h4):
            ul = h4.find_next_sibling("ul")
            p_list = ul.find_all("p")
            amount = 0

            for p in p_list:
                p_text = p.getText()
                if("Firmware" in p_text):
                    amount += 1
            if (amount > 1):
                model_name = model_name.replace("/", " ")
                add = add + "/" + model_name
                if not os.path.exists(add):
                    os.mkdir(add)

            for p in p_list:
                p_text = p.getText()
                if "Firmware" in p_text:
                    target = p.find_parent("a")
                    file_link = target.get("href")
                    #print(file_link)
                    if "confirm" in file_link:
                        target = soup.find("a",{"class": "btn link-new"})
                        file_link = target.get("href")
                    file_name_tmp = file_link.strip().split('/')
                    file_name = file_name_tmp[len(file_name_tmp)-1]
                    #print(file_name)
                    if "http" not in file_link:
                        continue
                    elif "zip" not in file_link:
                        continue
                    download_file = requests.get(file_link)
                    if not os.path.exists(add + "/" + file_name):
                        with open(add + "/" + file_name,"wb") as f:
                            f.write(download_file.content)
                            print("success "+file_name)
                        f.close()




if not os.path.exists("netgear_firmware"):
    os.mkdir("netgear_firmware")



firefoxOptions = Options()
firefoxOptions.add_argument("-headless")

browser = webdriver.Firefox(executable_path=r'./geckodriver', options=firefoxOptions)
browser.get("https://www.netgear.com/support/")

##### find categorys_id list at https://www.netgear.com/support/
category_id = browser.find_elements_by_class_name("scrolltoproducts")
category_id_list = []
for c in category_id:
    category_id_list.append(c.get_attribute("data-id").strip())


##### find category_name list
##### find category_href_list
soup = BeautifulSoup(browser.page_source, "html.parser")
category_name = soup.find("div", class_="grid").find_all("div", class_= "col")

category_name_list = []
category_href_list = []
for c in category_name:
    category_name_list.append(c.getText().strip())
    category_href = c.find("a").get("href")

    category_href_list.append(category_href)



for i in range(len(category_name_list)):
    
    address = "netgear_firmware"
    if "javascript" in category_href_list[i]:
        add = address + "/" + category_name_list[i]
        if not os.path.exists(add):
            os.mkdir(add)
        small_category = soup.find("div", id=category_id_list[i])
        small_categorys = small_category.find("div", id="scrolltoitems")
        small_categorys_name = small_categorys.find_all("h3")

        isLink = 0
        for s in small_categorys_name:
                href_link = s.find_parent().get('href')
                #print(href_link)
                
                if href_link == None:
                    isLink = 0
                else:
                    isLink = 1
                
                if isLink == 1: 
                    pass
                    
                else:
                    target = s.getText().strip()
                    target = target.replace("/", "+")
                    adds = add + "/" + target
                    if not os.path.exists(adds):
                        os.mkdir(adds)


                    internal_product = soup.find_all("span", class_="internal-product")
                    for internal in internal_product:
                        products = internal.getText().strip()
                        if target == products:
                            items = internal.find_parent().find_next_sibling()
                            item_model = items.find_all("span", class_="model")
                            for im in item_model:
                                model_name = im.getText().strip()
                                print(model_name)
                                file_download(model_name, adds)
                            break



for i in range(len(category_name_list)):
    address = "netgear_firmware"
    ##### "javascript" not in category_href_list
    if "javascript" not in category_href_list[i]:
        add = address + "/" + category_name_list[i]
        if not os.path.exists(add):
                    os.mkdir(add)

        if "meural" not in category_href_list[i]:
            link = "https://www.netgear.com" + category_href_list[i]
            browser.get(link)
        
            soup = BeautifulSoup(browser.page_source, "html.parser")
            model_list = soup.find("section", class_="orbi-model-grid").find_all("section")
            for model in model_list:
                model_name_tmp = model.find("a").get("href")
                model_name_tmp = model_name_tmp.strip().split('/')
                model_name_tmp = model_name_tmp[len(model_name_tmp)-1]
                model_name_tmp = model_name_tmp.split('.')
                model_name = model_name_tmp[0].upper()
                file_download(model_name, add)
                print(model_name)

    




def delete_empty_dir(dir):
    if os.path.isdir(dir):
        for d in os.listdir(dir):
            path = os.path.join(dir, d)
            if os.path.isdir(path):
                delete_empty_dir(os.path.join(dir, d))
    if not os.listdir(dir):
        os.rmdir(dir)


delete_empty_dir("netgear")





