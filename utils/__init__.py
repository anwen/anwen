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


def send_email(receiver, subject, msg_body):
    import smtplib
    from email.mime.text import MIMEText
    me = '%s<%s>' % (options.EMAIL_HOST_NICK, options.SERVICE_EMAIL)
    host = options.EMAIL_HOST
    port = options.EMAIL_PORT
    user = options.EMAIL_HOST_USER
    password = options.EMAIL_HOST_PASSWORD
    msg = MIMEText(msg_body, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = receiver  # ";".join(receivers)
    s = smtplib.SMTP()
    # s.set_debuglevel(1)  # show the debug log
    try:
        print(s.connect(host, port))
    except:
        print 'CONNECT ERROR ****'
    if options.EMAIL_USE_TLS:
        s.starttls()
    try:
        s.login(user, password)
        s.sendmail(me, receiver, msg.as_string())
        s.quit()
        return True
    except Exception as e:
        print(str(e))
        return False
