print("Msisdn", "Loyalty", "Product", "Count", "Location/Region", "Station", "Status");

const findResult = db.PromoTransaction.find({
  campaignId: "6448fd9329b3cbd2f1b3f22e",
  transaction_result: {
      $in: [ "USED", "INVALID"]
  }
})

print(findResult)


