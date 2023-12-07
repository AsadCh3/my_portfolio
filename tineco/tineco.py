import scrapy
from urllib.parse import quote
from .items import Manual

class TinecoSpider(scrapy.Spider):
    name = "tineco"
    allowed_domains = ["us.tineco.com"]
    start_urls = ["https://us.tineco.com/support/instruction-manual/"]

    def parse(self, response):
        manual = Manual()
        allmanuals = response.css("div[sensorsdata='ManualDownload'] > a")

        for url in allmanuals:
            manual_link = url.css('::attr(href)').get()
            manual_title = url.css('span::text').get()
            manual['file_urls'] = quote(manual_link.strip(), safe='/:')
            manual['model'] = manual_title.split('Instruction')[0]
            manual['product'] = self.get_product(manual_title)
            manual['source'] = 'tineco.com'
            manual['url'] = response.url
            manual['brand'] = 'Tineco'
            manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]
            manual['type'] = 'Instruction Manual'
            yield manual

    def get_product(self, title):
        if 'toasty' in title.lower():
            return 'Kitchen'
        elif 'moda one' in title.lower():
            return 'Beauty'
        elif 'pure' in title.lower() or 'a11 ' in title.lower() or 'pwrhero' in title.lower() or 'a10 ' in title.lower():
            return 'Vacuum Cleaners'
        elif 'carpet' in title.lower():
            return 'Carpet Cleaners'
        elif 'floor' in title.lower():
            return 'Floor Washers'
