import pymongo
from bson.objectid import ObjectId

class Comments():
	"""docstring for Comments"""
	def __init__(self, db):
		self.comments = pymongo.collection.Collection(db, 'Comments')

	def commentCreate(self,commentDict):
		try:
			obj_id = self.comments.insert_one(commentDict).inserted_id
			return obj_id
		except:
			return False

	def commentDelete(self, obj_id):
		try:
			self.comments.delete_one({"_id":ObjectId(obj_id)})
			return True
		except:
			return False

	def commentUpdate(self,commentDict):
		self.comments.find_and_modify(
			{"_id": ObjectId(commentDict["obj_id"])},
			{"$set":{"commentContent":commentDict["commentContent"]}},
			upsert=False
			)
		return True
	def getAllcomments(self, Index):
		index = str(Index)
		try:
			 result = self.comments.find({"commentIndex" : index})
			 return result
		except:
			return False

	def getOnecomment(self, obj_id):
		try:
			result = self.comments.find_one({"_id" : ObjectId(obj_id)})
			return result
		except:
			return False