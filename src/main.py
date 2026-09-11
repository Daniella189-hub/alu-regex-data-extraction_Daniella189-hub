#!/usr/bin/python3 
"""
main.py
Data extraction $secure validation
this file handles different type of data extraction and data validation
1.email addresses(ALU own)
2.credit card numbers
3.phone numbers
4.hastags
it also does some small basic checkings if the text is to be trusted or not especially if the text contains script tags and SQL injection, to test that we handle it safely
"""

import re
import json
import os
#------------------------
# HANDLING REGEX PATTERNS
#------------------------

# 1. Email validation          #this email output "something@something.something

valid-email = r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9_]+\.(com|org|fr|edu|net)$'

# 2.Credit cards              #this one has to contain 16 digits without letters and follow a paatern of 4 digit - 6 digits - 5digits with the "-"character included

valid_credit_card = r"\d{4}[ -]?\d{6}[ -]?\d{5}|\d{4}[ -]?\d{4}[ -]?\d{4}"

# 3. phone number validation       #a valid number contain(+250) or start with 07..) for rwandan numbers it is followed with 9 digits 

valid_phone_number = r"^\+250[ -]?7\d{2}[ -]?\d{3}[ -]?\d{3}|^\07\d{2}[ -]?\d{3}[ -]?\d{3}|\(\d{3}\)[ -]?\d{3,4}[ -]?\d{0,4}"

# 4. hastag validation

valid_hastag = r"\#[a-zA-Z]\w*"

# 5. ALU email validation
valid_alumni_email = r"@alumni\.alueducation\.com$"
valid_si_email = r"@si\.alueducation\.com$"
valid_official_email = r"@alueducation\.com$"

# -------------------------------
# CHECKING FOR FAKE OBVIOUS DATA
# -------------------------------

# cross checking for credit cards by using the LUhn algorithm

def credit_card_valid(card):
    digits = [int(d) for d in re.sub(r"\D","", card)]
    #reject obvious fake numbers like all zeros
    if len(set(digits)) == 1:
        return False
    total=0
    digigts.reverse()
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d = d * 2
            if d > 9:
                d = d - 9
         total += d
     return total % 10 == 0

def scan_alu_email(email):
     """ checks if the email given is an alu email"""
     if re.search(valid_alumi_email, email, re.IGNORECASE):
         return "alumni email"
     if re.search(valid_si_email, email, re.IGNORECASE):
         return "this is an si email"
     if re.search(valid_official_email, email, re.IGNORECASE):
         retrun "this is an official email at ALU"
     else:
         return "this is a normal email address not from ALU"
# ------------------------------------------------------------------
# HIDING SENSITIVE INFORMATION LIKE CREDIT CARD NUMBERS LAST DIGIT
# -----------------------------------------------------------------
# mask the credit_card

def mask_card(card):
    digits = re.sub(r"\D", "", card)
    return "**** **** ****" + digits[-4:]
# mask the email

def mask_email(email):
    name, domain = email.split("@")
    if len(name) <= 2 :
        hidden = name[0] + "*"
    else:
        hidden = name[0] + "*" * (len(name) -2) + name[-1]
    return hidden + "@" + domain

# mask the phone number
def mask_number(phone):
    digits = re.sub(r"\D", "", phone)
    return "*" * (len(digits) - 3) + digits[-3:]


# ----------------------------
# calling 
def main():
    input_path = os.path.join(os.path.dirname(__file__), "..", "input", "raw-text.txt")
    output_path = os.path.join(os.path.dirname(__file__), "..", "output", "sample-output.json")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    results = extract_all(raw_text)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent = 2)

        print("Emails extracted from raw data:", len(results["emails"]))
        print("Credit cards extracted from raw data :", len(results["credit_cards"]))
        print("phone numbers found:", len(results["phone_numbers"]))
        print("hastags extracted from raw data:", len(results["hasatags"]))
        print("the results sare saved to:", output_path)

if __name__=="__main__":
    main()
