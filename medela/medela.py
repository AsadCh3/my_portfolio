import scrapy
from .items import Manual

class MedelaSpider(scrapy.Spider):
    name = "medela"
    allowed_domains = ["medela.com"]
    start_urls = [
        "https://www.medela.com/breastfeeding/products/breast-pumps",
        "https://www.medela.com/breastfeeding/products/maternity-and-nursing-wear",
        "https://www.medela.com/breastfeeding/products/feeding",
        "https://www.medela.com/breastfeeding/products/collecting",
        "https://www.medela.com/breastfeeding/products/breast-care",
        "https://www.medela.com/breastfeeding/products/accessories",
        "https://www.medela.com/breastfeeding/products/medelababy"
    ]

    def parse(self, response):
        if response.url.endswith('medelababy'):
            product = 'Baby Care'
        else:
            product = response.css('div#page-intro > h1::text').get().title().strip()

        products = response.css('div.teaser.productTeaser.clearfix > a::attr(href)').extract()
        if products:
            for product_url in products:
                yield response.follow(product_url, callback=self.parse_product, meta={'product': product})
        else:
            product_section = response.xpath('//*[@id="main"]/div/div[4]')
            products = product_section.css('a.relatedArticle::attr(href)').extract()
            for product_url in products:
                yield response.follow(product_url, callback=self.parse_product, meta={'product': product})

    def parse_product(self, response):
        manual = Manual()
        product = response.meta.get('product')
        title = response.css('h1[itemprop="name"]::text').get()
        thumb_src = response.css('div.fullview-image > img::attr(src)').get()
        product_lang = response.css("html::attr(lang)").get().split("-")[0]

        if not title:
            title = response.css('h1.product-hero-title.fw-bold text-dark::text').get()

        for file_urls in response.css('li.download > a::attr(href)').extract():
            manual['source'] = 'medala.com'
            manual['brand'] = 'Medela'
            manual['product'] = product
            manual['model'] = title.strip().split('™')[0].replace(" Breast Pump", "")
            manual['file_urls'] = [f"https://www.medela.com{file_urls}"]
            manual['url'] = response.url
            manual['product_lang'] = product_lang
            manual['type'] = 'Instructions for use'
            manual['thumb'] = f"https://www.medela.com{thumb_src}"
            yield manual
