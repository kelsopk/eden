from portal import db

from flask_peewee.auth import BaseUser
from peewee import DateTimeField, FloatField, CharField


class Balance(db.Model):
    when = DateTimeField()
    balance = FloatField()
    value = FloatField()
    comment = CharField(null=True)
    
    def get_balance(self):
        return self.__class__.select().order_by(self.__class__.id.desc()).get().balance

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