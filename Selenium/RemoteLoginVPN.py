from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys

username = "bgeorge"
password = "(#beeJr55.0)"
success_stmt = "You're now connected to VPN!"
run_count = 0
#driver = webdriver.Firefox("D:\\CodeTEst\\projects\\Selenium")

def LoginToOKTA():

    try:
        start = input("Do you want to want to run the remote login driver....(y|n)")
        print(start)
        if start == 'n':
            sys.exit()

        print("**********Opening browser driver*********")
        driver = webdriver.Chrome("D:\\CodeTEst\\projects\\Selenium\\chromedriver.exe")
        driver.set_page_load_timeout(20)
        print("**********Opening Commvault OKTA**********")
        driver.get("https://commvault.okta.com/")

        #Insert Username
        print("Validating username...")
        elements = driver.find_elements_by_xpath("//div[@id='okta-sign-in']")
        uname = driver.find_element_by_xpath("//input[@id='okta-signin-username']")
        uname.send_keys(username)
        uname.send_keys(Keys.ENTER)

        time.sleep(5)

        #Insert password
        print("Validating password...")
        elements1 = driver.find_elements_by_xpath("//div[@id='okta-sign-in']")
        okta_password = driver.find_elements_by_xpath("//input[@name='password']")
        res = okta_password[0]
        res.send_keys(password)
        res.send_keys(Keys.ENTER)

        time.sleep(5)

        #Send push authentication
        print("Waiting for Authentication..")
        elements2 = driver.find_elements_by_xpath("//div[@id='okta-sign-in']")
        chk_send_push = driver.find_element_by_xpath("//input[@class='button button-primary']").click()


        for i in range(0,3):
            print("Waiting for confirmation")

        print("Successfully logged in.")
        print("Please confirm in okta app.")
        print("Loading  ", end = " ")
        for i in range(30,0,-1):
            print(i,end=" ")
            time.sleep(1)

        confirm = input("\nDid you confirm....(y|n)")
        if confirm == 'n':
            driver.quit()
            sys.exit()

        #IndiaVPN    
        print("\n**********Opening IndiaVPn**********")
        imgbtn_IndiaVPN = driver.find_element_by_xpath("//a[img/@src='https://ok2static.oktacdn.com/fs/bco/4/fs09jo0l9zof6UXJ90x7']").click()


        #Alert confirmation
        # time.sleep(10)
        # alert = driver.switch_to_alert
        # while True:
        #     if(alert != None):
        #         alert.accept()
        #         break
        
        time.sleep(15)
        
        count = 1
        print("Connecting to VPN..",end=" ")
        run_count = 0
        while True:
            
            try:
                print("Connecting.......")
                count = count + 1
                print("Inside root --- Switching to new window")
                driver.switch_to_window(driver.window_handles[1])
                print("            --- Now inside new window")
                connect = driver.find_element_by_tag_name("h1")
                print("            --- Element found")
                connect_stmt = connect.get_attribute("innerHTML")
                print("            --- Attribute found")
                print(connect_stmt)
                for i in range(count):
                    print(".")
                
            except:
                if run_count == 0:
                    time.sleep(10)
                    print("Exception raised.Trying again.")
                    run_count = 1
                    continue
                exit()

            if(connect_stmt == success_stmt):
                print("Connection Established SUCCESSFULLY !!!")
                driver.quit()
                break

        return True

    except SystemExit:
        print("Exiting the driver in ",end="")
        for i in range(3):
            print(i,end="")
            time.sleep(1)
    except:
        #run_count = run_count + 1
        print("Please wait for 10 seconds.")
        time.sleep(10)
        print("Running the driver.")
        LoginToOKTA()
        # if run_count == 2:
        #     print("Running the driver.")
        #     self.LoginToOKTA()
        # else:    
        #     print("Exiting the driver run!!!!")
        #     exit()
                       

if __name__ == "__main__":
        
    bRet = LoginToOKTA()
    if(bRet == False):
        print("Failed to run the driver")







