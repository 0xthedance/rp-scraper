# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    source_url = scrapy.Field()
    solutions  = scrapy.Field() 
    products   = scrapy.Field()  