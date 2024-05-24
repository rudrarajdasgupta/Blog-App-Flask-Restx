from flask_restx import Resource, fields, Namespace
from models import db, Comment
from flask import current_app
from authtoken import token_required

ns = Namespace('comments', description='Comment operations')

comment_model = ns.model('Comment', {
    'id': fields.Integer(readOnly=True, description='The comment unique identifier'),
    'content': fields.String(required=True, description='The comment content'),
    'user_id': fields.Integer(required=True, description='The user id who authored the comment'),
    'blogpost_id': fields.Integer(required=True, description='The blog post id the comment belongs to')
})

@ns.route('/')
class CommentList(Resource):
    @token_required
    @ns.marshal_list_with(comment_model)
    def get(self, current_user):
        current_app.logger.info('Fetching all comments')
        return Comment.query.all()

    @ns.expect(comment_model)
    @ns.marshal_with(comment_model, code=201)
    def post(self):
        data = ns.payload
        new_comment = Comment(content=data['content'], user_id=data['user_id'], blogpost_id=data['blogpost_id'])
        db.session.add(new_comment)
        db.session.commit()
        current_app.logger.info(f'Created new comment: {new_comment.content[:20]}')
        return new_comment, 201

@ns.route('/<int:id>')
class CommentResource(Resource):
    @token_required
    @ns.marshal_with(comment_model)
    def get(self, current_user, id):
        comment = Comment.query.get_or_404(id)
        current_app.logger.info(f'Fetching comment: {comment.content[:20]}')
        return comment

    @token_required
    @ns.expect(comment_model)
    @ns.marshal_with(comment_model)
    def put(self, current_user, id):
        comment = Comment.query.get_or_404(id)
        data = ns.payload
        comment.content = data['content']
        comment.user_id = data['user_id']
        comment.blogpost_id = data['blogpost_id']
        db.session.commit()
        current_app.logger.info(f'Updated comment: {comment.content[:20]}')
        return comment

    @token_required
    def delete(self, current_user, id):
        comment = Comment.query.get_or_404(id)
        current_app.logger.info(f'Deleting comment: {comment.content[:20]}')
        db.session.delete(comment)
        db.session.commit()
        return '', 204
