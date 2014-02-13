from portal import db

from flask_peewee.auth import BaseUser
from peewee import DateTimeField, FloatField, CharField


class Balance(db.Model):
    when = DateTimeField()
    value = FloatField()

class Setting(db.Model):
    name = CharField()
    value = CharField()
    
class User(db.Model, BaseUser):
    username = CharField(unique=True)
    password = CharField()    

    def __unicode__(self):
        return self.username
    
    @property
    def admin(self):
        return True
    
    @property
    def active(self):
        return True