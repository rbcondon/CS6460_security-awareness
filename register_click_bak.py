import os
import datetime
import time
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
testId = form.getvalue("tid", None)
mId = form.getvalue("id", None)
remoteIp = os.environ['REMOTE_ADDR']
timestamp = time.time()
st = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

fd = open("/Users/riley/Documents/Phishing Script/register.txt", "a")
fd.write("{0}, {1}, {2}, {3}\n".format(testId, mId, remoteIp, st))
fd.close()

if __name__ == '__main__'


    redirectURL = "file:///Users/riley/Documents/Phishing%20Script/hooked.html?" +testID

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
~
