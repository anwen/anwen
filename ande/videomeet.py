# -*- coding:utf-8 -*-

from anwen.base import BaseHandler
import logging
import random
import re
import json
import jinja2
import options
import threading

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        options.web_server['template_path']),
    auto_reload=True,  # 自动重载，调试用
)


# Lock for syncing DB operation in concurrent requests handling.
# TODO(brave): keeping working on improving performance with thread syncing.
# One possible method for near future is to reduce the message caching.
LOCK = threading.RLock()


def generate_random(len):
    word = ''
    for i in range(len):
        word += random.choice('0123456789')
    return word


def sanitize(key):
    return re.sub('[^a-zA-Z0-9\-]', '-', key) if key else None


def make_client_id(room, user):
    return room.key().id_or_name() + '/' + user


def make_pc_config(stun_server, turn_server, ts_pwd):
    servers = []
    if turn_server:
        turn_config = 'turn:{}'.format(turn_server)
        servers.append({'url': turn_config, 'credential': ts_pwd})
    if stun_server:
        stun_config = 'stun:{}'.format(stun_server)
    else:
        stun_config = 'stun:' + 'stun.l.google.com:19302'
    servers.append({'url': stun_config})
    return {'iceServers': servers}


def create_channel(room, user, duration_minutes):
    client_id = make_client_id(room, user)
    return client_id, duration_minutes


def make_loopback_answer(message):
    message = message.replace("\"offer\"", "\"answer\"")
    message = message.replace("a=ice-options:google-ice\\r\\n", "")
    return message


def maybe_add_fake_crypto(message):
    if message.find("a=crypto") == -1:
        index = len(message)
        crypto_line = "a=crypto:1 AES_CM_128_HMAC_SHA1_80 inline:BAADBAADBAADBAADBAADBAADBAADBAADBAADBAAD\\r\\n"
        # reverse find for multiple find and insert operations.
        index = message.rfind("c=IN", 0, index)
        while (index != -1):
            message = message[:index] + crypto_line + message[index:]
            index = message.rfind("c=IN", 0, index)
    return message


def handle_message(room, user, message):
    message_obj = json.loads(message)
    other_user = user
    room_key = room
    if message_obj['type'] == 'bye':
        # This would remove the other_user in loopback test too.
        # So check its availability before forwarding Bye message.
        logging.info('User ' + user + ' quit from room ' + room_key)
        logging.info('Room ' + room_key + ' has state ' + str(room))
    if other_user:
        if message_obj['type'] == 'offer':
            # Special case the loopback scenario.
            if other_user == user:
                message = make_loopback_answer(message)
            # Workaround Chrome bug.
            # Insert a=crypto line into offer from FireFox.
            # TODO(juberti): Remove this call.
            message = maybe_add_fake_crypto(message)
        on_message(room, other_user, message)
        return message

def on_message(room, user, message):
    logging.info('message: ' + message)
    if room:
        logging.info('Delivered message to user ' + user)
    else:
        logging.info('Saved message for user ' + user)


def make_media_constraints(hd_video):
    constraints = {'optional': [], 'mandatory': {}}
    # Demo 16:9 video with media constraints.
    if hd_video.lower() == 'true':
        # Demo with WHD by setting size with 1280x720.
        constraints['mandatory']['minHeight'] = 720
        constraints['mandatory']['minWidth'] = 1280
        # Disabled for now due to weird stretching behavior on Mac.
        # else:
        # Demo with WVGA by setting Aspect Ration
        # constraints['mandatory']['maxAspectRatio'] = 1.778
        # constraints['mandatory']['minAspectRatio'] = 1.777
    return constraints


def make_pc_constraints(compat):
    constraints = {'optional': []}
    # For interop with FireFox. Enable DTLS in peerConnection ctor.
    if compat.lower() == 'true':
        constraints['optional'].append({'DtlsSrtpKeyAgreement': True})
    return constraints


def make_offer_constraints(compat):
    constraints = {'mandatory': {}, 'optional': []}
    # For interop with FireFox. Disable Data Channel in createOffer.
    if compat.lower() == 'true':
        constraints['mandatory']['MozDontOfferDataChannel'] = True
    return constraints


def append_url_arguments(request, link):
    for argument in request.arguments:
        if argument != 'r':
            link += '&' + argument + '=' + argument
    return link


class VideoMeetHandler(BaseHandler):

    def get(self):
        """Renders the main page. When this page is shown, we create a new
        channel to push asynchronous updates to the client."""
        room_key = sanitize(self.get_argument('r', None))
        debug = self.get_argument('debug', None)
        unittest = self.get_argument('unittest', None)
        stun_server = self.get_argument('ss', None)
        turn_server = self.get_argument('ts', None)
        hd_video = self.get_argument('hd', 'true')
        ts_pwd = self.get_argument('tp', None)
        # set compat to true by default.
        compat = self.get_argument('compat', 'true')
        if debug == 'loopback':
        # set compat to false as DTLS does not work for loopback.
            compat = 'false'

        # token_timeout for channel creation, default 30min, max 2 days, min 3min.
        # token_timeout = self.request.get_range('tt',
        #                                        min_value = 3,
        #                                        max_value = 3000,
        #                                        default = 30)
        if unittest:
            # Always create a new room for the unit tests.
            room_key = generate_random(8)

        if not room_key:
            room_key = generate_random(8)
            redirect = '?r=' + room_key
            redirect = append_url_arguments(self.request, redirect)
            self.redirect(redirect)
            logging.info('Redirecting visitor to base URL to ' + redirect)
            return

        user = None
        initiator = 0
        with LOCK:
            room = None
            if not room and debug != "full":
                # New room.
                user = generate_random(8)
                if debug != 'loopback':
                    initiator = 0
                else:
                    initiator = 1
            elif room and 1 == 1 and debug != 'full':
                # 1 occupant.
                user = generate_random(8)
                initiator = 1
            else:
                # 2 occupants (full).
                template = jinja_environment.get_template('full.html')
                self.response.out.write(
                    template.render({'room_key': room_key}))
                logging.info('Room ' + room_key + ' is full')
                return
        room_link = 'http://%s/videomeet?r=%s' % (self.request.host, room_key)
        room_link = append_url_arguments(self.request, room_link)
        pc_config = make_pc_config(stun_server, turn_server, ts_pwd)
        pc_constraints = make_pc_constraints(compat)
        offer_constraints = make_offer_constraints(compat)
        media_constraints = make_media_constraints(hd_video)
        template_values = {
            'me': user,
            'room_key': room_key,
            'room_link': room_link,
            'initiator': initiator,
            'pc_config': json.dumps(pc_config),
            'pc_constraints': json.dumps(pc_constraints),
            'offer_constraints': json.dumps(offer_constraints),
            'media_constraints': json.dumps(media_constraints)
        }
        if unittest:
            target_page = 'test/test_' + unittest + '.html'
        else:
            target_page = 'videomeet.html'

        template = jinja_environment.get_template(target_page)
        self.write(template.render(template_values))
        logging.info('User ' + user + ' added to room ' + room_key)


class VideoMsgHandler(BaseHandler):
    def post(self):
        message = self.request.body
        room_key = self.get_argument('r')
        user = self.get_argument('u')
        logging.info('message is ' + message)
        logging.info('room_key is ' + room_key)
        logging.info('user is ' + user)
        with LOCK:
            room = room_key
            if room:
                message = handle_message(room, user, message)
                logging.info('message echo ' + message)
                self.write(message)
            else:
                logging.warning('Unknown room ' + room_key)
