from flask_restx import Resource, Namespace, fields
from flask import request, jsonify, current_app
from models import db, User

ns = Namespace('auth', description='Authentication operations')

login_model = ns.model('Login', {
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})

@ns.route('/register')
class Register(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user is None or not user.check_password(data['password']):
            return {'message': 'Invalid credentials'}, 401
        token = user.generate_jwt()
        return {'token': token}