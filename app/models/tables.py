from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.BLOB)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, unique = True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    site = db.Column(db.String)
    bio = db.Column(db.Text)

    token_iat = db.Column(db.String)
    followers_number = db.Column(db.Integer)
    following_number = db.Column(db.Integer)

    def __init__(self, email, name, user_name, password, image):
        self.image = image
        self.email = email
        self.name = name
        self.user_name = user_name
        self.password = generate_password_hash(password) #transformando a senha num hast
        self.followers_number = 0
        self.following_number = 0
    
    def add_follower(self):
        self.followers_number = self.followers_number + 1
    def remove_follower(self):
        self.followers_number = self.followers_number - 1
    def add_following(self):
        self.following_number = self.following_number + 1
    def remove_following(self):
        self.following_number = self.following_number - 1

    def verify_password(self, password):
        return check_password_hash(self.password, password) # verificando a senha pelo hast

    def __repr__(self):
        return '<User: %r>' %self.user_name

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_name', 'email', 'name', 'image', 'site', 'bio', 'followers_number',  'following_number')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)





class Publication(db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.BLOB, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likes = db.Column(db.Integer)

    owner = db.relationship('User', foreign_keys = owner_id)

    
    def __init__(self, description, owner_id, image):
        self.image = image
        self.description = description
        self.owner_id = owner_id
        self.date = datetime.datetime.utcnow()
        self.likes = 0

    def like(self):
        self.likes = self.likes + 1
    def unlike(self):
        self.likes = self.likes - 1

    def __repr__(self):
        return '<PPublication: %r>' %self.id

class PublicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'image', 'description', 'date', 'owner_id', 'likes')

publication_share_schema = PublicationSchema()
feed_share_schema = PublicationSchema(many=True)





class Publication_Like(db.Model):
    __tablename__ = "publication_likes"

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)
    publication = db.relationship('Publication', foreign_keys = publication_id)
    
    def __init__(self, owner_id, publication_id):
        self.owner_id = owner_id
        self.publication_id = publication_id

    def __repr__(self):
        return '<PPublication_Like: %r>' %self.id

class PublicationLikeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'owner_id', 'publication_id')

Publication_Likes_share_schema = PublicationLikeSchema(many=True)





class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'), nullable=False)
    likes = db.Column(db.Integer)

    owner = db.relationship('User', foreign_keys = owner_id)
    publication = db.relationship('Publication', foreign_keys = publication_id)
    

    def __init__(self, content, owner_id, publication_id):
        self.content = content
        self.date = datetime.datetime.utcnow()
        self.owner_id = owner_id
        self.publication_id = publication_id
        self.likes = 0

    def like(self):
        self.likes = self.likes + 1
    def unlike(self):
        self.likes = self.likes - 1

class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'date', 'owner_id', 'publication_id', 'likes')

Comments_share_schema = CommentSchema(many=True)





class Comment_Like(db.Model):
    __tablename__ = "comment_likes"

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)
    comment = db.relationship('Comment', foreign_keys = comment_id)

    def __init__ (self, owner_id, comment_id):
        self.owner_id = owner_id
        self.comment_id = comment_id

class CommentLikeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'owner_id', 'comment_id')

Comment_Like_share_schema = CommentLikeSchema(many=True)





class Comment_on_comment(db.Model):
    __tablename__ = "comments_on_comment"

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    likes = db.Column(db.Integer)

    owner = db.relationship('User', foreign_keys = owner_id)
    comment = db.relationship('Comment', foreign_keys = comment_id)

    def __init__ (self, content, owner_id, comment_id):
        self.date = datetime.datetime.utcnow()
        self.content = content
        self.owner_id = owner_id
        self.comment_id = comment_id
        self.likes = 0
    
    def like(self):
        self.likes = self.likes + 1
    def unlike(self):
        self.likes = self.likes - 1

class CommentOnCommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'date', 'owner_id', 'comment_id', 'likes')

Comment_on_comment_share_schema = CommentOnCommentSchema(many=True)





class Comment_on_comment_Like(db.Model):
    __tablename__ = "comment_on_comment_likes"

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_on_comment_id = db.Column(db.Integer, db.ForeignKey('comments_on_comment.id'), nullable=False)
    
    owner = db.relationship('User', foreign_keys = owner_id)
    comment_on_comment = db.relationship('Comment_on_comment', foreign_keys = comment_on_comment_id)

    def __init__ (self, owner_id, comment_on_comment_id):
        self.owner_id = owner_id
        self.comment_on_comment_id = comment_on_comment_id

class CommentOnCommentLikeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'owner_id', 'comment_on_comment_id')

Comment_on_comment_Like_share_schema = CommentOnCommentLikeSchema(many=True)





class Follow(db.Model):
    __tablename__ = "follow"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', foreign_keys = user_id)
    follower = db.relationship('User', foreign_keys = follower_id)

    def __init__ (self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id

class FollowSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'follower_id')

Follow_share_schema = FollowSchema()
Follows_share_schema = FollowSchema(many=True)





class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False)
    self_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    content = db.Column(db.Text, nullable=False)

    me = db.relationship('User', foreign_keys = self_id)
    recipient = db.relationship('User', foreign_keys = recipient_id)

    def __init__ (self, self_id, recipient_id, content):
        self.date = datetime.datetime.utcnow()
        self.self_id = self_id
        self.recipient_id = recipient_id
        self.content = content

class ConversationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'self_id', 'recipient_id', 'content')

message_share_schema = ConversationSchema()
direct_share_schema = ConversationSchema(many=True)
    




class Story(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.BLOB)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)

    def __init__(self, image, owner_id):
        self.image = image
        self.date = datetime.datetime.utcnow()
        self.owner_id = owner_id

class StorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'image', 'date', 'owner_id')

Story_share_schema = StorySchema(many=True)
