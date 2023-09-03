import scrapy, json, re
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

        #yield scrapy.Request(newLinks[0], callback=self.parseZhPage)
        #return

        for index, link in enumerate(newLinks):
            if index > 9:
                break
            yield scrapy.Request(link, callback=self.parseZhPage, meta={'pageIndex': index})

    def parseZhPage(self, response):
        if response.status == 404:
            return

        zhLink = response.url
        enLink = zhLink.replace('?l=zh-tw', '?l=en-us')

        zhData = self.getData(response)

        yield scrapy.Request(enLink,  callback=self.parseEnPage, meta={'zhData': zhData, 'zhLink': zhLink, 'pageIndex': response.meta['pageIndex']})

    def parseEnPage(self, response):
        pageIndex = response.meta['pageIndex']

        zhLink = response.meta['zhLink']
        enLink = response.url

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
        
        with open(f'../../result/tpex_tw/page{pageIndex}.json', 'w', encoding = 'utf-8') as file:
            json.dump(result, file, ensure_ascii = False, indent = 4)
    
    def getData(self, response):
        text = response.xpath('//a/text()').getall()

        return self.dataFilter(text)
    
    def checkDataNumber(self, zhData, enData):
        if len(zhData) != len(enData):
            return 'Data number is not equal'
        
    def dataFilter(self, dataList):
        pattern = r'^[^\w\s]+$'
        newDataList = []
        for data in dataList:
            if data.isnumeric():
                continue

            data.replace('\n', '')
            data.replace('\r', '')
            data.replace('\t', '')

            if re.match(pattern, data):
                continue

            newDataList.append(data.strip())

        return [item for item in newDataList if item != ""]




