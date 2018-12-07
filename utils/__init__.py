import random
import requests
import chardet


def get_charset(res):
    _charset = requests.utils.get_encoding_from_headers(res.headers)
    if _charset == 'ISO-8859-1':
        __charset = requests.utils.get_encodings_from_content(res.content)[0]
        # encode_type
        __charset = chardet.detect(res.content)['encoding']
        if __charset:
            _charset = __charset
        else:
            _charset = res.apparent_encoding
    return _charset


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
    import options
    import smtplib
    from email.mime.text import MIMEText
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
    try:
        # s = smtplib.SMTP()
        # s.connect(host, port)
        # s.starttls()
        s = smtplib.SMTP_SSL(host, port)
        s.set_debuglevel(1)  # show the debug log
        s.login(user, password)
        s.sendmail(me, receivers, msg.as_string())
        s.quit()
        print('send email Success')
    except smtplib.SMTPException as e:
        print('send email Fail: {}'.format(str(e).decode('u8')).encode('u8'))

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
        for line in f:
            line = line.strip()
            if not line:
                continue
            a.append(str(line))
    return random.choice(a).replace('\t', '<br>')


def get_tags():
    file1 = 'utils/Creative_Work.md'
    tags = {}
    with open(file1, 'r', encoding='u8') as f:
        for line in f:
            line = line.strip()
            if 'SubClassOf' not in line:
                continue
            _, s, p, o = line.split()
            if o == '作品':
                continue
            if o not in tags:
                tags[o] = []
            tags[o].append(s)
    return tags


if __name__ == '__main__':
    # print(random_sayings())
    print(get_tags())
