
import sys
import os
from lxml import html
import requests

class featureCollect:
    def __init__(self) :
        ''' each entry in this list is a feature
            featureList[i][0] is the main feature while
            rest (featureList[i][j]) are similar ones '''
        self.featureList = []
    
    def collect (self, url):
        page = requests.get(url)
        tree = html.fromstring(page.text)
        tele = tree.xpath ('//*[@id="rvcnt"]/section[3]/section[1]/aside/p[2]/a/b/text()')
        print tele


def main():
    url = 'http://www.justdial.com/Delhi/Oyo-Hotels-%3Cnear%3E-Spaze-I-Tech-Park-Sector-49-Gurgaon/011PXX11-XX11-140103173643-M1J4_RGVsaGkgT3lvIEhvdGVscyBTcGF6ZSBJIFRlY2ggUGFyayBTZWN0b3IgNDkgR3VyZ2Fvbg==_BZDET'
    collector = featureCollect()
    collector.collect (url)

if __name__ == "__main__":
    main()


        
