from flask import Flask, render_template, request, flash, logging, url_for, redirect, jsonify, make_response, session, g
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import logging
import xml.etree.ElementTree as ET
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github 
import os 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/projectdb'
app.config['SECRET_KEY'] = 'thisisasecretkey'

# Source: https://stackoverflow.com/questions/27785375/testing-flask-oauthlib-locally-without-https
# for github HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

twitter_blueprint = make_twitter_blueprint(api_key='snajatcEGgC19dwf9AFNQMtM8 ', api_secret='ieX5hO4amP6ay6bkPCyY1Bfla9BtWMla7NWRN9nyzu4tDdVKR4')
github_blueprint = make_github_blueprint(client_id='b1198cf45b0983ee621f', client_secret='80ad32fdf60fc3350e398da866e77891075d15b4')

app.register_blueprint(twitter_blueprint, url_prefix = '/twitter_login')
app.register_blueprint(github_blueprint, url_prefix = '/github_login')

db = SQLAlchemy(app)

employee_id = '1'

class Employee_details(db.Model):
	__tablename__ = 'emp_employee'
	username = db.Column('username', db.Unicode, primary_key=True)
	password = db.Column('password', db.Unicode)
	emp_name = db.Column('emp_name', db.Unicode)
	salary = db.Column('salary', db.Integer)
	emp_start_date = db.Column('emp_start_date', db.DateTime)


@app.route('/')
def home(): 
# if github.authorized:
	print("A")
	account_info = github.get('/user')
	print(account_info)
	git_username = ''
	print(git_username)
	print('Checking uname')
	if account_info.ok:
		print('Checking uname started')
	account_info_json = account_info.json()
	git_username = account_info_json['login']
	print(git_username)
	session['user'] = git_username
	print("Reach")
	return redirect(url_for('addEmployer',  username=session['user']))
	return render_template('employer_home.html')

@app.before_request
def before_request():
	g.user =None
	if 'user' in session:
		g.user = session['user']


# @app.route('/github')
# def github_login():	
# 	account_info = github.get('/user')
# 	print('4')
# 	if account_info.ok:
# 		account_info_json = account_info.json()

# 		return '<h1> Your GitHub name is @{}'.format(account_info_json['login'])


@app.route('/github_login', methods=['GET', 'POST'])
def github_login():

	

	session.pop('user', None)
	# print('1')
	# if not twitter.authorized:
	# 	print('2')
	# 	return redirect(url_for('twitter.login'))
	# print('3')
	# account_info = twitter.get('account/settings')
	# print('4')
	# if account_info.ok:
	# 	account_info_json = account_info.json()

	# 	return '<h1> Your Twitter name is @{}'.format(account_info_json['screen_name'])

	# Correct code
	# if not github.authorized:
	# 	return redirect(url_for('github.login'))
	# account_info = github.get('/user')
	# git_username = ''
	# if account_info.ok:
	# 	account_info_json = account_info.json()
	# 	git_username = account_info_json['login']



	f = open("log1.txt", "a+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8001/login \nparameters: None\n" )
	f.close()
	# Employee_details1 = Employee_details.query.filter_by(username=username),first()
	
	

	if request.method == 'POST':
		f = open("log1.txt", "a+")
		f.write("method: POST \nEnd-point: http://127.0.0.1:8001/login \nparameters: Login from git ")
		f.close()

		### CODE FOR OAUTH
		print("Reach0")
		if not github.authorized:
			print("NA")
			return redirect(url_for('github.login'))
		print("A")
		account_info = github.get('/user')
		print(account_info)
		git_username = ''
		print(git_username)
		print('Checking uname')
		if account_info.ok:
			print('Checking uname started')
			account_info_json = account_info.json()
			git_username = account_info_json['login']
			print(git_username)
			session['user'] = git_username
			print("Reach")
			return redirect(url_for('addEmployer',  username=session['user']))

		## MAINSTREAM LOGIN
		# for i in range(1):
		# 	f.write("POST, http://127.0.0.1:8001/login, username: "+request.form['username']+", password: "+request.form['password']+" %d\r\n" % (i))
		# emppass = request.form
		# username = request.form['username']
		# get_emp = Employee_details.query.filter_by(username=username).first()
		# password = request.form['password']


		# pathToXML = "Salt.xml"
		# tree = ET.parse(pathToXML)
		# root = tree.getroot()

		# # all items data
		# print('Expertise Data:'+str(root)+str(tree))
		# salt = ''
		# for elem in root:
		# 	salt = elem.text


		# if get_emp is None:
		# 	error = 'User not present! Try again.'
		# 	return render_template('login.html', error = error)
		# if  get_emp.password != password+salt:
		# 	error = 'Password do not match! Try again.'
		# 	return render_template('login.html', error = error)
		# else:
		# session['user'] = username
		# return redirect(url_for('addEmployer',  username=session['user']))
		
		
	# return '<h1>Request failed! <h1>'
	# return render_template('login.html')
	return render_template('github_login.html')


@app.route('/employer_form/<string:username>', methods=['POST','GET'])
def addEmployer(username):
	f = open("log1.txt", "a+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8001//employer_form/<string:username> \nparameters: None\n" )
	f.close()


	if request.method == 'POST':
		print(g.user)
		# f = open("log1.txt", "a+")
		# f.write("method: POST \nEnd-point: http://127.0.0.1:8001//employer_form/<string:username> \nparameters: username: "+request.form['username']+", application_no: "+request.form['application_no']+", mbr_web_service: "+request.form['mbr_web_service']+" ")
		# f.close()

		employee = Employee_details()
		employerDetails = request.form
		username = employerDetails["username"]
		application_number = employerDetails["application_no"]
		mbr_web_service_address = employerDetails["mbr_web_service"]

		get_employee = Employee_details.query.filter_by(username=g.user).first()
		url = str(mbr_web_service_address)+'?salary='+str(get_employee.salary)+'&application_number='+str(application_number)+'&emp_name='+str(get_employee.emp_name)+'&emp_start_date='+str(get_employee.emp_start_date)
		print(url)
		try:

			r = requests.get(str(mbr_web_service_address)+'?salary='+str(get_employee.salary)+'&application_number='+str(application_number)+'&emp_name='+str(get_employee.emp_name)+'&emp_start_date='+str(get_employee.emp_start_date))
		except:
			message = 'Invalid endpoint. try again'
			return render_template('employer_updatestatus.html', message=message)

		if r.text == 'success':

			message = 'Employee details submitted sucessfully to MBR portal.'
			return render_template('employer_updatestatus.html', message=message)
		else:

	 		return "<h1> Error occured while submitting details to MBR portal. </h1>"
	 		db.session.close_all()
	 		db.session.add(employee)
	 		db.session.commit()

	 		return"<h1> Employee details submitted sucessfully. </h1>"
	else:
		if g.user:
			return render_template('employer_form.html', username=username)


	return redirect(url_for('github.login'))

@app.route('/logout', methods=['GET'])
def logout():
	f = open("log1.txt", "w+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8001/logout \nparameters: logged out\n" )
	f.close()
	session.pop('user', None)
	# session.pop('user', None)
	return redirect(url_for('github_login'))

if __name__ == '__main__':
	app.secret_key = 'abcdweb'
	app.run(debug=True, port=8001)