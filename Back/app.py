from flask import Flask, request, json, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal, fields
from flask_cors import CORS
from requests.utils import quote
import datetime
import os
import jwt
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bismillah@localhost:5432/Rotation'
app.config['SECRET_KEY'] = os.urandom(24)
JWTsecretKey = "aserehe"
CORS(app)

db = SQLAlchemy(app)

class Access_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    npk = db.Column(db.Integer())
    email = db.Column(db.String())
    password = db.Column(db.String())
    photo = db.Column(db.String())
    token = db.Column(db.String())

class Position(db.Model):
    position_code = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String())
    company = db.Column(db.String())
    cost_center = db.Column(db.String())
    personal_area = db.Column(db.String())
    personal_sub_area = db.Column(db.String())
    employee_type = db.Column(db.String())
    employee_group = db.Column(db.String())
    employee_sub_group = db.Column(db.String())

class Employee(db.Model):
    npk = db.Column(db.Integer, primary_key=True)
    position_code = db.Column(db.Integer())
    nama = db.Column(db.String())

class Request_Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer())
    record_id = db.Column(db.Integer())
    requester_npk = db.Column(db.Integer())
    employee_npk = db.Column(db.Integer())
    receiver_npk = db.Column(db.Integer())
    proposed_position_code = db.Column(db.Integer())
    distribution_cost_center = db.Column(db.Integer())
    dates = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    justify = db.Column(db.String())


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_data = request.get_json()

        req_email = request_data.get('email')
        req_password = request_data.get('password')

        userDB = Access_User.query.filter_by(email=req_email, password=req_password).first()
        if userDB is not None:
            payload = {
                "email" : userDB.email,
                "secretkey" : "asarehe"
            }

            encoded = jwt.encode(payload, JWTsecretKey, algorithm = 'HS256')
            return encoded, 201

        else:
            return 'Email or Password is not found' , 404
    else:
        return 'Method Not Allowed', 405



if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), host=os.getenv("HOST"), port=os.getenv("PORT"))
