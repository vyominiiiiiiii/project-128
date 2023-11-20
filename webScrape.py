from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests

service=Service() #chrome driver open krne ke liya
options=webdriver.ChromeOptions() #chrome driver run krwane ke liya
startUrl="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/" #website ka url
browser=webdriver.Chrome(service=service,options=options)
browser.get(startUrl)
time.sleep(10) #webpage ko load hone se pehla to thoda time lapse

def scrape():
    headers=["Name of planet","Light-years from earth","Planet mass","Stellar magnitude","Discovery date","Hyperlink","Discovery date","Mass","Planet radius","Orbital radius","Orbital period","Eccentricity","Detection method"]#topics jinme data stored h wocsv file mei kaisa appear hone
    planetData=[]

    for i in range(0,428):#kyu ki 428 pages h read krne ko
        soup=BeautifulSoup(browser.page_source,"html.parser")#page ko read krne ke liya

        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):#topics ki andar jo data h wo li tag mei stored h webpage mei to saare ul tag ko access kr rahe h jinke class name exoplanet h
            li_tags=ul_tag.find_all("li")#phir hum ul tag ke andar saare li tag ko access kr rahe jinme actually data h isliya humne koi atrribute bhi nhi diya...waha 4 li tag h 4 data ke liya
            temp_list=[]

            for index,li_tag in enumerate(li_tags):#data 1 indirect diya hua h furthi li tag ke andar phir a tag ke andar par data 2 data 3 aur data4 direct diya hua h wo console mei elements mei jake chekc kr skta h
                if index==0: #agar li tag mei jo data 1 mei a tag h to uska info show ho jaye(fetch) 
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else :#agar false h to...
                    try:#error dikhane ke jagha(jiski wajhe se page load nhi hoga aur error dikhayega)
                        temp_list.append(li_tag.contents[0])
                    
                    except:#ye sir uss data ki jagha blank space chod dega
                        temp_list.append("")
#iss sabko hum time_list wale empty array mei store kr rahe h aur further planet data wale empty dal rahe h
            
            planetData.append(temp_list)

        browser.find_element(By.XPATH,'//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()#yaha humne next page click krne wala button tha to uska code uspa right click krke elements mei jake yaha pe pasta krdiya disse ab ye next page code ke har loop khatam hone ke baad khol skta h
    
    with open("Scarper.csv","w") as f:
        csv_writer=csv.writer(f)#csv file mei write krne ke liya 
        csv_writer.writerow(headers) #csv file mei rows mei header array mei jo topics stored h wo dal diya
        csv_writer.writerows(planetData)#csv file mei rows ke andar data jo planet data mei stored h wo dal diya

scrape() 

for index,data in enumerate(planetData):
    scrapeHyperlink(data[5])

hyperlink_data=[]

def scrapeHyperlink(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")

        temp_list=[]

        for tr_tag in soup.find_all("tr",attrs={"class","fact_row"}):
            td_tags=tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class","value"})[0].contents[0])

                except:
                    temp_list.append("")

        hyperlink_data.append(temp_list)
    
    except:
        temp.sleep(3)
        scrapeHyperlink(hyperlink)
        




