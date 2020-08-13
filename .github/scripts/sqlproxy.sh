#!/bin/sh

# download cloudsql proxy
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy

#start the proxy
./cloud_sql_proxy -instances=tapestry-pooling-284109:europe-west1:postgres=tcp:5432 \
                  -credential_file=secrets/tapestry-pooling-cloudsql-proxy-credentials.json &
