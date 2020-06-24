from flask import request, g, jsonify

import jwt

import datetime

from ..extensions import mongo

from functools import wraps

from os import environ

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, environ.get('SECRET_KEY'))
            current_user = mongo.Users.find_one({'username': data['username']})
            if current_user:
                g.current_user = current_user
            else:
                return jsonify({'message' : 'Not a valid user, Invalid token!'}), 401
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

