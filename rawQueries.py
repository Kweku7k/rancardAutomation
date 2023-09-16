import pprint
from pymongo import MongoClient
from bson.regex import Regex
import os

# Create the excel Sheets for the respective graph data


# Connect to your MongoDB server
campaignId = "6448fd9329b3cbd2f1b3f22e"
# client = MongoClient('localhost', 27017)
client = os.environ.get("mongoUri", MongoClient('localhost', 27017) )
print(client)
db = client['srgw_data_store']



# --------- FUNCTIONS
def sum_dictionary_values(dictionary):
    total = 0
    for value in dictionary.values():
        total += value
    return total

def getAllValuesBasedOnCriteria(array, data, label):
    print("Generating Values For " + label)
    total = 0
    for i in array:
        total += data.get(i, 0) 
        print(total)
    print(label, ":" ,total)
    return total
# --------- END


def getStatusOfTransactions(campaignId):
    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "campaignId": campaignId #ADD NE FIELDS?
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
    data = {}

    for item in result:
        print(item)
        print(item['_id'])
        print(item['count'])
        data[item['_id']] = item['count']
    
    print(data)

    totalEntries = sum_dictionary_values(data)
    totalWins = getAllValuesBasedOnCriteria(["REDEEMED","WIN","PENDING"], data, "Valid Entries") #✅
    valid = getAllValuesBasedOnCriteria(["REDEEMED","WIN","PENDING","TRY_AGAIN"], data, "Valid Entries") #✅
    invalidEntries = getAllValuesBasedOnCriteria(["INVALID", "FRAUD", "USED", "STAFF", "FAILED"], data, "Invalid Entries") #MUST TEST TO CHECK TRY AGAIN VALUES
    blacklisted = getAllValuesBasedOnCriteria(["SUSPENDED"], data, "Blacklisted Entries")
    winIgnores = getAllValuesBasedOnCriteria(["SUSPENDED"], data, "Win Ignored Entries")
    # unique_winners = len(db[collection_name].distinct("msisdn", query))


def getRewardData(campaignId):
    pipeline = [
        {
            "$match": {
                "campaignId": campaignId
            }
        },
        {
            "$group": {
                "_id": "$rewardType",
                "count": {"$sum": 1}
            }
        }
    ]

    result = list(db.PromoTransaction.aggregate(pipeline))
    print(result)

    data = {}

    for item in result:
        print(item)
        print(item['_id'])
        print(item['count'])
        data[item['_id']] = item['count']
    
    print(data)
    return data

# DEMOGRAPHICS HARVESTER!
def generateDemographicData(campaignId, product, demographic):
    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "product":  Regex(product, "i"),
                "campaignId": campaignId
            }
        },
        {
            "$lookup": {
                "from": "CampaignClient",
                "localField": "msisdn",
                "foreignField": "msisdn",
                "as": "clientInfo"
            }
        },
        {
            "$unwind": "$clientInfo"
        },
        {
            "$group": {
                "_id": "$clientInfo."+demographic,
                "count": {"$sum": 1}
            }
        }
    ]

    result = list(db.PromoTransaction.aggregate(pipeline))
    print(result)

    data = {}

    for item in result:
        print(item)
        print(item['_id'])
        print(item['count'])
        data[item['_id']] = item['count']

    return data
    
def demographicData(demographics, products):
    print("=====GENERATING DATA FOR PRODUCTS: ", products , "=====")
    finalResponse = {}

    for p in products: 
        print("PRODUCT: "+ p)

        demographicDictonaryArray = {}
        demographicDictonary = {}

        for d in demographics:
            print("-----------------------")
            print("PRODUCT " + p + " || DEMOGRAPHIC: "+ d)
            data = generateDemographicData(campaignId,p, d)
            print("-----------------------")
            demographicDictonary[d] = data
            pprint.pprint(demographicDictonary)

        response = {"product":p, "demographics":demographicDictonary}
        pprint.pprint(response)
    # finalResponse = response 

    # pprint.pprint(finalResponse)
    return "response"


# FIRST_SLIDE
# getStatusOfTransactions(campaignId)
# getRewardData(campaignId)
print(demographicData(["ageRange", "gender", "region"], ["Pepsodent", "Geisha","Key"]))


# generateDemographicData(campaignId, "Pepsodent", "ageRange")