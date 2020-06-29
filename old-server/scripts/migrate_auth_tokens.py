# Script to migrate tokens of form 'email' -> 'user_id:token:expiry_epoch' to 'token' -> 'user_id:email:expiry_epoch'
import lmdb

LMDB_SIZE = 16 * 1024 * 1024

def iterate_db(env, func, write=False):
    with env.begin(write=write) as txn:
        for key, value in txn.cursor():
            func(txn, key, value)

# func should take arguments of form: old_txn, new_txn, key, value
def migrate_db(old_env, new_env, func):
    with old_env.begin() as old_txn:
        with new_env.begin(write=True) as new_txn:
            for key, value in old_txn.cursor():
                func(old_txn, new_txn, key, value)

def convert_token(old_txn, new_txn, key, value):
    key = key.decode("utf8")
    value = value.decode("utf8")
    print(f'{key} : {value}')
    if key is None or value is None or value.count(':') != 2 or key.count('@') != 1:
        return
    # email -> user_id:token:expiry_epoch => token -> user_id:email:expiry_epoch
    user_id, token, expiry_epoch = value.split(':')
    new_txn.put(token.encode('utf8'), f'{user_id}:{key}:{expiry_epoch}'.encode('utf8'))

def print_tokens(txn, key, value):
    key = key.decode("utf8")
    value = value.decode("utf8")
    print(f'{key} : {value}')

#migrate_db(lmdb.open('./workdir/db', map_size=LMDB_SIZE), lmdb.open('./workdir/prod.lmdb', map_size=LMDB_SIZE), convert_token)
iterate_db(lmdb.open('./workdir/prod.lmdb', map_size=LMDB_SIZE), print_tokens)