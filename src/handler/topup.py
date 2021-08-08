from flask import request, jsonify
import uuid
import logging
import datetime
from src.handler import utils
from src.dal import mongo_dal


def top_up(request):
    ret = utils.generate_ret()
    try:
        auth_header = request.headers.get('Authorization')
        auth_token = ''
        if auth_header:
            auth_header_list = auth_header.split(" ")
            if len(auth_header_list) > 1:
                auth_token = auth_header_list[1]

        if auth_token:
            resp, err_msg = utils.decode_auth_token(auth_token)
            if err_msg != "":
                ret['status'] = "ERROR"
                ret['message'] = err_msg
                return ret

            if resp:
                request_data = request.get_json()
                amount_top_up = request_data.get('amount_top_up', 0)
                if int(amount_top_up) <= 0:
                    ret["message"] = "Invalid Amount"
                    ret["status"] = "ERROR"
                    return ret

                current_balance = 0

                db = mongo_dal.get_db()
                db_result = db.topup_tb.find({"user_id": resp}).sort("created_date", -1)
                if db_result:
                    for i in db_result[0:1]:
                        current_balance = i.get("balance_after", 0)

                payload = {
                    "user_id": resp,
                    "top_up_id": str(uuid.uuid4()),
                    "amount": amount_top_up,
                    "balance_before": current_balance,
                    "balance_after": int(amount_top_up) + current_balance,
                    "transaction_type": "CREDIT",
                    "remarks": "",
                    "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                db.topup_tb.insert_one(payload)

                ret["result"] = {
                    "user_id": payload.get("user_id", ""),
                    "top_up_id": payload.get("top_up_id", ""),
                    "amount_top_up": payload.get("amount", 0),
                    "balance_before": payload.get("balance_before", 0),
                    "balance_after": payload.get("balance_after", 0),
                    "created_date": payload.get("created_date", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "updated_date": payload.get("updated_date", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
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
