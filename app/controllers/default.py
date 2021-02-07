from flask import request, jsonify
from app import app, db
from app.models.tables import User, user_share_schema, users_share_schema

@app.route("/")
def home():
    print("aqui")
    return {"aqui"}

@app.route("/aqui")
def aqui():
    print("aqui")
    return "aqui"



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

        search_user = user_share_schema.dump(
            User.query.filter_by(user_name = user_name).first()
        )
        return jsonify(search_user)


@app.route("/auth/login", methods =["POST"])
def login():
    body = request.get_json()
    user = User.query.filter_by(user_name = body['user_name']).first()
    if not user:
        user = User.query.filter_by(email = body['email']).first()
        if not user:
            return jsonify({"error": "nome de usuário ou email inválido"})
            
    if not user.verify_password(body['password']):
        return jsonify({"error": "senha inválida"})
    
    search_user = user_share_schema.dump(user)

    token = jwt.encode

    return jsonify(search_user)

@app.route("/auth/delete", methods = ["POST"])
def delete():
    return


@app.route("/auth/logout")
def logout():
    return

@app.route("/auth/refresh")
def refresh():
    return





@app.route("/feed?<int:id>&token=<token>")
def getFeed(id,token):
    return
@app.route("/publication?<int:id>&token=<token>")
def getPublication(id,token):
    return
@app.route("/publications/new")
def newPublication():
    return
@app.route("/publications/edit")
def editPublication():
    return
@app.route("/publications/delete")
def deletePublication():
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