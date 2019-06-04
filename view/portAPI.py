from flask import Blueprint, flash, session, render_template, jsonify, request, redirect, url_for
from .db import connect_mongo, portsDAO
import time

db_connection = connect_mongo.ConnectDB().db
ports = portsDAO.Ports(db_connection)

portAPI = Blueprint('portAPI', __name__, template_folder='templates')

def dict_merge(x, y):
	return {**x, **y}

@portAPI.route('/port', methods=["GET", "POST"])
def port():
	if request.method == "GET":
		if "userEmail" in session:
			port_all = ports.getAllports()
			return render_template("portfolio.html", info=session["userEmail"], port_all=port_all)
		else:
			flash('You have to login first!')
			return redirect(url_for('userAPI.login'))

	if request.method == "POST":
		if "userEmail" in session:
			now = time.strftime("%Y-%m-%d %H:%M")
			obj_id = ports.portCreate(dict_merge({"portAuthor":session["userEmail"],"portDate":now}, request.form.to_dict(flat="true")))
			return redirect(url_for('portAPI.port'))
		else:
			flash('You have to login first!')
			return redirect(url_for('userAPI.login'))

@portAPI.route("/port/update", methods=["POST"])
def portUpdate():
	if "userEmail" in session:
		print(request.form.to_dict(flat=True)["obj_id"])
		ports.portUpdate(request.form.to_dict(flat=True))
		return redirect(url_for('portAPI.port'))
	else:
		flash('You have to logged in')
		return redirect(url_for('userAPI.login'))

@portAPI.route("/port/remove", methods=["POST"])
def portRemove():
	if "userEmail" in session:
		ports.portDelete(request.form.to_dict(flat=True)["obj_id"])
		return redirect(url_for('portAPI.port'))
	else:
		flash('You have to logged in')
		return redirect(url_for('userAPI.login'))