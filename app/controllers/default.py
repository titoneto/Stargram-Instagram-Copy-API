from flask import request, jsonify
from app import app, db
from app.authenticate import jwt_required
from werkzeug.security import generate_password_hash

from app.models.tables import(
    User, user_share_schema, users_share_schema, 
    Publication
)
    


import jwt
import datetime

@app.route("/aqui/a")
@jwt_required
def home(current_user):
    return jsonify({"msg": "aqui", "current_user": current_user.id})

@app.route("/aqui")
@jwt_required
def aqui(**kwargs):
    return jsonify({"msg": "aqui"})



@app.route("/auth/register", methods =["POST"])
def signUp():
    body = request.get_json()
    user_name = body['user_name']
    name = body['name']
    email = body['email']
    password = body['password']
    #image = body['image']

    if User.query.filter_by(user_name = user_name).first():
        return jsonify({"error": "O Nome de usuário " + user_name + " não está disponível"})
    elif User.query.filter_by(email = email).first():
        return jsonify({"error": "O Email já foi cadastrado anteriormente"})
    else :
        user = User(email, name, user_name, password)
        db.session.add(user)
        db.session.commit()

        payload = {
        "sub" : user.id,
        "iat" : datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

        user.token_iat = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")['iat']
        db.session.add(user)
        db.session.commit()

        search_user = user_share_schema.dump(
            User.query.filter_by(user_name = user_name).first()
        )

        return jsonify({"token": token, "data" : search_user})


@app.route("/auth/login", methods =["POST"])
def login():
    body = request.get_json()
    user = User.query.filter_by(user_name = body['login_name']).first()
    if not user:
        user = User.query.filter_by(email = body['login_name']).first()
        if not user:
            return jsonify({"error": "nome de usuário ou email inválido"})
            
    if not user.verify_password(body['password']):
        return jsonify({"error": "senha inválida"})
    
    payload = {
        "sub" : user.id,
        "iat" : datetime.datetime.utcnow()
    }

    

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

    user.token_iat = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")['iat']

    db.session.add(user)
    db.session.commit()

    search_user = user_share_schema.dump(
        User.query.filter_by(user_name = user.user_name).first()
    )

    return jsonify({"token": token, "data" : search_user})

@app.route("/auth/logout")
@jwt_required
def logout(current_user):

    current_user.token_iat = None
    db.session.add(current_user)
    db.session.commit()

    return jsonify({"msg": "deslogado com sucesso"})

@app.route("/auth/refresh")
@jwt_required
def refresh(current_user):
    payload = {
        "sub" : current_user.id,
        "iat" : datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    current_user.token_iat = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")['iat']
    db.session.add(current_user)
    db.session.commit()

    search_user = user_share_schema.dump(
        current_user
    )

    return jsonify({"token": token, "data" : search_user})

@app.route("/auth/profileedit", methods = ["POST"])
@jwt_required
def profileedit(current_user):
    body = request.get_json()

    if 'image' in body:
        current_user.image = body['image']

    if 'name' in body:
        current_user.name = body['name']

    if 'user_name' in body:
        user_name = User.query.filter_by(user_name = body['user_name']).first()
        if user_name:
            return jsonify({"error" : " user_name já utilizado!"})
        
        current_user.user_name = body['user_name']
        
    if 'password' in body:
        current_user.password = generate_password_hash(body['password'])

    if 'site' in body:
        current_user.site = body['site']

    if 'bio' in body:
        current_user.bio = body['bio']

    db.session.add(current_user)
    db.session.commit()

    return jsonify({"msg" : "A Alteração foi bem sucesso"})
    


@app.route("/publications/new", methods =["POST"] )
@jwt_required
def newPublication(current_user):
    body = request.get_json()

    publication = Publication(body['description'], current_user.id)
    db.session.add(publication)
    db.session.commit()

    return jsonify({ "msg" : "Publicação realizada com sucesso" })

@app.route("/publications/edit", methods =["POST"])
@jwt_required
def editPublication(current_user):
    body = request.get_json()

    publication_to_edit = Publication.query.filter_by(id = body['publication_id']).first()
    description = body['description']

    publication_to_edit.description = description
    
    db.session.add(publication_to_edit)
    db.session.commit()

    return jsonify({ "msg" : "Publicação editada com sucesso" })
#////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route("/publications/delete")
def deletePublication():
    return
@app.route("/publication?<int:id>&token=<token>")
def getPublication(id,token):
    return
@app.route("/feed?<int:id>&token=<token>")
def getFeed(id,token):
    return





@app.route("/publications/comments?<int:publicationId>&token=<token>")
def getComments(publicatioId):
    return
@app.route("/publications/comments/new")
def newComment():
    return
@app.route("/publications/comments/delete") 
def deleteComment():
    return




@app.route("/publications/comments/onComment?<int:commentId>&token=<token>")
def getComments_on_Comment(commentId):
    return
@app.route("/publications/comments/onComment/new")
def newComment_on_Comment():
    return
@app.route("/publications/comments/onComment/delete")
def deleteComment_on_Comment():
    return



@app.route("/followers?<int:userId>&token=<token>")
def getFollowers(userId, token):
    return
@app.route("/following?<int:userId>&token=<token>")
def getFollowing(userId, token):
    return
@app.route("/follow")
def follow():
    return
@app.route("/unfollow")
def unfollow():
    return




@app.route("/refresh")
def getConversation():
    return




@app.route("/stories?<int:userId>&token=<token>")
def getStories(userId, token):
    return
@app.route("/story?<int:storyId>&token=<token>")
def getStory(storyId, token):
    return




@app.route("/publications/likes?<int:publicationId>&token=<token>")
def getPublication_likes(publicationId, token):
    return
@app.route("/publications/like")
def likePublication():
    return
@app.route("/publications/unlike")
def unlikePublication():
    return




@app.route("/publications/comments/likes?<int:commentId>&token=<token>")
def getComment_likes(commentId,token):
    return
@app.route("/publications/comments/like")
def likeComment():
    return
@app.route("/publications/comments/unlike")
def unlikeComment():
    return




@app.route("/publications/comments/onComment/likes?<int:commentOnCommentId>&token=<token>")
def getComment_on_Comment_likes(commentOnCommentId, token):
    return
@app.route("/publications/comments/onComment/like")
def likeComment_on_Comment():
    return
@app.route("/publications/comments/onComment/unlike")
def unlikePComment_on_Comment():
    return