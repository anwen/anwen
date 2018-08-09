import json
import tornado.web
from tornado.web import RequestHandler
from tornado.escape import json_decode


class JsonHandler(RequestHandler):
    """Request handler where requests and responses speak JSON."""

    # def initialize(self, *args, **kwargs):
    #     self.remote_ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
    #     self.using_ssl = (self.request.headers.get('X-Scheme', 'http') == 'https')

    def prepare(self):
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                json_data = json.loads(self.request.body.decode('u8'))
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)  # Bad Request

        # Set up response dictionary. res=response
        self.res = dict()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get_current_user(self):
        token = self.request.headers.get('Authorization', '')
        if token:
            key, token = token.split()
            if key == 'token' and token:
                user_json = self.get_secure_cookie('user', token)
                if user_json:
                    return json_decode(user_json)
        user_json = self.get_secure_cookie("user")
        if user_json:
            return json_decode(user_json)
        # token = self.get_argument('token', '')
        # if token:
        #     user_json = self.get_secure_cookie('user', token)
        #     if user_json:
        #         return json_decode(user_json)
        return None

    def write_error(self, status_code, reason=None):
        print('_reason', self._reason)
        # if 'message' not in kwargs:
        #     if status_code == 405:
        #         kwargs['message'] = 'Invalid HTTP method.'
        #     elif status_code == 422:
        #         kwargs['message'] = 'Unprocessable Entity, miss field'
        #     elif status_code == 401:
        #         kwargs['message'] = 'Unauthorized, wrong email or password'
        #     else:
        #         kwargs['message'] = 'Unknown error.'
        # 如果缺少必要的 filed，会返回 422 Unprocessable Entity
        # 通过 errors 给出了哪些 field 缺少了，能够方便调用方快速排错
        self.set_status(status_code, reason)
        self.res = {'message': reason}
        # HTTP/1.1 401 Unauthorized
        self.write_json()

    def write_json(self):
        output = json.dumps(self.res)
        self.write(output)
