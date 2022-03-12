import smtplib
import os
import re
import socket
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv('YAHOO_EMAIL')
SMTP_PASSWORD = os.getenv('YAHOO_APP_TOKEN') #please use the app password instead of the plain password
EMAIL_FROM = os.getenv('YAHOO_EMAIL')
EMAIL_TO = [ os.getenv('MY_EMAIL') ] # or use this for multi emails = ['CEO@yahoo.com', 'CIO@google.com']
EMAIL_SUBJECT = "Weekly Report: "

def send_email(co_msg):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M")
    msg = MIMEMultipart()
    msg['Subject'] = EMAIL_SUBJECT + "Servers Aliveness - " + dt_string
    msg['From'] = EMAIL_FROM 
    msg['To'] = ', '.join(EMAIL_TO)

    txt = MIMEText(co_msg)
    msg.attach(txt)

    # debuglevel = True
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    # mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()

def is_running(site, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #the AF_INET and SOCK_Stream are the default values, it can be left empty
        sock.connect((site, port))
        return True
    except:
        return False

def checkServer():
    SERVER=[]
    PORT=22 #which port you want to connect to
    CONNTIMEOUT=5 #Connection timeout in sec, because the default is none and will hang if not set
    SITEOK=0
    TOTALSITE=0
    currentDir=os.getcwd()
    output=""

    with open(currentDir + '/serverlist.txt', 'r') as serverlist:
        for line in serverlist:
            line=re.sub(r'\n','',line) #removing the \n from the list
            SERVER.append(line)

    for site in SERVER:
        try:
            if is_running(site, PORT, CONNTIMEOUT):
                output=output+str(f'{site} is running!\n')
                SITEOK+=1
            else:
                output=output+str(f'There is NO response for server {site}\n')
        except:
            output=output+str('something went terribly wrong with the function\n')
        finally:
            TOTALSITE+=1

    return (f'{output}SUMMARY (OK/NOK): ' + str(SITEOK) + '/' + str(TOTALSITE))

if __name__=='__main__':
    msg=checkServer()
    send_email(msg)

