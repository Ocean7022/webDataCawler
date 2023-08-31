import scrapy


class WebrealteksemiconductorSpider(scrapy.Spider):
    name = "webRealtekSemiconductor"
    allowed_domains = ["www.realtek.com"]
    start_urls = ["https://www.realtek.com/en/"]

    def parse(self, response):
        pass
