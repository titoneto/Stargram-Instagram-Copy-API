from functools import wraps

import jwt
from flask import request, jsonify, current_app

from app.models import User

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, *kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return jsonify({"error": "token não autorizado"})

        decoded = jwt.decode(token, current_app.config['SECRET_KEY'])
        current_user = User.query.get(decoded['id'])


        return f(current_user = current_user, *args, *kwargs)

    return wrapper