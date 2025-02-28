from django.db import models
from mongoengine import Document, IntField, FloatField, fields
# Create your models here.
class Post(Document): # class name startwith in uppercase
    name = fields.StringField(max_length=50, required = True)
    add = fields.StringField(max_length=150, required = True)




    
    