import sys
sys.path.append('.')
import options
import utils

subject = 'test'
msg_body = 'hi'
email = options.superadmin_email
utils.send_email(email, subject, msg_body)
