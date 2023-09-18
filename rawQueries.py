from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
import pprint
import smtplib
from pymongo import MongoClient
from bson.regex import Regex
import os
import pandas as pd
import csv


# Create the excel Sheets for the respective graph data
# GET CAMPAIGN DETAILS - TODO

# Connect to your MongoDB server
campaignId = "6448fd9329b3cbd2f1b3f22e"

if os.environ.get("mongoUri"):
    client = MongoClient(os.environ.get("mongoUri"))
else:
    client = MongoClient('localhost', 27017) 
# client = MongoClient('localhost', 27017)
# uri = os.environ.get("mongoUri", ('localhost', 27017))

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


def getStatusOfTransactions(campaignId, product=None):
    # Define the aggregation pipeline
    if product == None:
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

    else:
        pipeline = [
            {
                "$match": {
                    "campaignId": campaignId, #ADD NE FIELDS?
                    "product":  Regex(product, "i"),

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

    responseBody = {
        "totalEntries":totalEntries,
        "totalWins":totalWins,
        "valid":valid,
        "invalidEntries":invalidEntries,
        "blacklisted":blacklisted,
        "winIgnores":winIgnores
    }

    print("------responsep-----")
    pprint.pprint(responseBody)
    return responseBody


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
    finalResponseArray = []

    for p in products: 
        print("PRODUCT: "+ p)

        demographicDictonaryArray = {}
        demographicDictonary = {}

        response = {p:demographicDictonary}
        for d in demographics:
            print("-----------------------")
            print("PRODUCT " + p + " || DEMOGRAPHIC: "+ d)
            data = generateDemographicData(campaignId,p, d)
            print("-----------------------")
            demographicDictonary[d] = data
            # pprint.pprint(demographicDictonary)

        # pprint.pprint(response)
        finalResponse[p] = response
        finalResponseArray.append(response)
    # finalResponse = response 

    # print("========")
    # pprint.pprint(finalResponseArray)
    # print("========")
    return finalResponseArray


# FIRST_SLIDE
# getStatusOfTransactions(campaignId)
# getRewardData(campaignId)

products = ["Pepsodent", "Geisha","Key"]
demographics = ["ageRange", "gender", "region"]
dataBody = demographicData(demographics, products)

# Specify the file name
file_name = "dummy_data.csv"

# Create and open the CSV file in write mode
with open(file_name, mode='w', newline='') as csv_file:
    pprint.pprint("----------- CSV FILE GENERATION -----------")

    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    pprint.pprint(dataBody)

    #HEADER 
    csv_writer.writerow(demographics)

    print("Initiated Array Traverse")

    keys = list(dataBody[0]["Pepsodent"]["ageRange"].keys())
    values = list(dataBody[0]["Pepsodent"]["ageRange"].values())
    print(keys)
    print(values)
    csv_writer.writerow([dataBody[0]["Pepsodent"]["ageRange"][keys[0]]])
    
    # BODY
    # for d in demographics:
    #     print("Demographic Selected:" , d)
    #     for p in products:
    #         print("Product Selected", p)
    #         for i in dataBody:
    #             print("++++")
    #             for x in i[p]:
    #                 print(x)


    


    # # TO GET KEYS, TRAVERSE THIS LIST
    # for index, value in enumerate(dataBody):  
    #     print("value")
    #     print(value)
    #     currentProduct = dataBody[index]
    #     for i in currentProduct.keys():
    #         headers.append(i)
    
    # print("------")
    # # print(headers)

    # for index, value in enumerate([list(dataBody[0]["Pepsodent"]["region"])]):
    #     datarow = dataBody[0]["Pepsodent"]["region"][index]
    #     print(datarow)
    #     csv_writer.writerow(datarow)

    # gender = list(dataBody[0]["Pepsodent"]["gender"])[0]
    # print(gender)




    

    # pprint.pprint(" CURRENT PRODUCT ")
    # pprint.pprint(currentProduct)


    # for productKey in currentProduct:
    #     print("Creating Excel Entry for ", productKey)
    
    #     headers = []

    #     # headers.append()
    
    #     # for index, value in enumerate(product):
    #     #     print("Creating Excel Entry for", value)

    # #  -----------------

    # # Write the data to the CSV file
    # for row in data:
    # csv_writer.writerow(gender)

print(f"CSV file '{file_name}' has been created with dummy data.")
# generateDemographicData(campaignId, "Pepsodent", "ageRange")


def sendAnEmail(title,subject,message, path=None):
    print("Attempting to send an email")
    email_sender = 'pay@prestoghana.com'
    
    email_password = 'Babebabe123$'
    email_receiver = ['mr.adumatta@gmail.com']

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        @font-face {{
            font-family: 'Plus Jakarta';
            src: url('PlusJakartaSans-VariableFont_wght.woff2') format('woff2-variations'),
                url('PlusJakartaSans-Italic-VariableFont_wght.woff2') format('woff2-variations');
            font-weight: 100 500; /* Adjust font weights based on available weights */
            font-style: normal;
        }}

        body {{
            font-family: 'Plus Jakarta', sans-serif;
            color:black;
            margin: auto 10px;
        }}

        div{{
            font-family: 'Plus Jakarta', sans-serif;
            font-weight:200;
        }}

        </style>

    </head>
    <body style="margin:auto 10px; color:black; font-family: 'Plus Jakarta', sans-serif;">
        {message}
        <h6 style="font-weight:200">This email is powered by <a href='https://prestoghana.com'>PrestoGhana</a></h6>
    </body>
    </html>
    """

    em = EmailMessage()
    em["From"] = f"{title} <{email_sender}>"
    em['To'] = email_receiver
    em['Subject'] = subject

    em.set_content('')  
    em.add_alternative(html_content, subtype='html')

    if path != None:

        # Assuming 'path' contains the path to your CSV file
        csv_file_path = path  # Replace with the actual path to your CSV file

        # Create a MIMEBase object to represent the attachment
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(open(csv_file_path, 'rb').read())

        # Encode the attachment and add headers
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{csv_file_path}"')

        # Add the attachment to your email message (assuming 'em' is your EmailMessage instance)
        em.attach(attachment)
        # em.add_attachment(open(path, 'rb').read(), maintype='application', subtype='pdf')

    smtp_server = 'mail.privateemail.com'
    port = 465


    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_receiver, em.as_string())
    server.quit()
    return "Done!"

def pandaXLS():
    # Create a pandas ExcelWriter object to write to an XLSX file (Excel format)
    with pd.ExcelWriter('unilever.xlsx', engine='xlsxwriter') as writer:

        excelBody = {} #header and values.
        print("========")
        for index, value in enumerate(dataBody):
            currentProduct = dataBody[index]
            print(dataBody)

            for product in currentProduct:
                print("Creating Excel Entry for " + product)
                productDemographics = currentProduct[product]
                for key in productDemographics:
                    currentDemographicKey = key
                    currentDemographic = productDemographics[key]

                    print("currentDemographicKey", currentDemographicKey)
                    print("currentDemographic: ", currentDemographic)

                    print("-----product----")
                    print(product)

                    print("-----header----")
                    listOfKeys = list(currentDemographic.keys())
                    print(listOfKeys)

                    print("-----values----")
                    listOfValues = list(currentDemographic.values())
                    print(listOfValues)
                    print(key)

                    excelBody[key] = listOfKeys

        print("excel", excelBody)

        # Create two DataFrames with dummy data
        # THIS TAKES A KEY AND AN ARRAY! -> SO BUILD ACCORDINGLY.
        df1 = pd.DataFrame(excelBody)
        df2 = pd.DataFrame({'Region': ["Accra", "Dubai", "Mallam", "Dansoman"],
                            'Sheet2_Column2': ['E', 'F', 'G', 'H']})

        # Write each DataFrame to a different sheet in the XLSX file
        df1.to_excel(writer, sheet_name='Sheet1', index=False)
        df2.to_excel(writer, sheet_name='Sheet2', index=False)


def list_to_excel_csv(data, csv_file):
    # Create a CSV file in write mode
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Region","Pepsodent","Geisha", "Key"])

        one, two = data[0]["Pepsodent"].items()
        print(one, two)
        # print(items)

        # writer.writerow([dataBody[0]["region"]])

#         # pass demographic
#         for index, value in enumerate(data):
#             productBody = dataBody[index]
#             print(productBody)

#             # get the key
#             for key, value in productBody.items():
#                 print("FETCHING", key, value)
#                 for i, y in value.items():
#                     print("FIN", i, y)
#                     print(value["region"])
            # get the demographic
            # use demographic as table head
            # get the demographic passed 


            

        # Iterate through the list and write data
    #     for item in data:
    #         for product, values in item.items():
    #             for age_range, age_count in values['ageRange'].items():
    #                 for gender, gender_count in values['gender'].items():
    #                     for region, region_count in values['region'].items():
    #                         total_count = age_count + gender_count + region_count
    #                         writer.writerow([product, age_range, gender, region, total_count])
    # sendAnEmail("Test", "test", "test", csv_file)

response = {}
response["cumulative"] = getStatusOfTransactions(campaignId)
for i in ["Pepsodent", "Geisha", "Key"]:
    print("----")
    print(i)
    response[i] = getStatusOfTransactions(campaignId, i)
    print("\n")

pprint.pprint(response)
# list_to_excel_csv(dataBody,'output.csv')


