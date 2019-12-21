from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import argparse
from helpers.checker import *

def check_vulnaribilty(email):
    haveibeenpwned_path = "https://haveibeenpwned.com/"

    path = os.path.abspath(os.curdir)
    chrome_driver_path = "{path}\{driverpath}".format(path=path, driverpath="driver\chromedriver.exe")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(haveibeenpwned_path)

    inputElement = driver.find_element_by_id("Account")
    inputElement.send_keys(email)
    inputElement.send_keys(Keys.ENTER)
    inputElement.submit()

    time.sleep(3)

    success_output = driver.find_element(By.CSS_SELECTOR, "#noPwnage > div > div > div.pwnTitle > h2").text
    error_output = driver.find_element(By.CSS_SELECTOR, "#pwnedWebsiteBanner > div > div > div.pwnTitle > h2").text
    vulnaribiltyList = driver.find_element(By.CSS_SELECTOR, "#pwnedSites").text

    print()
    if error_output is not '':
        error_detail = driver.find_element(By.CSS_SELECTOR, "#pwnCount").text
        print(str("{email} - {error_output} - {error_detail}").format(email=email,
                                                                  error_output=error_output,
                                                                  error_detail=error_detail))
        print()
    
        for i in vulnaribiltyList.split("\n"):
            if not i.split(":")[0].startswith("Compromised"):
                print(i.split(":")[0])
                print("---")
    else:
        print("Good news — no pwnage found!")

    driver.quit()