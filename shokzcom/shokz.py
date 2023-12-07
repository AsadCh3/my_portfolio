import scrapy

from .items import Manual


class ShokzSpider(scrapy.Spider):
    name = "shokz"

    start_urls = ['https://uk.shokz.com/', 'https://www.shokz.cz/']
    subdomains = ["ca", "de", "nl", "fr", "jp"]

    urls = list()
    rfiles = set()

    def parse(self, response):
        if response.request.url == 'https://www.shokz.cz/':
            url_section = response.css('ul#menu-main-menu')
            sub_menu = url_section.css('ul.sub-menu')
            urls = sub_menu.css('a::attr(href)').extract()
            for url in urls: self.urls.append(url)

        for url_sel in response.css('a::attr(href)').getall():
            if '/products' in url_sel:
                for subdomain in self.subdomains:
                    url = f"https://{subdomain}.shokz.com{url_sel}"
                    if subdomain == "vn": url = f"https://www.shokz.com.{subdomain}/"
                    self.urls.append(url)

        for url in self.urls:
            yield scrapy.Request(url,callback=self.parse_item)

    def parse_item(self, response, **kwargs):
        pdfs_span = response.css("a[href*='.pdf'] span::text").getall()
        pdfs_text = response.css("a[href*='.pdf']::text").getall()
        pdfs_links = response.css("a[href*='.pdf']::attr(href)").getall()

        pdf = [
            pp
            for pp in pdfs_span
            if "manual" in pp.lower()
            or "manuál" in pp.lower()
            or "user_guide" in pp.lower()
            or "user guide" in pp.lower()
            or "mode d'emploi" in pp.lower()
            or "userguide" in pp.lower()
        ]

        if not pdf:
            pdf = [
                pp
                for pp in pdfs_text
                if "manual" in pp.lower()
                or "manuál" in pp.lower()
                or "user_guide" in pp.lower()
                or "user guide" in pp.lower()
                or "mode d'emploi" in pp.lower()
                or "userguide" in pp.lower()
            ]

        if not pdf:
            pdf = [
                pp
                for pp in pdfs_links
                if "manual" in pp.lower()
                or "manuál" in pp.lower()
                or "user_guide" in pp.lower()
                or "user guide" in pp.lower()
                or "mode d'emploi" in pp.lower()
                or "userguide" in pp.lower()
            ]

        if not pdf:
            self.logger.warning("No manual found")
            return

        for pdf_sel in response.css('a[href*=".pdf"]'):
            manual = Manual()
            rfile = pdf_sel.css("::attr(href)").get()
            if rfile in self.rfiles:
                continue
            self.rfiles.add(rfile)

            rtype = self.clean_type(rfile)
            if not rtype:
                rtype = self.clean_type(pdf_sel.css("::text").get())
            if not rtype:
                rtype = self.clean_type(pdf_sel.css("span::text").get())
            manual["file_urls"] = [rfile]
            manual["type"] = rtype

            # Model
            # model = response.css(".c-variant-picker__title::text").get()
            # if not model:
            #     model = response.css(".product-single__meta h1::text").get()
            #     if response.css(".product-single__meta h1 strong::text").get():
            #         model = (
            #             model
            #             + " "
            #             + response.css(".product-single__meta h1 strong::text").get()
            #         )
            # if not model:
            #     model = response.css("title::text").get()
            # if not model.strip():
            #     continue
            # manual["model"] = (
            #     model.replace("- shokz", "").replace("- Shokz.cz", "").strip()
            # )
            manual["model"] = self.clean_model(response.request.url)

            # Products

            product = self.clean_product(response.request.url)
            manual["product"] = product

            thumb = response.css(
                'meta[property*="og:image:secure_url"]::attr(content)'
            ).get()
            if not thumb:
                continue
            manual["thumb"] = thumb
            manual["eans"] = response.css(
                "[data-product-id]::attr(data-product-id)"
            ).get()
            manual["url"] = response.url
            manual["source"] = self.name
            manual["brand"] = "Shokz"
            manual["product_lang"] = (
                response.css("html::attr(lang)").get().split("-")[0]
            )

            yield manual

    def clean_model(self, url):
        model = url
        if 'opencomm2uc' in model:
            return 'OpenComm2UC'
        elif 'opencomm2' in model:
            return 'OpenComm2'
        elif 'opencomm' in model:
            return 'OpenComm'
        elif 'openrun-pro' in model:
            return 'OpenRun Pro'
        elif 'openrun-mini' in model:
            return 'OpenRun Mini'
        elif 'openrun' in model:
            return 'OpenRun'
        elif 'openswim' in model:
            return 'OpenSwim'
        elif 'open-pro-mini' in model:
            return 'OpenRun PRO Mini'
        elif 'openfit' in model:
            return 'OpenFit'
        elif 'open-move' in model or 'openmove' in model:
            return 'OpenMove'
        elif 'dongle' in model:
            return 'Dongle'


    def clean_type(self, rtype):
        if not rtype:
            return rtype
        elif (
            "manual" in rtype.lower()
            or "uživatelský manuál" in rtype.lower()
            or "huong" in rtype.lower()
            or "日本語 >" in rtype
            or "-uk" in rtype.lower()
            or "1646184252" in rtype
        ):
            return "User Manual"
        elif "size" in rtype.lower():
            return "Size Guide"
        elif "guide" in rtype.lower() or "AEROPEX" in rtype:
            return "User Guide"
        elif "line drawings" in rtype.lower():
            return "Line Drawings"
        elif "instructions" in rtype.lower():
            return "Instructions"
        else:
            return ""

    def clean_product(self, url):
        if "opencomm2" in url:
            return "Bone Conduction Stereo Bluetooth Headset"
        elif "opencomm" in url:
            return "Bone Conduction Stereo Headset"
        elif "openfit" in url:
            return "Open-Ear True Wireless Earbuds"
        elif "opencomm2uc" in url:
            return "UC Bone Conduction Stereo Bluetooth Headset"
        elif "openrun" in url:
            return "Open-Ear Bone Conduction Wireless Headphones"
        elif "openswim" in url:
            return "Waterproof Bone Conduction MP3 Headphones"
        elif "openrun-charging-cable" in url:
            return "Aeropax Magnetic Charging Cable"
        elif "openmove" in url or "open-move" in url:
            return "Wireless Bone Conduction Headphones"
        elif "opencomm-charging-cable" in url:
            return "Charging Cable"
        elif "dongle" in url:
            return "Loop 110 Wireless Adapter"
        elif "openswim-charging-data-cable" in url:
            return "Charging / Data Cable"
        elif "openrun-pro" in url:
            return "Pro Open-Ear Bone Conduction Wireless Headphones"
