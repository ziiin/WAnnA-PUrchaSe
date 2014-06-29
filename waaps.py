
import sys
import os
from lxml import html
import requests
import re
import featureCollect

class analyseSentiment:
    def sentenceToAnalyse():
        pass
    def analyse():
        pass
    def fillSentiment():
        pass

def printSentence (review):
    print review
    print "#########################"
    #r = re.compile(r"*(\s\.)")
    sentences = re.split(r"([a-zA-Z]\.)", review)
    #print "***********************"
    #print sentences
    i = 0
    fill = 0
    while ( i < len(sentences)):
        ''' need better sentence formation algorithm 
            to skip short-forms '''
        if re.search(r"([a-zA-Z]\.)",sentences[i]) == None:
            sentence = sentences[i]
            if i+1 < len(sentences):
                sentence += sentences[i+1]
            print sentence.strip() + "$$$"
            print "***********************"
            i+=2
        else:
            print "Skipping ... " + sentences[i] + " $$end"
            i+=1
            continue

class reviewsCollector:
    def setBaseProductUrl (self, url):
        self.baseUrl = url
    
    def traverseFlipkartReviews(self):
        url = self.baseUrl
        url+= "?type=all&start="
        start = 0
        r = ""
        while True:
            reviewPage = requests.get(url + str (start))
            print "Printing url " + url + str (start)
            #raw_input("continue ....")
            reviewPageHtml = html.fromstring (reviewPage.text)
            reviewList = reviewPageHtml.xpath('//span[@class="review-text"]/text()')
            if len(reviewList) == 0:
                break
            else :
                for review in reviewList:
                    r += review
                    #print "***************************"
                break
                start+=10
        print "\n\n\n"
        printSentence (r )

    def traverseAmazonReviews (self):
        url = self.baseUrl
        url += "?pageNumber="
        start = 1
        while True:
            reviewPage = requests.get (url + str(start))
            print "Printing url(Amazon) " + url + str(start)
            raw_input("continue ....")
            reviewPageHtml = html.fromstring (reviewPage.text)
            reviewList = reviewPageHtml.xpath('//div[@class="reviewText"]/text()')
            if len(reviewList) == 0:
                break
            else:
                for review in reviewList:
                    print review
                    print "\n\n"
                start += 1

    def traverseAllReviews (self, urlType="flipkart"):
        ''' Depending on urlType traverse amazon or flipkart review pages '''
        if urlType == "flipkart":
            self.traverseFlipkartReviews()
        elif urlType == "amazon" :
            self.traverseAmazonReviews()
        else :
            pass

def main ():
    r = reviewsCollector()
    #f = featureCollect.
    url1 = "http://www.flipkart.com/seagate-backup-plus-1-tb-external-hard-disk/p/itmdmyf9kzkvsx8a"
    url = "http://www.flipkart.com/seagate-backup-plus-1-tb-external-hard-disk/product-reviews/ITMDMYF9KZKVSX8A"
    url2 = "http://www.amazon.in/product-reviews/B009PJG3MQ"
    r.setBaseProductUrl (url)
    r.traverseAllReviews()

if __name__ == "__main__":
    main()


