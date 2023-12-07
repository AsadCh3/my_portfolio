import scrapy

class Manual(scrapy.Item):
    brand = scrapy.Field()
    product = scrapy.Field()
    model = scrapy.Field()
    product_lang = scrapy.Field()
    file_urls = scrapy.Field()
    type = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()

class IbexovenSpider(scrapy.Spider):
    name = "ibexoven"
    allowed_domains = ["berkelequipment.com", "gaylordventilation.com", "stero.com"]

    def start_requests(self):
        urls = ["https://www.berkelequipment.com/slicers",
                  "https://www.berkelequipment.com/vacuum-packaging",
                  "https://www.gaylordventilation.com/products/ventilation",
                  "https://www.gaylordventilation.com/products/demand-control-kitchen-technology-dckv",
                  "https://www.gaylordventilation.com/products/additional-products",
                  "https://www.gaylordventilation.com/resource-center?query=&file-type=258&product-type=all&sort=recent",
                  "https://www.gaylordventilation.com/resource-center?query=&file-type=258&product-type=all&sort=recent&page=1",
                  "https://stero.com/products/rack-conveyors/",
                  "https://stero.com/products/modular-conveyors/",
                  "https://stero.com/products/undercounter/",
                  "https://stero.com/products/pot-pan-utensil-washer/",
                  "https://stero.com/products/door-machines/",
                  "https://stero.com/products/flight-type-conveyors/",
                  "https://stero.com/products/glasswasher/"
                  ]

        for url in urls:
            if "berkelequipment" in url:
                yield scrapy.Request(
                    url,
                    self.parse_berkelequipment
                )
            elif "https://www.gaylordventilation.com/resource-center" in url:
                yield scrapy.Request(
                    url,
                    self.parse_gaylordventilation_manuals,
                )
            elif "gaylordventilation" in url:
                yield scrapy.Request(
                    url,
                    self.parse_gaylordventilation,
                )
            elif "stero.com" in url:
                yield scrapy.Request(
                    url,
                    self.parse_stero
                )

    def parse_stero(self, response):
        manual = Manual()
        
        prod = response.css('h1::text').get()
        if not prod:
            prod = response.css('h1 span::text').get()
        manual["source"] = "stero.com"
        manual["brand"] = "stero"
        manual["product"] = prod

        specsheets = response.css('body').re(r'/specsheets/.+?"')
        for file in specsheets:
            manual["file_urls"] = f"https://www.stero.com{file}"
            manual["type"] = "specsheet"
            manual["model"] = file.split('/')[-1].split('.')[0]
            manual["url"] = response.request.url
            yield manual

    def parse_gaylordventilation_manuals(self, response):
        resource_items = response.css('div.resource-item')

        for resource in resource_items:
            manual = Manual()
            resource_headline = resource.css('div.field-name-field-resource-headline > div.field-items > div.field-item::text').get().strip()
            product = resource.css('div.field-name-field-sub-title > div.field-items > div.field-item::text').get().strip()
            download_resource = resource.css('div.download-resource > a.button::attr(href)').get()

            manual["source"] = "gaylordventilation.com"
            manual["brand"] = "gaylordventilation"
            manual["product"] = product
            manual["file_urls"] = f"https://www.gaylordventilation.com{download_resource}"
            manual["type"] = "Manual"

            manual["model"] = self.clean_model_by_resource_headline(resource_headline)
            if not manual["model"]:
                manual["model"] = self.clean_model_by_product(product)

            manual["url"] = response.request.url
            yield manual

    def clean_model_by_product(self, product: str):
        if 'C-7000A' in product:
            return 'C-7000A' 
        elif 'C-6000D' in product:
            return 'C-6000D' 
        elif 'VH2' in product:
            return 'VH2' 
        elif 'ELXC & ELXC-UV' in product:
            return 'ELXC & ELXC-UV'
        elif 'EL ' in product:
            return 'EL'
        elif 'CUV' in product:
            return 'CUV'
        elif 'CG3-UVi' in product:
            return 'CG3-UVi' 
        elif 'ELX & ELX-UV' in product:
            return 'ELX & ELX-UV'

    def clean_model_by_resource_headline(self, resource_headline: str):
        if 'ELXC-SPC' in resource_headline:
            return 'ELXC-SPC'
        elif 'RSPC-TPF-PCV' in resource_headline:
            return 'RSPC-TPF-PCV'
        elif 'RSPC-TPF-FM-1000A' in resource_headline:
            return 'RSPC-TPF-FM-1000A'
        elif 'RSPC-TPF' in resource_headline:
            return 'RSPC-TPF'
        elif 'RSPC-ESP-OW' in resource_headline:
            return 'RSPC-ESP-OW'

    def parse_gaylordventilation(self, response):
        products = response.css('div.content.product-family-page-lander-teaser')
        for product in products:
            path = product.css('a::attr(href)').extract()[0]
            product_url = f"https://www.gaylordventilation.com{path}"
            yield scrapy.Request(
                product_url,
                self.process_gaylordventilation_prod
            )

    def process_gaylordventilation_prod(self, response):
        manual = Manual()
        manual["source"] = "gaylordventilation.com"
        manual["brand"] = "gaylordventilation"
        manual["product"] = response.css('h1::text').extract()[0]

        files = response.css('a.document-file')
        for file in files:
            title = file.css('::text').get()
            manual["file_urls"] = file.css('::attr(href)').get()

            if "Data Sheet" in title:
                manual["type"] = "Data sheet"
            elif "Spec Sheet" in title:
                manual["type"] = "Spec Sheet"
            elif "Brochures" in title:
                manual["type"] = "Brochures"
            else:
                manual["type"] = "Brochures"

            manual["model"] = None
            manual["url"] = response.request.url
            yield manual

    def parse_berkelequipment(self, response):
        wrapper_class = response.css('div.product-category__items-wrapper')
        articles = wrapper_class.css('article')

        for article in articles:
            path = article.css('a.link::attr(href)').extract()[0]
            full_url = f"https://www.berkelequipment.com{path}"
            yield scrapy.Request(
                full_url,
                self.process_berkelequipment_prod
            )

    def process_berkelequipment_prod(self, response):
        manual = Manual()
        manual["source"] = "berkelequipment.com"
        manual["brand"] = "berkelequipment"
        try:
            file_urls = response.css('div.product__spec-sheet').css('a::attr(href)').extract()[0]
            manual["file_urls"] = f"https://www.berkelequipment.com{file_urls}"
            manual["type"] = "Spec Sheet"
        except:
            manual["file_urls"] = None
            manual["type"] = None

        manual["product"] = response.css('h1.product__title.title-larger::text').extract()[0]
        manual["model"] = response.css('h3.product__model::text').extract()[0].strip().split('#')[-1].strip()
        manual["url"] = response.request.url
        yield manual
