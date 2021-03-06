import boto3
from cachecontrol import CacheControl
from flask import Flask, request, json, jsonify, g, redirect
from functools import wraps
from google.oauth2 import id_token
import google.auth.transport.requests
import lmdb
import logging
import numpy as np
import orjson
import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import Json
import requests
import secrets
from sentry_sdk import init as sentry_init
import sys
import time
from traceback import format_exc

import matrix_manager
from pdf_maker import get_pdf_name
from grid import parse_batch, batch_size_from_batch_name
sentry_init('https://e615dd3448f9409293c2f50a7c0d85a7@sentry.zyxw365.in/8', environment= os.getenv('SENTRY_ENV', 'dev'), release=os.getenv('SENTRY_RELEASE', 'unknown'))

from compute_wrapper import get_test_results

"""
    App setup, teardown and constants
"""

app = Flask(__name__)
app.secret_key = 'byom-testing-backend'

# Response headers
CONTENT_TYPE = "Content-Type"
CONTENT_JSON = "application/json"

# Using lmdb as a simple K/V store for storing auth tokens and OTP for mobile numbers. Can be replaced by redis once requirements get more complex
# Max lmdb size
LMDB_SIZE = 16 * 1024 * 1024
LMDB_PATH = './workdir/prod.lmdb'
lmdb_write_env = lmdb.open(LMDB_PATH, map_size=LMDB_SIZE)
lmdb_read_env = lmdb.open(LMDB_PATH, readonly=True)

# Matrices
ACTIVE_BATCHES, ALL_BATCHES, BATCH_SIZE_TO_BATCH_NAME = matrix_manager.load_cache()
MLABELS = {k : ALL_BATCHES[k]['matrix'] for k in ALL_BATCHES}
BATCH_TO_CODENAMES = {k : ALL_BATCHES[k]["codename"] for k in ALL_BATCHES}
ACTIVE_BATCH_JSON = orjson.dumps({"data" : {k : ACTIVE_BATCHES[k]['readable'] for k in ACTIVE_BATCHES}})
VECTOR_SIZES = {int(k.split("x")[0]) for k in ALL_BATCHES}
GRID_JSON = {}
for k in ALL_BATCHES:
    GRID_JSON[k] = orjson.dumps({ "gridData" :  ALL_BATCHES[k]["gridData"]["gridData"],
       "cellData" :  ALL_BATCHES[k]["cellData"]["cellData"], "codename" :  ALL_BATCHES[k]["codename"] })

# App Version
MIN_VERSION = "1.0"
MIN_VERSION_INTS = tuple(int(x) for x in MIN_VERSION.split("."))
APP_UPDATE_URL = "https://play.google.com/store/apps/details?id=com.app.byom"

# Auth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'dummy')
GOOGLE_OLD_CLIENT_ID = os.getenv('GOOGLE_OLD_CLIENT_ID', 'old-dummy')
VALID_CLIENTS = {GOOGLE_CLIENT_ID, GOOGLE_OLD_CLIENT_ID}
CACHED_SESSION = CacheControl(requests.session())
TOK_INFO_KEYS = {'aud', 'iss', 'email', 'sub', 'iat', 'exp'}
VALID_ISSUERS = {'accounts.google.com', 'https://accounts.google.com'}
NEW_APP_USER_AGENT_FRAGMENT = 'BYOM Smart Testing'
AUTH_TOKEN_VALIDITY = 90 * 24 * 60 * 60 # 90 days validity of auth token

# Postgres related
psycopg2.extras.register_default_jsonb(loads=orjson.loads, globally=True)
PG_POOL = psycopg2.pool.SimpleConnectionPool(1, 4, user = "covid", password = "covid", host = "127.0.0.1", port = "5432", database = "covid", application_name = "byom")

# Alerts on test upload and failure
NOTIFY_EMAILS = ['ssgosh@gmail.com', 'manoj.gopalkrishnan@gmail.com']
TEST_ARN = 'arn:aws:sns:ap-south-1:691823188847:c19-test'
PROD_ARN = 'arn:aws:sns:ap-south-1:691823188847:C19-PROD'
SNS_CLIENT = boto3.client('sns')
NOTIFICATIONS_ENABLED = False

"""
    Utils
"""

def curr_epoch():
    return int(time.time())

def err_json(msg):
    app.logger.error(f"Error occured {msg}")
    return jsonify(error=msg),500

def app_version_check(version):
    if version is None or version == "" or version.isspace() or version.count(".") < 1:
        return False
    vs = tuple(int(x) for x in version.split("."))
    return vs >= MIN_VERSION_INTS

@app.errorhandler(Exception)
def error_handler(error):
    app.logger.error(f"Error occured {error}", exc_info=True)
    return err_json(f"Unhandled error!! {error}")

def normalize_email(email):
    if email is None or email == "" or email.isspace() or email.count("@") != 1 or email.count(":") != 0:
        return None
    esp = email.split("@")
    if esp[1] == "" or esp[1].count(".") == 0:
        return None
    return email.strip()

def parse_lmdb_auth_data(raw_data):
    # user_id:auth_token:timestamp
    return raw_data.decode('utf8').split(':')

def retrieve_auth_token_info(token, client_id):
    try:
        # According to https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.id_token.html#module-google.oauth2.id_token
        return id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(session=CACHED_SESSION), client_id)
    except Exception as e:
        app.logger.info(f"Google auth token retrieval failed for {token} and clientid {client_id} with error {e}")
    return {}

def validate_token_info(tok_info, email):
    # Expected fields in tok_info : https://developers.google.com/identity/protocols/oauth2/openid-connect#obtainuserinfo
    if not tok_info or not all(k in tok_info for k in TOK_INFO_KEYS):
        return {"error" : "Invalid token info"}
    reg_email = normalize_email(email)
    if reg_email is None or tok_info['email'] != reg_email:
        return {"error" : f"Invalid email supplied: {email}"}
    if tok_info['aud'] not in VALID_CLIENTS or tok_info['iss'] not in VALID_ISSUERS:
        return {"error" : f"Invalid client id / issuer"}
    # Is an expiry check necessary?
    if curr_epoch() > tok_info['exp'] + 60:
        return {"error" : f"Expired token"}
    return tok_info

def save_login_callback(tok_info, user_agent):
    email = tok_info['email']
    # Saving email : authToken in LMDB
    curr_time = curr_epoch()
    token = secrets.token_urlsafe(16)
    upsert_sql = "insert into users(email, name) values (%s,%s) on conflict(email) do update set name=excluded.name returning id;"
    user_id = execute_sql(upsert_sql, (email, tok_info.get('name', '')), one_row=True)[0]
    stored_value = str(user_id) + ":" + email + ":" + str(curr_time)
    with lmdb_write_env.begin(write=True) as txn:
        txn.put(token.encode('utf8'), stored_value.encode('utf8'))
    user_auth_sql = """insert into user_auth(user_id, token_info, auth_token, user_agent) values (%s, %s, %s, %s) on conflict(user_id) do
        update set token_info = excluded.token_info, auth_token = excluded.auth_token, user_agent = excluded.user_agent returning user_id;"""
    execute_sql(user_auth_sql, (user_id, Json(tok_info), token, user_agent))
    return jsonify(user_id=user_id, token=token, email=email)

def check_auth(request):
    "Checks if user is signed in using auth header"
    headers = request.headers
    auth_token = headers.get('X-Auth', "")
    email = headers.get('X-Email', "")
    reg_email = normalize_email(email)
    app.logger.info(f'Email : {reg_email}  Token: {auth_token}')
    if auth_token is None or auth_token == '' or reg_email is None:
        return False
    raw_data = None
    with lmdb_read_env.begin() as txn:
        raw_data = txn.get(auth_token.encode('utf8'))
    if raw_data is None:
        return False
    data = parse_lmdb_auth_data(raw_data)
    saved_email = data[1]
    if saved_email == reg_email and curr_epoch() - int(data[2]) < AUTH_TOKEN_VALIDITY:
        g.user_id = int(data[0])
        return True
    return False

def requires_auth(func):
    "Function for basic authentication check"
    @wraps(func)
    def decorated(*args, **kwargs):
        "Decorator function for auth"
        if not check_auth(request):
            return jsonify(error="Invalid credentials"),401
        return func(*args, **kwargs)
    return decorated

def select(query, params):
    try:
        conn = PG_POOL.getconn()
        with conn.cursor() as cur:
            app.logger.info(f"Executing query: {query} with params {params}")
            cur.execute(query, params)
            return cur.fetchall()
    except:
        raise
    finally:
        PG_POOL.putconn(conn)

def execute_sql(query, params, one_row=False):
    try:
        conn = PG_POOL.getconn()
        with conn.cursor() as cur:
            app.logger.info(f"Executing query: {query} with params {params}")
            cur.execute(query, params)
            conn.commit()
            if one_row:
                return cur.fetchone()
            return cur.fetchall()
    except:
        raise
    finally:
        PG_POOL.putconn(conn)

def publish_message(topic, message, subject=None):
    if not NOTIFICATIONS_ENABLED:
        return
    SNS_CLIENT.publish(TopicArn=topic, Message=message, Subject=subject)

def process_test_upload(test_id, batch, vector, num_samples):
    try:
        app.logger.info(f'Starting processing of test uploads for test id {test_id}')
        return get_test_results(MLABELS[batch], np.float32(vector), num_samples)
        app.logger.info(f'Finished processing of test uploads for test id {test_id}')
    except Exception as e:
        app.logger.error(f"Error occured {e}", exc_info=True)
        return {"error" : f'Error: {e}, Trace: {format_exc(e)}'}

def notify_test_success(test_id, batch, mresults, test_data, num_samples):
    succ_msg = f"""
    Test ID: {test_id} successful at {time.ctime()}
    Batch size: {batch}
    Matrix used: {MLABELS[batch]}
    CT Vector: {test_data}
    Number of samples: {num_samples}
    Result summary:
    {mresults["result_string"]}
    """
    publish_message(PROD_ARN, succ_msg, "Test upload success")

def notify_test_failure(test_id, batch, mresults, test_data, num_samples):
    err_msg = f"""
    Test ID: {test_id} failed at {time.ctime()}
    Batch size: {batch}
    Matrix used: {MLABELS[batch]}
    CT Vector: {test_data}
    Number of samples: {num_samples}
    Error summary:
    {mresults["error"]}
    Raw results value:
    {mresults}
    """
    publish_message(PROD_ARN, err_msg, "Test upload failure")

def post_process_results(test_id, batch, mresults, test_data, num_samples):
    if "error" in mresults:
        notify_test_failure(test_id, batch, mresults, test_data, num_samples)
        return err_json("Error occured while processing test upload. Don't worry! We will try again soon!")
    app.logger.info(f'{mresults}')
    test_results_sql = """insert into test_results (test_id, matrix_label, result_data ) values (%s, %s, %s) on conflict(test_id) 
    do update set updated_at = now(), matrix_label=excluded.matrix_label, result_data=excluded.result_data returning test_id;"""
    execute_sql(test_results_sql, (test_id, MLABELS[batch], Json(mresults)))
    notify_test_success(test_id, batch, mresults, test_data, num_samples)
    return jsonify(test_id=str(test_id), results=mresults["result_string"])

"""
    Endpoints here
"""

@app.route('/ping', methods=['GET'])
def ping():
    return "PONG"

@app.route('/debug_info', methods=['GET'])
def debug_info():
    return jsonify(matrix_labels=MLABELS, vector_sizes=list(VECTOR_SIZES), batch_to_codenames=BATCH_TO_CODENAMES)

@app.route('/pdf_info/<batch>', methods=['GET'])
def get_pdf_for(batch):
    return redirect(f'/pdfs/{get_pdf_name(batch, BATCH_TO_CODENAMES[batch])}', 302)

@app.route('/login_callback', methods=['POST'])
def login_sucess():
    payload = request.json
    app.logger.info(f'Google Auth Callback: {payload}')
    token = payload['token']
    email = payload['email']
    user_agent = request.headers.get('User-Agent', "")
    client_id = GOOGLE_CLIENT_ID if user_agent.startswith(NEW_APP_USER_AGENT_FRAGMENT) else GOOGLE_OLD_CLIENT_ID
    tok_info = retrieve_auth_token_info(token, client_id)
    if not tok_info:
        return jsonify(error="Invalid token"), 401
    app.logger.info(f'Validated with Google {tok_info}')
    val_tok_info = validate_token_info(tok_info, email)
    if "error" in val_tok_info:
        return jsonify(val_tok_info), 401
    return save_login_callback(val_tok_info, user_agent)

@app.route('/app_version_check', methods=['GET'])
def app_version_check_endpoint():
    app_version = request.args.get('version')
    force = not app_version_check(app_version)
    return jsonify(force=force, url=APP_UPDATE_URL)

@app.route('/dashboard', methods=['GET'])
@requires_auth
def user_dashboard():
    pagination = request.args.get('pagination', '')
    app.logger.info(f'Pagination : {pagination}')
    pagination_clause = ' and u.id < %s'
    if pagination is None or not pagination or pagination == '' or pagination == 'false':
        pagination_clause = ''
        pagination = 0
    dashboard_sql = f"""select u.id as test_id, u.updated_at, r.test_id, u.test_data, u.label, u.batch_size, 
    extract(minute from (u.batch_end_time - u.batch_start_time)) as test_duration_minutes, u.batch_start_time, u.batch_end_time,
    u.num_screens, u.test_mode from test_uploads u left join test_results r on u.id = r.test_id where u.user_id = %s and u.batch_end_time is not null
    {pagination_clause} order by u.id desc limit 50;"""
    params = (g.user_id,) if pagination == 0 else (g.user_id, int(pagination))
    res = select(dashboard_sql, params)
    last_pag = False
    if not res or len(res) == 0:
        return jsonify(data=[], pagination=last_pag)
    results = [{"test_id" : str(r[0]), "updated_at" : r[1], "results_available" : r[2] != None, 
        "test_data": r[3], "label" : r[4], "batch" : r[5], "duration_minutes" : r[6],
        "test_start_time" : r[7], "test_end_time" : r[8], "num_samples" : r[9], "test_mode" : r[10]} for r in res]
    if len(results) >= 50:
        last_pag = str(results[-1]["test_id"])
    return jsonify(data=results, pagination=last_pag)

@app.route('/start_test', methods=['POST'])
@requires_auth
def start_test():
    payload_json = request.json
    batch = payload_json.get('batch', "").strip()
    label = payload_json.get('label', "").strip()
    if label == "" or label.isspace() or batch == "" or batch.isspace() or batch not in MLABELS:
        return err_json(f"Empty test label or invalid batch size {batch}")
    nw, ns = parse_batch(batch)
    test_uploads_sql = "insert into test_uploads (user_id, label, batch_size, num_screens) values (%s, %s, %s, %s) on conflict(user_id, label) do nothing returning id;"
    res = execute_sql(test_uploads_sql, (g.user_id, label, batch, ns))
    if not res or len(res) == 0:
        return err_json(f"Label '{label}' already exists.")
    test_id = res[0][0]
    return jsonify(test_id=str(test_id))

@app.route('/end_test', methods=['POST'])
@requires_auth
def end_test():
    payload_json = request.json
    test_id = payload_json.get('test_id', "").strip()
    if test_id == "" or test_id.isspace() or not test_id.isdigit():
        return err_json(f"Invalid test id {test_id}")
    test_uploads_sql = "update test_uploads set batch_end_time = now(), updated_at = now() where user_id = %s and id = %s returning id;"
    res = execute_sql(test_uploads_sql, (g.user_id, int(test_id)))
    if not res or len(res) == 0:
        return err_json(f"Test id {test_id} not found")
    test_id = res[0][0]
    return jsonify(test_id=str(test_id))

@app.route('/test_data', methods=['POST', 'PUT'])
@requires_auth
def upload_test_data():
    payload_json = request.json
    test_id = payload_json.get('test_id', "").strip()
    if test_id == "" or test_id.isspace() or not test_id.isdigit():
        return err_json(f"Invalid test id {test_id}")
    test_data = payload_json.get('test_data', [])
    batch = payload_json.get('batch', "").strip()
    test_mode = payload_json.get('test_mode', "app").strip()
    num_samples = payload_json.get('num_samples', None)
    if batch == "" or batch.isspace() or batch not in ALL_BATCHES:
        return err_json(f"Invalid batch size : {batch}")
    lp = len(test_data)
    nw, ns = parse_batch(batch)
    if nw != lp or lp not in VECTOR_SIZES:
        err_msg = f"Invalid CT vector size of {lp} for batch type {batch}"
        app.logger.error(err_msg)
        return err_json(err_msg)
    if num_samples is None:
        num_samples = ns
    test_id = int(test_id)
    test_uploads_sql ="update test_uploads set updated_at = now(), test_data = %s, num_screens = %s, batch_size = %s, test_mode = %s where id = %s and user_id = %s returning id;"
    res = execute_sql(test_uploads_sql, (test_data, num_samples, batch, test_mode, test_id, g.user_id))
    if not res or len(res) == 0:
        return err_json(f"Test id not found {test_id}")
    updated_id = res[0][0]
    mresults = process_test_upload(test_id, batch, test_data, num_samples)
    return post_process_results(test_id, batch, mresults, test_data, num_samples)

@app.route('/results/<test_id>', methods=['GET'])
@requires_auth
def fetch_test_results(test_id):
    test_id = int(test_id)
    result_sql = "select r.test_id, r.result_data, r.matrix_label, u.batch_size, u.label, u.num_screens, u.test_mode from test_results r, test_uploads u where r.test_id = u.id and u.user_id = %s and u.id = %s"
    res = select(result_sql, (g.user_id, test_id))
    if not res or len(res) == 0:
        return err_json(f"Test not found for test_id : {test_id}")
    result = res[0]
    app.logger.info(f'Result: {result}')
    return jsonify(test_id=str(test_id), result=result[1]["result_string"], matrix=result[2], batch=result[3], label=result[4], num_samples=result[5], test_mode = result[6])

@app.route('/batch_data', methods=['GET'])
def batch_data():
    return ACTIVE_BATCH_JSON, 200, {CONTENT_TYPE : CONTENT_JSON}

@app.route('/grid_data/<batch>', methods=['GET'])
def screen_data(batch):
    return GRID_JSON.get(batch.strip(), "{}"), 200, {CONTENT_TYPE : CONTENT_JSON}

@app.route('/cell_data/<batch>', methods=['GET'])
def cell_data(batch):
    return GRID_JSON.get(batch.strip(), "{}"), 200, {CONTENT_TYPE : CONTENT_JSON}

@app.route('/available_matrices/<batch>', methods=['GET'])
def all_available_batches(batch):
    return jsonify(matrices=BATCH_SIZE_TO_BATCH_NAME.get(batch_size_from_batch_name(batch), []))

"""
    Main
"""
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    NOTIFICATIONS_ENABLED = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
