import scrapy, json
from datetime import datetime

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

        yield scrapy.Request(newLinks[0], callback=self.parseZhPage)
        return

        for index, link in enumerate(newLinks):
            if index > 1:
                break
            yield scrapy.Request(link, callback=self.parseZhPage)

    def parseZhPage(self, response):
        zhLink = response.url
        enLink = zhLink.replace('?l=zh-tw', '?l=en-us')

        zhData = self.getData(response)

        yield scrapy.Request(enLink,  callback=self.parseEnPage, meta={'zhData': zhData, 'zhLink': zhLink})

    def parseEnPage(self, response):
        zhLink = response.meta['zhLink']
        enLink = response.url

        title = response.xpath('//title/text()').get()

        zhData = response.meta['zhData']
        enData = self.getData(response)

        result = {
                "en_url": enLink,
                "zh_url": zhLink,
                "category": self.checkDataNumber(zhData, enData),
                "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "para_aligned_status": None,
                "contents": {'zh': zhData, 'en': enData}
            } 
        
        with open(f'../../result/tpex_tw/{title}.json', 'w', encoding = 'utf-8') as file:
            json.dump(result, file, ensure_ascii = False, indent = 4)
    
    def getData(self, response):
        tab_a_text = response.xpath('//a/text()').getall()
        return tab_a_text
    
    def checkDataNumber(self, zhData, enData):
        if len(zhData) != len(enData):
            return 'Data number is not equal'
        
    def dataFilter(self, data):
        pass




