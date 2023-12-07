import scrapy

class Manual(scrapy.Item):
    model = scrapy.Field()
    model_2 = scrapy.Field()
    brand = scrapy.Field()
    product = scrapy.Field()
    product_parent = scrapy.Field()
    product_lang = scrapy.Field()
    file_urls = scrapy.Field()
    eans = scrapy.Field()
    files = scrapy.Field()
    type = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    thumb = scrapy.Field()

class ArtromSpider(scrapy.Spider):
    name = "artrom"
    allowed_domains = ["artrom.es"]
    start_urls = [
        "https://artrom.es/familias-de-productos/aire-acondicionado/",
        "https://artrom.es/humidificadores/",
        "https://artrom.es/deshumidificadores/",
        "https://artrom.es/climatizadores-evaporativos/",
        "https://artrom.es/ventilacion/",
        "https://artrom.es/cocina/microondas/",
        "https://artrom.es/cocina/hornos",
        "https://artrom.es/cocina/pequeno-electrodomestico/"
    ]

    def parse(self, response):
        products = response.css('article.obfx-grid-col')
        data = self.get_product_and_prod_parent(response.request.url)
        for product in products:
            prodcut_url = product.css('a::attr(href)').get()
            yield scrapy.Request(prodcut_url, callback=self.parse_product, meta=data)

        if response.request.url == "https://artrom.es/deshumidificadores/":
            url = f"https://artrom.es/deshumidificadores/page/2/"
            yield scrapy.Request(url, self.parse)
        elif response.request.url == "https://artrom.es/climatizadores-evaporativos/":
            url = f"https://artrom.es/climatizadores-evaporativos/page/2/"
            yield scrapy.Request(url, self.parse)

    def parse_product(self, response):
        manual = Manual()
        thumb_element = response.css('img.attachment-shop_single.size-shop_single.wp-post-image::attr(src)').get()
        manual["thumb"] = thumb_element
        manual["product"] = response.meta['product']
        manual["product_parent"] = response.meta['product_parent']
        product_title = response.css('h1.product_title::text').get()
        manual["model"] = product_title
        manual["brand"] = "Artrom"
        manual["product_lang"] = "es"

        file_urls = response.xpath('//*[@id="tab-description"]/p[3]/a')
        file_urls = file_urls.css('a::attr(href)').get()
        manual["file_urls"] = file_urls
        manual["eans"] = ""
        manual["type"] = "Manual usuario"
        manual["url"] = response.request.url
        manual["source"] = "artrom.es"
        if file_urls:
            yield manual

    def get_product_and_prod_parent(self, url):
        data = dict()
        if 'aire-acondicionado' in url:
            data['product'] = 'Aire acondicionado'
            data['product_parent'] = 'Climatización'
        elif 'humidificadores' in url:
            data['product'] = 'Humidificadores'
            data['product_parent'] = 'Climatización'
        elif 'deshumidificadores' in url:
            data['product'] = 'Deshumidificadores'
            data['product_parent'] = 'Climatización'
        elif 'climatizadores-evaporativos' in url:
            data['product'] = 'Climatizadores Evaporativos'
            data['product_parent'] = 'Climatización'
        elif 'ventilacion' in url:
            data['product'] = 'Ventilacion'
            data['product_parent'] = 'Climatización'
        elif 'microondas' in url:
            data['product'] = 'Microondas'
            data['product_parent'] = 'Cocina'
        elif 'hornos' in url:
            data['product'] = 'Hornos'
            data['product_parent'] = 'Cocina'
        elif 'pequeno-electrodomestico' in url:
            data['product'] = 'Pequeno Electrodomestico'
            data['product_parent'] = 'Cocina'
        
        return data
