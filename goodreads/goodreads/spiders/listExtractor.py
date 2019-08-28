import scrapy
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from goodreads.items import ListItem

class ListSpider(scrapy.Spider):
    name = "list_extractor"
    bookList = ListItem()
    bookList['bookUrls'] = []
    start_urls = [
        #'https://www.goodreads.com/list/show/9440.100_Best_Books_of_All_Time_The_World_Library_List'
        'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once'
    ]

    def parse(self, response):
        for book_page in response.css('a.bookTitle').xpath('@href'):
            if(len(self.bookList['bookUrls']) >= 50):
                break
            self.bookList['bookUrls'].append(urlparse.urljoin(response.url, book_page.extract()))
        
        next_page = response.xpath("//*[@rel='next']/@href").extract_first()
        if next_page is not None and len(self.bookList['bookUrls']) < 50 :
            yield response.follow(next_page, callback=self.parse)
        else:
            yield self.bookList