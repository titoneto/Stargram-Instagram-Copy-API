from functools import wraps

import jwt
from flask import request, jsonify, current_app

from app.models.tables import User

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return jsonify({"error": "token não encontrado"})

        if not "Bearer " in token:
            return jsonify({"error": " Bearer token inválido"})

        try:
            token_pure = token.replace("Bearer ", "")
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'],algorithms="HS256") # jwt com campos de sub e iat
            current_user = User.query.filter_by(id = decoded['sub']).first()
            if (int(current_user.token_iat) != decoded['iat']):
                return jsonify({"error": "token desatualizado"})
        except:
            return jsonify({"error: ": "token inválido"})

        
        

        return f(current_user = current_user,  *args, **kwargs)
    return wrapper