from pymongo import MongoClient
from umongo import Instance, Document, fields

db = MongoClient().demo_umongo
instance = Instance(db)

@instance.register
class User(Document):
    nick = fields.StrField(required=True)
    firstname = fields.StrField()
    lastname = fields.StrField()
    birthday = fields.DateTimeField()
    listfield = fields.ListField(fields.StringField)
    password = fields.StrField()  # Don't store it in clear in real life !

    class Meta:
        collection = db.demo_user

@instance.register
class Test(Document):
    name = fields.StringField()
    father = fields.ListField(fields.ReferenceField(User))

    class Meta:
        collection = db.demo_test
