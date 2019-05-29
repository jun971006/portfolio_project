import pymongo
from bson.objectid import ObjectId

class Posts():
	def __init__(self, db):
		self.posts = pymongo.collection.Collection(db, 'Posts')

	def postDelete(self,postDict):
		try:
			obj_id = self.posts.insert_one(postDict).inserted_id
			return obj_id
		except:
			return False

	def postDelete(self, obj_id):
		try:
			self.posts.delete_one({"_id":ObjectId(obj_id)})
			return True
		except:
			return False
	def postUpdate(self,postDict):
		self.posts.find_and_modify(
			{"_id": ObjectId(postDict["obj_id"])},
			{"$set":{"postTitle":postDict["postTitle"],"postContent":postDict["postContent"]}},
			upsert=False
			)
		return True
	def getAllposts(self):
		try:
			 result = self.posts.find({})
			 return result
		except:
			return False