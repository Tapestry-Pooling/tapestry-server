#!/bin/sh

# Decrypt the file
mkdir secrets
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$CLOUD_STORAGE_VIEW_SECRET" \
--output secrets/tapestry-pooling-storage-object-viewer-credentials.json \
tapestry-pooling-storage-object-viewer-credentials.json.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$CLOUD_STORAGE_CREATE_SECRET" \
--output secrets/tapestry-pooling-storage-object-creator-credentials.json \
tapestry-pooling-storage-object-creator-credentials.json.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$CLOUD_SQL_PROXY_SECRET" \
--output secrets/tapestry-pooling-cloudsql-proxy-credentials.json \
tapestry-pooling-cloudsql-proxy-credentials.json.gpg