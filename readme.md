# speech2JOSM

Prototype of an external tool, that controls the Java OpenStreetMap editor by your voice. So you don't need to pick the most common OSM tagging presets manually and can speedup your tagging without interrupting your geometry editing.

## limitations

* false positives detected  esp. with noise
* number of recognized tags is pretty limited
* only english language
* no numeric / ... custom values
* JOSM control limited to tagging features only

# setup

Start JOSM (>3850) and enable remote control for all actions (edit - preferences - remote)
* `sudo apt install pocketsphinx python-pocketsphinx pocketsphinx-en-us python-pyaudio python-requests` (or use `pip -R requirements.txt` and python virtualenv for the python dependencies)
* `python speech2josm.py`
* wait and say 'footway' and confirm JOSM security dialog

# tech

* Python 2 script
* [Pocketsphinx](https://github.com/cmusphinx/pocketsphinx) native STT library with twigs based [pocketsphinx-python](https://github.com/cmusphinx/pocketsphinx-python) binding
* [n-gram based dictionary](https://cmusphinx.github.io/wiki/tutoriallm/#building-a-simple-language-model-using-a-web-service) with EN-US voice modell
* match speech control words against OSM tags
* control JOSM via HTTP API by [remote plugin](https://wiki.openstreetmap.org/wiki/JOSM/RemoteControl)

# Contribute

* extend osm_corpus.txt with control words
    * minimal command lenght, while beeing unique on all items
* upload corpus to [LM onlinetool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) and update osm.lm and osm.dic
* add matching to `tags.yaml` and [validate it](https://codebeautify.org/yaml-validator)
