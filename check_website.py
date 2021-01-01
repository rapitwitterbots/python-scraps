from __future__ import print_function
from datetime import datetime
import urllib.request
import smtplib, ssl, os

port = 465 # for ssl
password = "password"
url = 'enter url'
keyword = 'website'
email = 'email'


def validate(res):
    result = (keyword in res)
    return result


def check_website():
    print('Checking Site...')

    try:
        if not validate(urllib.request.urlopen(url, None, 12).read().decode()):
            print('Site not reachable')
            raise Exception('Validation failed')
    except:
        print('Check failed!  Rebooting raspi.')
        message='Had to restart the Raspberry Pi - website check failed!'
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(email, password)
            server.sendmail(email, email, message)
    else:
        print('Check passed!')
        return 1;
    finally:
        print('Check complete at {}'.format(str(datetime.now())))
