# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy

class GoodreadsItem(scrapy.Item):
    name = scrapy.Field()
    average_rating = scrapy.Field()
    reviews = scrapy.Field()
    num_of_raters = scrapy.Field()
    rating_distribution = scrapy.Field()
    pass
    
class GoodreadsItemWithEdition(scrapy.Item):
    name = scrapy.Field()
    average_rating = scrapy.Field()
    reviews = scrapy.Field()
    edition_language = scrapy.Field()
    pass

class BookEditionsItem(scrapy.Item):
    name = scrapy.Field()
    urls = scrapy.Field()
    pass