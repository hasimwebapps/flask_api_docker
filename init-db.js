db = db.getSiblingDB("example_data");
db.user_tb.drop()

db.user_tb.insertMany([
    {
        "address": "Masjid Annur 15",
        "created_date": "2021-08-08 18:27:19",
        "first_name": "Hasim",
        "id": "61102207f7708051c6cc55ea",
        "last_name": "Imahdudin",
        "phone_number": "08123456",
        "pin": "sha256$Beyk4Ap8QmhKFrdD$225af65fa6ed94a4762bcb258c0883e6156d0a7367d019d44c51762f72d95f0f",
        "updated_date": "2021-08-08 18:27:19",
        "user_id": "aee5c9e6-9cd5-43d9-85e0-8149977b51af"
    },
    {
        "address": "Masjid Annur 14",
        "created_date": "2021-08-08 18:53:10",
        "first_name": "Muhammad",
        "id": "611028169a7ca13fcd80c328",
        "last_name": "Cahyo",
        "phone_number": "08123457",
        "pin": "sha256$v6XRS7HSeJYcdEYf$9577c624febb2290367b258a410e4b21ab7366e1498d8fe318fd7b94ca40181a",
        "updated_date": "2021-08-08 18:53:10",
        "user_id": "3a1192d8-c9d8-4d88-bdd6-c4fe2b49d067"
    },
    {
        "address": "Jiban",
        "created_date": "2021-08-08 19:14:45",
        "first_name": "Aldy",
        "id": "61102d25c21cbf79a7fbd826",
        "last_name": "Abdat",
        "phone_number": "081125558",
        "pin": "sha256$q7qTptKXraY22LU0$fa14e6fa4458e73a31e05c1fd675ac711f7e01d84837dc03e012187e5b264486",
        "updated_date": "2021-08-08 19:14:45",
        "user_id": "720c68ff-0607-46f8-90c7-f816d8fa8d52"
    }
])
