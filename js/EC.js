const query = {
    campaignId: "6448fd9329b3cbd2f1b3f22e",
    rewardType:"AIRTIME"
};

const findResult = db.PromoTransaction.find(query);

findResult.forEach(function (doc) {
    const msisdn = doc.msisdn;
    const rewardType = doc.rewardType;

    print(msisdn + "," + rewardType );
});