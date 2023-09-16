print("MSISDN", "REWARD");
  db.PromoTransaction.aggregate([
    {
      $match: {
        rewardType: {
          $nin: ["AIRTIME", "MOMO"],
        },
        campaignId: "6448fd9329b3cbd2f1b3f22e"
      }
    },
    {
      $project: {
        _id: 0, 
        msisdn: 1,
        rewardType: 1
      }
    }
  ])




