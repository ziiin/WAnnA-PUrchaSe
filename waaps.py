
import sys
import os
from lxml import html
import requests

class reviewsCollector:
    def setBaseProductUrl (self, url):
        self.baseUrl = url
    
    def traverseFlipkartReviews(self):
        url = self.baseUrl
        url+= "?type=all&start="
        start = 0
        while True:
            reviewPage = requests.get(url + str (start))
            print "Printing url " + url + str (start)
            raw_input("continue ....")
            reviewPageHtml = html.fromstring (reviewPage.text)
            reviewList = reviewPageHtml.xpath('//span[@class="review-text"]/text()')
            if len(reviewList) == 0:
                break
            else :
                for review in reviewList:
                    print review
                    print "\n\n"
                start+=10

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
    url1 = "http://www.flipkart.com/seagate-backup-plus-1-tb-external-hard-disk/p/itmdmyf9kzkvsx8a"
    url = "http://www.flipkart.com/seagate-backup-plus-1-tb-external-hard-disk/product-reviews/ITMDMYF9KZKVSX8A"
    url2 = "http://www.amazon.in/product-reviews/B009PJG3MQ"
    r.setBaseProductUrl (url2)
    r.traverseAllReviews("amazon")

if __name__ == "__main__":
    main()


