
import sys
import os
from lxml import html
import requests
import re
import featureCollect
from textblob import TextBlob


def getSentence (review):
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
            #print sentence.strip() + "$$$"
            #print "***********************"
            yield sentence.strip()
            i+=2
        else:
            print "Skipping ... " + sentences[i] + " $$end"
            i+=1
            continue

class reviewsCollector:
    def __init__ (self):
        self.startFlipkartPage = 0
        ''' need to write another method to reset it to 0 '''
    def setBaseProductUrl (self, url):
        self.baseUrl = url
    
    def traverseFlipkartReviews(self):
        url = self.baseUrl
        url+= "?type=all&start="
        review = ""
        start = self.startFlipkartPage
        reviewPage = requests.get(url + str (start))
        print "Printing url " + url + str (start)
        #raw_input("continue ....")
        reviewPageHtml = html.fromstring (reviewPage.text)
        reviewList = reviewPageHtml.xpath('//span[@class="review-text"]/text()')
        if len(reviewList) == 0:
            return None
        else :
            for r in reviewList:
                review += r
            self.startFlipkartPage +=10
            return review

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
            return self.traverseFlipkartReviews()
        elif urlType == "amazon" :
            self.traverseAmazonReviews()
        else :
            pass

class analyseSentiment:
    def __init__ (self):
        self.featureMap = {}
        self.featureOccurence = []
        self.featureSentiment = []

    def setFeatureMap (self, featureList):
        index = 0
        for feature in featureList:
            self.featureMap[feature[0]] = index
            self.featureOccurence.append(0)
            self.featureSentiment.append (0.0)
            index += 1
            print "Setting ", feature[0], " to ", index -1
        self.featureMap['over-all'] = index
        self.featureOccurence.append (0)
        self.featureSentiment.append (0.0)
        print "Setting ", 'over-all', " to ", index

    def analyse (self, sentence ):
        blob = TextBlob(sentence)
        senti = 0.0
        for sent in blob.sentences:
            senti += sent.sentiment.polarity
        return senti

    def sentenceToAnalyse(self, review):
        #print "-----> ", review
        for sentence in getSentence(review):
            print "----> ", sentence
            self.analyse (sentence)
    def fillSentiment (self, review, featureList):
        for sentence in getSentence(review):
            for feature in featureList:
                for subFeature in feature:
                    if sentence.lower().find(subFeature) != -1:
                        fIndex = self.featureMap[feature[0]]
                        occurence = self.featureOccurence[fIndex]
                        sentiValue = self.featureSentiment[fIndex]\
                                     * self.featureOccurence[fIndex]
                        sentiValue = (sentiValue + self.analyse(sentence))
                        sentiValue = (sentiValue / (occurence +1) )
                        self.featureOccurence[fIndex] +=1
                        self.featureSentiment[fIndex] = sentiValue
                        break
                    else :
                        fIndex = self.featureMap['over-all']
                        occurence = self.featureOccurence[fIndex]
                        sentiValue = self.featureSentiment[fIndex]\
                                     * self.featureOccurence[fIndex]
                        sentiValue = (sentiValue + self.analyse(sentence))
                        sentiValue = (sentiValue / (occurence +1) )
                        self.featureOccurence[fIndex] +=1
                        self.featureSentiment[fIndex] = sentiValue

    def getAll (self, featureList):
        print "Occurences : "
        for feature in featureList:
            fIndex = self.featureMap[feature[0]]
            print feature, " --> ", self.featureOccurence[fIndex]
        print "$$$$$$$$$  DONE $$$$$$$$$$$$"
        print "Sentiment : "
        for feature in featureList:
            fIndex = self.featureMap[feature[0]]
            print feature, " --> ", self.featureSentiment[fIndex]
        fIndex = self.featureMap['over-all']
        print "Over-all", " --> ", self.featureSentiment[fIndex]
        print "$$$$$$$$$  DONE2 $$$$$$$$$$$$"



def main ():
    r = reviewsCollector()
    sentiment = analyseSentiment ()
    #f = featureCollect.
    url1 = "http://www.flipkart.com/seagate-backup-plus-1-tb-external-hard-disk/p/itmdmyf9kzkvsx8a"
    url = "http://www.flipkart.com/seagate-backup-plus-1-tb-external-hard-disk/product-reviews/ITMDMYF9KZKVSX8A"
    url2 = "http://www.amazon.in/product-reviews/B009PJG3MQ"
    url3 = "http://www.flipkart.com/google-nexus-5/product-reviews/ITMDV6F6Z6AMGNWR"
    url3_1 = 'http://www.flipkart.com/google-nexus-5/p/itmdv6f6z6amgnwr'
    collector = featureCollect.featureCollect()
    collector.collect (url3_1)
    collector.viewFeature()
    raw_input ("Collecting features")
    f = collector.getFeature()


    r.setBaseProductUrl (url3)
    raw_input ("Initial values, sentiment and occurence ")
    sentiment.setFeatureMap (f)
    raw_input("Mapped values, sentiment and occurence")
    sentiment.getAll(f)
    while (True):
        review = r.traverseAllReviews()
        if review == None:
            break
        else:
            raw_input ("Printing from this page reviews **************")
            raw_input ("Final values, sentiment and occurence")
            sentiment.fillSentiment (review, f)
            sentiment.getAll (f)
            #sentiment.sentenceToAnalyse(review)


if __name__ == "__main__":
    main()


