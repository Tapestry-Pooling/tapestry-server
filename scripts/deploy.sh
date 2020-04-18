#!/bin/bash
REPO="$HOME/covid"
source $HOME/env/covid.env
cd $REPO
# Activate virtualenv
source env/bin/activate
echo "Checking for updated pip requirements"
pip install -r requirements.txt
echo "Regenerate versioning.json"
python matrix_manager.py
# TODO : Update DB
SENTRY_VERSION=$(sentry-cli releases propose-version)
sentry-cli releases new $SENTRY_VERSION --finalize
echo "Sentry version created: $SENTRY_VERSION"
sudo systemctl restart covid.service
echo "App restarted"
sentry-cli releases deploys $SENTRY_VERSION new -e $SENTRY_ENV
echo "Generating HTML files for batch sizes"
./scripts/generate_batch_html.sh
