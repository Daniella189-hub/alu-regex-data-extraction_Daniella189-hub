# REGEX ONBOARDING HACKATHON

This is a simple python script that reads a messy raw-data text and extractinside of it the number of emails, credit cards, phone numbers and hastags:
  
## The project Structure

<img width="439" height="180" alt="image" src="https://github.com/user-attachments/assets/b5c0a5cd-68fb-4b73-b688-e0eb6f6da1a2" />

 
## How to run it
`cd alu-regex-data-extraction_Daniella189-hub
python3 src/main.py    or  ./src/main.py`

<img width="924" height="50" alt="image" src="https://github.com/user-attachments/assets/a1996af4-dbeb-4dd3-9553-23ab1d3f3901" />


## About the input file

input/raw-text.txt is made up to look like a batch of support tickets like ALU submit tickets from a job portal, it contains different messy messages sent by the users and what it stocks is mainly the numbers, emails, credit cards and hashtags of the ticket of each user.it has mixed up information(mails from ALU staff or community and other external people who used the platfor m of submitting tickets)

## The regex patterns
   - Email: `[a-zA-Z0-9_.%]+@[a-zA-Z0-9_.%]+\.(?:com|org|fr|edu|net|io|portal)` matches the normal name@doamin.tld shape. after matching the code also throwa away anything with a double dot (like fake@fake..com) since that's not a real email even though it kind of matches.
   - Credit card: `\d{4}[ -]?\d{6}[ -]?\d{5}|\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}"` First part catches Amex style(4-6-5 digits), second part catches Visa/mastercard style(4-4-4-4 igits). Spaces or dashes between the groups are both allowed since real receipts use both.
   - Phone number: `\+\d{1,3}[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}|0\d{3}[ -]?\d{3}[ -]?\d{3}|\(\d{3}\)[ -]?\d{3,4}[ -]?\d{0,4}` covers Rwandan number or any other number from another country written as +250 788 123 456 or 0788123456, plus generic (022) 5551234 style number.
   - Hashtag: `#[a-zA-Z]\w*`  A# followed by a letter and then any letters/numbers/underscores. it has tostart with a letter so it doesn't accidentally grab things like "Ticket#10231" as hashtag.

## ALU email check
we use three small regex patterns to verify if the emails are from ALU. using the ALU domain and search with re.esarch()
 <img width="663" height="122" alt="image" src="https://github.com/user-attachments/assets/dc529e2b-ec03-4391-b678-a44694bf2fd8" />

## Security notes

Since the text is supposed to be coming from an external API, we don't trust it fully:

   - clean_text() runs first and removes <script> tags, any other HTML tags, and basic SQL injection keywords (DROP TABLE, UNION SELECT) before we even start searching for emails/cards/etc. That way bad content can't sneak into our results or mess up how the text is read.
   - credit_card_valid() runs the Luhn algorithm (the standard math check used by real card systems) on every card we find, and also rejects numbers that are just one repeated digit (like all zeros), since those would technically pass Luhn but are obviously fake.
   - We never print or save full emails/cards/phone numbers. Everything gets masked first with `mask_email()`, `mask_card()`, and `mask_number()` — e.g. a****e@alueducation.com or **** **** **** 6467 — so no real personal data ends up sitting in a log file or JSON output.


this isn't a full security system, it's just meant to show that we thought about the input possibly being unsafe, not just messy

sample output(console)
<img width="942" height="193" alt="image" src="https://github.com/user-attachments/assets/ed767dfe-4463-4841-bb15-53fb483e8dbf" />

