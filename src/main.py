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
def clean_text(text):

    text = re.sub(r"<script.*?>.*?</script>", "[removed script]", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", "[removed html]", text)  # remove any other html tags
    text = re.sub(r"DROP TABLE", "[blocked]", text, flags=re.IGNORECASE)
    text = re.sub(r"UNION SELECT", "[blocked]", text, flags=re.IGNORECASE)
    return text


#------------------------
# HANDLING REGEX PATTERNS
#------------------------

# 1. Email validation          #this email output "something@something.something

valid_email = r"[a-zA-Z0-9_.%]+@[a-zA-Z0-9_.%]+\.(com|org|fr|edu|net|io)$"   # this regex pattern starts with either letters(lower or upper) with dots , underscores, numbers and is followed with the "@" sign and the same features continues and then it ends with .com or .fr or .edu or .net

# 2.Credit cards              #this one has to contain 16 digits without letters and follow a paatern of 4 digit - 6 digits - 5digits with the "-"character included

valid_credit_card = r"\d{4}[ -]?\d{6}[ -]?\d{5}|\d{4}[ -]?\d{4}[ -]?\d{4}"       # a credit card contains only numbers as you can see, it accpets first 4 digits  then space or hyphens and then six digits and followed with 5 digits or it can starts with 4 digits separated by another successive four digits and the n again 4 digits

# 3. phone number validation       #a valid number contain(+250) or start with 07..) for rwandan numbers it is followed with 9 digits 

valid_phone_number = r"\+\d{1,3}[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}|0\d{3}[ -]?\d{3}[ -]?\d{3}|\(\d{3}\)[ -]?\d{3,4}[ -]?\d{0,4}"       # the phone number starts with the code (+250) or any other code and then it followed by eith 3 other digits and spearted by other 3 or it can also start with a "0" and then followed by more digits can be 3 ir 4 

# 4. hastag validation

valid_hastag = r"#[a-zA-Z]\w*"     # the hashtags always  start with a "#" and then followed by a letter and then followed by any other character

# 5. ALU email validation
valid_alumni_email = r"@alumni\.alueducation\.com$"       # this verifies if the email is form an alumni
valid_si_email = r"@si\.alueducation\.com$"               # this verifies if the email is for an SI by its end si.alueducation.com
valid_official_email = r"@alueducation\.com$"             # this verifies if the email is an official on and it ends with @alueducation.com

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
    digits.reverse()
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
         return "this is an official email at ALU"
     else:
         return "this is a normal email address not from ALU"

# -----------------------------------------------------------------
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
# -----------------------
# PUT EVERYTHING TOGETHER
# -----------------------

def extract_all(text):
    """ in this side we are trying to extract  the very thing we would like to have in our output, results is a dictionary where emails, credit-cards, phone numbers are keys and they are being attributed the output of what wiill be found in the raw-text.txt file and that matches the regex pattern found in respectively valid -email, valid-credit-card, valid-phone numbers and valid-hastag as values and this is what will be stocked in the sample-output.json file """

    text = clean_text(text)        # here we decided to use the clean Data so we can deal with easy and not messy data

    results = {                         #we declared a dictionary results that contain everything from what we want to regex pattern
            "emails":[],
            "credit_cards":[],
            "phone_numbers":[],
            "hashtags":[],
    }

    for email in set(re.findall(valid_email, text)):        # find in the raw-text.txt anything that matches the pattern in valid_email
        if ".." in email:
            continue        # if it is not a valid it just jumps it and doesnt store it in the output file
        results["emails"].append({          # the results collected will be appended as values to the key email
            "email": mask_email(email),     # for security purposes tthe email will be hidden in hastags in th eoutput fie
            "alu_type": scan_alu_email(email),    # it will also identify if the email is alu type or ordinary email
        })

    # credit cards
    for card in set(re.findall(valid_credit_card, text)):        # find in the raw-text.txt anything that matches the pattern in valid_credit_card
        results["credit_cards"].append({                         # the resulys are to be appended as values to the keys credit_cards
            "card":mask_card(card),                              # remember to hash the credit card for security purpose
            "valid": credit_card_valid(card),                    # applying th Luhn Algorithm to be able to track a credit card
        })
    # phone numbers
    for phone in set(re.findall(valid_phone_number, text)):      # find in the raw-text.txt anything that matches the pattern in valid_phone_number
        results["phone_numbers"].append({                         # appending the results to the key phone_numbers  as its values  found
            "phone": mask_number(phone),                           # Hashing the phone number for security purposes
        })
    #hashtags
    results["hashtags"] = sorted(set(re.findall(valid_hastag, text)))      #sorting the results found in the raw-text.txt that matches hashtags

    return results     # return the results as a dictionary containing all the informations


# ------------------------------
# calling everything in the main
# ------------------------------
def main():
    input_path = os.path.join(os.path.dirname(__file__), "..", "input", "raw-text.txt")      # defining the path where our raw data is storing the path in a variable input_path
    output_path = os.path.join(os.path.dirname(__file__), "..", "output", "sample-output.json")   # definign where the output of the main.py execution is going to be and storing in a variable output_path

    with open(input_path, "r", encoding="utf-8") as f:     # Here our main.py document is supposed to open this document in the input_path and read it, this is helpful in the data extraction, helpful in the execution of the main.py doc and cant execute without it
        raw_text = f.read()
    results = extract_all(raw_text)     # here it is assigning extract_all function to a module so it can be called and execute

    with open(output_path, "w", encoding="utf-8") as f:      # here our main.py is supposed to open this document in outpat_path(sample_output.json) and overwrite it or even write in it the results from the extraction in the first place.
        json.dump(results, f, indent = 2)

        print("Emails extracted from raw data:", len(results["emails"]))     # this is how it is supposed to write it and the the dictonary "results" will diaplay what it holds for the key "emails" and its values
        print("Credit cards extracted from raw data :", len(results["credit_cards"]))   # this is how it is supposed to write it and the dictionary"results" will display what it hols for the key "credit_cards" and its values
        print("phone numbers found:", len(results["phone_numbers"]))
        print("hastags extracted from raw data:", len(results["hashtags"]))
        print("the results sare saved to:", output_path)

if __name__=="__main__":
    main()
