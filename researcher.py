from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import argparse
from helpers.checker import check

parser = argparse.ArgumentParser(description='Check emails for https://haveibeenpwned.com/')
parser.add_argument("--email")

args = parser.parse_args()

if args is not '':
    if check(args.email):
        email = args.email
    else:
        print("Please check your email..")
        exit()
else:
    print("Please check parameters..")
    exit()

path = os.path.abspath(os.curdir)
chrome_driver_path = "{path}\{driverpath}".format(path=path, driverpath="driver\chromedriver.exe")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_driver_path)
driver.get("https://haveibeenpwned.com/")

inputElement = driver.find_element_by_id("Account")
inputElement.send_keys(email)
inputElement.send_keys(Keys.ENTER)
inputElement.submit()

time.sleep(3)

success_output = driver.find_element(By.CSS_SELECTOR, "#noPwnage > div > div > div.pwnTitle > h2").text
error_output = driver.find_element(By.CSS_SELECTOR, "#pwnedWebsiteBanner > div > div > div.pwnTitle > h2").text

print("---")
if error_output is not '':
    error_detail = driver.find_element(By.CSS_SELECTOR, "#pwnCount").text
    print(str("{email} - {error_output} - {error_detail}").format(email=email,
                                                                  error_output=error_output,
                                                                  error_detail=error_detail))
else:
    print("Good news — no pwnage found!")

print("---")
driver.quit()

