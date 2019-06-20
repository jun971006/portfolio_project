from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from .db import connect_mongo, mypagesDAO
from werkzeug.utils import secure_filename

db_connection = connect_mongo.ConnectDB().db
mypages = mypagesDAO.Mypages(db_connection)

mypageAPI = Blueprint('mypageAPI', __name__, template_folder='templates')

def dict_merge(x, y):
	return {**x, **y}

@mypageAPI.route('/mypage')
def mypage():
	
	if "userEmail" in session:
		mypage = mypages.getOnemypage(session["userEmail"])
		print(mypage)
		return render_template("Mypage.html", info=session['userEmail'], mypage=mypage)
	else:
		return redirect(url_for('userAPI.login'))

@mypageAPI.route('/mypage/update', methods=["POST"])
def mypageUpdate():
	if "userEmail" in session:		
		f = request.files['myImagepath']
		f.save("./static/img/" + secure_filename(f.filename))
		image = secure_filename(f.filename)
		print(image)
		imagepath = "../../static/img/" + image
		print(imagepath)
		mypages.mypageUpdate(dict_merge({"myImagepath":imagepath} ,request.form.to_dict(flat=True)))
		return redirect(url_for('mypageAPI.mypage'))
		# else:
		# 	flash('You have to admin logged in')
			# return redirect(url_for('userAPI.login'))
	else:
		flash('You have to logged in first')
		return redirect(url_for('userAPI.login'))