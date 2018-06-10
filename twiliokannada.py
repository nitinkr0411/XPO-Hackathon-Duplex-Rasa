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
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
translator = Translator()


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
    gather = Gather(input='speech', action='/completed', timeout=5, language='en')
    if globalSid != request.values['CallSid']:
        gather.say('Willkommen beim xpo-Support.', voice='woman', language='de')
    resp.append(gather)
    return str(resp)


@app.route("/completed", methods=['GET', 'POST'])
def answer_call2():
    global globalSid
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()
    try:
        #convertedText = translator.translate(request.values['SpeechResult'], src='').text
        convertedText = request.values['SpeechResult']
        globalSid = request.values['CallSid']
        url = "http://localhost:5005/conversations/"+ request.values['CallSid']+"/respond"
        payload = "{\"query\":\""+convertedText+"\"}"
        headers = {
			'content-type': "application/json",
			'cache-control': "no-cache",
			'postman-token': "9f483742-6dba-b699-fe81-7e3f5e474af8"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        responseData = json.loads(response.text)
        print(responseData)
        convertedReply = translator.translate(responseData[0]['text'], src='en', dest='de').text
        print('Human -> ' + convertedText)
        print('Bot   -> ' + convertedReply)
        spit_out_text = convertedReply
        resp.say(spit_out_text, voice='woman', language='de')
        resp.redirect('/answer')
    except Exception as e:
        print(str(e))
        resp.say('I am having trouble understanding you.', voice='woman', language='hi')
        resp.redirect('/answer')
    return str(resp)

@app.route("/triggerCall", methods=['GET', 'POST'])
def triggerCall():
    global globalSid
    call = client.calls.create(
        to='+',
        from_='+16104631764',
        url='http://f5ce2f9a.ngrok.io/outbound'
        )
    return str('ok')

@app.route('/outbound', methods=['POST'])
def outbound():
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/completed', timeout=5)
    if globalSid != request.values['CallSid']:
        gather.say('Hi, I am Jane, calling on behalf on XPO. Do you have some time to give us a feedback?', voice='woman', language='hi')
    resp.append(gather)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
