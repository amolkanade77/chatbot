from posixpath import split
import sqlite3
from turtle import pd
from typing import Final
from flask import Flask, request,render_template
import requests

from twilio.twiml.messaging_response import MessagingResponse
from flask import jsonify
app = Flask(__name__)
app.debug = True
from flask_sqlalchemy import SQLAlchemy

# Import for Migrations
from flask_migrate import Migrate, migrate
# Settings for migrations
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopname=db.Column(db.String(20), unique=False, nullable=False)
    Orderone = db.Column(db.String(20), unique=False, nullable=False)
    ornumber =db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.String(20), unique=False, nullable=False)


conn = sqlite3.connect('site.db',check_same_thread=False)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    
    print(request.values.get)
    Finaldata=incoming_msg.splitlines()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'shopname' in incoming_msg:      
        new_user = Profile(shopname=Finaldata[0].split('-')[1],Orderone=Finaldata[1].split('-')[1],ornumber=Finaldata[2].split('-')[1],last_name=Finaldata[3].split('-')[1],age=Finaldata[4].split('-')[1])
        db.session.add(new_user)
        db.session.commit()
        quote="Your order saved SucessFully"
        msg.body(quote)
        responded = True
    if not responded:
        msg.body('Please place order!')
    return str(resp)


@app.route('/displaydata', methods=['GET'])
def display():
    users = Profile.query.all()
    return render_template("admin.html", data=users,len = len(users))


@app.route('/excel',methods=['GET']) 
def excel():
    
    data=pd.read_sql('SELECT *FROM profile',conn)
    finaexcel=data.to_excel("data.xlsx")
    # return render_template("admin.html", data=finaexcel)
    
    
       
   
