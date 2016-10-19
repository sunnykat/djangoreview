from __future__ import unicode_literals
from django.contrib import messages
import re
import bcrypt
from django.db import models

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(models.Model):
     fname=models.CharField(max_length=15)
     lname=models.CharField(max_length=15)
     email=models.CharField(max_length=40)
     pass_hash=models.CharField(max_length=255)
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)

class UserManager(models.Manager):
    def validEmail(self,postData):
        if len(postData) <1:
            return False
        if not EMAIL_REGEX.match(postData):
            return False
        return True
    def existingEmail(self, postData):
        if User.objects.filter(email=postData):
            return False
        else:
            return True
    def passCheck(self, postEmail, postPass):
        user=User.objects.get(email=postEmail)
        passhash=user.pass_hash
        if bcrypt.checkpw(postPass, passhash):
            return True

    def lengthCheck(self, postfname, postlname,postemail,postpass1):
        if len(postfname) < 1:
            return False
        if len(postlname) < 1:
            return False
        if len(postpass1) < 1:
            return False
        if len(postemail) < 1:
            return False
        return True
    def addUser(self, postfname, postlname, postemail,postpass):
        newhash=bcrypt.hashpw(postpass, bcrypt.gensalt())
        User.objects.create(fname=postfname,lname=postlname,email=postemail,pass_hash=newhash)
        return True

userManager=UserManager()
