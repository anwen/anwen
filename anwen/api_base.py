# https://gist.github.com/mminer/5464753
import json
import tornado.web
import tornado.httpserver
from tornado.web import RequestHandler
from tornado.escape import json_decode


class JsonHandler(RequestHandler):
    """Request handler where requests and responses speak JSON."""

    # def initialize(self, *args, **kwargs):
    #     self.remote_ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
    #     self.using_ssl = (self.request.headers.get('X-Scheme', 'http') == 'https')

    # def prepare(self):
    #     # Incorporate request JSON into arguments dictionary.
    #     if self.request.body:
    #         try:
    #             json_data = json.loads(self.request.body.decode('u8'))
    #             self.request.arguments.update(json_data)
    #         except ValueError:
    #             message = 'Unable to parse JSON.'
    #             self.send_error(400, message=message)  # Bad Request
    #     # Set up response dictionary. res=response

    def prepare(self):
        super().prepare()
        self.json_data = None
        self.res = dict()
        if self.request.body:
            try:
                json_data = tornado.escape.json_decode(self.request.body)
                # self.json_data = json.loads(self.request.body.decode('u8'))
            except ValueError:
                # TODO: handle the error
                print('json_data error')
                pass
                raise tornado.httpserver._BadRequestException(
                    "Invalid JSON structure."
                )
            if type(json_data) != dict:
                raise tornado.httpserver._BadRequestException(
                    "We only accept key value objects!"
                )
            for key, value in json_data.items():
                self.request.arguments[key] = [value, ]
            # self.done()

    # def get_argument(self, arg, default=None):
    #     # TODO: there's more arguments in the default get_argument() call
    #     # TODO: handle other method types
    #     if self.request.method in ['POST', 'PUT'] and self.json_data:
    #         return self.json_data.get(arg, default)
    #     else:
    #         return super().get_argument(arg, default)

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
        self.set_status(status_code)
        print('_reason', self._reason)
        # if not self._reason:
        #     if status_code == 422:
        #         kwargs['message'] = 'Unprocessable Entity, miss field'
        # if 'message' not in kwargs:
        #     if status_code == 405:
        #         kwargs['message'] = 'Invalid HTTP method.'
        #     elif status_code == 401:
        #         kwargs['message'] = 'Unauthorized, wrong email or password'
        #     else:
        #         kwargs['message'] = 'Unknown error.'
        # 如果缺少必要的 filed，会返回 422 Unprocessable Entity
        # 通过 errors 给出了哪些 field 缺少了，能够方便调用方快速排错
        self.res = {'success': False, 'message': self._reason}
        # HTTP/1.1 401 Unauthorized
        self.write_json()

    def write_json(self):
        out = {}
        out['data'] = self.res
        out['success'] = True
        output = json.dumps(out)
        self.write(output)
