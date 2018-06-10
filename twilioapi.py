from flask import Flask, request
import requests
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from flask import url_for
import speech_recognition as sr
import requests
import urllib
import vlc
import time
import json

app = Flask(__name__)

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
globalSid = ''


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    global globalSid
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/completed', timeout=10)
    if globalSid != request.values['CallSid']:
        gather.say('Hi, Welcome to XPO Support.', voice='woman', language='en-IN')
    resp.append(gather)
    return str(resp)


@app.route("/completed", methods=['GET', 'POST'])
def answer_call2():
    global globalSid
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()
    try:
        globalSid = request.values['CallSid']
        url = "http://localhost:5005/conversations/"+ request.values['CallSid']+"/respond"
        payload = "{\"query\":\""+request.values['SpeechResult']+"\"}"
        headers = {
			'content-type': "application/json",
			'cache-control': "no-cache",
			'postman-token': "9f483742-6dba-b699-fe81-7e3f5e474af8"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        responseData = json.loads(response.text)
        print('Human -> ' + request.values['SpeechResult'])
        print('Bot   -> ' + responseData[0]['text'])
        spit_out_text = responseData[0]['text']
        resp.say(spit_out_text, voice='woman', language='en')
        resp.redirect('/answer')
    except Exception as e:
        print(str(e))
        resp.say('I am having trouble understanding you.', voice='woman', language='en-IN')
        resp.redirect('/answer')
    return str(resp)

@app.route("/triggerCall", methods=['GET', 'POST'])
def triggerCall():
    global globalSid
    call = client.calls.create(
        to='+917406172019',
        from_='+16104631764',
        url='http://bbf7a186.ngrok.io/outbound'
        )

    return str('ok')

@app.route('/outbound', methods=['POST'])
def outbound():
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/completed', timeout=10)
    if globalSid != request.values['CallSid']:
        gather.say('Hi, Welcome to XPO Support. Do you have some time to give us a feedback?', voice='woman', language='en-IN')
    resp.append(gather)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
