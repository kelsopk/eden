from flask import Flask
from flask_peewee.db import Database
from flask_peewee.admin import Admin

 
app = Flask(__name__)
app.config.from_object('settings')

db = Database(app)


import views
import models


admin = Admin(app, None)
admin.register(models.Balance)
admin.setup()