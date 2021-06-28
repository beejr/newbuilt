
import time
import sys
import pip

try:
    __import__('selenium')
except ImportError:
    pip.main(['install','selenium'])
    __import__('selenium' )

try:
    __import__('webdriver_manager')
except ImportError:
    pip.main(['install','webdriver_manager'])
    __import__('webdriver_manager' )

pip.main(['install','BeautifulSoup4'])  
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
from webdriver_manager.chrome import ChromeDriverManager


from bs4 import BeautifulSoup

class WebScrapper():
     
    def __init__(self,url,username,password):
        self.url = url
        self.username = username
        self.password = password

        self.options= Options()
        self.options.add_argument('--headless')
        #self.driver = webdriver.Chrome("C:\\Users\\iambo\\.wdm\\drivers\\chromedriver\\win32\\89.0.4389.23\\chromedriver.exe")        
        self.driver = webdriver.Chrome(ChromeDriverManager().install())        
        
    def Authenticate(self):
        print("Authenticating....")
        
        self.driver.get(self.url)
        self.driver.set_page_load_timeout(20)
        time.sleep(5)
        self.username_input = self.driver.find_element_by_xpath('//input[@name="username"]')
        self.password_input = self.driver.find_element_by_xpath('//input[@name="password"]')

        self.username_input.send_keys(self.username)
        self.password_input.send_keys(self.password)

        self.password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        self.driver.get("https://www.instagram.com/%s" % self.username)

    def ListFollowers(self):
        
        print("Finding Followers....")       
        
        lstfollowers = []
        self.driver.get("https://www.instagram.com/%s/"% self.username)
        time.sleep(10)

        self.driver.find_element_by_xpath('//a[@href="/%s/followers/"]'%self.username).click()
        #self.driver.find_element_by_xpath('//a[@href="/me_bonisebi/followers/"]').click()
        time.sleep(5)
        
        self.noOfFollowers = self.driver.find_element_by_xpath('//a[@href="/%s/followers/"]/span'%self.username).get_attribute("title")
        print(self.noOfFollowers)
        self.times = int(int(self.noOfFollowers.strip())/12)
        
        self.target = self.driver.find_element_by_xpath('//div[@role="dialog"]//ul/parent::div')        
        while self.times > 0:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',self.target)
            time.sleep(1)
            self.times -= 1
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        followers = soup.find_all("a", class_='FPmhX notranslate _0imsa')
        
        for eachItem in followers:
            lstfollowers.append(eachItem.text)
        
        return lstfollowers
        
    def ListFollowing(self):
        
        print("Finding Following....")
        
        lstfollowing = []
        self.driver.get("https://www.instagram.com/%s/"%self.username)
        time.sleep(3)

        self.driver.find_element_by_xpath('//a[@href="/%s/following/"]'%self.username).click()
        time.sleep(5)
        
        self.noOfFollowing = self.driver.find_element_by_xpath('//a[@href="/%s/following/"]/span'%self.username).text
        print(self.noOfFollowing)
        self.times = int(int(self.noOfFollowing.strip())/12)
        
        
        self.target = self.driver.find_element_by_xpath('//div[@role="dialog"]//ul/parent::div')
        while self.times > 0:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',self.target)
            time.sleep(1)
            self.times -= 1

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        following = soup.find_all("a", class_='FPmhX notranslate _0imsa')
        
        for eachItem in following:
            lstfollowing.append(eachItem.text)
               
        return lstfollowing

if __name__ == "__main__":
    
    #Main Pgm
    print("*****************************************WELCOME*****************************************")
    username = input("Enter Username: ")     
    password = input("Enter Password: ")   
    url = "https://www.instagram.com/"

    scrapper = WebScrapper(url,username,password)
    #Login
    scrapper.Authenticate()
    #ListFollowers
    lst_followers = scrapper.ListFollowers()
    time.sleep(2)    
    #ListFollowing
    lst_following = scrapper.ListFollowing()
    

    
    #Find Followers that are not following you
    final = set(lst_followers)-set(lst_following)
    print("**********************************Users that follows you, but you are not following = %d***********************************\n"%len(list(final)))
    print(list(final))
    print("**********************************************************************************************************************")
    final = set(lst_following)-set(lst_followers)
    print("**********************************Users that you follow, but they are not following = %d***********************************\n"%(len(list(final))))
    print(list(final))
    print("**********************************************************************************************************************")
    scrapper.driver.quit()

