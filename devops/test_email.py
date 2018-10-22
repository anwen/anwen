import sys
sys.path.append('.')
import options
import utils

subject = 'test'
msg_body = 'hi'
email = options.superadmin_email
print(email)
email = '527639661@qq.com'
utils.send_email(email, subject, msg_body)
