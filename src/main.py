#!/usr/bin/python3 

import re
import json
## Email validation
raw_text= input("what is your email:")
if re.search(r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9_]+\.(com|org|fr|edu|net)$', raw_text):
    print("this is an email")
else:
    print("this cannot be an email address")
