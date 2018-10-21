

def make_password(pw):
    import hashlib
    return hashlib.md5(pw.encode('utf-8')).hexdigest()

# def make_password(pw):
#     import hashlib
#     from options import ssaalltt
#     pw = hashlib.sha512(pw.encode('utf-8')).hexdigest()
#     pw += ssaalltt
#     pw = hashlib.sha512(pw.encode('utf-8')).hexdigest()
#     return pw


def make_emailverify():
    import uuid
    import time
    return str(time.time()) + str(uuid.uuid4())


def send_email_2(receivers, subject, msg_body):
    import options
    import smtplib
    from email.mime.text import MIMEText
    from email.Header import Header
    me = '%s<%s>' % (options.EMAIL_HOST_NICK, options.SERVICE_EMAIL)
    host = options.EMAIL_HOST
    port = options.EMAIL_PORT
    user = options.EMAIL_HOST_USER
    password = options.EMAIL_HOST_PASSWORD
    msg = MIMEText(msg_body, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = me
    msg['To'] = receivers
    s = smtplib.SMTP()
    s.set_debuglevel(1)  # show the debug log
    s.connect(host, port)
    # s.starttls()
    s.login(user, password)
    s.sendmail(me, receivers, msg.as_string())
    s.quit()


def send_email(receivers, subject, msg_body):
    import options
    import smtplib
    from email.mime.text import MIMEText
    # from email.Header import Header
    from email.header import Header
    me = '%s<%s>' % (options.EMAIL_HOST_NICK, options.SERVICE_EMAIL)
    host = options.EMAIL_HOST
    port = options.EMAIL_PORT
    user = options.EMAIL_HOST_USER
    password = options.EMAIL_HOST_PASSWORD
    msg = MIMEText(msg_body, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = me
    msg['To'] = receivers
    s = smtplib.SMTP()
    s.set_debuglevel(1)  # show the debug log
    s.connect(host, port)
    # s.starttls()
    s.login(user, password)
    s.sendmail(me, receivers, msg.as_string())
    s.quit()

    # import smtplib
    # from email.mime.text import MIMEText
    # msg = MIMEText('hi')
    # msg['Subject'] = 'The title'
    # msg['From'] = 'me'
    # msg['To'] = 'you'
    # s = smtplib.SMTP('localhost')
    # s.send_message(msg)
    # s.quit()


def random_sayings():
    file1 = 'utils/sayings.txt'
    a = []
    with open(file1, 'r', encoding='u8') as f:
        for eachline in f:
            a.append(str(eachline.replace('\n', '')))
    import random
    return random.choice(a)


if __name__ == '__main__':
    print(random_sayings())
