from flask import request, jsonify
import uuid
import logging
import datetime
from src.handler import utils
from src.dal import mongo_dal


def transfer(request):
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
            if err_msg != '':
                ret["message"] = err_msg
                ret["status"] = "ERROR"
                return ret
            if resp:
                request_data = request.get_json()
                target_user = request_data.get('target_user', "")
                amount = request_data.get('amount', 0)
                remarks = request_data.get('remarks', '')

                if int(amount) <= 0 or target_user == "":
                    ret["message"] = "Invalid Parameter"
                    ret["status"] = "ERROR"
                    return ret

                current_balance = 0

                db = mongo_dal.get_db()
                db_result = db.topup_tb.find({"user_id": resp}).sort("created_date", -1)
                if db_result:
                    for i in db_result[0:1]:
                        current_balance = i.get("balance_after", 0)

                if amount > current_balance:
                    ret["message"] = "Balance is not enough"
                    ret["status"] = "ERROR"
                    return ret

                exist = db.user_tb.find_one({"user_id": target_user})
                if exist:
                    if exist["user_id"] == resp:
                        ret["message"] = "Can't transfer to self"
                        ret["status"] = "ERROR"
                        return ret

                    transfer_id = str(uuid.uuid4())
                    current_balanced_receiver = 0

                    db_receiver_result = db.topup_tb.find({"user_id": target_user}).sort("created_date", -1)
                    if db_receiver_result:
                        for i in db_receiver_result[0:1]:
                            current_balanced_receiver = i.get("balance_after", 0)

                    payload_user_receiver = {
                        "user_id": exist.get("user_id", ""),
                        "transfer_id": transfer_id,
                        "amount": amount,
                        "balance_before": current_balanced_receiver,
                        "balance_after": int(current_balanced_receiver) + int(amount),
                        "transaction_type": "CREDIT",
                        "remarks": remarks,
                        "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    db.topup_tb.insert_one(payload_user_receiver)

                    payload_user_sender = {
                        "user_id": resp,
                        "transfer_id": transfer_id,
                        "amount": amount,
                        "balance_before": current_balance,
                        "balance_after": int(current_balance) - int(amount),
                        "transaction_type": "DEBIT",
                        "remarks": remarks,
                        "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    db.topup_tb.insert_one(payload_user_sender)
                else:
                    ret["message"] = "invalid target user id"
                    return ret
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
