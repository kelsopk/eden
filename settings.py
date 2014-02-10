# Database config file

# Feel free to use another backend, you can choose from SqliteDatabase, MySQLDatabase and PostgresqlDatabase
# To use backends other than sqlite please fill user, passwd, host and port fields with proper values :)
# More info (not so many ;) ) at  http://flask-peewee.readthedocs.org/en/latest/database.html  
 

DATABASE  = {
    'name': 'eden.db', 
    'engine': 'peewee.SqliteDatabase',
    'threadlocals': True
    
    #'user': 'db_user',        
    #'passwdord': 'secret password',
    #'host': '',
    #'port': '',    
}

