# Employees
Employees Application that can employees send leave requests to manager and manager can accept or reject 

### for install project 
#### venv install :
```
$ sudo pip install virtualenv 
$ virtualenv -p /usr/bin/python3.8 venv # path to python interprater python3.
$ source venv/bin/activate
$ pip install -r requirements.txt
```
#### Project Run:
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py add_countries # for fill country tabel from country.json 
$ python manage.py createsuperuser # create superuser to use in project
$ python manage.py runserver
```
