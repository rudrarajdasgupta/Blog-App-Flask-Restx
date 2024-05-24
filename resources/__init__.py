from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp, doc='/doc', title='Blogging API', version='1.0', description='A simple blogging API')

from .user import ns as user_ns
from .blogpost import ns as blogpost_ns
from .comment import ns as comment_ns
from .reply import ns as reply_ns
from .auth import ns as auth_ns

api.add_namespace(user_ns)
api.add_namespace(blogpost_ns)
api.add_namespace(comment_ns)
api.add_namespace(reply_ns)
api.add_namespace(auth_ns)