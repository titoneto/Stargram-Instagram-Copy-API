from flask import request, jsonify
from app import app, db
from app.authenticate import jwt_required
from werkzeug.security import generate_password_hash
from sqlalchemy import desc

from app.models.tables import(
    User, user_share_schema, users_share_schema, 
    Publication, publication_share_schema, feed_share_schema,
    Publication_Like, Publication_Likes_share_schema,
    Comment, Comments_share_schema,
    Comment_Like, Comment_Like_share_schema,
    Comment_on_comment, Comment_on_comment_share_schema,
    Comment_on_comment_Like, Comment_on_comment_Like_share_schema,
    Follow, Follow_share_schema, Follows_share_schema,
    Conversation, message_share_schema, direct_share_schema,
    Story, Story_share_schema
)
    

import jwt
import datetime

@app.route("/auth/register", methods =["POST"])
def signUp():
    body = request.get_json()
    user_name = body['user_name']
    name = body['name']
    email = body['email']
    password = body['password']
    image = body['image'].encode()
    print(image)

    if User.query.filter_by(user_name = user_name).first():
        return jsonify({"error": "O Nome de usuário " + user_name + " não está disponível"})
    elif User.query.filter_by(email = email).first():
        return jsonify({"error": "O Email já foi cadastrado anteriormente"})
    else :
        user = User(email, name, user_name, password, image)
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

        return jsonify({"token": token, "user" : search_user})


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
        current_user.image = body['image'].encode()

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
    description = body['description']
    image = body['image'].encode()

    publication = Publication(description, current_user.id, image)
    db.session.add(publication)
    db.session.commit()

    return jsonify({ "msg" : "Publicação realizada com sucesso" })




@app.route("/publications/edit", methods =["POST"])
@jwt_required
def editPublication(current_user):
    body = request.get_json()

    publication_to_edit = Publication.query.filter_by(id = body['publication_id']).first()
    description = body['description']

    if not publication_to_edit:
        return jsonify({"error" : "Publicação não encontrada"})

    publication_to_edit.description = description
    
    db.session.add(publication_to_edit)
    db.session.commit()

    return jsonify({ "msg" : "Publicação editada com sucesso" })

@app.route("/publications/delete", methods =["POST"])
@jwt_required
def deletePublication(current_user):
    body = request.get_json()
    publicationId = body['publication_id']

    publication_to_delete = Publication.query.filter_by(id = publicationId).first()
    
    comments = Comment.query.filter_by(publication_id = publicationId).all()

    for c in comments:
        comments_on_comment = Comment_on_comment.query.filter_by(comment_id = c.id).all()
        for cc in comments_on_comment:
            db.session.delete(cc)
        db.session.delete(c)
    db.session.delete(publication_to_delete)

    db.session.commit()

    return jsonify({ "msg" : "Publicação deletada com sucesso" })

@app.route("/publication?<int:publicationId>")
@jwt_required
def getPublication(current_user, publicationId):

    search_publication = publication_share_schema(
        Publication.query.filter_by(id = publicationId).first()
    )

    return jsonify({"data" : search_publication})

@app.route("/feed", methods =["POST"])
@jwt_required
def getFeed(current_user):
    body = request.get_json()
    lastPublicationId = body['last_Publication_Id']
    limit = body['limit']

    hasLastPublication = Publication.query.filter_by(id = lastPublicationId).first()
    offset = 0


    followeds = Follow.query.filter_by(follower_id = current_user.id).all()
    feed = []

    for f in followeds:
        followed_feed = Publication.query.filter_by(owner_id = f.user_id).order_by(desc(Publication.date)).limit(5).all()
        for p in followed_feed:
            feed.append(p)

    feed.sort(reverse=True,key = lambda p: p.date)

    if hasLastPublication:
        offset = feed.index(hasLastPublication)+1

    result = feed_share_schema.dump(feed[offset:offset + limit])

    return jsonify({"data" : result })





@app.route("/publications/comments", methods =["POST"])
@jwt_required
def getComments(current_user):
    body = request.get_json()
    
    publicationId = body['publication_id']
    lastCommentId = body['last_Comment_Id']
    limit = body['limit']
    offset = 0

    hasLastComment = Comment.query.filter_by(id = lastCommentId).first()

    all_comments = Comment.query.filter_by(publication_id = publicationId).all()
    all_comments.sort(reverse=True,key = lambda p: p.date)

    if hasLastComment:
        offset = all_comments.index(hasLastComment)+1

    result = Comments_share_schema.dump(all_comments[offset:offset + limit])

    return jsonify({"comments" : result })

@app.route("/publications/comments/new", methods =["POST"])
@jwt_required
def newComment(current_user):
    body = request.get_json()
    publicationId = body['publication_id']
    content = body['content']

    if not Publication.query.filter_by(id = publicationId).first():
        return jsonify({ "error" : "Publicação não encontrada" })

    comment = Comment(content, current_user.id, publicationId)

    db.session.add(comment)
    db.session.commit()

    return jsonify({ "msg" : "Comentario adicionado com sucesso" })

@app.route("/publications/comments/delete", methods =["POST"])
@jwt_required 
def deleteComment(current_user):
    body = request.get_json()
    comentId = body['comment_id']

    comment_to_delete = Comment.query.filter_by(id = comentId).first()
    db.session.delete(comment_to_delete)

    comment_on_comments = Comment_on_comment.query.filter_by(comment_id = comentId).all()

    for c in comment_on_comments:
        db.session.delete(c)

    db.session.commit()

    return jsonify({ "msg" : "Comentario deletado com sucesso" })




@app.route("/publications/comments/onComment", methods =["POST"])
@jwt_required
def getComments_on_Comment(current_user):
    body = request.get_json()
    
    commentId = body['comment_id']
    lastComCommentId = body['last_Comment_on_Comment_Id']
    limit = body['limit']
    offset = 0

    hasLastComComment = Comment_on_comment.query.filter_by(id = lastComCommentId).first()

    all_com_comments = Comment_on_comment.query.filter_by(comment_id = commentId).all()
    all_com_comments.sort(reverse=True,key = lambda p: p.date)

    if hasLastComComment:
        offset = all_com_comments.index(hasLastComComment)+1

    result = Comment_on_comment_share_schema.dump(all_com_comments[offset:offset + limit])

    return jsonify({"Comments_on_comment" : result })

@app.route("/publications/comments/onComment/new", methods =["POST"])
@jwt_required
def newComment_on_Comment(current_user):
    body = request.get_json()
    commentId = body['comment_id']
    content = body['content']

    if not Comment.query.filter_by(id = commentId).first():
        return jsonify({ "error" : "Comentario não encontrado" })

    com_comment = Comment_on_comment(content, current_user.id, commentId)

    db.session.add(com_comment)
    db.session.commit()

    return jsonify({ "msg" : "Resposta adicionada com sucesso" })

@app.route("/publications/comments/onComment/delete", methods =["POST"])
@jwt_required
def deleteComment_on_Comment(current_user):
    body = request.get_json()
    Comment_on_Comment_to_delete = Comment_on_comment.query.filter_by(id = body['Comment_on_comment_id']).first()

    db.session.delete(Comment_on_Comment_to_delete)
    db.session.commit()

    return jsonify({ "msg" : "Resposta deletada com sucesso" })




@app.route("/followers/userId=<int:userId>")
@jwt_required
def getFollowers(current_user, userId):
    
    followers = Follow.query.filter_by(user_id = userId).all()
    search = Follows_share_schema.dump(followers)


    return jsonify({"followers" : search})

@app.route("/following/userId=<int:userId>")
@jwt_required
def getFollowing(current_user, userId):

    following = Follow.query.filter_by(follower_id = userId).all()
    search = Follows_share_schema.dump(following)

    return jsonify({"following" : search})

@app.route("/follow", methods =["POST"])
@jwt_required
def follow(current_user):
    body = request.get_json()

    followed_id = body['followed_id']
    follower_id = current_user.id

    user = User.query.filter_by(id = followed_id).first()
    follower = User.query.filter_by(id = follower_id).first()

    hasFollow = Follow.query.filter_by(user_id = followed_id, follower_id = follower_id).first()

    if hasFollow:

        db.session.delete(hasFollow)

        user.remove_follower()
        follower.remove_following()
        db.session.add(user)
        db.session.add(follower)

        db.session.commit()

        return jsonify({"msg" : "Unfollow realizado com sucesso"})

    if not User.query.filter_by(id = followed_id).first():
        return jsonify({"error": "Usuario não existente"})
    
    follows = Follow(followed_id, follower_id)
    db.session.add(follows)

    user.add_follower()
    follower.add_following()
    db.session.add(user)
    db.session.add(follower)

    db.session.commit()

    search_follow = Follow_share_schema.dump(
        Follow.query.filter_by(id = follows.id).first()
    )

    return jsonify({"data" : search_follow})





@app.route("/direct", methods =["POST"])
@jwt_required
def getConversation(current_user):
    body = request.get_json()
    recipientId = body['recipient_id']
    limit = body['limit']
    lastMessageId = body['last_message_id']
    offset = 0

    userMessages = Conversation.query.filter_by(self_id = current_user.id, recipient_id = recipientId).all()
    recipientMessages = Conversation.query.filter_by(self_id = recipientId, recipient_id = current_user.id).all()
    messages = userMessages + recipientMessages

    hasLastMessage = Conversation.query.filter_by(id = lastMessageId).first()

    messages.sort(reverse = True,key = lambda m: m.date )

    if hasLastMessage:
        offset = messages.index(hasLastMessage) + 1

    
    search_messages = direct_share_schema.dump(messages[offset:offset+limit])
    
    return jsonify({"direct": search_messages})

@app.route("/direct/message", methods =["POST"])
@jwt_required
def addMessage(current_user):
    body = request.get_json()

    recipientId = body['recipient_id']
    content = body['content']

    hasRecipientUser = User.query.filter_by(id = recipientId).first()
    if not hasRecipientUser:
        return jsonify({"error" : "Usuário não encontrado"})
    
    message = Conversation(current_user.id, recipientId, content)
    db.session.add(message)
    db.session.commit()

    search_message = message_share_schema.dump(message)

    return jsonify({"message" : search_message })




@app.route("/hasstories", methods =["POST"])
@jwt_required
def getStories(current_user):
    followeds = Follow.query.filter_by(follower_id = current_user.id).all()
    stories = []

    for f in followeds:
        followed_story = Story.query.filter_by(owner_id = f.user_id).order_by(desc(Story.date)).first()
        if followed_story:
            stories.append(followed_story)

    self_Stories = Story.query.filter_by(owner_id = current_user.id).order_by(desc(Story.date)).first()
    if self_Stories:
        stories.append(self_Stories)

    stories.sort(reverse=True,key = lambda p: p.date)

    usersStories = []
    for s in stories:
        user = User.query.filter_by(id = s.owner_id).first()
        usersStories.append(user)
 
    result = users_share_schema.dump(usersStories)

    return jsonify({"users" : result })

@app.route("/story/new", methods =["POST"])
@jwt_required
def newStory(current_user):
    body = request.get_json()
    image = body['image'].encode()
    story = Story(image, current_user.id)

    db.session.add(story)
    db.session.commit()

    search_story = Story_share_schema.dump([story])

    return jsonify({"story" : search_story[0]})

@app.route("/story/userId=<int:userId>")
@jwt_required
def getStory(current_user, userId):
    stories = Story.query.filter_by(owner_id = userId).all()

    stories_schema = Story_share_schema.dump(stories)

    return jsonify({"stories" : stories_schema})





@app.route("/publications/likes/publicationId=<int:publicationId>")
@jwt_required
def getPublication_likes(current_user, publicationId):
    
    likes_schema = Publication_Likes_share_schema.dump(
        Publication_Like.query.filter_by(publication_id = publicationId).all()
    )

    return jsonify({"likes" : likes_schema})

@app.route("/publications/like", methods =["POST"])
@jwt_required
def likePublication(current_user):
    body = request.get_json()
    publicationId = body['publication_id']

    publication = Publication.query.filter_by(id = publicationId).first()
    if not publication:
        return jsonify({"error": "publicação não encontrada"})

    hasLike = Publication_Like.query.filter_by(owner_id = current_user.id, publication_id = publicationId).first()

    if hasLike:
        publication.unlike()
        db.session.add(publication)
        db.session.delete(hasLike)
        db.session.commit()

        return jsonify({"msg": "Curtida removida"})


    like = Publication_Like(current_user.id, publicationId)

    publication.like()
    db.session.add(like)
    db.session.add(publication)
    db.session.commit()

    return jsonify({"msg": "Publicação curtida com sucesso"})



@app.route("/publications/comments/likes/commentId=<int:commentId>")
@jwt_required
def getComment_likes(current_user, commentId):
    likes_schema = Comment_Like_share_schema.dump(
        Comment_Like.query.filter_by(comment_id = commentId).all()
    )

    return jsonify({"likes" : likes_schema})

@app.route("/publications/comments/like", methods =["POST"])
@jwt_required
def likeComment(current_user):
    body = request.get_json()
    commentId = body['comment_id']

    comment = Comment.query.filter_by(id = commentId).first()
    if not comment:
        return jsonify({"error": "comentário não encontrado"})

    hasLike = Comment_Like.query.filter_by(owner_id = current_user.id, comment_id = commentId).first()

    if hasLike:
        comment.unlike()
        db.session.add(comment)
        db.session.delete(hasLike)
        db.session.commit()

        return jsonify({"msg": "Curtida removida"})


    like = Comment_Like(current_user.id, commentId)

    comment.like()
    db.session.add(like)
    db.session.add(comment)
    db.session.commit()

    return jsonify({"msg": "Comentario curtido com sucesso"})




@app.route("/publications/comments/onComment/likes/commentOnCommentId=<int:commentOnCommentId>")
@jwt_required
def getComment_on_Comment_likes(current_user, commentOnCommentId):
    likes_schema = Comment_on_comment_Like_share_schema.dump(
        Comment_on_comment_Like.query.filter_by(comment_on_comment_id = commentOnCommentId).all()
    )

    return jsonify({"likes" : likes_schema})
    
@app.route("/publications/comments/onComment/like", methods =["POST"])
@jwt_required
def likeComment_on_Comment(current_user):
    body = request.get_json()
    commentOnCommentId = body['comment_on_comment_id']

    commentOnComment = Comment_on_comment.query.filter_by(id = commentOnCommentId).first()
    if not commentOnComment:
        return jsonify({"error": "resposta não encontrada"})

    hasLike = Comment_on_comment_Like.query.filter_by(owner_id = current_user.id, comment_on_comment_id = commentOnCommentId).first()

    if hasLike:
        commentOnComment.unlike()
        db.session.add(commentOnComment)
        db.session.delete(hasLike)
        db.session.commit()

        return jsonify({"msg": "Curtida removida"})


    like = Comment_on_comment_Like(current_user.id, commentOnCommentId)

    commentOnComment.like()
    db.session.add(like)
    db.session.add(commentOnComment)
    db.session.commit()

    return jsonify({"msg": "Resposta curtida com sucesso"})