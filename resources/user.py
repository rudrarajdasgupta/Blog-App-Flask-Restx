from flask_restx import Resource, fields, Namespace
from models import db, User
from flask import current_app
from authtoken import token_required

ns = Namespace('users', description='User operations')

user_model = ns.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email')
})

@ns.route('/')
class UserList(Resource):
    @token_required
    @ns.marshal_list_with(user_model)
    def get(self, current_user):
        current_app.logger.info('Fetching all users')
        return User.query.all()

    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        data = ns.payload
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f'Created new user: {new_user.username}')
        return new_user, 201

@ns.route('/<int:id>')
class UserResource(Resource):
    @token_required
    @ns.marshal_with(user_model)
    def get(self, current_user, id):
        user = User.query.get_or_404(id)
        current_app.logger.info(f'Fetching user: {user.username}')
        return user

    @token_required
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, current_user, id):
        user = User.query.get_or_404(id)
        data = ns.payload
        user.username = data['username']
        user.email = data['email']
        user.set_password(data['password'])  # Update password as well
        db.session.commit()
        current_app.logger.info(f'Updated user: {user.username}')
        return user

    @token_required
    def delete(self, current_user, id):
        user = User.query.get_or_404(id)
        current_app.logger.info(f'Deleting user: {user.username}')
        db.session.delete(user)
        db.session.commit()
        return '', 204