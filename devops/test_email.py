import smtplib
from email.mime.text import MIMEText


# fp = open(textfile, 'rb')
# msg = MIMEText(fp.read())
# fp.close()

msg = MIMEText('hi')

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = 'me'
msg['To'] = 'you'

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
