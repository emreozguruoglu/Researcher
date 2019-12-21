import re
import os.path
from os import path

# Define a function for
# for validating an Email
def check_email(email):
    # Make a regular expression
    # for validating an Email
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

    if (re.search(regex, email)):
        return True
    else:
        return False

def check_file_exist(filePath):
    if path.exists(filePath):
        return True
    else:
        return False