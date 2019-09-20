from django.db import models
import re
import bcrypt
from datetime import date, datetime

# Create your models here.

class User_Validate (models.Manager):
# REGISTRATION
    def validate_reg_name(self, error, post):
        if len(post['reg_first_name']) < 2:
            error['reg_first_name'] = 'First name must have at least 2 characters'
        if len(post['reg_last_name']) < 2:
            error['reg_last_name'] = 'Last name must have at least 2 characters'
    
    def validate_birthday(self, error, post):
        birthday_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if not birthday_regex.match(post['reg_birthday']):
            error['invalid_birthdate'] = 'Please enter a valid birthdate'
        if 'invalid_birthdate' not in error:
            given = datetime.strptime(post['reg_birthday'], '%Y-%m-%d')
            today = datetime.today()
            if given > today:
                error['future_birthday'] = 'Birthday must be a date in the past'

            def calculate_age(born):
                today = date.today()
                return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

            if calculate_age(given) < 13:
                error['too_young'] = 'You must be at least 13 years old to register'

    def validate_reg_email(self, error, post):
        regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not regex.match(post['reg_email']):
            error['reg_email'] = 'Invalid email'
        if User.objects.filter(email = post['reg_email']):
            error['reg_ed_email'] = 'This email is associated with another account'
    
    def validate_registration_password(self, error, post):
        if post['reg_password'] != post['reg_password_confirm']:
            error['reg_password_confirm'] = 'Password and confirm password must match'
        if 'reg_password_confirm' not in error:
            if len(post['reg_password']) < 8:
                error['invalid_password_length'] = 'Password must have at least 8 characters'
# LOGIN
    def validate_login(self, error, post):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post['login_email']):
            error['login_email'] = 'Please enter a valid email'
        if 'login_email' not in error:
            filtered_users = User.objects.filter(email = post['login_email'].lower())
            if not filtered_users or not bcrypt.checkpw(post['login_password'].encode(), filtered_users[0].password.encode()):
                error['login_error'] = 'Email or password is not recognized'


class User(models.Model):
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = User_Validate()
    # trips_created
    # trips_attending



class Trip_Validate(models.Manager):
    def validate_destination_plan(self, error, post):
        if len(post['new_destination']) < 3:
            error['new_destination'] = 'Destination must have at least 2 characters'
        if len(post['new_plan']) < 3:
            error['new_plan'] = 'Plan must have at least 2 characters'

    def validate_date_type(self, error, post):
        regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if not regex.match(post['new_start_date']):
            error['new_start_date'] = 'Please enter a valid start date'
        if not regex.match(post['new_end_date']):
            error['new_end_date'] = 'Please enter a valid end date'
    
    def validate_time_travel(self, error, post):
        if 'new_start_date' not in error and 'new_end_date' not in error:
            start = datetime.strptime(post['new_start_date'], '%Y-%m-%d')
            end = datetime.strptime(post['new_end_date'], '%Y-%m-%d')
            today = datetime.today()
            if today > start:
                error['past_trip'] = 'Start date must be in the future'
            if start > end:
                error['time_travel'] = 'Time travel not allowed. End date must be after start date'


class Trip (models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    plan = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='trips_created')
    attendees = models.ManyToManyField(User, related_name='trips_attending')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = Trip_Validate()