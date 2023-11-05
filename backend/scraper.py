from urllib.request import urlopen
from html.parser import HTMLParser
import re
import numpy as np
from midi_extract import extract
import requests
from os.path import join
import os

extension = '.mid'

dataset = []

class Parser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...):
        super().__init__(convert_charrefs=convert_charrefs)
        self.url_list = []

    def handle_starttag(self, tag, attrs):
        try:
            for attribute in attrs:
                attr_type, attr_content = attribute[0], attribute[1]
                if attr_type and attr_content:
                    isURL = re.match(r"(https?:\/\/)([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)", attr_content)
                    ispartialURL = re.match("^(.+)\/([^\/]+)$", attr_content)
                    if attr_type == 'href' and isURL and attr_content not in self.url_list and attr_content[-4:] == extension:
                        self.url_list.append(attr_content)
                        response = requests.get(attr_content)
                        fname = attr_content.split(r"/")[-1]
                        open(join(save_dir,fname), "wb").write(response.content)
                        dataset.append(extract(join(save_dir,fname)))
                        os.remove(join(save_dir,fname))


                    elif attr_type == 'href' and ispartialURL and attr_content not in self.url_list and attr_content[-4:] == extension:
                        self.url_list.append(attr_content)
                        response = requests.get("http://piano-midi.de/" + attr_content)
                        fname = attr_content.split(r"/")[-1]
                        open(join(save_dir,fname), "wb").write(response.content)
                        dataset.append(extract(join(save_dir,fname)))
                        os.remove(join(save_dir,fname))

        except Exception as e:
            print("Error: "+ str(e))

    def feed(self, data: str):
        self.url_list = []
        return super().feed(data)

start_urls = ['https://www.midiworld.com/classic.htm', 'http://piano-midi.de/albeniz.htm', 'http://piano-midi.de/bach.htm', 'http://piano-midi.de/balakirew.htm', 'http://piano-midi.de/beethoven.htm', 'http://piano-midi.de/borodin.htm', 'http://piano-midi.de/brahms.htm', 'http://piano-midi.de/burgmueller.htm', 'http://piano-midi.de/chopin.htm', 'http://piano-midi.de/clementi.htm', 'http://piano-midi.de/debussy.htm', 'http://piano-midi.de/godowsky.htm', 'http://piano-midi.de/granados.htm', 'http://piano-midi.de/grieg.htm', 'http://piano-midi.de/haydn.htm', 'http://piano-midi.de/liszt.htm', 'http://piano-midi.de/mendelssohn.htm', 'http://piano-midi.de/moszkowski.htm', 'http://piano-midi.de/mozart.htm', 'http://piano-midi.de/mussorgsky.htm', 'http://piano-midi.de/rachmaninov.htm', 'http://piano-midi.de/ravel.htm', 'http://piano-midi.de/schubert.htm', 'http://piano-midi.de/schumann.htm', 'http://piano-midi.de/sinding.htm', 'http://piano-midi.de/tchaikovsky.htm']

parser = Parser()
urls = []
save_dir = "midi_files"

for url in start_urls:
    try:
        f = urlopen(url)
        mybytes = f.read()
        mystr = mybytes.decode("utf8")
        f.close()
    except Exception as e:
        print("Error accessing '"+url+"': "+str(e))
    else:
        parser.feed(mystr)

np.save("dataset.npy", dataset)