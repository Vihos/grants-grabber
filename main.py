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
    msg = MIMEText(body, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = user
    msg['To'] = ", ".join(recipient)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    try:
        server.starttls()
        server.login(user, pwd)
        server.sendmail(msg['From'], recipient, msg.as_string())

        return True
    except Exception as e:
        print(e)
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

    f.close()

    message_content = ""

    for i in range(0, len(filtered_links)):
        message_content += '<li><a href="' + filtered_links[i]['href'] + '">' + filtered_links[i][
            'heading'] + '</a></li><br>'

    if len(message_content) > 0:
        message_content = '<ul>' + message_content + '</ul>'

        if send_email("Доступна возможность(и)", message_content):
            i = 0

            f = open("caches", "a")

            for i in range(0, len(filtered_links)):
                f.write(filtered_links[i]['cache'] + '\n')
                i += 1

            f.close()

            print('Successfully sent the mail with ' + str(i) + ' options')
        else:
            print("failed to send mail")
    else:
        print('Nothing to send')
else:
    f = open("caches", "w+")

    f.close()
