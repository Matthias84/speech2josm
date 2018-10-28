#!/usr/bin/python

import sys, os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import requests


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', '/usr/share/pocketsphinx/model/en-us/en-us')
config.set_string('-lm', 'osm.lm')
config.set_string('-dict', 'osm.dic')
config.set_string('-logfn', '/dev/null')


# Alternatively you can read from microphone
import pyaudio

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

# Process audio chunk by chunk. On keyphrase detected perform action and restart search
decoder = Decoder(config)
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
         decoder.process_raw(buf, False, False)
    else:
         break
    if decoder.hyp() != None:
        print ("Detection!")
        for seg in decoder.seg():
            if seg.word == 'BUILDING':
                print '\033[92m BUILDING \033[0m'
                r = requests.get('http://localhost:8111/load_and_zoom?addtags=building=yes&select=way23071688,way23076176,way23076177,&left=13.739727546842&right=13.740890970188&top=51.049987191025&bottom=51.048466954325')
            else:
                print (seg.word, seg.prob, seg.start_frame, seg.end_frame)
        decoder.end_utt()
        decoder.start_utt()
