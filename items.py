import scrapy

class Manual(scrapy.Item):
    brand = scrapy.Field()
    product = scrapy.Field()
    model = scrapy.Field()
    model_2 = scrapy.Field()
    product_lang = scrapy.Field()
    product_parent = scrapy.Field()
    file_urls = scrapy.Field()
    type = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    eans = scrapy.Field()
    thumb = scrapy.Field()
    files = scrapy.Field()
