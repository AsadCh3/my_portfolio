# import logging

import scrapy
from .items import Manual

# from manual_scraper_ext.items import Manual

# logger = logging.getLogger(__name__)


class SpeedqueenComSpider(scrapy.Spider):
    name = 'speedqueen.com'

    start_urls = [
        "https://speedqueen.com/products/all-products/"
    ]

    def parse(self, response, **kwargs):
        cat_urls = response.css('.product-category .row > div a::attr(href)').getall()
        for url in cat_urls:
            yield response.follow(url, callback=self.parse_item)

    def parse_item(self, response, **kwargs):
        if not response.xpath("//p[text()='Product Code']/../span/text()").get():
            return

        for pdfs_div in response.css("a[href*='.pdf']"):
            manual = Manual()
            manual['file_urls'] = pdfs_div.css('::attr(href)').getall()
            manual['type'] = pdfs_div.css('::text').get().title()
            manual['brand'] = 'Speed Queen'
            manual['source'] = self.name
            manual['url'] = response.url
            manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]
            manual['thumb'] = response.css(".destaque a::attr(href)").get()
            manual['model'] = response.xpath("/html/body/main/section/div[1]/div/div/div[2]/p[1]/text()[3]").get().strip()
            try:
                manual['product'] = response.xpath("/html/body/main/section/div[1]/div/div/div[2]/h2/text()").getall()[-1]
            except IndexError:
                self.logger.warning("Product not found")
                return

            yield manual
