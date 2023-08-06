# Module: owlwatch
# Author: Benjamin Hobson

import sys
import smtplib, ssl
from getpass import getpass
import traceback

OWL_WATCH_PREFIX = '\033[1m' + 'OW - ' + '\033[0m'
OWL_WATCH_SUFFIX = ''
OWL_WATCH_SUCCESS_MESSAGE = """
The algorithm succeeded!
"""
OWL_WATCH_FAILURE_MESSAGE = """
The algorithm failed.
"""

def __format__(str):
    return OWL_WATCH_PREFIX + str + OWL_WATCH_SUFFIX

# Thanks https://realpython.com/python-send-email/
def send_email(sender_email, sender_password, recipient_email, message, subject, smtp_server, port, error_trace=None):
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    print(__format__('Sending email...'))
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, 'Subject: {}\n\n{}\n\nErrors: {}'.format(subject, message, error_trace))
        print(__format__('Email sent.'))
    except Exception as e:
        print(__format__('Could not send email with error: \n\n{}\n').format(e))
    finally:
        server.quit() 


class Client:
    def __init__(self, sender_email, recipient_email, sender_password = None, subject = 'OWL Watch', smtp_server = "smtp.gmail.com", port = 587):
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.sender_password = sender_password
        self.subject = subject
        self.smtp_server = smtp_server
        self.port = port


    def execute(self, func, *args, **kwargs):

        while self.sender_password is None:
            try:
                self.sender_password = getpass('Please enter the sender email password: ')
            except:
                pass
        
        try:
            ret = func(*args, **kwargs)
            # Assumes algorithm will raise Exception on error
            # Send email success
            print(__format__('Algorithm returned successfully.'))
            send_email(self.sender_email, self.sender_password, self.recipient_email, OWL_WATCH_SUCCESS_MESSAGE, self.subject, self.smtp_server, self.port)

            return ret
        except Exception as e:
            # Send email failed
            print(__format__('Algorithm failed with error: \n'))
            traceback.print_exc()
            print('\n')
            send_email(self.sender_email, self.sender_password, self.recipient_email, OWL_WATCH_FAILURE_MESSAGE, self.subject, self.smtp_server, self.port, error_trace=e)

if __name__ == '__main__':

    def failing_func(a):
        raise Exception('You failed')

    def passing_func(a):
        print('Recieved param:', a)

    #client = Client('sender_email@gmail.com', 'destination_email@gmail.com')
    #client.execute(passing_func, 'test')