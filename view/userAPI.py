from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from .db import connect_mongo, usersDAO, mypagesDAO

db_connection = connect_mongo.ConnectDB().db
users = usersDAO.Users(db_connection)
mypages = mypagesDAO.Mypages(db_connection)

userAPI = Blueprint('userAPI', __name__, template_folder='templates')

@userAPI.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'GET':
		if not 'userEmail' in session:
			return render_template('signup.html')
		# return render_template('welcome.html', info = session['userEmail'])
		return redirect(url_for('portAPI.port'))
	elif request.method == 'POST':
		if not 'userEmail' in session:
			if users.userCreate(request.form.to_dict(flat='true')):
				mypages.mypageCreate(request.form.to_dict(flat='true')['userEmail'])
				session['userEmail'] = request.form['userEmail']
				return redirect(url_for('mypageAPI.mypage'))
			else:
				flash('Email is already Exists, try again with other Email.')
				return redirect(url_for('userAPI.signup'))		
		return redirect(url_for('mypageAPI.mypage'))
@userAPI.route('/')
def home():
	return redirect(url_for("portAPI.port"))

@userAPI.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		if 'userEmail' in session:
			return redirect(url_for('portAPI.port'))
			# return render_template('portfolio.html')
		return render_template('login.html')
	elif request.method == 'POST':
		if 'userEmail' in session:
			return redirect(url_for('portAPI.port'))
		else:
			if users.userAuthentication(request.form.to_dict(flat='true')):
				session['userEmail'] = request.form['userEmail']				
				# return render_template('welcome.html', info = session['userEmail'])
				#return render_template('portfolio.html', info= session['userEmail'])
				return redirect(url_for('portAPI.port'))
			else:
				flash('Wrong ID or PW, You have to check your ID or PW', 'error')
				return redirect(url_for('userAPI.login'))
@userAPI.route('/logout')
def logout():
	if "userEmail" in session:
		session.pop('userEmail')
		return redirect(url_for('userAPI.login'))
	else:
		flash('You have to logged in')
		return redirect(url_for('userAPI.login'))



#if __name__ =='__main__':
#	userAPI.run(host = '0.0.0.0', port = 5000)
