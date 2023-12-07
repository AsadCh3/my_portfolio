import scrapy
from .items import Manual


class WarptechSpider(scrapy.Spider):
    name = "warptech"
    allowed_domains = ["warptech.com.ar"]
    start_urls = [
        "https://warptech.com.ar/categoria-producto/hogar/hornito/",
        "https://warptech.com.ar/categoria-producto/hogar/aspiradoras-inteligentes/",
        "https://warptech.com.ar/categoria-producto/notebooks/"
    ]

    def parse(self, response):
        product_urls = response.css('a.ast-loop-product__link::attr(href)').getall()

        for product_url in product_urls:
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        manual = Manual()
        for file in response.css('a.elementor-button-link::attr(href)').getall():
            if file.endswith('.pdf'):
                product_title = response.css('h1.product_title::text').get()
                manual['product'] = product_title.split('-')[0] if '-' in product_title else product_title.split(' ')[0]
                manual['model'] = product_title.split('-')[-1] if '-' in product_title else product_title.split(' ')[-1]
                manual['file_urls'] = file
                manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]
                manual['url'] = response.url
                manual['thumb'] = response.css("figure.woocommerce-product-gallery__wrapper > div > a::attr(href)").get()
                manual['source'] = 'warptech.com.ar'
                manual['brand'] = 'Warptech'
                manual['type'] = 'manual'
                yield manual
