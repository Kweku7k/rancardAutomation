const query = {
    campaignId: "6448fd9329b3cbd2f1b3f22e",
    transaction_result: {
        $in: ["USED", "INVALID"]
    }
};

const findResult = db.PromoTransaction.find(query);

findResult.forEach(function (doc) {
    const msisdn = doc.msisdn;
    const transaction_result = doc.transaction_result;

    print(msisdn + "," + transaction_result );
});