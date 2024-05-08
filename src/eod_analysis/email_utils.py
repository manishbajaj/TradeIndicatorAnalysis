#!/usr/bin/env python
# coding: utf-8

# This little project is hosted at: <https://gist.github.com/1455741>
# Copyright 2011-2020 Álvaro Justen [alvarojusten at gmail dot com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from smtplib import SMTP


def sendmail(name, email, mail_server, to_email, to_name, subject, message, fileName):
    password = "..." # add your password here
    print("\n")
    print("Connecting to server...")
    server = EmailConnection(mail_server, email, password)
    print('Preparing the email...')
    email = Email(from_='"%s" <%s>' % (name, email), #you can pass only email
              to='"%s" <%s>' % (to_name, to_email), #you can pass only email
              subject=subject, message=message, attachments=fileName)
    print("Sending...")
    server.send(email)
    print("Disconnecting...")
    server.close()
    print("Done!")
    

def get_email(email):
    if '<' in email:
        data = email.split('<')
        email = data[1].split('>')[0].strip()
    return email.strip()

class Email(object):
    def __init__(self, from_, to, subject, message, message_type='plain',
                 attachments=None, cc=None, message_encoding='us-ascii'):
        self.email = MIMEMultipart()
        self.email['From'] = from_
        self.email['To'] = to
        self.email['Subject'] = subject
        if cc is not None:
            self.email['Cc'] = cc
        text = MIMEText(message, message_type, message_encoding)
        self.email.attach(text)
        if attachments is not None:
            mimetype, encoding = guess_type(attachments)
            fp = open(attachments, 'rb')
            attachment = MIMEBase(mimetype[0], mimetype[1])
            attachment.set_payload(fp.read())
            fp.close()
            encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment',
                                      filename=os.path.basename(attachments))
            self.email.attach(attachment)

    def __str__(self):
        return self.email.as_string()


class EmailConnection(object):
    def __init__(self, server, username, password):
        if ':' in server:
            data = server.split(':')
            self.server = data[0]
            self.port = int(data[1])
        else:
            self.server = server
            self.port = 25
        self.username = username
        self.password = password
        self.connect()

    def connect(self):
        self.connection = SMTP(self.server, self.port)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()
        self.connection.login(self.username, self.password)

    def send(self, message, from_=None, to=None):
        if type(message) == str:
            if from_ is None or to is None:
                raise ValueError('You need to specify `from_` and `to`')
            else:
                from_ = get_email(from_)
                to = get_email(to)
        else:
            from_ = message.email['From']
            if 'Cc' not in message.email:
                message.email['Cc'] = ''
            to_emails = [message.email['To']] + message.email['Cc'].split(',')
            to = [get_email(complete_email) for complete_email in to_emails]
            message = str(message)
        return self.connection.sendmail(from_, to, message)

    def close(self):
        self.connection.close()