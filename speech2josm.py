#!/usr/bin/python

import sys, os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import requests
import yaml

def checkJOSM() :
    try:
        r = requests.get('http://localhost:8111/version')
    except requests.ConnectionError:
        print 'No JOSM connection - please check if JOSM is running and remote control is enabled.'
        exit()

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', '/usr/share/pocketsphinx/model/en-us/en-us')
config.set_string('-lm', 'osm.lm')
config.set_string('-dict', 'osm.dic')
config.set_string('-logfn', '/dev/null')

# load OSM tags mapping
mapfile = open('tags.yaml','r')
mapping = yaml.load(mapfile)
checkJOSM()

# read from microphone
import pyaudio

p = pyaudio.PyAudio()
audioStream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
audioStream.start_stream()

# Process audio chunk by chunk. On keyphrase detected perform action and restart search
decoder = Decoder(config)
decoder.start_utt()
while True:
    buf = audioStream.read(1024)
    if buf:
         decoder.process_raw(buf, False, False)
    else:
         break
    if decoder.hyp() != None:
        for seg in decoder.seg():
            if seg.word in mapping:
                print '\033[92m ' + seg.word +' \033[0m'
                tags = '|'.join(mapping[seg.word])
                r = requests.get('http://localhost:8111/zoom?left=8.19&right=8.20&top=48.605&bottom=48.590&select=currentselection&addtags=' + tags)
            else:
                print '\033[95m ' + seg.word + str(seg.prob) + ',' + str(seg.start_frame) + ':' + str(seg.end_frame) + ' \033[0m'
        decoder.end_utt()
        decoder.start_utt()
