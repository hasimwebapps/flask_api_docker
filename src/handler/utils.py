from flask import request, jsonify
import jwt
import datetime
import logging

SECRET_KEY = 's3cr3T'


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        ), "None"
    except Exception as e:
        logging.error(e, exc_info=True)


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return payload['sub'], ''
    except jwt.ExpiredSignatureError:
        return '', 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return '', 'Invalid token. Please log in again.'


def generate_ret():
    return {
        "status": "ERROR",
    }
