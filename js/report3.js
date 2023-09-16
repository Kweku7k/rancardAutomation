print(
    "Msisdn",
    "Loyalty",
    "Product",
    "Count",
    "Location/Region",
    "Station",
    "Status"
  );
  
  const finalResult = [];
  
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
      }
    ]).toArray();
  
    const campaignClient = db.CampaignClient.findOne({ msisdn: wallet.userId, $or: [{ location: { $ne: null } }, { region: { $ne: null } }] });
  
    if (aggregationResult.length > 0 && campaignClient !== null) {
      aggregationResult.forEach(function (productWithCount) {
        const locationOrRegion = campaignClient.location ? campaignClient.location : campaignClient.region;
        finalResult.push({
          userId: wallet.userId,
          loyalty: wallet.loyaltyPoints,
          product: productWithCount._id,
          count: productWithCount.count,
          locationRegion: locationOrRegion,
          station: productWithCount.station,
          region: campaignClient.region
        });
      });
    }
  });
  
  // Sort the final result by count in descending order
  finalResult.sort((a, b) => b.count - a.count);
  
  // Print the sorted result
  finalResult.forEach((item) => {
    print(item.userId + "," + item.loyalty + "," + item.product + "," + item.count + "," + item.locationRegion + "," + item.station + "," + item.region);
  });
  