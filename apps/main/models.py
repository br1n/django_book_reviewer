# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def validate_and_create_user(self, form):
        errors = []

        #name validation
        if form['name'] == "": 
            errors.append('Name field cannot be blank')
        elif len(form['name']) < 3:
            errors.append('Name field must be at least 3 characters long')
        
        #username validation
        if form['username'] == "":
            errors.append( 'Username field cannot be blank')
        elif len(form['username']) < 3:
            errors.append( 'Username field must be at least 3 characters long')

        #email validation
        if form['email'] == "": 
            errors.append('Email required')
        elif not EMAIL_REGEX.match(form['email']): #validate for email uniqueness
            errors.append('Email must be valid')
        elif len(form['email']) < 4: #validate for length
            errors.append('Email must valid')

        #password validation
        if form['password'] == "": 
            errors.append('Password required')
        elif len(form['password']) < 8: #validate for length
            errors.append('Password must be at least 8 characters long')
        elif form['password'] != form['confirm']:
            errors.append('Password and confirm password must match')


        #Ex.checking for pre-existing Username
        username_list = self.filter(username=form['username'])
        if len(username_list) > 0:
            errors.append('Username already in use')

        #checking db for pre-existing email
        try:
            email_list = self.get(email=form['email'])
            errors.append('Email already in use')
            return (False, errors)
        except:
            if len(errors) > 0:
                return (False, errors)
            else: #create new user
                pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
                user = self.create(name=form['name'], username=form['username'], email=form['email'], pw_hash=pw_hash)
                return (True, user)

    def validate_login(self, form):
        errors = []

        try:
            user = self.get(email=form['email'])
            #log user in
            if bcrypt.checkpw(form['password'].encode(), user.pw_hash.encode()):
                return (True, user)
            else: #check if password matches
                errors.append('Incorrect email or password')
                return (False, errors)
        except: #email doesn't exist
            errors.append('Incorrect email or password')
            return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        output = "<User object:{}{}>".format(self.name, self.email)
        return output

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Review(models.Model):
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)