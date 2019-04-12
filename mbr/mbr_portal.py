from flask import Flask, render_template, request, flash, logging, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/projectdb'
db = SQLAlchemy(app)

class Mortgage_details(db.Model):
	__tablename__ = 'mbr_mortgage_details'
	id = db.Column('id', db.Unicode, primary_key=True)
	name = db.Column('name', db.Unicode)
	address = db.Column('address', db.Unicode)
	phone_number = db.Column('phone_number', db.Integer)
	employer_info = db.Column('employer_info', db.Unicode)
	salary = db.Column('salary', db.Unicode)
	start_date=db.Column('start_date',db.DateTime)
	mortgage_value=db.Column('mortgage_value',db.Unicode)
	mortid=db.Column('mortid', db.Unicode)
	m1sid=db.Column('m1sid',db.Unicode)
	ins_value=db.Column('ins_value',db.Unicode)
	ded_value=db.Column('ded_value',db.Unicode)
	password = db.Column('password', db.Unicode)
	application_status = db.Column('application_status', db.Unicode)

class re_Details(db.Model):
	__tablename__ = 'realestate'
	M1sID= db.Column('m1sid', db.Unicode, primary_key=True)
	Value= db.Column('value', db.Unicode)
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	f = open("log2.txt", "w+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8000/login \nparameters: None\n" )
	f.close()
	if request.method == 'POST':

		f = open("log2.txt", "w+")
		f.write("Method: POST \nEndpoint: http://127.0.0.1.8000/login, \nParameters: userid: "+request.form['userid']+", name: "+request.form['name']+" \r\n\n\n")
		f.close()

		userid = request.form['name']
		get_user = Mortgage_details.query.filter_by(name=userid).first()
		password = request.form['password']
		
		if get_user.password == password :
			if get_user.address is None or get_user.phone_number is None or get_user.employer_info is None or get_user.salary is None or get_user.mortgage_value is None or get_user.start_date is None or get_user.m1sid is None or get_user.ins_value is None or get_user.ded_value: 
				get_user.application_status='Complete'
				print(get_user.application_status)
			else: 
				get_user.application_status='Incomplete'
				print(get_user.application_status)
			
			return render_template('updatemessage2.html',mo=get_user)
		else:
			error = 'Employee ID and password do not match! Try again.'
			return render_template('login.html', error = error)

	return render_template('login.html')


@app.route('/mbr/registration', methods=['GET', 'POST'])
def addEmployer():

	f = open("log2.txt", "w+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8000/mbr/registration \nparameters: None\n" )
	f.close()
	if request.method == 'POST':

		f = open("log2.txt", "w+")
		f.write("Method: POST \nEndpoint: http://127.0.0.1.8000/mbr/registration, \nParameters: address: "+request.form['address']+", name: "+request.form['name']+", contact_no: "+request.form['contact_no']+", employer_name: "+request.form['employer_name']+" \r\n\n\n")
		f.close()

	 	mbr=Mortgage_details()

	 	mbrDetails = request.form
	 	mbr.name=str(mbrDetails['name'])
	 	mbr.address=mbrDetails['address']
	 	mbr.phone_number=mbrDetails['contact_no']
	 	mbr.employer_info=mbrDetails['employer_name']
	 	mbr.password=mbrDetails['password']
	 	mbr.application_status='Incomplete'
	 	
	 	for x in range(1):
	 		_id= random.randint(1,100)
	 	mbr.id = str(_id)
	 	db.session.add(mbr)
	 	db.session.commit()
	 	return render_template('updatemessage1.html', mbr1 = _id)

	return render_template('registration.html')

@app.route('/mbr/application_status', methods=['GET'])
def addEmployeeDetails():
	f = open("log.txt2", "w+")
	f.write("Method: GET \nEndpoint: http://127.0.0.1.8000/mbr/application_status, \nParameters: [salary: "+salary+", aplication_number: "+application_number+", emp_name: "+emp_name+", emp_start_date: "+emp_start_date+" ] \r\n\n\n")
	f.close()


	salary = request.args['salary']
	aplication_number = request.args['application_number']
	name = request.args['emp_name']
	start_date = request.args['emp_start_date']

	mbr_details = Mortgage_details.query.filter_by(id=aplication_number).first()
	mbr_details.salary = salary
	mbr_details.name=name
	mbr_details.start_date=start_date
	
	db.session.commit()
	print('success')

	return 'success'

@app.route('/mbr/mortgage_request', methods=['GET','POST'])

def addMortgageRequest():
	f = open("log2.txt", "w+")
	f.write("method: GET \nEnd-point: http://127.0.0.1:8000/mbr/mortgage_request \nparameters: None\n" )
	f.close()
	if request.method == 'POST':

		f = open("log2.txt", "w+")
		f.write("Method: POST \nEndpoint: http://127.0.0.1.8000/mbr/mortgage_request, \nParameters: name: "+request.form['name']+", mortgage_value: "+request.form['mortgage_value']+" \r\n\n\n")
		f.close()

		mbrDetails=request.form
		name = request.form['name']
		mortgage_value = request.form['mortgage_value']
		M1sID = request.form.getlist('M1sID')
		
		mbr_details = Mortgage_details.query.filter_by(name=name).first()

		mbr_details.mortgage_value=mortgage_value
		mbr_details.M1sID=M1sID
		
		_mortid = ''
		for x in range(1):
	 		_mortid= random.randint(1,100)
		
		mbr_details.mortid = str(_mortid)	
		db.session.commit()
		return render_template('updatemessage3.html', mbr1 = _mortid)

	get_re= re_Details.query.all()
	
	return render_template('mor_registration.html',  mbr2 = get_re)


@app.route('/mbr/insurance', methods=['GET', 'POST'])
def addInsurance():
	f = open("log.txt2", "w+")
	f.write("Method: GET \nEndpoint: http://127.0.0.1.8000/mbr/insurance, \nParameters: [ins_value: "+ins_value+", ded_value: "+ded_value+", name: "+name+", misid: "+misid+" ] \r\n\n\n")
	f.close()
	ins_value = request.args['ins_value']
	ded_value = request.args['ded_value']
	name = request.args['name']
	misid=request.args['m1sid']

	mbr_details = Mortgage_details.query.filter_by(name=name).first()
	mbr_details.ins_value = ins_value
	mbr_details.name=name
	mbr_details.ded_value=ded_value
	mbr_details.m1sid=misid
	
	return 'success'	
	
	db.session.commit()


if __name__ == '__main__':
	app.secret_key = 'abcdweb'
	app.run(debug=True, port=8000)