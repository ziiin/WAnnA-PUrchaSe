
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
        features = tree.find_class ("productSpecs specSection")
        for feature in features:
            mainFeature = feature.xpath ('.//td[@class="specsKey"]/text()')
            subFeature = feature.xpath ('.//td[@class="specsValue"]/text()')
            self.featureList.append (mainFeature + subFeature)
        for feature in self.featureList:
            for i in range (len (feature)):
                feature[i] = feature[i].lower()


    def viewFeature (self):
        for feature in self.featureList:
            print feature
            print "\n\n"

    def getFeature (self):
        return self.featureList

def main():
    url = 'http://www.flipkart.com/google-nexus-5/p/itmdv6f6fbzekayt'
    collector = featureCollect()
    collector.collect (url)
    collector.viewFeature()

if __name__ == "__main__":
    main()


        
