import re

# Define a function for
# for validating an Email
def check(email):
    # Make a regular expression
    # for validating an Email
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if (re.search(regex, email)):
        return True
    else:
        return False
