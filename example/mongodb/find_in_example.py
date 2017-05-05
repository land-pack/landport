from pymongo import MongoClient

client = MongoClient("192.168.41.54", 27017)

# db_name = "crazy_bet"
# db = client[db_name]
db = client.crazy_bet
db.add_user("crazy_bet", "crazy_bet_rw")
db.add_authenticate("crazy_bet_rw", "crazy_bet")

collection_useraction = db['yourcollection']
ret = collection_useraction.find()
for i in ret:
	print(ret)