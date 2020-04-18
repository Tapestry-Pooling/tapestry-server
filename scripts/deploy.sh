#!/bin/bash
REPO="$HOME/covid"
cd $REPO
# Activate virtualenv
source env/bin/activate
# Update requirements
pip install -r requirements.txt
# Regenerate versioning.json
python matrix_manager.py
# TODO : Regenerate SVG HTML and PDFs
# TODO : Update DB
SENTRY_VERSION=$(sentry-cli releases propose-version)
sentry-cli releases new $SENTRY_VERSION --finalize
sudo systemctl restart covid.service
sentry-cli releases deploys $SENTRY_VERSION new -e $SENTRY_ENV
