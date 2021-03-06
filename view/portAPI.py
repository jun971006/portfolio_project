from flask import Blueprint, flash, session, render_template, jsonify, request, redirect, url_for
from .db import connect_mongo, portsDAO, commentsDAO
import time
from werkzeug.utils import secure_filename

db_connection = connect_mongo.ConnectDB().db
ports = portsDAO.Ports(db_connection)
comments = commentsDAO.Comments(db_connection)

portAPI = Blueprint('portAPI', __name__, template_folder='templates')

def dict_merge(x, y):
	return {**x, **y}

@portAPI.route('/port')
def port():
	port_all = ports.getAllports()
	if "userEmail" in session:
		return render_template("portfolio.html", info=session["userEmail"], port_all=port_all)
	else:
		return render_template("portfolio.html", port_all=port_all)


@portAPI.route('/port/<int:index>',  methods=["GET", "POST"])
def portView(index):
	if "userEmail" in session:
		comment_all = comments.getAllcomments(index)
		result = ports.findOnePort(index)
		print(comment_all)
		return render_template("readMore.html", Index=index, info=session["userEmail"], port=result, comments=comment_all)
	
	else:
		comment_all = comments.getAllcomments(index)
		result = ports.findOnePort(index)
		print(comment_all)
		return render_template("readMore.html", Index=index, port=result, comments=comment_all)

@portAPI.route("/port/create", methods=["GET", "POST"])
def portCreate():
	if request.method == "GET":
		if "userEmail" in session:
			if "admin@admin" in session["userEmail"]:
				return render_template("CPortfolio.html")
			else:
				flash('You have to admin logged in')
				return redirect(url_for('portAPI.port'))

		else:
			flash('You have to admin logged in')
			return redirect(url_for('portAPI.port'))

	if request.method == "POST":
		if "userEmail" in session:
			if "admin@admin" in session["userEmail"]:
				f = request.files['portImage']
				f.save("./static/img/" + secure_filename(f.filename))
				image = secure_filename(f.filename)
				print(image)
				imagepath = "../../static/img/" + image
				print(imagepath)
				find = list(ports.getAllports())
				if not find:
					index = 1
				
				else:
					index = find[-1]["index"] + 1
				
				now = time.strftime("%Y-%m-%d %H:%M")
				

				obj_id = ports.portCreate(dict_merge({"index":index,"portAuthor":session["userEmail"],"portDate":now, "imagepath":imagepath}, request.form.to_dict(flat="true")))
				return redirect(url_for('portAPI.port'))

			else:
				flash('You have to admin logged in')
				return redirect(url_for('portAPI.port'))

		else:
			flash('You have to admin logged in')
			return redirect(url_for('portAPI.port'))

@portAPI.route("/port/update", methods=["POST"])
def portUpdate():
	if "userEmail" in session:
		if "admin@admin" in session["userEmail"]:
			f = request.files['portImagepath']
			if f:
				f.save("./static/img/" + secure_filename(f.filename))
				image = secure_filename(f.filename)
				print(image)
				iimagepath = "../../static/img/" + image
				print(iimagepath)
				print(request.form.to_dict(flat=True)["obj_id"])
				ports.portUpdate(dict_merge({"imagepath":iimagepath}, request.form.to_dict(flat=True)))
			else:
				ports.portUpdate(request.form.to_dict(flat=True))
			return redirect(url_for('portAPI.port'))
		else:
			flash('You have to admin logged in')
			return redirect(url_for('userAPI.login'))
	else:
			flash('You have to admin logged in')
			return redirect(url_for('userAPI.login'))

@portAPI.route("/port/remove", methods=["POST"])
def portRemove():
	if "userEmail" in session:
		if "admin@admin" in session["userEmail"]:
			ports.portDelete(request.form.to_dict(flat=True)["obj_id"])
			return redirect(url_for('portAPI.port'))
		else:
			flash('You have to admin logged in')
			return redirect(url_for('userAPI.login'))
	else:
			flash('You have to admin logged in')
			return redirect(url_for('userAPI.login'))
 	