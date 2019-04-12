from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import logging

app = Flask(__name__)

# Connecting to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/cloudproject'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/projectdb'
db = SQLAlchemy(app)

class re_Details(db.Model):
	__tablename__ = 'realestate'
	M1sID = db.Column('m1sid', db.VARCHAR(20), primary_key=True)
	# Name = db.Column(db.VARCHAR(20))
	# MortID = db.Column(db.VARCHAR(20))
	Value = db.Column('value', db.Integer)

	def __init__(self, M1sID, Value):
		self.M1sID = M1sID
		# self.MortID = MortID
		# self.Name = Name
		self.Value = Value



@app.route('/', methods=['GET', 'POST'])
def index():
	f = open("log.txt", "w+")
	if request.method == 'POST':
		# Name = request.form['Name']
		# MortID = request.form['MortID']
		for i in range(1):
			f.write("POST, http://127.0.0.1:8003/, M1sID: "+request.form['M1sID']+", Value: "+request.form['Value']+" %d\r\n" % (i))
		M1sID = request.form['M1sID']
		Value = request.form['Value']
		Value = (Value + str(1111)) #parsing logic to XML...
		realestate = re_Details(M1sID, Value)
		db.session.add(realestate)
		db.session.commit()
		return "<p> Data updated </p>"
	# f.write("END POST")
	f.close()
		# logging.debug('Data updated')

@app.route('/m1sid', methods=['GET'])
def get_Properties():
	re_Details1 = re_Details.query.all()
	f = open("log.txt", "a+")

	m1sid =""
	value=""
	# Myre_Details = re_Details1.query.all()

	for details in re_Details1:
		m1sid+= details.M1sID+ " "
		value+= str(details.Value)+ " "
	
	f.write("Method: GET, \nEndpoint: http://127.0.0.1:8003/m1sid,\nParameters: [m1sid: "+m1sid+", value: "+value+"] \r\n\n\n")
	f.close()
	realestate=re_Details.query.all()

	# for real in realestate:
	# 	print(real.M1sID)
	# 	print(real.Value)
	return render_template('re_index.html', realestate=re_Details.query.all())

@app.route('/property/<string:M1sID>/<string:Value>', methods=['GET', 'POST'])
def property(M1sID, Value):

	get_user = re_Details.query.filter_by(M1sID=M1sID).first()

	if request.method == 'POST':
		Name =  request.form['Name']
		Value = request.form['Value']
		# M1sID = request.form['M1sID']
		# MortID = request.form['MortID']

		
		r = requests.get(str('http://127.0.0.1:8004/insurance')+'?Name='+str(Name)+ '&Value='+str(get_user.Value)+'&M1sID='+str(get_user.M1sID) )
		if r.text == 'success':
			message = 'Employee details submitted sucessfully to MBR portal.'
			return render_template('re_updatestatus.html', message=message)
		else:
			return "<h1> details updated. </h1>"

	
	return render_template('re_property.html', M1sID=M1sID, Value=Value)




	

if __name__ == '__main__':
	app.run(debug=True, port=8003)