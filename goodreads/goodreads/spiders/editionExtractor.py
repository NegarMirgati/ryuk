import scrapy
import urlparse
import json
from goodreads.items import BookListEditions
from scrapy.loader import ItemLoader

class EditionSpider(scrapy.Spider):
    name = "edition_extractor"
    list_editions = BookListEditions()
    list_editions['dic'] = {}

    with open('links.json') as json_file:
        data = json.load(json_file)
        start_urls = data[0]['bookUrls']

    def parse(self, response):
        editions = {'name' : '' }
        editons_page = response.xpath("//div[@class='otherEditionsActions']/a[@class='actionLinkLite'][1]/@href").extract()
        if(len(editons_page) > 0):
            url = urlparse.urljoin(response.url, editons_page[0])
            request = scrapy.Request(url, callback = self.parse_editions_url)
            request.meta['editions'] = editions
            yield request

    def parse_editions_url(self, response):
        name = response.css('div.mainContentFloat h1 a::text').extract_first().strip()
        editions = response.meta['editions']
        if(name not in editions['name']):
            editions['name'] = name
            editions['urls'] = []

        for book_page in response.css('a.bookTitle').xpath('@href'):
            editions['urls'].append((urlparse.urljoin(response.url, book_page.extract())))
                
        next_page = response.xpath("//*[@rel='next']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse_editions_url, meta = {'editions' : editions})
        else:
            yield editions