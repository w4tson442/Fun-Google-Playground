#!/usr/bin/env python

# Created BY: Justin Toyomitsu
# Create Date: Nov 15th 2020
# Last Update:
# =================================================

import cgi
import requests as req

# =================================================

# Search Button on front page
def getAuthorization():
    form = cgi.FieldStorage()
    email = str(form['email'].value)

    print('success')

def main():
    getAuthorization()

if __name__ == "__main__":
    main()
