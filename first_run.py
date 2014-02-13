# -*- coding: utf-8 -*-
from portal import models
from portal import db
from peewee import IntegrityError, OperationalError

import getpass
import inspect
import sys


def sync():
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and issubclass(obj, db.Model):
            try:
                obj.create_table()
            except OperationalError:
                print "so unexpected: Error while creating table for %s: %s" % (obj, sys.exc_info()[1])
            else:
                print "wow: Table for %s was created" % obj

def add_user():
    
    username, password = False, False
    
    while not username:
        username = raw_input("Please enter your username: ")
     
    while not password:
        password = getpass.getpass("Please your password: ")
         
    try:
        user = models.User(username=username)
        user.set_password(password)
        user.save()
    except IntegrityError:
        print "so unexpected: User with username %s already exist in database" % username
    else:
        print "wow: User was succesfully created"

def set_card():
    try:
        item = models.Setting.get(models.Setting.name=='card_number')
        print "Current card_number %s" % item.value 
    except models.Setting.DoesNotExist:
        item = models.Setting(name='card_number')
    
       
    card_number, integer = False, False
    
    while not (card_number and len(str(card_number)) == 10 and integer):
        try:
            card_number = int(raw_input("Please input your CARD NUMBER (10 digits): "))
        except ValueError:
            integer = False
        else:
            integer = True
        
    item.value = card_number
    item.save()

        
    
def first():
    sync()
    add_user()
    set_card()


CMDS = {
        'first': ('Initial execution', first),
        'syncdb': ('Create tables in database based on models', sync),
        'useradd': ('Add new user', add_user),
        'set_card': ('Create settings containing EDENRED card details', set_card),
        }


def show_commands():
    for key, value in CMDS.items():
        print '%s   \t %s' % (key, value[0])


if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_commands()
    elif len(sys.argv) > 2:
        print "such limited: Not so fast dude! - I`m able to do one thing at the time."
    else:
        try:
            CMDS[sys.argv[1]][1]()
        except KeyError:
            print "so unfamiliar: Command not found!"

        

