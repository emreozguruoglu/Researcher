from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import argparse
from helpers.checker import *
from helpers.helpler import *
from helpers.enums import *

parser = argparse.ArgumentParser(description='Check emails for https://haveibeenpwned.com/')

parser.add_argument("--email")
parser.add_argument("--filepath")

#Getting parameters
args = parser.parse_args()

if args is not '':
    if args.email: 
        if check_email(args.email):
            email_list = args.email
            check_vulnaribilty(email_list, OperationTypes.Single)
    elif args.filepath:
        if check_file_exist(args.filepath):
            email_list = open(args.filepath)
            check_vulnaribilty(email_list, OperationTypes.Multiple)             
else:
    print("Please check parameters or arguments..")
    exit()
