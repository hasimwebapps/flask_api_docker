db = db.getSiblingDB("example_data");
db.user_tb.drop()

db.user_tb.insertMany([
    {
        "address": "Masjid Annur 15",
        "first_name": "Hasim",
        "last_name": "Imahdudin",
        "phone_number": "08123456",
        "pin": "123456",
    },
    {
        "address": "Masjid Annur 14",
        "first_name": "Muhammad",
        "last_name": "Cahyo",
        "phone_number": "08123457",
        "pin": "123456",
    },
    {
        "address": "Jiban",
        "first_name": "Aldy",
        "last_name": "Abdat",
        "phone_number": "081125558",
        "pin": "123456"
    }
])
