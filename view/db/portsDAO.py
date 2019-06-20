import pymongo
from bson.objectid import ObjectId

class Ports():
	def __init__(self, db):
		self.ports = pymongo.collection.Collection(db, 'Ports')

	def portCreate(self,portDict):

		try:
			obj_id = self.ports.insert_one(portDict).inserted_id
			return obj_id
		except:
			return False

	def portDelete(self, obj_id):
		try:
			self.ports.delete_one({"_id":ObjectId(obj_id)})
			return True
		except:
			return False

	def portUpdate(self,portDict):
		self.ports.find_and_modify(
			{"_id": ObjectId(portDict["obj_id"])},
			{"$set":{"portTitle":portDict["portTitle"],"portContent":portDict["portContent"], "imagepath":portDict["imagepath"]}},
			upsert=False
			)
		return True
	def getAllports(self):
		try:
			 result = self.ports.find({})
			 return result
		except:
			return False

	#TODO
	# port 디비에서 특정 id한개에 해당하는 portfolio만 가져온다.
	def findOnePort(self, Index):
		try:
			result = self.ports.find_one({"index" : Index})
			return result
		except:
			return False
