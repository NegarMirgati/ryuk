
import scrapy
from scrapy.loader import ItemLoader
import os
#import urlparse
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import json
import logging
import re
from lxml import html
from goodreads.items import BookListEditions
from goodreads.items import BookEditionItem

class EditionSpider(scrapy.Spider):
    name = "edition_extractor"
    list_editions = BookListEditions()
    list_editions['dic'] = {}

    if os.path.exists('links.json'):
        with open('links.json', 'r') as json_file:
            data = json.load(json_file)
            start_urls = data[0]['bookUrls']

    def parse(self, response):
        editions = {'name' : '' }
        editons_page = response.xpath("//div[@class='otherEditionsActions']/a[@class='actionLinkLite'][1]/@href").extract()
        if(len(editons_page) > 0):
            url = urlparse.urljoin(response.url, editons_page[0]) 
            #url = urlparse.urljoin(url,'?sort=num_ratings')
            request = scrapy.Request(url, callback = self.parse_editions_url, meta = {'editions' : editions})
            #request.meta['editions'] = editions
            yield request

    def parse_editions_url(self, response):
        name = response.css('div.mainContentFloat h1 a::text').extract_first().strip()
        editions = response.meta['editions']
        all_books_data = {}
        if(name not in editions['name']):
            editions['name'] = name
            editions['urls'] = []

        for book_page in response.css('a.bookTitle').xpath('@href'):
            editions['urls'].append((urlparse.urljoin(response.url, book_page.extract())))
                
        next_page = response.xpath("//*[@rel='next']/@href").extract_first()

        if next_page is not None and (len(editions['urls']) <= 200):
            yield response.follow(next_page, callback = self.parse_editions_url, meta = {'editions' : editions})
        else:
            print(editions['name'])
            print(len(editions['urls']))
            for link in editions['urls']:
                request = scrapy.Request(link, callback = self.parse_editions_data, meta = {'all_books_data' : all_books_data, 'name' : editions['name']})
                yield request
                #yield editions
            editions = {}
    

    def parse_editions_data(self, response):
        name = response.xpath('//*[@id="bookTitle"]//text()').extract_first()
        original_name = response.meta['name']
        #all_books_data = response.meta['all_books_data']
        language = response.xpath('//*[@itemprop="inLanguage"]//text()').extract_first()
        ratingText = response.xpath('//*[@id="bookMeta"]/script').get()
        values = self.extractRatingAndNumOfRaters(ratingText)
        edition = BookEditionItem(name = name, original_name = original_name, language = language, averageRating = values['rating'], numOfRaters = values['numOfRaters'])

        #if(original_name not in all_books_data):
        #    all_books_data[original_name] = []

        #all_books_data[original_name].append(edition)
        #yield all_books_data
        if(int(values['numOfRaters']) > 100 and language != None):
            yield edition
        else :
            yield

    
    def extractRatingAndNumOfRaters(self, ratingText):
        values = {}
        text = ratingText.replace('<![CDATA[', '').replace(']]>', '').rstrip().replace('\\n', '').replace('\\','').replace('//', '').replace('    ', '')
        new = re.search('<div id="moreBookData"(.*)</table></div>', text).group()
        str = new.encode('utf8')
        tree = html.fromstring(str)
        rating = tree.xpath('//*[@id="moreBookData"]')[0][2][1][1][0].text
        values['rating'] = rating
        numOfRaters = tree.xpath('//*[@id="moreBookData"]')[0][2][1][1][1].text
        values['numOfRaters'] = numOfRaters
        return values