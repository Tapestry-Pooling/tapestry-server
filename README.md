# Backend for Covid-19 testing data manager

- Uses Python 3.6
- Flask
- Postgres 11+
- LMDB

Python libraries used for scientific computation:
- numpy
- scipy
- pandas
- scikit-learn
- pylops
- joblib

```sh
# Clone
git clone https://github.com/rrampage/covid-test-py.git ~/covid
cd covid
mkdir workdir
# Create virtual environment:
python3 -m venv env
# activate
source env/bin/activate
# install requirements with pinned versions from requirements.txt
pip install -r requirements.txt
git submodule init
git submodule update
```


### setting up initially
```sh
pip install numpy scipy pandas scikit-learn pylops[advanced] joblib Flask psycopg2
pip freeze > requirements.txt
```

### Development
```sh
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

### Production
```sh
# gunicorn -w 2 app:app
# Integrated with systemd as a user service
# First time, run `systemctl --user enable covid.service` to enable the app to start when machine boots
systemctl --user start covid.service
# Auto deployed on git push using webhook
# See ~/deploy folder
# Using webhook example from https://github.com/adnanh/webhook/blob/master/docs/Hook-Examples.md
```
#### Instance provisioning steps
```sh
sudo apt update
sudo apt upgrade
sudo apt install build-essential python3-dev git curl libffi-dev python3-venv python3-certbot
# Install openresty and postgres 12
wget -O - https://openresty.org/package/pubkey.gpg | sudo apt-key add -
sudo add-apt-repository -y "deb http://openresty.org/package/ubuntu $(lsb_release -sc) main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt-get update
sudo apt install openresty postgresql-12 libpq-dev
# Getting SSL
sudo certbot certonly --webroot -w /home/ubuntu/webroot --preferred-challenges http -d c19.zyxw365.in
```


### Endpoints

```sh
APP_URL="https://c19.zyxw365.in/api"
# Request OTP
curl -XPOST -d '{"phone" : "MOBILE"}' -H "Content-Type: application/json" "$APP_URL/request_otp"
# Validate OTP
curl -XPOST -d '{"phone" : "MOBILE", "otp" : "OTP"}' -H "Content-Type: application/json" "$APP_URL/validate_otp"
# Upload test data
curl -XPOST -d '[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]' -H "Content-Type: application/json" -H 'X-Auth: TOKEN' -H 'X-Mob: MOBILE' "$APP_URL/test_data"
# Modify data for an existing test
curl -XPUT -d '{"test_id": "TEST_ID", "test_data" : [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02]}' -H "Content-Type: application/json" -H 'X-Auth: TOKEN' -H 'X-Mob: MOBILE' "$APP_URL/test_data"
```

### Requirements:

[doc](https://docs.google.com/document/d/1SlwcXj-hDZjgEOiGL999BB13Yn8m4bD6RN5SUEPQ2Vo/edit)


