We'll have some standard test sizes - such as testing 40 people using 16 tests, 60 people using 24 tests, 400 people using 64 tests, 1000 people using 96 tests. The test matrices will be known to the user - they'll likely be printed out beforehand. I am assuming there'll be only one matrix for each test x people size, else there'll be much confusion. After the technician performs the tests, they'll want to enter test results. This is a vector of size equal to number of tests, so 16, 24, 64 tests for now. Maybe also 96. How to enter it in a user-friendly manner is something you guys may have to solve. 

Upon opening the app, the user should be able to see past tests done by him sorted by most recent, along with a very prominent new test button. He should be able to choose test size (16x40, 24x60, 64x400, 96x1000). The new test will enable him to enter data. 

Upon submitting, the test data will be logged on server. Python backend will compute results and send back which people are infected. In fact, the result may have four categories - surely infected,  possibly infected, possibly not infected, surely not infected. For example 11, 15 and 37 are surely infected, 2 is possibly infected, 9 and 24 are possibly not infected. We can color code these by Red, Orange and Yellow. The result should also be logged on the server database. 

We should allow the user to view and correct the entered data. Every time he hits submit, the submitted data will be logged on the server. The old submission will also remain on the server database, but the user should be able to see only the last submission. 

Each new test should create a notification to people like Manoj and I who'll closely monitor all test results and ensure everything is correct. In time, there might be a dashboard to view test results by various filters/categories - the primary one being which lab the test is being done in (which may be indicated by the device id for now). There may need to be a device id and lab association, which we can think of later.  

I am not sure, but perhaps there should be some form of one-time login as well because of sensitivity of data. For now just use device id. Particular user should be able to see only his tests.

I think there is enough to make the first version of the app. Maybe we could field test the app as well in a few days..

```sh
# Create virtual environment:
python3 -m venv env
# activate
source env/bin/activate
# install requirements with pinned versions from requirements.txt
pip install -r requirements.txt
```

Python libraries used:
numpy
scipy
pandas
scikit-learn
pylops
joblib
Flask

### setting up initially
```sh
pip install numpy scipy pandas scikit-learn pylops[advanced] joblib Flask
pip freeze > requirements.txt
```

### Development
```sh
export FLASK_APP=.
export FLASK_ENV=development
flask run
```

Requirements:

1. users -> People who will upload test matrices
2. tests -> matrices with number of tests and number of users (fixed size)
    40 x 16
    60 x 24
    400 x 64
    1000 x 96

