from flask import request, jsonify
import uuid
import logging
import datetime
import json
from src.handler import utils
from src.dal import mongo_dal


def transaction(request):
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
                ret["status"] = "ERROR",
                ret['message'] = err_msg
                return ret
            if resp:
                db = mongo_dal.get_db()
                db_result = db.topup_tb.find({"user_id": resp}).sort("created_date", -1)

                result = []
                for i in db_result:
                    obj = {}
                    obj["amount"] = i.get("amount", 0)
                    obj["balance_before"] = i.get("balance_before", 0)
                    obj["balance_after"] = i.get("balance_after", 0)
                    obj["transaction_type"] = i.get("transaction_type", 0)
                    obj["remarks"] = i.get("remarks", "")
                    obj["status"] = "SUCCESS"
                    obj["created_date"] = i.get("created_date", "")
                    obj["updated_date"] = i.get("updated_date", "")

                    top_up_id = i.get("top_up_id", "")
                    transfer_id = i.get("transfer_id", "")
                    payment_id = i.get("payment_id", "")

                    if top_up_id != "":
                        obj["top_up_id"] = i.get("top_up_id", "")

                    elif transfer_id != "":
                        obj["transfer_id"] = i.get("transfer_id", "")

                    elif payment_id != "":
                        obj["payment_id"] = i.get("payment_id", "")

                    result.append(obj)

                ret['result'] = result
                ret['user_id'] = resp
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
