import scrapy
import urlparse
import json
import logging
import re
from goodreads.items import BookEditionItem
from lxml import html
'''
class EditionRatingsSpider(scrapy.Spider):
    name = "edition_rating_extractor"
    editions = []
    with open('editionUrls.json') as json_file:
        data = json.load(json_file)
        start_urls = data[0]['urls']
        languages = []
    
    def extractRatingAndNumOfRaters(self, ratingText):
        values = {}
        text = ratingText.replace('<![CDATA[', '').replace(']]>', '').rstrip().replace('\\n', '').replace('\\','').replace('//', '').replace('    ', '')
        new = re.search('<div id="moreBookData"(.*)</table></div>', text).group()
        str = new.encode('utf8')
        tree = html.fromstring(str)
        rating = tree.xpath('//*[@id="moreBookData"]')[0][2][1][1][0].text
        values['rating'] = rating
        print('rating : ' + rating)
        numOfRaters = tree.xpath('//*[@id="moreBookData"]')[0][2][1][1][1].text
        print('num of raters ' + numOfRaters)
        values['numOfRaters'] = numOfRaters
        return values

    def parse(self, response):
        name = response.xpath('//*[@id="bookTitle"]//text()').extract_first().
        language = response.xpath('//*[@itemprop="inLanguage"]//text()').extract_first()
        ratingText = response.xpath('//*[@id="bookMeta"]/script').get()
        values = self.extractRatingAndNumOfRaters(ratingText)
        edition = BookEditionItem(name = name, language = language, averageRating = values['rating'], numOfRaters = values['numOfRaters'])
        self.editions.append(edition)
        yield edition
        '''