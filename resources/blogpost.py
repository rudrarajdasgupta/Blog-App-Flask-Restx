from flask_restx import Resource, fields, Namespace
from models import db, BlogPost
from flask import current_app
from authtoken import token_required

ns = Namespace('blogposts', description='Blog post operations')

blogpost_model = ns.model('BlogPost', {
    'id': fields.Integer(readOnly=True, description='The blog post unique identifier'),
    'title': fields.String(required=True, description='The blog post title'),
    'content': fields.String(required=True, description='The blog post content'),
    'user_id': fields.Integer(required=True, description='The user id who authored the blog post')
})

@ns.route('/')
class BlogPostList(Resource):
    @token_required
    @ns.marshal_list_with(blogpost_model)
    def get(self, current_user):
        current_app.logger.info('Fetching all blog posts')
        return BlogPost.query.all()

    @ns.expect(blogpost_model)
    @ns.marshal_with(blogpost_model, code=201)
    def post(self):
        data = ns.payload
        new_blogpost = BlogPost(title=data['title'], content=data['content'], user_id=data['user_id'])
        db.session.add(new_blogpost)
        db.session.commit()
        current_app.logger.info(f'Created new blog post: {new_blogpost.title}')
        return new_blogpost, 201

@ns.route('/<int:id>')
class BlogPostResource(Resource):
    @token_required
    @ns.marshal_with(blogpost_model)
    def get(self, current_user, id):
        blogpost = BlogPost.query.get_or_404(id)
        current_app.logger.info(f'Fetching blog post: {blogpost.title}')
        return blogpost

    @token_required
    @ns.expect(blogpost_model)
    @ns.marshal_with(blogpost_model)
    def put(self, current_user, id):
        blogpost = BlogPost.query.get_or_404(id)
        data = ns.payload
        blogpost.title = data['title']
        blogpost.content = data['content']
        blogpost.user_id = data['user_id']
        db.session.commit()
        current_app.logger.info(f'Updated blog post: {blogpost.title}')
        return blogpost

    @token_required
    def delete(self, current_user, id):
        blogpost = BlogPost.query.get_or_404(id)
        current_app.logger.info(f'Deleting blog post: {blogpost.title}')
        db.session.delete(blogpost)
        db.session.commit()
        return '', 204
