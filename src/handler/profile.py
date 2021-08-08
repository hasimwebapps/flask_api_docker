from flask import request, jsonify
import uuid
import logging
import datetime
from src.handler import utils
from src.dal import mongo_dal


def profile_update(request):
    ret = utils.generate_ret()
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp, err_msg = utils.decode_auth_token(auth_token)
            if err_msg != '':
                ret["message"] = err_msg
                return ret
            if resp:
                db = mongo_dal.get_db()
                request_data = request.get_json()
                if not request_data:
                    ret["message"] = "Invalid Parameter"

                first_name = request_data.get('first_name', '')
                last_name = request_data.get('last_name', '')
                address = request_data.get('address', '')

                filter = {'user_id': str(resp)}

                payload = {}
                if first_name != '':
                    payload["first_name"] = first_name
                if last_name != '':
                    payload["last_name"] = last_name
                if address != '':
                    payload["address"] = address
                new_values = {"$set": payload}
                db.user_tb.update_one(filter, new_values)

                user = db.user_tb.find_one({"user_id": resp})
                ret["result"] = {
                    "user_id": user.get("user_id", ""),
                    "first_name": user.get("first_name", ""),
                    "last_name": user.get("last_name", ""),
                    "phone_number": user.get("phone_number", ""),
                    "address": user.get("address", ""),
                    "created_date": user.get("created_date", ""),
                }
                ret['status'] = "SUCCESS"
                return ret
        else:
            return {
                'status': 'ERROR',
                'message': 'Unauthenticated'
            }

    except Exception as e:
        logging.error(e, exc_info=True)
        return ret
