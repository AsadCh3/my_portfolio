import scrapy
from .items import Manual

class ClimadiffSpider(scrapy.Spider):
    name = "climadiff"
    allowed_domains = ["climadiff.com"]
    start_urls = [
        "https://www.climadiff.com/gb/19-aging-wine-cellar",
        "https://www.climadiff.com/gb/21-multi-purpose-wine-cellars",
        "https://www.climadiff.com/gb/22-service-wine-cellars",
        "https://www.climadiff.com/gb/40-caves-a-vin-connectees",
        "https://www.climadiff.com/gb/23-built-in-wine-cellars",
        "https://www.climadiff.com/gb/23-built-in-wine-cellars",
        "https://www.climadiff.com/gb/12-wine-cellars-shelves",
        "https://www.climadiff.com/gb/13-carbon-filters",
        "https://www.climadiff.com/gb/15-thermometer-hygrometer",
        "https://www.climadiff.com/gb/35-mobile-air-conditioners",
        "https://www.climadiff.com/gb/36-air-fresheners",
        "https://www.climadiff.com/gb/32-air-cleaners",
        "https://www.climadiff.com/gb/38-filters",
        "https://www.climadiff.com/gb/44-fin-de-serie",
        "https://www.climadiff.com/gb/43-anciennes-references",
        "https://www.climadiff.com/gb/14-wine-products",
        "https://www.climadiff.com/fr/19-aging-wine-cellar",
        "https://www.climadiff.com/fr/21-multi-purpose-wine-cellars",
        "https://www.climadiff.com/fr/22-service-wine-cellars",
        "https://www.climadiff.com/fr/40-caves-a-vin-connectees",
        "https://www.climadiff.com/fr/23-built-in-wine-cellars",
        "https://www.climadiff.com/fr/23-built-in-wine-cellars",
        "https://www.climadiff.com/fr/12-wine-cellars-shelves",
        "https://www.climadiff.com/fr/13-carbon-filters",
        "https://www.climadiff.com/fr/15-thermometer-hygrometer",
        "https://www.climadiff.com/fr/35-mobile-air-conditioners",
        "https://www.climadiff.com/fr/36-air-fresheners",
        "https://www.climadiff.com/fr/32-air-cleaners",
        "https://www.climadiff.com/fr/38-filters",
        "https://www.climadiff.com/fr/44-fin-de-serie",
        "https://www.climadiff.com/fr/43-anciennes-references",
        "https://www.climadiff.com/fr/14-wine-products"
    ]

    def parse(self, response):
        product_elems = response.css('div.item')
        for product_elem in product_elems:
            product_url = product_elem.css('a::attr(href)').get()
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        manual = Manual()
        title = response.css('h1::text').re(r'\b[A-Z0-9]+\b')
        if len(title) > 0:
            for file_elem in response.css('div.attachment'):
                manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]
                manual['product_parent'] = response.xpath('//*[@id="wrapper"]/div/nav/ol/li[2]/a/span/text()').get().strip()
                if title[0].strip().isdigit():
                    continue
                manual['model'] = title[0].strip()
                product = response.xpath('//*[@id="wrapper"]/div/nav/ol/li[3]/a/span/text()').get().replace(title[0], '')
                if 'bouteilles' in product:
                    product = product.replace('bouteilles', '').replace('-', '')[:-4]
                manual['product'] = product.strip().title()
                file_urls = file_elem.css('a::attr(href)').get()
                file_urls = 'https:' + file_urls if 'https' not in file_urls else file_urls
                manual['file_urls'] = [file_urls]
                manual['type'] = file_elem.css('a::text').get().split(' ')[0].strip()
                if manual['type'] == '':
                    manual['type'] = file_elem.css('div.attachment a').re('</i>(.+)</a>')[0].split(' ')[0]
                manual['brand'] = 'Climadiff'
                manual['url'] = response.url
                manual['source'] = 'climadiff.com'
                manual['thumb'] = response.css('div.images-container img::attr(src)').get()
                yield manual
 
