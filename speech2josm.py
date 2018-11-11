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
                #TODO zerlegen und mapping externalisieren
                r = requests.get('http://localhost:8111/zoom?left=8.19&right=8.20&top=48.605&bottom=48.590&select=currentselection&addtags=foo=bar')
            else:
                print (seg.word, seg.prob, seg.start_frame, seg.end_frame)
        decoder.end_utt()
        decoder.start_utt()
