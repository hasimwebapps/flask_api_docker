from pymongo import MongoClient


def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource="admin")
    db = client["example_data"]
    return db
