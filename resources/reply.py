from flask_restx import Resource, fields, Namespace
from models import db, Reply
from flask import current_app
from authtoken import token_required

ns = Namespace('replies', description='Reply operations')

reply_model = ns.model('Reply', {
    'id': fields.Integer(readOnly=True, description='The reply unique identifier'),
    'content': fields.String(required=True, description='The reply content'),
    'user_id': fields.Integer(required=True, description='The user id who authored the reply'),
    'comment_id': fields.Integer(required=True, description='The comment id the reply belongs to')
})

@ns.route('/')
class ReplyList(Resource):
    @token_required
    @ns.marshal_list_with(reply_model)
    def get(self, current_user):
        current_app.logger.info('Fetching all replies')
        return Reply.query.all()

    @ns.expect(reply_model)
    @ns.marshal_with(reply_model, code=201)
    def post(self):
        data = ns.payload
        new_reply = Reply(content=data['content'], user_id=data['user_id'], comment_id=data['comment_id'])
        db.session.add(new_reply)
        db.session.commit()
        current_app.logger.info(f'Created new reply: {new_reply.content[:20]}')
        return new_reply, 201

@ns.route('/<int:id>')
class ReplyResource(Resource):
    @token_required
    @ns.marshal_with(reply_model)
    def get(self, current_user, id):
        reply = Reply.query.get_or_404(id)
        current_app.logger.info(f'Fetching reply: {reply.content[:20]}')
        return reply

    @token_required
    @ns.expect(reply_model)
    @ns.marshal_with(reply_model)
    def put(self, current_user, id):
        reply = Reply.query.get_or_404(id)
        data = ns.payload
        reply.content = data['content']
        reply.user_id = data['user_id']
        reply.comment_id = data['comment_id']
        db.session.commit()
        current_app.logger.info(f'Updated reply: {reply.content[:20]}')
        return reply

    @token_required
    def delete(self, current_user, id):
        reply = Reply.query.get_or_404(id)
        current_app.logger.info(f'Deleting reply: {reply.content[:20]}')
        db.session.delete(reply)
        db.session.commit()
        return '', 204