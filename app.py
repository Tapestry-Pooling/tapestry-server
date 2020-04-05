from flask import Flask, request, json, jsonify, redirect, url_for, g
from functools import wraps
import lmdb

"""
    App setup and teardown
"""

app = Flask(__name__)
app.secret_key = 'covid-19-testing-backend'
# Using lmdb as a simple K/V store. Can be replaced by redis once requirements get more complex
# Max db size
LMDB_SIZE = 16 * 1024 * 1024
LMDB_PATH = './workdir/db'
lmdb_write_env = lmdb.open(LMDB_PATH, map_size=LMDB_SIZE)
lmdb_read_env = lmdb.open(LMDB_PATH, readonly=True)
VECTOR_SIZES = [16, 24, 64, 96]

"""
    Utils
"""

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


"""
    Endpoints here
"""

def register():
    # mobile number, OTP / password
    pass

def login():
    # mobile number, OTP / Password
    pass

def user_dashboard(user_id):
    user_sql = "select * from test_uploads where user_id = ?"
    pass

def modify_test_data():
    pass

@app.route('/test_data', methods=['POST'])
@requires_auth
def upload_test_data():
    payload = request.json
    # payload is a float array
    # length check on payload to see if it falls in one of the test matrices
    l = len(payload)
    if l not in VECTOR_SIZES:
        return jsonify(result={"status": 500, "error" : "Invalid vector size"})
    # TODO : Insert into database with valid template_id
    # TODO : Call computation function, save result
    return jsonify(result={"status": 200})

"""
    Main
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)