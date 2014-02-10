from portal import db

from peewee import Model, DateTimeField, FloatField


class Balance(Model):
    when = DateTimeField()
    value = FloatField()
    
    class Meta:
        database = db