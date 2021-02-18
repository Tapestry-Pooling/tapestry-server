* Install Postgres from [here](https://www.postgresql.org/download/linux/ubuntu/) [[This](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) site might be helpful]

* Ensure the username is postgres and password is postgres(if you want to use any other password be sure to update it in the pooling/settings/dev.py later)
* Now, create a folder /home/username/workspace/

```
git clone https://github.com/Tapestry-Pooling/tapestry-server #(only first time)

sudo apt install postgresql #(set username postgres)(only first time)

psql -U postgres -h localhost 
```

* Update the password to postgres by typing `\password` in the psql shell and entering the new password(postgres) twice

* Activating virtual environment
```
virtualenv env #(only first time)
source env/bin/activate

pip install -r requirements.txt #(only first time)
```  


* Copy the secrets file to /home/username/workspace/secrets/
* Add the following lines to the end of the file `~/.bashrc`
```
export GOOGLE_APPLICATION_CREDENTIALS= "/home/username/workspace/secrets/secret.json"
export KIRKMAN_MATRIX_BUCKET="kirkman_matrices"
```
* Enter the following command to apply the changes permanently

```
source ~/.bashrc
```

* Now migrate the data and start the django server
```
python3 manage.py migrate
python3 manage.py createsuperuser (only first time)
python manage.py loaddata fixtures/initial_data_user_labs.json (only first time)
python3 manage.py runserver
```

<!-- ssh-keygen - to generate ssh key - dont enter any info in prompt just press enter for all i.e. empty values

cat /home/.ssh/id_rsa.pub
cat /home/tanmay/.ssh/id_rsa.pub


https://github.com/settings/keys -->
