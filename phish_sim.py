import glob
import datetime
import csv
import os
import smtplib
import hashlib
import re
import time
import ssl

# List of phishing email templates
input_templates = glob.glob("/Users/riley/Documents/Phishing Script/email_templates/*")

# Input file containing phishing simulation recipients
input_recipients = "/Users/riley/Documents/Phishing Script/emailRecipients.csv"

# List contains all the email email_templates
template_list = []
template_list.extend(input_templates)

# counter to iterate through templates
count = 1

# variable to hold selected template by test coordinator
userInput = 1

# Display email template options
# Ask test coordinator to choose email template for this test

print("#######################################################")
print("")
print("Email Templates")
for temp in input_templates:
    print(" " + str(count) + ": " + temp)
    count += 1
print("")
print("#######################################################")
print("")

# Take note of selected email template based on user input
userInput = int(input("Enter the email template number that you want to use for this test: "))
print("")

# This email template file will be used for this phishing simulation
TEMPLATE_FILE = template_list[userInput]

print(TEMPLATE_FILE)
print("")

# Define a test ID specific to this phishing simulation
current_datetime = datetime.datetime.now()
testID = current_datetime.strftime("%Y%m%d") # may need to make this ID more specific

print(testID)

# Define map file that will map recipients to unique recipient hash
MAP_FILE = "/Users/riley/Documents/Phishing Script/usermap.txt"

# Define mail server that will send out emails (GMAIL?)
MAIL_SERVER = "smtp.gmail.com" #have to define port and SSL???

recipient_list = []
# Import email recipients from input csv file
with open(input_recipients) as file:
    readFile = csv.reader(file)
    for entry in readFile:
        recipient_list.append(entry[0])

print(recipient_list)

# Show list of email recipients for this campaign
# Add or remove emails to this target list
while(True):
    userInput = 0
    count = 1
    print("")
    print("Email recipients for this simulated phishing campaign:")
    for rec in recipient_list:
        print(" "+str(count) + ": " + str(rec))
        count += 1
    print("")
    print("1: Add recipient to list")
    print("2: Remove recipient from list")
    print("3: Continue")

    userInput = int(input("Choose an option: "))

    if(userInput == 1):
        addEmail = raw_input("Please enter email to add: ")
        recipient_list.append(addEmail)
    elif(userInput == 2):
        removeEmail = raw_input("Please enter email to remove: ")
        recipient_list.remove(removeEmail)
    elif(userInput == 3):
        break
    else:
        print("ERROR, try again")

print("")
print("Continuing on...")
print("")


# Create hash mapping for each email recipient

# Check that recipient hash mapping file exists, creates it if it does not
if not os.path.exists(MAP_FILE):
    open(MAP_FILE, "a").close()

# Data structure to hold recipient hash mappings
recipientHashMap = {}

# Open current hash mapping file, add previous hash mappings to data structure
# Do I want to clear this file? Do I care about the old hash mappings?
fd = open(MAP_FILE, "r")
for line in fd.readlines():
    line = line.rstrip()
    tokens = line.split(",",2)
    recipient = tokens[0]
    hash = tokens[1]
    recipientHashMap[recipient] = hash
fd.close()

# Generate hash for each email recipient
for rec in recipient_list:
    md5 = hashlib.md5()
    md5.update(rec)
    recipientHashMap[rec] = md5.hexdigest()

# Add this simulation's email recipients to hash mappings file
fd = open(MAP_FILE, "w")
for rec in recipientHashMap:
    fd.write("{0},{1}\n".format(rec, recipientHashMap[rec]))
fd.close()

print("Recipient hash mappings file created.")


# Define email headers
email_sender = ""
email_subject = ""
email_title = ""
email_message = """Subject: <SUBJECT>
Mime-Version: 1.0\ncontent-Transfer-Encoding: 7bit\ncontent-type: text/html; charset=ISO-8859-1\n\n
<!doctype html public \"-//W3C//DTD HTML 4.0 Transitional//EN\"><html><head><title><TITLE></title></head><body>
"""

print(email_message)

# Each recipient has unique link in email, md5 of recipient email address
base_link = "http://localhost/cgi-bin/register_click.py?tid=" + testID + "&id="

print(base_link)

fd = open(TEMPLATE_FILE, "r")
for line in fd.readlines():
    line = line.rstrip()
    if line.startswith("FROM:"):
        tokens = line.split(None, 1)
        email_sender = tokens[1]
    elif line.startswith("SUBJ:"):
        tokens = line.split(None, 1)
        email_subject = tokens[1]
    elif line.startswith("TITL:"):
        tokens = line.split(None, 1)
        email_title = tokens[1]
    elif line.startswith("BODY:"):
        tokens = line.split(None, 1)
        email_message += tokens[1]
    else:
        email_message += line
fd.close()

email_message += "</body></html>"

email_message = re.sub('<SUBJECT>', email_subject, email_message)
email_message = re.sub('<TITLE>', email_title, email_message)

count = 1

print("#################################################################")
print("")

# Need to create gmail account for phishing simulation first
# This account will authenticate and use the GMAIL SMTP server to send out the emails

#    Credentials:
#        Username: awareness.training.2019
#        Password: 5!Sf$Whgze3w5C$XvKbg

port = 587
gmail_account = "awareness.training.2019@gmail.com"
password = "5!Sf$Whgze3w5C$XvKbg"

for receiver in recipient_list:
    if(count % 100 ==0):
        time.sleep(300)
    email_URL = base_link + recipientHashMap[receiver]
    print(email_URL)
    message = re.sub('\<MYLINK\>', email_URL, email_message)
    print(message)
    print("Sending email to: " + [receiver].__str__())
    server = smtplib.SMTP(MAIL_SERVER, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_account, password)
    print(email_sender)
    print([receiver])
    server.sendmail(email_sender, [receiver], message)
    server.quit()
    count += 1

print("")
print("##################################################################")

exit(0)
