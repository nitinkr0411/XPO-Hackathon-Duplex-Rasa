import speech_recognition as sr
import requests
import urllib
import vlc
import time
from mutagen.mp3 import MP3
from gtts import gTTS

r = sr.Recognizer()
m = sr.Microphone()

try:
	while True:
		print("Configuring Mic Noise Cancellation, please wait...")
		with m as source: r.adjust_for_ambient_noise(source)
		print("Set minimum energy threshold to {}".format(r.energy_threshold))

		print("Say something!")
		with m as source: audio = r.listen(source)
		print("Recognizing...")
		try:
			# recognize speech using Google Speech Recognition
			value = r.recognize_google(audio)

			# we need some special handling here to correctly print unicode characters to standard output
			if str is bytes:  # this version of Python uses bytes for strings (Python 2)
				print(u"{}".format(value).encode("utf-8"))
			else:  # this version of Python uses unicode for strings (Python 3+)
				print("Synthesizing Complete ->\n")
				spit_out_text = "{}".format(value)

				# spit_out_text is question here

				####################################################################################
									# FORGET THIS GARBAGE BLOCK #
				####################################################################################
				# print(spit_out_text + "\n Calling web API to get response...\n")

				# qs = {'lang' : 'en', 'text' : spit_out_text}
				# Call the other API and get mp3 File
				# req = requests.get('http://localhost/speech_synth?' + urllib.parse.urlencode(qs))
				# with open("neowin.mp3", 'wb') as f:
				# 	for chunk in req.iter_content(chunk_size=1024): 
				# 		if chunk: # filter out keep-alive new chunks
				# 			f.write(chunk)
				####################################################################################

				####################
				##	GET spit_out_text to be the response
				####################

				# spit_out_text should be answer here

				tts = gTTS(text=spit_out_text, lang='en')
				tts.save("neowin.mp3")
				audio = MP3("neowin.mp3")
				player = vlc.MediaPlayer("neowin.mp3")
				player.play()
				time.sleep(audio.info.length)
		except sr.UnknownValueError:
			print("Oops! Didn't catch that")
		except sr.RequestError as e:
			print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyBoardInterrupt:
	print("Good Bye!")
finally:
	pass
