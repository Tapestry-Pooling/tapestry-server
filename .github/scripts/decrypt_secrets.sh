#!/bin/sh

# Decrypt the file
mkdir secrets
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output secrets/tapestry-pooling-service_account_credentials.json \
tapestry-pooling-service_account_credentials.json.gpg