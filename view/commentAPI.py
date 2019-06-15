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

