from flask import Flask
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask_peewee.rest import RestAPI, UserAuthentication, RestResource
from flask_peewee.auth import Auth

app = Flask(__name__)
app.config.from_object('settings')

db = Database(app)

import views
import models

auth = Auth(app, db, user_model=models.User)
auth.setup()

rest_auth = UserAuthentication(auth, protected_methods=['POST'])

class BalanceResource(RestResource):
    fields = ('value', 'when',)
    


api = RestAPI(app, default_auth=rest_auth)
api.register(models.Balance, BalanceResource, allowed_methods=['GET'])
api.setup()