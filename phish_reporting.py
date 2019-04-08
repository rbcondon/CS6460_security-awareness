import os
import csv

MAP_FILE = "/Users/riley/Documents/Phishing Script/usermap.txt"
REGISTER_FILE = "/Users/riley/Documents/Phishing Script/register.txt"

if not os.path.exists(MAP_FILE):
    print "Could no find: " + REGISTER_FILE
    exit(-1)

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

fd = open(REGISTER_FILE, "r")
clickers = []
for line in fd.readlines():
    line = line.rstrip()
    tokens = line.split(",",4)
    user = recipientHashMap.keys()[recipientHashMap.values().index(tokens[1])]
    tokens[1] = user
    clickers.append(tokens)
fd.close()

file = open("clickers.txt","w")

for clicker in clickers:
    file.write(clicker[1])
    file.write(",")
    file.write(clicker[2])
    file.write("\n")

file.close()
