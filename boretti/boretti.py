import scrapy
import json
from .items import Manual

class BorettiSpider(scrapy.Spider):
    name = "boretti"
    allowed_domains = ["boretti.com"]
    start_urls = [
        {"url": "https://boretti.com/cookers/", "product_parent": "Kitchen"},
        {"url": "https://boretti.com/hoods/", "product_parent": "Kitchen"},
        {"url": "https://boretti.com/ovens/", "product_parent": "Kitchen"},
        {"url": "https://boretti.com/hobs/", "product_parent": "Kitchen"},
        {"url": "https://boretti.com/wine-cabinets/", "product_parent": "Kitchen"},
        {"url": "https://boretti.com/kitchen-accessories/", "product_parent": "Kitchen"},
        {"url": "https://boretti.com/lifestyle/", "product_parent": "Kitchen"},
        {"url": "https://boretti.com/barbecues/", "product_parent": "Barbecue"},
        {"url": "https://boretti.com/gas-barbecues/", "product_parent": "Barbecue"},
        {"url": "https://boretti.com/outdoor-kitchens/", "product_parent": "Barbecue"},
        {"url": "https://boretti.com/barbecue-accessories/", "product_parent": "Barbecue"}
    ]

    def start_requests(self):
        for url_item in self.start_urls:
            yield scrapy.Request(
                url_item['url'], 
                meta={'product_parent': url_item['product_parent']}
            )

    def parse(self, response):
        data = json.loads(response.css('script#__NEXT_DATA__::text').get())
        # file = open('data.json', 'w', encoding='utf-8')
        # file.write(response.css('script#__NEXT_DATA__::text').get())
        products = data['props']['pageProps']['page']['products']

        for product_data in products:
            manual = Manual()
            if isinstance(product_data, dict):
                manual['product_parent'] = response.meta.get('product_parent')
                manual['brand'] = 'Boretti'
                manual['source'] = 'boretti.com'
                manual['url'] = f'https://boretti.com/{product_data["slug"]}/'
                manual['model'] = product_data['sku'].split('/')[-1]
                manual['model_2'] = product_data['title']
                manual['product_lang'] = response.css("html::attr(lang)").get().split("-")[0]
                manual['product'] = data['props']['pageProps']['page']['title']
                try:
                    thumbs = product_data['family']['linkedFrom']['pageProductCollection']['items']
                    for thumb in thumbs:
                        if thumb['sku'] == product_data['sku']:
                            manual['thumb'] = thumb['thumbnailImage1']['url']
                except:
                    continue

                pdf_items = product_data['family']['linkedFrom']['pageProductCollection']['items'][0]['documentsCollection']['items']

                for pdf in pdf_items:
                    if pdf['contentType'] == 'application/pdf':
                        manual['file_urls'] = [pdf['url']]
                        manual['type'] = self.get_type(pdf['title'])
                        if manual['type'] and manual['thumb']:
                            yield manual

    def get_type(self, title):
        if 'manual' in title.lower():
            return 'Manual'
        elif 'energy label' in title.lower():
            return 'Energy Label'
        elif 'line drawing' in title.lower():
            return
        elif 'product information' in title.lower():
            return
        elif 'handeiding' in title.lower() or 'handleiding' in title.lower():
            return 'Handeiding'
        else:
            return title.split('-')[0].strip()
