import speech_recognition as sr
import requests
import urllib
import vlc
import time
from mutagen.mp3 import MP3
from gtts import gTTS
import json
r = sr.Recognizer()
m = sr.Microphone()

try:
	while True:
		print("Preparing to listen, please wait...")
		with m as source: r.adjust_for_ambient_noise(source)
		#print("Set minimum energy threshold to {}".format(r.energy_threshold))
		print("I'm listening")
		with m as source: audio = r.listen(source)
		print("Recognizing...")
		try:
			# recognize speech using Google Speech Recognition
			value = r.recognize_google(audio)
			spit_out_text = "{}".format(value)
			print(spit_out_text)
			url = "http://localhost:5005/conversations/default/respond"
			payload = "{\"query\":\""+spit_out_text+"\"}"
			headers = {
				'content-type': "application/json",
				'cache-control': "no-cache",
				'postman-token': "9f483742-6dba-b699-fe81-7e3f5e474af8"
				}
			response = requests.request("POST", url, data=payload, headers=headers)
			print(response.text)
			responseData = json.loads(response.text)
			print(responseData[0]['text'])
			spit_out_text = responseData[0]['text']
			# spit_out_text is question here
			tts = gTTS(text=spit_out_text, lang='en')
			tts.save("neowin.mp3")
			audio = MP3("neowin.mp3")
			player = vlc.MediaPlayer("neowin.mp3")
			player.play()
			time.sleep(audio.info.length)
		except:
			# Inform the user, bot is having trouble understanding what you're speaking
			print('Playing error response')
			tts = gTTS(text='I am having trouble understanding you', lang='en')
			tts.save("error.mp3")
			audio = MP3("error.mp3")
			player = vlc.MediaPlayer("error.mp3")
			player.play()
			time.sleep(audio.info.length)
except KeyBoardInterrupt:
	print("Good Bye!")
finally:
	pass
