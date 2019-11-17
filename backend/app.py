from flask import Flask, jsonify, request
from flask_cors import CORS
from faker import Faker
from chatBot import *
import json
import os
import random
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname

app = Flask(__name__)
CORS(app)
fake = Faker()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
api_key = os.environ['TWILIO_API_KEY']
api_secret = os.environ['TWILIO_API_SECRET'] 
auth_token = os.environ['TWILIO_AUTH_TOKEN']
service_sid = os.environ['TWILIO_CHAT_SERVICE_SID']

client = Client(account_sid, auth_token)
service = client.chat.services.create(friendly_name='friendly_name')

availableU = []
AIU = []
channel = None
@app.route('/')
def index():
    return 'Welcome to the website'


@app.route('/token')
def token():
    identity = fake.user_name()
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    chat_grant = ChatGrant(service_sid)
    token.add_grant(chat_grant)
    
    return jsonify(identity=identity, token=token.to_jwt().decode('utf-8'))
    
    
@app.route('/chat')
def chat():
    return identity

@app.route('/chat/find')
def findChat():
    global channel
    global availableU
    global AIU
    
    # Put user into "search" mode
    # When another user is found, create channel and invite both.
    # Chat happens     
    identity = str(request.args.get('id'))
    if random.random() < 0.2:
        AIU.append(identity)
        return ""

    availableU.append(identity)
    while (len(availableU)!=0):
        if len(availableU) == 1:
            channel = client.chat.services(service_sid).channels.create()
            return {
                "channelSid": channel.sid,
                "serviceSid": service.sid

            }
        if len(availableU) > 1:
            member = client.chat.services (service_sid).channels(channel.sid).members.create(identity=availableU.pop(0))
            member = client.chat.services(service_sid).channels(channel.sid).members.create(identity=availableU.pop(0))            
      
            return {
                "channelSid": channel.sid,
                "serviceSid": service.sid 
            }
            
    return 'Please wait'
   
# Once chat found, will communicate with Twillio to connect
# Once ended, will redirect to chat

@app.route('/chat/survey')
def chatSurvey(choice):
    if(choice in AIU):
        if(choice == 'y'):
            return 'Win'
        return 'lose'
    else:
        if(choice == 'y'):
            return 'lose'
        return 'Win'
        
@app.route('/test')
def static_file():

    messages = client.chat.services(service_sid).channels('CH34a4b25aec71481aaaba6ba89c68dce6').messages.list(limit=20)
    for record in messages:
        print(record.sid,str(record.body) )   
        
    message = client.chat.services(service_sid).channels('CH34a4b25aec71481aaaba6ba89c68dce6').messages.create(body='CUNT')
    print(message.sid,message.body)
    return "cunt"
    


@app.route('/health')
def health():
    return ""
    
if __name__ == '__main__':
    app.run()
