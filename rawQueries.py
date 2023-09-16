from pymongo import MongoClient
from bson.regex import Regex

# Connect to your MongoDB server
client = MongoClient('localhost', 27017)
db = client['srgw_data_store']


def getStatusOfTransactions(product = "Key"):
    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "product": Regex(product, "i"),
                "campaignId": "6448fd9329b3cbd2f1b3f22e"
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]

    # Execute the aggregation query
    result = list(db.PromoTransaction.aggregate(pipeline))

    # Print the result
    for item in result:
        print(item)
