from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField,
    ListField, ReferenceField, StringField,
    ObjectIdField, IntField, BooleanField, FloatField
)

class User(Document):
    meta = {'collection': 'user'}
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    date_joined = StringField(required=True)
    verified = BooleanField(required=True)
    allergic_to = StringField(required=False)

class AccessTokens(Document):
    meta = {'collection': 'accesstokens'}
    user_id = StringField(required=True)
    active = BooleanField(required=True)
    signin_date = StringField(required=True)

class Product(Document):
    meta = {'collection': 'product'}
    name = StringField(required=True)
    description = StringField(required=True)
    image = StringField(required=True)
    price = FloatField(required=True)
    target_skin_types = StringField(required=True)
    target_skin_disorders = StringField(required=True)
    allergens = StringField(required=False)