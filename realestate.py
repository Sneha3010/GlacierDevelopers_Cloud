from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import logging

app = Flask(__name__)

# Connecting to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/projectdb'
db = SQLAlchemy(app)

# Creating a model for Real Estate Company. 
class re_Details(db.Model):
	__tablename__ = 'realestate'
	M1sID = db.Column('m1sid', db.VARCHAR(20), primary_key=True)
	Value = db.Column('value', db.Integer)

	def __init__(self, M1sID, Value):
		self.M1sID = M1sID
		self.Value = Value

# Create a route for posting M1sID and Value of properties to database using Postman
@app.route('/', methods=['GET', 'POST'])
def index():
	f = open("log.txt", "w+")
	if request.method == 'POST':
		for i in range(1):
			f.write("Method: POST, \nEndpoint: http://127.0.0.1:8003/, \nParameters: M1sID: "+request.form['M1sID']+", Value: "+request.form['Value']+" %d\r\n" % (i))
		M1sID = request.form['M1sID']
		Value = request.form['Value']
		Value = (Value + str(1111)) #parsing logic to XML...
		realestate = re_Details(M1sID, Value)
		db.session.add(realestate)
		db.session.commit()
		return "<p> Data updated </p>"
	f.close()

# Getting the M1sID i.e. the urls of properties from database
@app.route('/m1sid', methods=['GET'])
def get_Properties():
	re_Details1 = re_Details.query.all()
	f = open("log.txt", "a+")

	m1sid =""
	value=""

	for details in re_Details1:
		m1sid+= details.M1sID+ " "
		value+= str(details.Value)+ " "
	
	f.write("Method: GET, \nEndpoint: http://127.0.0.1:8003/m1sid,\nParameters: [m1sid: "+m1sid+", value: "+value+"] \r\n\n\n")
	f.close()
	realestate=re_Details.query.all()

	return render_template('re_index.html', realestate=re_Details.query.all())

#Getting the value of apartments based on their IDs from the database. 
@app.route('/property/<string:M1sID>/<string:Value>', methods=['GET', 'POST'])
def property(M1sID, Value):
	f = open("log.txt", "w+")
	f.write("Method: GET \nEndpoint: http://127.0.0.1.8003/property/<string:M1sID>/<string:Value>, \nParameters: [m1sid: "+m1sid+", value: "+value+"] \r\n\n\n")
	f.close()

	get_user = re_Details.query.filter_by(M1sID=M1sID).first()

# Posting the User's name and value of property to the insurance company
	if request.method == 'POST':
	f = open("log.txt", "w+")
	f.write("Method: POST \nEndpoint: http://127.0.0.1.8003/property/<string:M1sID>/<string:Value>, \nParameters: Name: "+request.form['Name']+", Value: "+request.form['Value']+" \r\n\n\n")
	f.close()

		Name =  request.form['Name']
		Value = request.form['Value']

		
		r = requests.get(str('http://127.0.0.1:8004/insurance')+'?Name='+str(Name)+ '&Value='+str(get_user.Value)+'&M1sID='+str(get_user.M1sID) )
		if r.text == 'success':
			message = 'Employee details submitted sucessfully to MBR portal.'
			return render_template('re_updatestatus.html', message=message)
		else:
			return "<h1> details updated. </h1>"

	
	return render_template('re_property.html', M1sID=M1sID, Value=Value)

if __name__ == '__main__':
	app.run(debug=True, port=8003)