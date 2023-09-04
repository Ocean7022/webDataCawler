# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class DataCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    en_url = Field()
    zh_url = Field()
    page_name = Field()
    id = Field()
    category = Field()
    release_date = Field()
    para_aligned_status = Field()
    contents = Field()


class ContentItem(scrapy.Item):
    zh = Field()
    en = Field()
    mixed_enzh = Field()
