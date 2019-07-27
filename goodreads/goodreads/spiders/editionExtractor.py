import scrapy
import urlparse
from goodreads.items import BookEditionsItem

class ReviewsSpider(scrapy.Spider):
    name = "edition_extractor"
    editions = BookEditionsItem()
    editions['urls'] = []
    start_urls = [
        'https://www.goodreads.com/work/editions/3295655-cien-a-os-de-soledad'
    ]

    def parse(self, response):
        self.editions['name'] = response.css('div.mainContentFloat h1 a::text').extract_first().strip()
        # self.editions['urls'] = []
            
        # editions['urls'].append(self.extract_urls(response))
        
        for book_page in response.css('a.bookTitle').xpath('@href'):
            self.editions['urls'].append(urlparse.urljoin(response.url, book_page.extract()))
        
        next_page = response.xpath("//*[@rel='next']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            yield self.editions