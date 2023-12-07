import scrapy
from .items import Manual


class CyrusTechSpider(scrapy.Spider):
    name = "cyrus_tech"
    allowed_domains = ["cyrus-technology.de"]
    start_urls = [
        "https://www.cyrus-technology.de/en/products/cm8/",
        "https://www.cyrus-technology.de/en/products/cs45-xa/",
        "https://www.cyrus-technology.de/en/products/cm17-xa/",
        "https://www.cyrus-technology.de/en/products/ct1-xa/",
        "https://www.cyrus-technology.de/en/products/cs22-xa/"
    ]

    def parse(self, response):
        manual = Manual()
        model = response.url.split('/')[-2].upper()
        manual['model'] = model
        manual['brand'] = 'Cyrus'
        manual['source'] = 'cyrus-technology.de'
        manual['url'] = response.url
        manual['thumb'] = response.css('span.big_img > img::attr(src)').get()
        manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]

        # product
        if model.startswith('CS'):
            manual['product'] = 'Smartphones' 
        elif model.startswith('CM'):
            manual['product'] = 'Mobile Phones'  
        elif model.startswith('CT'):
            manual['product'] = 'Tablets'
        else:
            manual['product'] = None

        manual_area = response.xpath('//*[@id="cs-content"]/div[5]/div/div/div[2]/div[4]')
        manual_urls = manual_area.css('a[href*=".pdf"]::attr(href)').getall()

        for urls in manual_urls:
            manual['type'] = 'Manual'
            manual['file_urls'] = urls
            yield manual

        warranty = response.xpath('//*[@id="cs-content"]/div[5]/div/div/div[2]/div[8]')
        warranty_urls = warranty.css('a[href*=".pdf"]::attr(href)').getall()

        for urls in warranty_urls:
            manual['type'] = 'Warranty'
            manual['file_urls'] = urls
            yield manual
