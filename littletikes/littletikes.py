import scrapy
import regex as re

class Manual(scrapy.Item):
    brand = scrapy.Field()
    product = scrapy.Field()
    model = scrapy.Field()
    product_lang = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    type = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    thumb = scrapy.Field()

class LittletikesSpider(scrapy.Spider):
    name = "littletikes"
    allowed_domains = ["littletikes.nl"]

    def start_requests(self):
        urls = [
            "https://www.littletikes.nl/categorieen/baby-en-kleuter/",
            "https://www.littletikes.nl/categorieen/speelgoedautos/",
            "https://www.littletikes.nl/categorieen/schommels-en-glijbanen/",
            "https://www.littletikes.nl/categorieen/zand-en-watertafels/",
            "https://www.littletikes.nl/categorieen/ranges/trikes/",
            "https://www.littletikes.nl/categorieen/rollenspel/",
            "https://www.littletikes.nl/categorieen/ranges/cozy-coupe/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('div.product-post')
        data = {'product': self.get_product(response.request.url)}
        for product in products:
            url = product.css('a.woocommerce-LoopProduct-link::attr(href)').get()
            yield scrapy.Request(url=url, callback=self.parse_product, meta=data)

    def parse_product(self, response):
        manual = Manual()

        manual["source"] = "littletikes.nl"
        manual["brand"] = "Little Tikes"
        manual["product_lang"] = "en-GB"

        product_title = response.css('h1.product_title::text').get()
        manual["product"] = response.meta['product']
        file_urls = response.css('div#tab-additional_information > a::attr(href)').get()

        manual["file_urls"] = file_urls
        manual["files"] = ""
        manual["url"] = response.request.url
        manual["type"] = "Producthandleiding"

        thumb_section = response.css('ul.product_gallery')
        manual["thumb"] = thumb_section.css('img::attr(src)').get()

        manual["source"] = "littletikes.nl"

        if file_urls:
            file_title = file_urls.split('/')[-1]
            file_title = file_title.split('.')[0]
            if '-' in file_title:
                model = file_title.split('-')[0]
            else:
                model = file_title

            manual["model"] = model
            yield manual

    def get_product(self, url):
        if 'baby-en-kleuter' in url:
            return 'BABY EN KLEUTER'
        elif 'speelgoedautos' in url:
            return 'SPEELGOEDAUTO'
        elif 'schommels-en-glijbanen' in url:
            return 'SCHOMMELS EN GLIJBANEN'
        elif 'zand-en-watertafels' in url:
            return 'ZANDBANK EN WATERTAFELS'
        elif 'trikes' in url:
            return 'TRIKES'
        elif 'rollenspel' in url:
            return 'ROLLENSPEL'
        elif 'cozy-coupe' in url:
            return 'COZY COUPE'
