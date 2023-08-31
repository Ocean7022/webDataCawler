import scrapy

class WebrealteksemiconductorSpider(scrapy.Spider):
    name = "webRealtekSemiconductor"
    allowed_domains = ["www.tpex.org.tw"]
    start_urls = ["https://www.tpex.org.tw/web/index.php?l=zh-tw"]

    def parse(self, response):
        links = response.xpath('//a/@href').getall()

        # get links
        newLinks = []
        for link in links:
            if '?l=en-us' in link or '?l=ja-jp' in link:
                continue
            if link[0] == '/':
                newLinks.append(f'https://{self.allowed_domains[0]}{link}')

        for index, link in enumerate(newLinks):
            if index > 10:
                break
            yield scrapy.Request(link, callback=self.parsePage)

    def parsePage(self, response):
        zhLink = response.url
        enLink = zhLink.replace('?l=zh-tw', '?l=en-us')

        

        return {
            'zh': zhLink,
            'en': enLink
        }




