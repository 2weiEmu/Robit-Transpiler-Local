#!/usr/bin/env python
import sys
from os import system

import requests

req_files = [

]

if __name__ == "__main__":

    system("pip install -r requirements.txt")

    for URL in req_files:
        required_file = requests.get(URL)