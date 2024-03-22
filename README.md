# Employees
Employees Application that can employees send leave requests to manager and manager can accept or reject 

### for install project 
#### venv install :
```commandline
$ sudo pip install virtualenv 
$ virtualenv -p /usr/bin/python3.8 venv # path to python interprater python3.
$ source venv/bin/activate
$ pip install -r requirements.txt
```
#### Project Run:
```commandline
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py add_countries # for fill country tabel from country.json 
$ python manage.py createsuperuser # create superuser to use in project
$ python manage.py runserver
```

```commandline
# SuperUser
username: admin
email:admin@admin.com
password: admin

# Employee
username: employee
email:employee@employee.com
password: aw123456

# Manager
username: manager
email:manager@manager.com
password: aw123456
```# ExpenseApplication
