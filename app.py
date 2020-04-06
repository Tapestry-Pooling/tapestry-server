from flask import Flask, request, json, jsonify, redirect, render_template, url_for, g
from functools import wraps
import lmdb
import os
import psycopg2
from psycopg2 import pool
import secrets

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
# pg connection pool
pgpool = psycopg2.pool.SimpleConnectionPool(1, 10, user = "covid", password = "covid", host = "127.0.0.1", port = "5432", database = "covid")


"""
    Utils
"""

def normalize_phone(phone):
    if phone.startswith('+91') and len(phone) == 13:
        return phone
    if len(phone) == 11 and phone.startswith('0') and phone.isdigit():
        return '+91' + phone[1:]
    if len(phone) == 10 and phone.isdigit():
        return '+91' + phone
    return None

def parse_lmdb_data(raw_data):
    # user_id:auth_token:timestamp
    return raw_data.decode('ascii').split(':')

def check_auth(request):
    "Checks if user is signed in from cookie"
    headers = request.headers
    auth_token = headers['X-Auth']
    mob = headers['X-Mob']
    if auth_token is None or auth_token == '' or mob is None or mob == '':
        return False
    raw_data = None
    with lmdb_read_env.begin() as txn:
        raw_data = txn.get(mob.encode('ascii'))
    if raw_data is None:
        return False
    data = parse_lmdb_data(raw_data)
    saved_token = data[1]
    if saved_token == auth_token:
        g.user_id = data[0]
        # TODO : timestamp validation
        return True
    return False

def requires_auth(func):
    "Function for basic authentication check"
    @wraps(func)
    def decorated(*args, **kwargs):
        "Decorator function for auth"
        if not check_auth(request.cookies):
            return redirect(url_for('login', next=url_for(request.endpoint)))
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

def insertone(query, params):
    try:
        conn = pgpool.getconn()
        with g.conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
            return cur.fetchone()
    except:
        raise
    finally:
        pgpool.putconn(conn)


"""
    Endpoints here
"""

@app.route('/request_otp')
def request_otp():
    # TODO : generate OTP, save to lmdb, add ttl of 5 min, send SMS using Exotel
    payload = request.json
    phone = payload['phone']
    reg_phone = normalize_phone(phone)
    if reg_phone is None:
        return jsonify(result={"status": 500, "error" : "Invalid mobile number"})
    return DUMMY_OTP

@app.route('/validate_otp')
def validate_otp():
    payload = request.json
    phone = payload['phone']
    otp = payload['otp']
    # TODO : check OTP for number from LMDB
    if phone is None or otp is None:
        return jsonify(result={"status": 500, "error" : "Mobile or OTP missing"})
    reg_phone = normalize_phone(phone)
    if reg_phone is None:
        return jsonify(result={"status": 500, "error" : "Invalid mobile number"})
    token = secrets.token_urlsafe(16)
    # DB upsert
    return 'Auth-token'

@app.route('/user_login/')
def login():
    # mobile number, OTP, return auth token
    return render_template('login.html')

@app.route('/dashboard/<user_id>', methods=['GET'])
@requires_auth
def user_dashboard(user_id):
    if g.user_id != user_id:
        return jsonify(result={"status": 500, "error" : "Invalid user details"})
    user_sql = """select t1.id as test_id, t1.created_at, t1.updated_at, t1.test_data, t2.result_data 
        from test_uploads t1, test_results t2 where t1.id = t2.test_id and t1.user_id = %s;"""
    result = select(user_sql, (user_id,))
    return result


@app.route('/test_data', methods=['PUT'])
@requires_auth
def modify_test_data():
    payload = request.json
    test_id = payload['test_id']
    test_data = payload['test_data']
    if test_id is None or test_data is None or len(test_data) not in VECTOR_SIZES:
        return jsonify(result={"status": 500, "error" : "Invalid test id or test data"})
    
    pass


@app.route('/test_data', methods=['POST'])
@requires_auth
def upload_test_data():
    payload = request.json
    # payload is a float array
    # length check on payload to see if it falls in one of the test matrices
    if len(payload) not in VECTOR_SIZES:
        return jsonify(result={"status": 500, "error" : "Invalid vector size"})
    # Insert into test_uploads
    test_uploads_sql = "insert into test_uploads (user_id, test_data) values (%s, %s) returning id;"
    test_id = insertone(test_uploads_sql, (g.user_id, payload))
    # TODO : Call computation function, save result. For now, saving dummy payload
    test_results_sql = "insert into test_results (test_id, result_data ) values (%s, %s);"
    insertone(test_results_sql, (test_id, [1 for x in range(40)]))
    return jsonify(result={"status": 200})

"""
    Main
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)