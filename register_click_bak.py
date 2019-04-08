#!/usr/bin/python

import os
import datetime
import time
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
testId = form.getvalue("tid", None)
mId = form.getvalue("id", None)
timestamp = time.time()
st = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

print "Content-type: text/html\n\n";

fd = open("/Library/WebServer/CGI-Executables/register.txt", "a+")
fd.write("{0},{1},{2}\n".format(testId, mId, st))
fd.close()

if __name__ == '__main__':

   redirectURL = "http://localhost/hooked.html?" +testId

   print "Content-Type: text/html"
   print "Location: %s" % redirectURL
   print # HTTP needs blank line between headers and Content
   print "<html>"
   print " <head>"
   print "     <meta http-equiv='refresh' content='0;url=%s' />" % redirectURL
   print "     <title>You are going to be redirected</title>"
   print " </head>"
   print " <body>"
   print "     Redirecting... <a href='%s'>Click here if you are not redirected</a>" % redirectURL
   print " </body>"
   print "</html>"
