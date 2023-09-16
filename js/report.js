print("Msisdn", "Loyalty", "Product", "Count", "Location/Region", "Station", "Status");
db.wallet.find({ campaignId: "6448fd9329b3cbd2f1b3f22e" }).forEach(function (wallet) {
  const aggregationResult = db.PromoTransaction.aggregate([
    {
      $match: {
        _id: { $ne: null },
        msisdn: wallet.userId,
        transaction_result: "WIN",
        campaignId: "6448fd9329b3cbd2f1b3f22e"
      },
    },
    {
      $group: {
        _id: "$product",
        station: { $first: "$station" },
        count: { $sum: 1 },
      },
    },
    {
      $limit: 1, // Get only the first document (highest count)
    }

  ]).toArray();

  const campaignClient = db.CampaignClient.findOne({ msisdn: wallet.userId, $or: [{ location: { $ne: null } }, { region: { $ne: null } }] });


  if (aggregationResult.length > 0 && campaignClient !== null) {

    const productWithHighestCount = aggregationResult[0];
    const locationOrRegion = campaignClient.location ? campaignClient.location : campaignClient.region;
    print(wallet.userId + "," + wallet.loyaltyPoints + "," + productWithHighestCount._id + "," + productWithHighestCount.count + "," + locationOrRegion + "," + productWithHighestCount.station + "," + campaignClient.region);
  }
});


