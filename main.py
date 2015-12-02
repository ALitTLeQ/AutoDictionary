# -*- coding: utf8 -*-
__author__ = 'ee830804'
import requests
from pyquery import PyQuery as pq
import re
import codecs

class YahooDictPaser():
    def __init__(self):
        self.url = 'https://tw.dictionary.search.yahoo.com/search?p='
        self.session  = requests.Session()

    def search(self, engWord):
        def processExplain(str):
            str = re.sub('\[(.*)\]', '',str)
            str = re.sub('([0-9]\. )', '',str)
            return str
        def processPartOfSpeech(str):
            str = re.sub('[^a-z\.]', '',str)
            return str

        response = self.session.get(self.url + engWord).text
        d = pq(response)

        self.explain = []
        self.partOfSpeech = []
        for item in d(".ov-a").items("h4"):
            self.explain.append(processExplain(item.text()))


        for item in d(".fz-s").items(".mb-10"):
            self.partOfSpeech.append(processPartOfSpeech(item.text()))

        self.pronunciation = re.findall('KK(.*) ',d("#pronunciation_pos").text())

        if len(self.partOfSpeech) > 0 and len(self.explain) > 0:
            pronunciation = self.pronunciation[0] if len(self.pronunciation)>0 else ''
            print engWord
            return pronunciation+'\t'+self.partOfSpeech[0]+'\t'+self.explain[0]+'\n'
        else:
            return '\t\n'


if __name__ == '__main__':
    ydict = YahooDictPaser()
    file = open('word.txt', 'r')
    outfile = codecs.open('output.txt','w', "utf-8")
    for word in file:
        out = ydict.search(word)
        outfile.write(out)
    file.close()
    outfile.close()