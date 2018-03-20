from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime
import _thread
import urllib
import socket
import os

from sites import stgr
from sites import scholarshipsads
from sites import scholarship_positions
from sites import scholars4dev
import mmap
import os.path
import smtplib

from email.mime.text import MIMEText
from email.header import Header


MAIL_USER = "grantsgrabber@gmail.com"
MAIL_PWD = "grantsgrabber@max"
RECIPIENT = ["maxlero@ya.ru", "powerfuldeff@gmail.com"]

status = 0


#  Initialize LCD (must specify pinout and dimensions)
lcd = Adafruit_CharLCD(rs=26, en=19,
						d4=13, d5=6, d6=5, d7=11,
						cols=16, lines=2)

def get_ip_address():
	try:
		return [
					(s.connect(('8.8.8.8', 53)),
					s.getsockname()[0],
					s.close()) for s in
						[socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
					][0][1]
	except Exception as e:
		return '0.0.0.0'

def measure_temp():
	temp = os.popen("vcgencmd measure_temp").readline()
	return temp.replace("temp=","").replace("\n","")

def internet_on():
    try:
        urllib.request.urlopen('https://www.google.by/', timeout=1)
        return True
    except Exception as err: 
        return False


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


def process_information(links):
	if not os.path.exists("caches"):
		f = open("caches", "w+")
		f.write('\n')
		f.close()

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
			print("Failed to send mail")
	else:
		print('Nothing to send')


def parsing_process(arg0, arg1):
	global status

	try:
		results = []

		# Parse site http://st-gr.com/?cat=3
		stgr.parse_site(results)

		# Parse site https://www.scholarshipsads.com/degree/bachelor
		scholarshipsads.parse_site(results)

		# http://scholarship-positions.com/category/under-graduate-scholarship/
		scholarship_positions.parse_site(results)

		# http://www.scholars4dev.com/category/level-of-study/undergraduate-scholarships/
		scholars4dev.parse_site(results)

		print("Parsed: " + str(len(results)) + " items")

		process_information(results)

		status = 0
	except Exception as e:
		print(e)

		status = -1


if __name__ == "__main__":
	try:
		ip = get_ip_address()

		lcd.clear()
		lcd.set_cursor(0, 0)
		lcd.message('Powered by Vihos')
		lcd.set_cursor(0, 1)
		lcd.message('IP {:>13}'.format(ip))

		sleep(5)

		lcd.clear()

		counter = 0

		while 1:
			lcd.set_cursor(0, 0)
			lcd.message('{:8}'.format(measure_temp()))
			lcd.message('{:>8}'.format(datetime.now().strftime('%H:%M:%S')))

			if internet_on():
				lcd.set_cursor(0, 1)
				lcd.message('{:8}'.format('Online'))
			else:
				lcd.set_cursor(0, 1)
				lcd.message('{:8}'.format('Offline'))

			# 1800s == 30min
			if counter < 1800 and status <= 0:
				counter += 1
			if counter >= 1800 and status == 1:
				counter = 0
			elif counter >= 1800 and status <= 0:
				#  Start parsing
				counter = 0
				status = 1

				try:
					_thread.start_new_thread(parsing_process, ("Thread-1", ()))
				except Exception as e:
					status = -1
					print("Error: unable to start thread")

			if status == 0:
				lcd.message('Idle {:2}m'.format(str(int((1800 - counter)/60))))
			elif status == 1:
				lcd.message('{:8}'.format('Parsing'))
			elif status == -1:
				lcd.message('{:8}'.format('!!EDPP!!'))

			sleep(1)

	except KeyboardInterrupt:
		print('CTRL-C pressed.  Program exiting...')

	finally:
		lcd.clear()
