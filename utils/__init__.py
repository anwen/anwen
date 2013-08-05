import options


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


def send_email(receivers, subject, msg_body):
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


def send_error_email(title, error_log):
    sender = conf['smtp_user']
    password = conf['smtp_password']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(title, "UTF-8")

    part = MIMEText(error_log, 'html', _charset='UTF-8')
    msg.attach(part)
