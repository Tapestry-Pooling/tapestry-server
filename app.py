import boto3
from flask import Flask, request, json, jsonify, g
from functools import wraps
import lmdb
import logging
import os
import psycopg2
from psycopg2 import pool
import secrets
import time

"""
    App setup and teardown
"""

app = Flask(__name__)
app.secret_key = 'covid-19-testing-backend'
# Using lmdb as a simple K/V store for storing auth tokens and OTP for mobile numbers. Can be replaced by redis once requirements get more complex
# Max lmdb size
LMDB_SIZE = 16 * 1024 * 1024
LMDB_PATH = './workdir/db'
lmdb_write_env = lmdb.open(LMDB_PATH, map_size=LMDB_SIZE)
lmdb_read_env = lmdb.open(LMDB_PATH, readonly=True)
VECTOR_SIZES = [16, 24, 64, 96]
DUMMY_OTP = '34567890'
AUTH_TOKEN_VALIDITY = 90 * 24 * 60 * 60 # 90 days validity of auth token
OTP_VALIDITY = 900
# pg connection pool
pgpool = psycopg2.pool.SimpleConnectionPool(1, 10, user = "covid", password = "covid", host = "127.0.0.1", port = "5432", database = "covid")
NOTIFY_EMAILS = ['ssgosh@gmail.com', 'manoj.gopalkrishnan@gmail.com']
TEST_ARN = 'arn:aws:sns:ap-south-1:691823188847:c19-test'
PROD_ARN = 'arn:aws:sns:ap-south-1:691823188847:C19-PROD'
"""
    Utils
"""
def curr_epoch():
    return int(time.time())

def err_json(msg):
    return jsonify(error=msg),500

@app.errorhandler
def error_handler(error):
    return err_json("Unhandled error!!")

def normalize_phone(phone):
    if phone is None or phone == "" or phone.isspace():
        return None
    if phone.startswith('+91') and len(phone) == 13:
        return phone
    if len(phone) == 11 and phone.startswith('0') and phone.isdigit():
        return '+91' + phone[1:]
    if len(phone) == 10 and phone.isdigit() and not phone.startswith('0'):
        return '+91' + phone
    return None

def parse_lmdb_otp_data(raw_data):
    # otp:current time
    return raw_data.decode('utf8').split(':')

def parse_lmdb_auth_data(raw_data):
    # user_id:auth_token:timestamp
    return raw_data.decode('utf8').split(':')

def check_auth(request):
    "Checks if user is signed in using auth header"
    headers = request.headers
    auth_token = headers['X-Auth']
    mob = headers['X-Mob']
    reg_phone = normalize_phone(mob)
    if auth_token is None or auth_token == '' or reg_phone is None:
        return False
    raw_data = None
    with lmdb_read_env.begin() as txn:
        raw_data = txn.get(reg_phone.encode('utf8'))
    if raw_data is None:
        return False
    data = parse_lmdb_auth_data(raw_data)
    saved_token = data[1]
    if saved_token == auth_token and curr_epoch() - int(data[2]) < AUTH_TOKEN_VALIDITY:
        g.user_id = int(data[0])
        return True
    return False

def requires_auth(func):
    "Function for basic authentication check"
    @wraps(func)
    def decorated(*args, **kwargs):
        "Decorator function for auth"
        if not check_auth(request):
            return err_json("Invalid credentials")
        return func(*args, **kwargs)
    return decorated

def select(query, params):
    try:
        conn = pgpool.getconn()
        with g.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except:
        raise
    finally:
        pgpool.putconn(conn)

def execute_sql(query, params, one_row=False):
    try:
        conn = pgpool.getconn()
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
            if one_row:
                return cur.fetchone()
            return cur.fetchall()
    except:
        raise
    finally:
        pgpool.putconn(conn)


"""
    Endpoints here
"""

@app.route('/ping', methods=['GET'])
def ping():
    return "PONG"

@app.route('/request_otp', methods=['POST'])
def request_otp():
    # TODO : generate OTP, send SMS using Exotel
    payload = request.json
    app.logger.info(payload)
    reg_phone = normalize_phone(payload.get('phone', None))
    if reg_phone is None:
        return err_json("Invalid mobile number")
    otp_key = 'otp:' + reg_phone
    otp_value = DUMMY_OTP + ':' + str(curr_epoch())
    with lmdb_write_env.begin(write=True) as txn:
        txn.put(otp_key.encode('utf8'), otp_value.encode('utf8'))
    return jsonify(phone=reg_phone)

@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    payload = request.json
    otp = payload['otp']
    reg_phone = normalize_phone(payload.get('phone', None))
    if reg_phone is None or otp is None or not otp.isdigit():
        return err_json("Mobile or OTP incorrect")
    otp_key = 'otp:' + reg_phone
    raw_data = None
    with lmdb_read_env.begin() as txn:
        raw_data = txn.get(otp_key.encode('utf8'))
    if raw_data is None:
        return err_json("Invalid mobile number")
    data = parse_lmdb_otp_data(raw_data)
    curr_time = curr_epoch()
    if data[0] != otp or curr_time - int(data[1]) > 900:
        return err_json("Invalid or expired OTP")
    token = secrets.token_urlsafe(16)
    # DB upsert
    upsert_sql = "insert into users(phone) values (%s) on conflict(phone) do update set phone=excluded.phone returning id;"
    user_id = execute_sql(upsert_sql, (reg_phone,), one_row=True)[0]
    auth_value = str(user_id) + ":" + token + ":" + str(curr_time)
    with lmdb_write_env.begin(write=True) as txn:
        txn.put(reg_phone.encode('utf8'), auth_value.encode('utf8'))
    return jsonify(user_id=user_id, token=token, phone=reg_phone)

@app.route('/dashboard/<user_id>', methods=['GET'])
@requires_auth
def user_dashboard(user_id):
    if g.user_id != user_id:
        return err_json("Invalid user details")
    user_sql = """select t1.id as test_id, t1.updated_at, t1.test_data, t2.result_data 
        from test_uploads t1, test_results t2 where t1.id = t2.test_id and t1.user_id = %s order by t1.updated_at desc;"""
    result = select(user_sql, (user_id,))
    return result


@app.route('/test_data', methods=['PUT'])
@requires_auth
def modify_test_data():
    payload = request.json
    test_id = int(payload['test_id'])
    test_data = payload['test_data']
    if test_id is None or test_data is None or len(test_data) not in VECTOR_SIZES:
        return err_json("Invalid test id or test data")
    update_sql = "update test_uploads set test_data = %s where id = %s and user_id = %s returning id;"
    res = execute_sql(update_sql, (test_data, test_id, g.user_id))
    if res:
        updated_id = res[0][0]
        return jsonify(test_id=updated_id)
    return err_json("Test id not found")


@app.route('/test_data', methods=['POST'])
@requires_auth
def upload_test_data():
    payload = request.json
    # payload is a float array
    # length check on payload to see if it falls in one of the test matrices
    if len(payload) not in VECTOR_SIZES:
        return err_json("Invalid vector size")
    # Insert into test_uploads
    test_uploads_sql = "insert into test_uploads (user_id, test_data) values (%s, %s) returning id;"
    test_id = execute_sql(test_uploads_sql, (g.user_id, payload), one_row=True)[0]
    # TODO : Call computation function, save result. For now, saving dummy payload
    time.sleep(0.75)
    test_results_sql = "insert into test_results (test_id, result_data ) values (%s, %s) returning test_id;"
    execute_sql(test_results_sql, (test_id, [1 for x in range(40)]))
    return jsonify(test_id=test_id)

"""
    Main
"""
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)