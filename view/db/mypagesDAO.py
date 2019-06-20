import pymongo
from bson.objectid import ObjectId

class Mypages():
	def __init__(self, db):
		self.mypages = pymongo.collection.Collection(db, 'Mypages')

	def mypageCreate(self, mypageDict):
		try:
			self.mypages.insert_one({"myUserEmail":mypageDict})
			return True
		except:
			return False

	def mypageUpdate(self,mypageDict):
		self.mypages.find_and_modify(
			{"_id": ObjectId(mypageDict["obj_id"])},
			{"$set":{"myNickname":mypageDict["myNickname"], "myContent":mypageDict["myContent"], "myPhoneNum":mypageDict["myPhoneNum"],"myImagepath":mypageDict["myImagepath"]}},
			upsert=False
			)
		return True

			
	def getOnemypage(self, myUserEmail):
		try:
			result = self.mypages.find_one({"myUserEmail" : myUserEmail})
			return result
		except:
			return False