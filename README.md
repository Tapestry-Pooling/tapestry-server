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
gunicorn -w 2 app:app
# TODO : integrate with systemd
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
APP_URL="https://c19.zyxw365.in"
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

(Old)

```
- We'll have some standard test sizes - such as testing 40 people using 16 tests, 60 people using 24 tests, 400 people using 64 tests, 1000 people using 96 tests. The test matrices will be known to the user - they'll likely be printed out beforehand. I am assuming there'll be only one matrix for each test x people size, else there'll be much confusion. After the technician performs the tests, they'll want to enter test results. This is a vector of size equal to number of tests, so 16, 24, 64 tests for now. Maybe also 96. How to enter it in a user-friendly manner is something you guys may have to solve.

- Upon opening the app, the user should be able to see past tests done by him sorted by most recent, along with a very prominent new test button. He should be able to choose test size (16x40, 24x60, 64x400, 96x1000). The new test will enable him to enter data.

- Upon submitting, the test data will be logged on server. Python backend will compute results and send back which people are infected. In fact, the result may have four categories - surely infected,  possibly infected, possibly not infected, surely not infected. For example 11, 15 and 37 are surely infected, 2 is possibly infected, 9 and 24 are possibly not infected. We can color code these by Red, Orange and Yellow. The result should also be logged on the server database.

- We should allow the user to view and correct the entered data. Every time he hits submit, the submitted data will be logged on the server. The old submission will also remain on the server database, but the user should be able to see only the last submission.

- Each new test should create a notification to people like Manoj and I who'll closely monitor all test results and ensure everything is correct. In time, there might be a dashboard to view test results by various filters/categories - the primary one being which lab the test is being done in (which may be indicated by the device id for now). There may need to be a device id and lab association, which we can think of later.

- one-time login. For now just use device id. Particular user should be able to see only his tests.
```

