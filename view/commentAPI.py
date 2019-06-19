from flask import Blueprint, flash, session, render_template, jsonify, request, redirect, url_for
from .db import connect_mongo, commentsDAO
import time

db_connection = connect_mongo.ConnectDB().db
comments = commentsDAO.Comments(db_connection)

commentAPI = Blueprint('commentAPI', __name__, template_folder='templates')

def dict_merge(x, y):
	return {**x, **y}

@commentAPI.route('/comment/create', methods=["POST"])
def commentCreate():
	if request.method == "POST":
		now = time.strftime("%Y-%m-%d %H:%M")
		dic_index = int(request.form.to_dict(flat="true")["commentIndex"], base=10)
		print(type(dic_index))
		print(dic_index)
		obj_id = comments.commentCreate(dict_merge({"commentDate":now}, request.form.to_dict(flat="true")))
		return redirect(url_for('portAPI.portView',index=dic_index))

@commentAPI.route("/comment/update", methods=["POST"])
def commentUpdate():
	dic_to_update = comments.getOnecomment(request.form.to_dict(flat=True)["obj_id"])
	dic_index = int(request.form.to_dict(flat="true")["commentIndex"], base=10)
	print(dic_to_update)
	if "userEmail" in session:
		if "admin@admin" in session["userEmail"]:
			comments.commentUpdate(request.form.to_dict(flat=True))
			return redirect(url_for('portAPI.portView',index=dic_index))
		else:
			if "userEmail" == dic_to_update["commentAuthor"]:	
				comments.commentUpdate(request.form.to_dict(flat=True))
				return redirect(url_for('portAPI.portView',index=dic_index))
			else:
				flash('You have no permission to update')
				return redirect(url_for('portAPI.portView',index=dic_index))
	else:
		pw = request.form.to_dict(flat=True)["commentPW"]
		if dic_to_update["commentPW"] == pw:
			comments.commentUpdate(request.form.to_dict(flat=True))
			# flash('You have to admin logged in')
			return redirect(url_for('portAPI.portView',index=dic_index))
		else:
			flash('You entered wrong password in')
			return redirect(url_for('portAPI.portView',index=dic_index))

@commentAPI.route("/comment/remove", methods=["POST"])
def commentRemove():
	dic_index = int(request.form.to_dict(flat="true")["commentIndex"], base=10)
	dic_to_remove = comments.getOnecomment(request.form.to_dict(flat=True)["obj_id"])
	if "userEmail" in session:
		if "admin@admin" in session["userEmail"]:
			comments.commentDelete(request.form.to_dict(flat=True)["obj_id"])
			return redirect(url_for('portAPI.portView',index=dic_index))
		else:
			if session["userEmail"] == dic_to_remove["commentAuthor"]:	
				comments.commentDelete(request.form.to_dict(flat=True)["obj_id"])
				return redirect(url_for('portAPI.portView',index=dic_index))
			else:
				flash('You have no permission to update')
				return redirect(url_for('portAPI.portView',index=dic_index))
	else:
		pw = request.form.to_dict(flat=True)["commentPW"]
		if dic_to_remove["commentPW"] == pw:
			comments.commentDelete(request.form.to_dict(flat=True)["obj_id"])
			return redirect(url_for('portAPI.portView',index=dic_index))
		else:
			flash('You entered wrong password in')
			return redirect(url_for('portAPI.portView',index=dic_index))
