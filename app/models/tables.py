from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

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


    def __init__(self, email, name, user_name, password):
        self.email = email
        self.name = name
        self.user_name = user_name
        self.password = generate_password_hash(password) #transformando a senha num hast

    def verify_password(self, password):
        return check_password_hash(self.password, password) # verificando a senha pelo hast

    def __repr__(self):
        return '<UUser: %r>' %self.user_name

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_name', 'email', 'name', 'image', 'site', 'bio')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)


class Publication(db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.BLOB, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)

    def __repr__(self):
        return '<PPublication: %r>' %self.id

class Publication_Like(db.Model):
    __tablename__ = "publication_likes"

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)
    publication = db.relationship('Publication', foreign_keys = publication_id)
    

    def __repr__(self):
        return '<PPublication_Like: %r>' %self.id


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)
    publication = db.relationship('Publication', foreign_keys = publication_id)

class Comment_Like(db.Model):
    __tablename__ = "comment_likes"

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)
    comment = db.relationship('Comment', foreign_keys = comment_id)

class Comment_on_comment(db.Model):
    __tablename__ = "comments_on_comment"

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)
    comment = db.relationship('Comment', foreign_keys = comment_id)

class Comment_on_comment_Like(db.Model):
    __tablename__ = "comment_on_comment_likes"

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_on_comment_id = db.Column(db.Integer, db.ForeignKey('comments_on_comment.id'), nullable=False)
    
    owner = db.relationship('User', foreign_keys = owner_id)
    comment_on_comment = db.relationship('Comment_on_comment', foreign_keys = comment_on_comment_id)

class Follow(db.Model):
    __tablename__ = "follow"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', foreign_keys = user_id)
    follower = db.relationship('User', foreign_keys = follower_id)

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user1 = db.relationship('User', foreign_keys = user1_id)
    user2 = db.relationship('User', foreign_keys = user2_id)
    

class Story(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.BLOB, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', foreign_keys = owner_id)