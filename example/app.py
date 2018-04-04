import os

from flask import Flask, request

from example.documents import User, Test
from flask_umongorest import UMongoRest
from flask_umongorest.resources import Resource
from flask_umongorest.views import ResourceView
import flask_umongorest.operators as ops
from flask_umongorest.methods import *

app = Flask(__name__)

app.url_map.strict_slashes = False

app.config.update(
    DEBUG = True,
    TESTING = True)

api = UMongoRest(app)

class UserResource(Resource):
    document = User
    allowed_ordering = ['firstname']
    filters = {
        'firstname': [ops.Exact,ops.Ne],
        'lastname': [ops.Exact,ops.Ne],
        'nick': [ops.Exact,ops.Ne]
    }

@api.register()
class UserView(ResourceView):
    resource = UserResource
    methods = [Create, Update, Fetch, List, Delete]


class TestResource(Resource):
    document = Test
    allowed_ordering = ['father']
    related_resources = {'father': User}
    related_resources_hints = {'father': User}
    filters = {
        'father': [ops.Exact,ops.Ne]
    }

@api.register()
class TestView(ResourceView):
    resource = TestResource
    methods = [Create, Update, Fetch, List, Delete]


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

