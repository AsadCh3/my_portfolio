import scrapy
from .items import Manual


class BkfglobalSpider(scrapy.Spider):
    name = "bkfglobal.com"
    allowed_domains = ["bkfglobal.com"]
    start_urls = ["http://bkfglobal.com/descargas/"]
    custom_settings = {
        "CRAWLERA_ENABLED": True
    }

    def parse(self, response):
        products = response.css('div.row.descargas-row')

        for product in products:
            manual = Manual()

            title = product.css('div.col.desc-titulo > div::text').get()

            if title:
                title = title.strip()
                if title == "":
                    title = product.css('div.col.desc-titulo > div > p::text').get()
            else:
                continue

            manual['thumb'] = product.css('div.col.descargas.large-3 > div > a::attr(href)').get()
            file = product.css('[href*=".pdf"]::attr(href)').get()
            if not file:
                continue

            manual['file_urls'] = [file]

            if '(' in title:
                model = title.split('(')[-1][:-1]
                title = title.split('(')[0]
            else:
                model = file.split('/')[-1].split('-')[-1].split('_')[0].replace(".pdf", "")

            manual['product'] = title.title().strip()
            manual['model'] = model.strip()
            manual['type'] = product.css('[href*=".pdf"] span::text').get().title()

            manual['source'] = 'bkfglocal.com'
            manual['url'] = response.url
            manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]
            manual['brand'] = 'BKF'

            if file:
                yield manual
