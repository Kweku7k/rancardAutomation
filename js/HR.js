print("MSISDN", "LOCATION", "REWARD","PRODUCT","SKU");

const query = {
    campaignId: "6448fd9329b3cbd2f1b3f22e",

    rewardType: {
            $nin: ["undefined"],
            $exists: true
          } 
    };

const findResult = db.PromoTransaction.find(query);

findResult.forEach(function (doc) {

    client = db.CampaignClient.find({msisdn:doc.msisdn})[0]

    const msisdn = doc.msisdn;
    const rewardType = doc.rewardType;
    const product = doc.product;
    const sku = doc.sku;
    const location = client.location ? client.location : client.region;
    const dateAdded = doc._created;

    print(msisdn + "," + location +","+rewardType+","+dateAdded+","+product+","+sku );
});


    