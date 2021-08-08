import logging
from flask import request, jsonify
from src.dal import mongo_dal
from src.handler import utils
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid


def login(request):
    ret = utils.generate_ret()
    try:
        db = mongo_dal.get_db()
        request_data = request.get_json()
        phone_number = request_data.get('phone_number', '')
        pin = request_data.get('pin', '')

        if phone_number == '' or pin == '':
            ret["message"] = "Invalid Parameter!!"
            return ret

        user = db.user_tb.find_one({"phone_number": phone_number})
        if not user:
            ret["status"] = 'ERROR'
            ret["message"] = 'Phone number not registered'
            return ret

        if check_password_hash(user["pin"], pin):
            ret['status'] = "SUCCESS"
            access_token, refresh_token = utils.encode_auth_token(user_id=str(user["user_id"]))
            ret["result"] = {
                "access_token": access_token.decode("utf-8"),
                # "refresh_token": refresh_token,
            }
        else:
            ret['message'] = "Phone number and pin doesn’t match."
        return ret
    except Exception as e:
        ret["message"] = 'INTERNAL ERROR'
        logging.error(e, exc_info=True)
        return ret


def register(request):
    db = ""
    ret = utils.generate_ret()
    try:
        request_data = request.get_json()
        first_name = request_data.get('first_name', '')
        last_name = request_data.get('last_name', '')
        phone_number = request_data.get('phone_number', '')
        address = request_data.get('address', '')
        pin = request_data.get('pin', '')
        user_id = str(uuid.uuid4())

        if phone_number == '' or pin == '':
            ret["message"] = "Invalid Parameter!!"
            return ret

        hashed_password = generate_password_hash(pin, method='sha256')

        db = mongo_dal.get_db()
        exists = db.user_tb.find_one({"phone_number": phone_number})
        if exists:
            ret["status"] = 'ERROR'
            ret["message"] = 'Phone Number already registered'
            return ret

        payload = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "address": address,
            "pin": hashed_password,
            "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        db.user_tb.insert_one(payload)
        ret["result"] = {
            "user_id": payload.get("user_id", ""),
            "first_name": payload.get("first_name", ""),
            "last_name": payload.get("last_name", ""),
            "phone_number": payload.get("phone_number", ""),
            "address": payload.get("address", ""),
            "created_date": payload.get("created_date", ""),
        }
        ret["status"] = 'SUCCESS'
        return ret
    except Exception as e:
        logging.error(e, exc_info=True)
        return ret
