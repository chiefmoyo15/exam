from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime


# Create your models here.

# Our new manager!
# No methods in our new manager should ever catch the whole request object
# with a parameter!!! (just parts, like request.POST)
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):

    def login(self, postData):
        modelResponse = {}
        # check to see if user is in DB
        user = self.filter(email=postData['email'])
        # if user exists
        if user:
            # check for matching passwords
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                # send success to views
                modelResponse['status'] = True
                modelResponse['userid'] = user[0].id
                modelResponse['name'] = user[0].first_name
                modelResponse['email'] = postData['email']
            else:
                # send error message to views
                modelResponse['status'] = False
                modelResponse['error'] = 'Invalid email/password '
        else:
            # send message to views
            modelResponse['status'] = False
            modelResponse['error'] = 'Invalid email'

        return modelResponse

    def register(self, fname, lname, email, password, password2, dateHired):
        errors = []
        NAME_REGEX = re.compile(r'^[a-zA-Z]')
        if len(fname) < 3:
            errors.append('First name is too short!')
        if len(lname) < 3:
            errors.append('Last name is too short!')
            # first and last name letters only
        if not fname == '' and fname == '':
            if not NAME_REGEX.match(fname):
                errors.append('First name must be letters only')
            if not NAME_REGEX.match(request.POST['last_name']):
                errors.append('last name must be letters only')
        # email
        if self.filter(email=email):
            errors.append('-email- already exists')

        if not EMAIL_REGEX.match(email):
            errors.append('Invalid email')

        # password
        if len(password) >= 8 and password == password2:
            password = password.encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt())
        else:
            errors.append('Invalid password')

        if datetime.strptime(dateHired, "%Y-%m-%d") > datetime.now():
            errors.append('Invalid date, has to be before today')

        if errors:
            modelResponse = {
                'status': False,
                'errors': errors
            }
            return modelResponse

        self.create(
            first_name=fname, last_name=lname, email=email, password=password, isLoggedin=True, dateHired=dateHired
        )

        modelResponse = {
            'status': True,
            'userid': self.filter(email=email)[0].id,
            'name': fname
        }

        return modelResponse


class User(models.Model):

    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=50)
    isLoggedin = models.BooleanField(default=False)
    dateHired = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userManager = UserManager()
