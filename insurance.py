from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sneha3010@localhost/cloudproject'
db = SQLAlchemy(app)

@app.route('/insurance', methods=['GET'])
def Insurance_Company():
	# print(request)
	# print(request.args['Name'])
	# print(request.args['M1sID'])


	Name = request.args['Name']
	Value = request.args['Value']
	M1sID = request.args['M1sID']
	# ins_value = request.args['ins_value']
	# Value = request.args['Value']
	# mbr_insurance = request.args['mbr_insurance']

	# get_value = re_Details.query.filter_by(M1sID=M1sID).first()

	# va = Value


	ded_value = 0.05 * float(Value)
	ins_value = float(Value) - ded_value


	# return 'Name :' +Name+ 'M1sID :' +M1sID+ 'ded_value :' +ded_value+ 'ins_value :' +ins_value

	r = requests.get(str('http://127.0.0.1:8000/mbr/insurance')+'?name='+str(Name)+ '&m1sid='+str(M1sID)+ '&ded_value='+str(ded_value)+'&ins_value='+str(ins_value))

	if r.text == 'success':
		return "<h1> Updated </h1>"
	else:
		return "<h1> Error occured while submitting details to MBR portal. </h1>"

	# template('property1.html', name=name, ded_value=ded_value, ins_value=ins_value)

if __name__ == '__main__':
	app.run(debug=True, port=8004)