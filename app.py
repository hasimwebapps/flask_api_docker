from flask import Flask, jsonify, request
import logging


from src.handler import utils
from src.handler import topup, auth, transaction, payment, profile, transfer
from src.dal import mongo_dal

app = Flask(__name__)
app.debug = True


@app.route('/register', methods=['POST'])
def register():
    ret = utils.generate_ret()
    try:
        ret = auth.register(request)
        return jsonify(ret)
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify(ret), 500


@app.route('/login', methods=['POST'])
def login():
    ret = utils.generate_ret()
    try:
        ret = auth.login(request)
        return jsonify(ret)
    except Exception as e:
        logging.error(e, exc_info=True)
        ret["message"] = 'Internal Error'
        return jsonify(ret), 500


@app.route('/topup', methods=['POST'])
def top_up():
    ret = utils.generate_ret()
    try:
        ret = topup.top_up(request)
        return jsonify(ret)
    except Exception as e:
        ret["message"] = 'Internal Error'
        logging.error(e, exc_info=True)
        return jsonify(ret), 500


@app.route('/pay', methods=['POST'])
def pay():
    ret = utils.generate_ret()
    try:
        ret = payment.pay(request)
        return jsonify(ret)
    except Exception as e:
        ret["message"] = 'Internal Error'
        logging.error(e, exc_info=True)
        return jsonify(ret), 500


@app.route('/transfer', methods=['POST'])
def user_transfer():
    ret = utils.generate_ret()
    try:
        ret = transfer.transfer(request)
        return jsonify(ret)
    except Exception as e:
        ret["message"] = 'Internal Error'
        logging.error(e, exc_info=True)
        return jsonify(ret), 500


@app.route('/transactions', methods=['POST'])
def transactions():
    ret = utils.generate_ret()
    try:
        ret = transaction.transaction(request)
        return jsonify(ret)
    except Exception as e:
        ret["message"] = 'Internal Error'
        logging.error(e, exc_info=True)
        return jsonify(ret), 500


@app.route('/profile', methods=['PUT'])
def user_profile():
    ret = utils.generate_ret()
    try:
        ret = profile.profile_update(request)
        return jsonify(ret)
    except Exception as e:
        ret["message"] = 'Internal Error'
        logging.error(e, exc_info=True)
        return jsonify(ret), 500


@app.route('/user_list', methods=['GET'])
def user_list():
    ret = utils.generate_ret()
    try:
        db = mongo_dal.get_db()
        _users = db.user_tb.find().sort("created_date", 1)
        users = [
            {
                "id": str(user["_id"]),
                "user_id": user.get("user_id", ""),
                "first_name": user.get("first_name", ""),
                "last_name": user.get("last_name", ""),
                "phone_number": user.get("phone_number", ""),
                "address": user.get("address", ""),
                "created_date": user.get("created_date", ""),
                "updated_date": user.get("updated_date", ""),
            } for user in _users]

        ret["result"] = users
        ret["status"] = 'SUCCESS'
    except Exception as e:
        logging.error(e, exc_info=True)
    return jsonify(ret)


@app.route('/user_delete', methods=['POST'])
def user_delete():
    ret = utils.generate_ret()
    try:
        request_data = request.get_json()
        _id = request_data['id']

        db = mongo_dal.get_db()
        result = db.user_tb.delete_one({'user_id': _id})
        ret["result"] = result.deleted_count
        ret["status"] = 'SUCCESS'
    except Exception as e:
        logging.error(e, exc_info=True)
    return jsonify(ret)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
