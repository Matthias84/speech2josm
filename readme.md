JOSM presets via voice control

# speech 2 JOSM

Prototype of an external tool, that controls JOSM remote by your voice.

# setup

* sudo apt install pocketsphinx python-pocketsphinx pocketsphinx-en-us python-pyaudio
* python speech2josm.py

# tech

* Python 3 script
* [Pocketsphinx](https://github.com/cmusphinx/pocketsphinx) native STT library with twigs based [pocketsphinx-python](https://github.com/cmusphinx/pocketsphinx-python) binding
* [n-gram based dictionary](https://cmusphinx.github.io/wiki/tutoriallm/#building-a-simple-language-model-using-a-web-service) with EN-US voice modell
* matching against 
* control JOSM via HTTP API by remote plugin

# Contribute

* extend osm_corpus.txt with control words
* upload corpus to [LM onlinetool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) and update osm.lm and osm.dic
