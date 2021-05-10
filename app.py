from flask import Flask, request
import logging
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from threading import Timer
import random
import string
import datetime
from Utils.constants import Constants, ErrorCode, ErrorMessage
import jwt
from Utils.db_helper import DatabaseConnector

logger = logging.getLogger("restfulapi")
app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
cur_salt = {}  # {sault: sault, expire_time: utc timestamp(second)}
db_connector = DatabaseConnector()

def gen_salt(salt_len):
    return ''.join(random.sample(string.ascii_letters + string.digits, salt_len))

def set_salt():
    cur_salt['salt'] = gen_salt(Constants.SALT_LEN)
    cur_salt['expire'] = datetime.datetime.utcnow().timestamp() + Constants.SALT_EXPIRE_TIME

set_salt()
Timer(Constants.SALT_EXPIRE_TIME, set_salt).start()

def pack(error_code, error_msg, data):
    return {
        'error_code': error_code,
        'error_msg': error_msg,
        'data': data
    }

@app.route('/get_salt')
def get_salt():
    return pack('', '', cur_salt)

@auth.verify_token
def verify_token(token):
    try:
        body = jwt.decode(token, Constants.CONST_SALT, algorithms=["HS256"])
        username = body['username']
        token = body['token']
        err, token_col = db_connector.query_user_token(username)
        cur_time = datetime.datetime.utcnow().timestamp()
        if err or not token_col:
            logger.warn('wrong token')
            return None
        if token == token_col.get('token') and \
            cur_time >= token_col.get('expire_time', float('inf')):
            db_connector.update_user_token(username, token, cur_time + Constants.TOKEN_EXPIRE_TIME)
            return username
        return None
    except jwt.exceptions.InvalidTokenError:
        return None
    except KeyError:
        return None

@app.route('/login', methods=["POST"])
def login():
    data = request.get_data()
    salt = cur_salt.get('salt', '')
    if salt == '':
        logger.error('salt empty')
        return pack(ErrorCode.INTERNEL_ERROR, ErrorMessage.INTERNEL_ERROR, '')
    try:
        json_body = jwt.decode(data, salt, algorithms=["HS256"])
        username = json_body['username']
        password = json_body['password']
    except jwt.exceptions.InvalidTokenError:
        return pack(ErrorCode.INVALID_SALT, ErrorMessage.INVALID_SALT, '')
    except KeyError:
        return pack(ErrorCode.INVALID_BODY, ErrorMessage.INVALID_BODY, '')
    err, user = db_connector.query_user_with_username(username)
    if err or not user:
        return pack(ErrorCode.INVALID_USERNAME, ErrorMessage.INVALID_USERNAME)
    if password == user.get('password'):
        token = gen_salt(Constants.SALT_LEN)
        expire_time = datetime.datetime.utcnow().timestamp() + Constants.TOKEN_EXPIRE_TIME
        db_connector.update_user_token(username, token, expire_time)
        ret = {
            'data': {
                'username': username,
                'token': token
            }
        }
        return pack('', '', jwt.encode(ret, Constants.CONST_SALT, algorithm="HS256"))
    return pack(ErrorCode.WRONG_PASSWORD, ErrorMessage.WRONG_PASSWORD)

@app.route('/logout')
@auth.login_required
def logout():
    username = auth.current_user()
    if not username:
        return pack(ErrorCode.LOGIN_NEEDED, ErrorMessage.LOGIN_NEEDED, None)
    db_connector.clear_user_token(username)
    return pack(None, None, 'logged out')

@app.route('/')
def test():
    return 'hello world'

