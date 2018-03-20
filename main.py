# TODO Twitter
import stgr
import mmap
import os.path
import smtplib

from email.mime.text import MIMEText
from email.header import Header

MAIL_USER = "grantsgrabber@gmail.com"
MAIL_PWD = "grantsgrabber@max"
RECIPIENT = ["maxlero@ya.ru", "powerfuldeff@gmail.com"]


def send_email(subject, body, user=MAIL_USER, pwd=MAIL_PWD, recipient=RECIPIENT):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = user
    msg['To'] = ", ".join(recipient)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    try:
        server.starttls()
        server.login(user, pwd)
        server.sendmail(msg['From'], recipient, msg.as_string())
        print('successfully sent the mail')

        return True
    except Exception as e:
        print(e)
        print("failed to send mail")
    finally:
        server.quit()

    return False


# send_email("test2", "test2")

links = stgr.parse_site()

if os.path.exists("caches"):
    f = open("caches", "r")
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    filtered_links = []

    for i in range(0, len(links)):
        if s.find(links[i]['cache'].encode()) == -1:
            filtered_links.append(links[i])
        else:
            print('true')

    f.close()

    message_content = ""

    for i in range(0, len(filtered_links)):
        message_content += filtered_links[i]['heading'] + ': ' + filtered_links[i]['href'] + '\n\n'

    if send_email("Доступна возможность(и)", message_content):
        f = open("caches", "w+")

        for i in range(0, len(filtered_links)):
            print(filtered_links[i]['cache'])

        f.close()
else:
    f = open("caches", "w+")

    f.close()
