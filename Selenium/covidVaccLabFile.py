

import time
import sys
import pip

try:
    __import__('selenium')
except ImportError:
    #pip.main(['install','selenium'])
    __import__('selenium' )

try:
    __import__('webdriver_manager')
except ImportError:
    #pip.main(['install','webdriver_manager'])
    __import__('webdriver_manager' )

#pip.main(['install','BeautifulSoup4'])  
# try:
#     __import__('BeautifulSoup')
# except ImportError:
#     pip.main(['install','BeautifulSoup4'])
    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager

import datetime

date = datetime.datetime.now()

from bs4 import BeautifulSoup

class WebScrapper():
     
    def __init__(self,url):
        self.url = url
        self.options= Options()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome("D:\\Test\\chromedriver\\chromedriver.exe")
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())        
        
    def FindVaccineLocation(self,pincode):    
        self.FinalResult = {}    
        self.driver.get(self.url)
        self.driver.set_page_load_timeout(10)
        time.sleep(1)

        self.pin = self.driver.find_element_by_xpath('//input[@placeholder="Enter your PIN"]')
        self.pin.send_keys(pincode)

        self.pin.send_keys(Keys.ENTER)
        time.sleep(5)
        rowsHtML = self.driver.find_element_by_class_name("center-box").get_attribute('innerHTML')
        
        
        # self.location = self.driver.find_element_by_class_name("center-name-title").text
        # #print(self.location)
        # self.VaccineNum = self.driver.find_element_by_class_name("slot-available-wrap").get_attribute('innerHTML')
        # #self.VaccineNum = self.driver.find_element_by_class_name("vaccine-box vaccine-box1 vaccine-padding")      
        # #print(self.VaccineNum)
        # #<a _ngcontent-quf-c68="" tooltip="Fully Booked" placement="top" show-delay="100" title="Fully Booked"> Booked </a>
        # soup = BeautifulSoup(self.VaccineNum, "html.parser")    
        # result = soup.findAll('a')
        # for eachItem in result:    
        #     item = eachItem.text
        #     #print(self.location,item)
        #     if(item.isdigit()):
        #         self.final[self.location]=item
        
        soup = BeautifulSoup(rowsHtML,'html.parser')
        rows = soup.find_all(class_="row")
        
        for eachRow in rows:
            finalList = []
            #print(eachRow) 
            #print("************************************************************************************************************")
            location = (eachRow.findAll(class_="center-name-title"))[0].text.strip()
            #print(eachRow.findAll(class_="center-name-title"))
            #print("************************************************************************************************************")
            #print(eachRow.findAll('a'))
            for count,eachCol in enumerate(eachRow.findAll('a')):
                #print("####################################################################################################")
                status = (eachCol.text).strip()
                #print((eachCol.text).strip())
                today = str(date.day+count)+'-'+str(date.month)+'-'+str(date.year)
                finalList.append((today,status))

            self.FinalResult[location]=finalList    
        
        
        #print(self.FinalResult)

    def PrintRes(self):
        for key,val in self.FinalResult.items():
            print(key,val)

if __name__ == "__main__":
    
    #Main Pgm
    print("*****************************************WELCOME*****************************************")
    url = "https://www.cowin.gov.in/home"
    print(url)

    scrapper = WebScrapper(url)
    for pinCode in ["500005","680303","680007"]:
        print("Calling FindVaccine for PIN:"+pinCode)
        scrapper.FindVaccineLocation(pinCode)
        scrapper.PrintRes()   

    # if(bool(scrapper.final)):
    #     print("########################VACCANCY########################")
    #     print(scrapper.final)
    print("Exiting")
    scrapper.driver.quit()
