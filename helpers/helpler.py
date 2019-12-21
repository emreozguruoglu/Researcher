from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import argparse
from helpers.checker import *
import xlsxwriter
from helpers.enums import *

haveibeenpwned_path = "https://haveibeenpwned.com/"
path = os.path.abspath(os.curdir)
chrome_driver_path = "{path}\{driverpath}".format(path=path, driverpath="driver\chromedriver.exe")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_driver_path)
datetime = time.strftime("%Y%m%d-%H%M%S")
#Workbook() takes one, non-optional, argument  
# which is the filename that we want to create. 
workbook = xlsxwriter.Workbook(str("reports\{filename}.xlsx").format(filename=datetime))
        
# The workbook object is then used to add new  
# worksheet via the add_worksheet() method. 
worksheet = workbook.add_worksheet()
    
# Use the worksheet object to write 
# data via the write() method. 
worksheet.write('A1', 'E-Mail') 
worksheet.write('B1', 'Potential Risk')

def check_vulnaribilty(email_list, type_of_email):
    
    row_count = 2
    
    if type_of_email == OperationTypes.Single:
       dataResult  =  get_pwned_result(email_list)
       if dataResult is not '':
           result_to_report(row_count, email_list, dataResult)
    elif type_of_email == OperationTypes.Multiple:
         for email in email_list:
            dataResult  =  get_pwned_result(email)
            if dataResult is not '':
                result_to_report(row_count, email, dataResult)
                row_count = row_count + 1

    workbook.close() 
    driver.quit()


def get_pwned_result(email):
    
    if not check_email(email):
        return "Invalid E-Mail"

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

    success_output = driver.find_element(By.CSS_SELECTOR, "#noPwnage > div > div > div.pwnTitle > h2").text
    error_output = driver.find_element(By.CSS_SELECTOR, "#pwnedWebsiteBanner > div > div > div.pwnTitle > h2").text
    vulnaribiltyList = driver.find_element(By.CSS_SELECTOR, "#pwnedSites").text

    print()
    email_risk_data = ""
    
    if error_output is not '':
        error_detail = driver.find_element(By.CSS_SELECTOR, "#pwnCount").text
        print(str("{email} - {error_output} - {error_detail}").format(email=email,
                                                                  error_output=error_output,
                                                                  error_detail=error_detail))
        print()
    
        splited_data = vulnaribiltyList.split("\n")
          
        for risk in splited_data:
            if "Compromised" not in risk:
                email_risk_data = email_risk_data + risk.split(":")[0] + ","
    else:
        print("Good news — no pwnage found!")

    return email_risk_data

def result_to_report(row_count, email, message):
    worksheet.write(str('A{row_count}').format(row_count=row_count), email)
    worksheet.write(str('B{row_count}').format(row_count=row_count), message)


