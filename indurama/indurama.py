import scrapy
from .items import Manual

class InduramaSpider(scrapy.Spider):
    name = "indurama"
    allowed_domains = ["latam.indurama.com"]

    start_urls = [
            "https://latam.indurama.com/es/categorias-de-productos/l%C3%ADnea-zafiro",
            "https://latam.indurama.com/es/categorias-de-productos/refrigeraci%C3%B3n",
            "https://latam.indurama.com/es/categorias-de-productos/aires-acondicionados-y-purificadores",
            "https://latam.indurama.com/es/categorias-de-productos/lavadora-semiautom%C3%A1tica",
            "https://latam.indurama.com/es/categorias-de-productos/electromenores",
            "https://latam.indurama.com/es/categorias-de-productos/campanas",
            "https://latam.indurama.com/es/categorias-de-productos/congeladores-tapa-solida",
            "https://latam.indurama.com/es/categorias-de-productos/qled",
            "https://latam.indurama.com/es/categorias-de-productos/vitrinas",
            # uy
            "https://latam.indurama.com/uy/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/uy/categorias-de-productos/anafes",
            # bo
            "https://latam.indurama.com/bo/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/bo/categorias-de-productos/vitrinas",
            # pe - peru
            "https://latam.indurama.com/pe/categorias-de-productos/androidtv",
            "https://latam.indurama.com/pe/categorias-de-productos/linea-quarzo-home",
            "https://latam.indurama.com/pe/categorias-de-productos/refrigeraci%C3%B3n",
            "https://latam.indurama.com/pe/categorias-de-productos/lavadora-autom%C3%A1tica",
            "https://latam.indurama.com/pe/categorias-de-productos/freidoras-de-aire",
            "https://latam.indurama.com/pe/categorias-de-productos/campanas",
            "https://latam.indurama.com/pe/categorias-de-productos/vitrinas",
            "https://latam.indurama.com/pe/categorias-de-productos/congeladores-tapa-solida",
            # co - columbia
            "https://latam.indurama.com/co/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/co/categorias-de-productos/refrigeraci%C3%B3n",
            "https://latam.indurama.com/co/categorias-de-productos/campanas",
            "https://latam.indurama.com/co/categorias-de-productos/vitrinas",
            "https://latam.indurama.com/co/categorias-de-productos/congeladores-tapa-solida",
            # do - dominicia
            "https://latam.indurama.com/do/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/do/categorias-de-productos/refrigeraci%C3%B3n",
            "https://latam.indurama.com/do/categorias-de-productos/electromenores",
            "https://latam.indurama.com/do/categorias-de-productos/campanas",
            "https://latam.indurama.com/do/categorias-de-productos/congeladores-tapa-solida",
            # gt
            "https://latam.indurama.com/gt/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/gt/categorias-de-productos/refrigeraci%C3%B3n",
            "https://latam.indurama.com/gt/categorias-de-productos/vitrinas",
            "https://latam.indurama.com/gt/categorias-de-productos/congeladores",
            # pa - panama
            "https://latam.indurama.com/pa/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/pa/categorias-de-productos/refrigeraci%C3%B3n",
            "https://latam.indurama.com/pa/categorias-de-productos/campanas",
            # ni
            "https://latam.indurama.com/ni/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/ni/categorias-de-productos/refrigeraci%C3%B3n",
            "https://latam.indurama.com/ni/categorias-de-productos/vitrinas",
            # sv
            "https://latam.indurama.com/sv/categorias-de-productos/cocinas-gas",
            "https://latam.indurama.com/sv/categorias/refrigeradoras",
            "https://latam.indurama.com/sv/categorias/empotrables",
            "https://latam.indurama.com/sv/categorias-de-productos/vitrinas",
            # ca
            "https://latam.indurama.com/ca/categorias-de-productos/cocinas-gas",
            # en
            "https://latam.indurama.com/en/categorias-de-productos/gas-stoves"
        ]

    def parse(self, response):
        all_product_urls = response.css('a.node-teaser::attr(href)').getall()
        for url in all_product_urls:
            yield scrapy.Request(f"https://latam.indurama.com{url}", callback=self.parse_products)

    def parse_products(self, response):
        manual = Manual()
        files = response.css('div#descargar-manual > a::attr(href)').getall()
        files += response.css('div#descargar-infomail > a::attr(href)').getall()
        for file in files:
            pdf_file_no = file.split('/')[-1]
            type = 'infomail' if 'infomail' in file else 'manual'

            manual['type'] = type
            manual['file_urls'] = [f"https://latam.indurama.com/_externo/infomail/pdf/{type}_{pdf_file_no}.pdf"] if type == 'infomail' else file
            manual['product'] = response.css('div.cont-info > h3::text').get()
            manual['model'] = response.css('div.cont-info > h1::text').get()
            manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]
            manual['thumb'] = response.css('div.item.active > a::attr(href)').get()
            manual['url'] = response.url
            manual['source'] = 'latam.indurama.com'
            manual['brand'] = 'indurama.com'
            yield manual
