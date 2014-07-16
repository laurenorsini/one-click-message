from flask import Flask, render_template, flash, redirect, session, url_for, request, g, send_from_directory
from app import app #, db
from sqlalchemy import desc, insert
from flask.ext.sqlalchemy import SQLAlchemy
# from models import Message
from twilio.rest import TwilioRestClient 

client = TwilioRestClient ('ABC', '0123') # Paste in your AccountSID and AuthToken here
twilio_number = "+1234567890" # Replace with your Twilio number

# @app.before_request
# def before_request():
	# g.user = current_user
	# getmsgs = firebase.get('/messages', None)

@app.route('/')
def home():
	return render_template('pages/form.html')
  
@app.route("/submit-form/", methods = ['POST']) 
def submit_number():
    number = request.form['number']
    formatted_number = "+1" + number # Switch to your country code of choice
    client.messages.create(to=formatted_number, from_ = twilio_number, body = "Message of your choice to text people.") # Replace body with your message of choice
    return redirect('/messages/')
  
@app.route("/messages/")
def list_messages():
    messages = client.messages.list(to=twilio_number)
    return render_template('pages/messages.html', messages = messages)

#----------------------------------------------------------------------------#
# Error Handling
#----------------------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
	return render_template('errors/500.html'), 500

@app.errorhandler(404)
def internal_error(error):
	return render_template('errors/404.html'), 404