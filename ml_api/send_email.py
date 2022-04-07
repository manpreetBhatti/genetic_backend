import smtplib

gmail_user = 'manpreetignite@gmail.com'
gmail_password = 'igniter0cks'

sent_from = gmail_user


class SendEmail:
    def __init__(self, emailBody, to):
        self.emailBody = emailBody
        self.to = to
        self.emailText = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, self.to, "Neural Network Architecture", self.emailBody)

    def send_email(self):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, self.to, self.emailText)
            server.close()
            return True
        except:
            return False
