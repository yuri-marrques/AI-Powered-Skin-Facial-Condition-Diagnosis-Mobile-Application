from mongoengine import connect
from models import User, Product
from datetime import datetime
from encrypt import encrypt_password, check_encrypted_password

# connect('ai-based-digital-beauty-advisor-1', host='mongomock://localhost', alias='default') # temp mongo inside python, disposed when app is stopped
connect('ai-based-digital-beauty-advisor-1', host='localhost', port=27017, alias='default') # local mongo

def init_db():
    users = User.objects.all()