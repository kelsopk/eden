from portal import db

from peewee import Model, DateTimeField, FloatField



class Balance(db.Model):
    when = DateTimeField()
    value = FloatField()
