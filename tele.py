
import sys
import os
from lxml import html
import requests

class featureCollect:
    def __init__(self) :
        ''' each entry in this list is a feature
            featureList[i][0] is the main feature while
            rest (featureList[i][j]) are similar ones '''
        self.hotelTele = dict()
    
    def collect (self, url):
        hotelList = []
        teleList = []
        page = requests.get(url)
        tree = html.fromstring(page.text)
        #infos = tree.find_class ("rslwrp")
        hotels = tree.find_class ("jcnwrp")
        for hotel in hotels:
            hotelName =  hotel.xpath ('.//span/a/text()')
            hotelList.append(hotelName[0])

        phones = tree.find_class ("jrcw")
        for phone in phones:
            hotelPhone = phone.xpath( './/a/b/text()')
            if len(hotelPhone) == 0:
                hotelPhone = phone.xpath( './/a/text()')
            teleList.append(hotelPhone)

        l = len(hotelList)
        print l
        l1 = len(teleList)
        print l1

        for i in range(0,l):
            self.hotelTele[hotelList[i]] = teleList[i]
        for key in self.hotelTele :
            print key, self.hotelTele[key]
            
        # xpath: /html/body/section[1]/section[2]/section[4]
        #tele = tree.xpath ('/html/body/section[1]/section[2]/section[4]/section[1]/section[2]/section[1]/aside[1]/p[2]/a[1]/text()')
        # tele xpath: /html/body/section[1]/section[2]/section[4]/section[1]/section[2]/section[1]/aside[1]/p[2]/a[1]
        #             /html/body/section[1]/section[2]/section[4]/section[2]/section[2]/section[1]/aside[1]/p[2]/a
        #print tele


def main():
    url = 'http://www.justdial.com/Delhi/Oyo-Hotels-%3Cnear%3E-Spaze-I-Tech-Park-Sector-49-Gurgaon/011PXX11-XX11-140103173643-M1J4_RGVsaGkgT3lvIEhvdGVscyBTcGF6ZSBJIFRlY2ggUGFyayBTZWN0b3IgNDkgR3VyZ2Fvbg==_BZDET'
    
    url1 = "http://www.justdial.com/Delhi/Hotels-%3Cnear%3E-gurgaon/ct-303533"
    url2 = "http://www.justdial.com/Delhi/Hotels-%3Cnear%3E-Gurgaon/ct-303533/page-2"
    collector = featureCollect()
    collector.collect (url2)

if __name__ == "__main__":
    main()


        
