from flask import Blueprint, flash, session, render_template, jsonify, request, redirect, url_for
from .db import connect_mongo, postsDAO
import time

db_connection = connect_mongo.ConnectDB().db
posts = postsDAO.Posts(db_connection)

postAPI = Blueprint('postAPI', __name__, template_folder='templates')

def dict_merge(x, y):
	return {**x, **y}

@postAPI.route('/post', methods=["GET", "POST"])
def post():
	if request.method == "GET":
		if "userEmail" in session:
			return render_template("post.html", info=session["userEmail"], post_all=posts.getAllposts())
		else:
			flash('You have to login first!')
			return redirect(url_for('userAPI.login'))

	if request.method == "POST":
		if "userEmail" in session:
			now = time.strftime("%Y-%m-%d %H:%M")
			obj_id = posts.postCreate(dict_merge({"postAuthor":session["userEmail"],"postDate":now}, request.form.to_dict(flat="true")))
			return redirect(url_for('postAPI.post'))
		else:
			flash('You have to login first!')
			return redirect(url_for('userAPI.login'))


