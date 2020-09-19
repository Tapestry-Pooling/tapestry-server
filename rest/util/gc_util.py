import requests
import binascii
import collections
import datetime
import hashlib
import sys
import json
import os

from google.oauth2 import service_account

import six
from six.moves.urllib.parse import quote

from google.cloud import storage


service_account_file = os.path.join(
    'secrets',
    'tapestry-pooling-cloud-storage-credentials.json'
)

def get_report_download_url(object_name):
    bucket_name = os.environ.get('RESULT_REPORT_BUCKET')

    # compute signed url
    report_download_url = generate_signed_url(
        service_account_file,
        bucket_name,
        object_name,
        expiration=86400,  # 1 day
    )
    return report_download_url


def get_object_list(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    object_list = [(blob.name, blob.name) for blob in blobs]

    return object_list


def get_pooling_matrix_download_url(payload=None, object_name=None):
    pooling_function_url = os.environ.get('POOLING_FUNCTION_URL')

    headers = {
        'Content-Type': 'application/json'
    }

    bucket_name = os.environ.get('POOLING_SCHEME_BUCKET')

    if object_name is None:
        # request google cloud function
        response = requests.request("POST", pooling_function_url, headers=headers, data=payload)
        if response.status_code == 200:
            object_name = json.loads(response.text.encode('utf8'))['filename']

    # compute signed url
    pooling_matrix_signed_url = generate_signed_url(
        service_account_file,
        bucket_name,
        object_name,
        expiration=86400,  # 1 day
    )
    return object_name, pooling_matrix_signed_url


def get_ct_value_upload_url(object_name):
    #headers = {
    #    'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #}
    bucket_name = os.environ.get('POOLING_RESULT_BUCKET')

    upload_signed_url = generate_signed_url(
        service_account_file,
        bucket_name,
        object_name,
        expiration=86400, # 1 day
        http_method='PUT'
     #  ,
     #  headers=headers
    )
    return upload_signed_url


def generate_signed_url(service_account_file, bucket_name, object_name,
                        subresource=None, expiration=604800, http_method='GET',
                        query_parameters=None, headers=None):

    if expiration > 604800:
        print('Expiration Time can\'t be longer than 604800 seconds (7 days).')
        sys.exit(1)

    escaped_object_name = quote(six.ensure_binary(object_name), safe=b'/~')
    canonical_uri = '/{}'.format(escaped_object_name)

    datetime_now = datetime.datetime.utcnow()
    request_timestamp = datetime_now.strftime('%Y%m%dT%H%M%SZ')
    datestamp = datetime_now.strftime('%Y%m%d')

    google_credentials = service_account.Credentials.from_service_account_file(
        service_account_file)
    client_email = google_credentials.service_account_email
    credential_scope = '{}/auto/storage/goog4_request'.format(datestamp)
    credential = '{}/{}'.format(client_email, credential_scope)

    if headers is None:
        headers = dict()
    host = '{}.storage.googleapis.com'.format(bucket_name)
    headers['host'] = host

    canonical_headers = ''
    ordered_headers = collections.OrderedDict(sorted(headers.items()))
    for k, v in ordered_headers.items():
        lower_k = str(k).lower()
        strip_v = str(v).lower()
        canonical_headers += '{}:{}\n'.format(lower_k, strip_v)

    signed_headers = ''
    for k, _ in ordered_headers.items():
        lower_k = str(k).lower()
        signed_headers += '{};'.format(lower_k)
    signed_headers = signed_headers[:-1]  # remove trailing ';'

    if query_parameters is None:
        query_parameters = dict()
    query_parameters['X-Goog-Algorithm'] = 'GOOG4-RSA-SHA256'
    query_parameters['X-Goog-Credential'] = credential
    query_parameters['X-Goog-Date'] = request_timestamp
    query_parameters['X-Goog-Expires'] = expiration
    query_parameters['X-Goog-SignedHeaders'] = signed_headers
    if subresource:
        query_parameters[subresource] = ''

    canonical_query_string = ''
    ordered_query_parameters = collections.OrderedDict(
        sorted(query_parameters.items()))
    for k, v in ordered_query_parameters.items():
        encoded_k = quote(str(k), safe='')
        encoded_v = quote(str(v), safe='')
        canonical_query_string += '{}={}&'.format(encoded_k, encoded_v)
    canonical_query_string = canonical_query_string[:-1]  # remove trailing '&'

    canonical_request = '\n'.join([http_method,
                                   canonical_uri,
                                   canonical_query_string,
                                   canonical_headers,
                                   signed_headers,
                                   'UNSIGNED-PAYLOAD'])

    canonical_request_hash = hashlib.sha256(
        canonical_request.encode()).hexdigest()

    string_to_sign = '\n'.join(['GOOG4-RSA-SHA256',
                                request_timestamp,
                                credential_scope,
                                canonical_request_hash])

    # signer.sign() signs using RSA-SHA256 with PKCS1v15 padding
    signature = binascii.hexlify(
        google_credentials.signer.sign(string_to_sign)
    ).decode()

    scheme_and_host = '{}://{}'.format('https', host)
    signed_url = '{}{}?{}&x-goog-signature={}'.format(
        scheme_and_host, canonical_uri, canonical_query_string, signature)

    return signed_url
