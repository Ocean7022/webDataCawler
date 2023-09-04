from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time, json

class webAspeedtechTW():
    zhUrl = "https://www.aspeedtech.com/tw/news"
    enUrl = "https://www.aspeedtech.com/news/"
    s = Service(executable_path='./chromedriver.exe')
    driver = webdriver.Chrome(service = s)

    def startCawler(self):
        # to zh page
        print("Start Cawler in zh page")
        self.driver.get(self.zhUrl)
        time.sleep(10)
        zhLinkList = self.getNews(self.driver)
        
        # to en page
        print("Start Cawler in en page")
        self.driver.get(self.enUrl)
        time.sleep(10)
        enLinkList = self.getNews(self.driver)

        # pair the links
        print("Pair the links")
        linkList = self.pairTheLinks(zhLinkList, enLinkList)

        # get page content per page
        for index, link in enumerate(linkList):
            print("Getting en page content")
            enData = self.getPageContent(self.driver, link["en"]["link"])
            print("Getting zh page content")
            zhData = self.getPageContent(self.driver, link["zh"]["link"])

            result = {
                "en_url": link["en"]["link"],
                "zh_url": link["zh"]["link"],
                "category": None,
                "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "para_aligned_status": None,
                "contents": {'zh': zhData, 'en': enData}
            }

            with open(f'../result/aspeedtech_tw/page-{index}.json', 'w', encoding = 'utf-8') as file:
                json.dump(result, file, ensure_ascii = False, indent = 4)

        self.driver.close()

    def getNews(self, driver):
        haveNextPage = True
        newsList = []

        while haveNextPage:
            print("Getting News List")
            time.sleep(3)
            newsElements = driver.find_element(By.ID, "news").find_elements(By.TAG_NAME, "tr")
            for newElement in newsElements:
                td = newElement.find_elements(By.TAG_NAME, "td")
                newsList.append({
                    "date": td[0].text, 
                    "link": td[1].find_element(By.TAG_NAME, "a").get_attribute("href"), 
                    "linkText": td[1].text
                })
            haveNextPage = self.nextPage(driver)
        return newsList
    
    def nextPage(self, driver):
        print("Find next page")
        if driver.find_element(By.ID, "news-next").is_displayed():
            print("Next page is found")
            driver.find_element(By.ID, "news-next").click()
            time.sleep(3)
            return True
        else:
            print("Next page is not found")
            return False

    def pairTheLinks(self, zhLinkList, enLinkList):
        linkList = []
        for zhLink in zhLinkList:
            for enLink in enLinkList:
                if zhLink["date"] == enLink["date"]:
                    linkList.append({
                        "zh": zhLink,
                        "en": enLink
                    })
                    break
        return linkList
        
    def getPageContent(self, driver, link):
        driver.get(link)
        time.sleep(6)

        # get news title
        title = driver.find_element(By.ID, "news-title").text

        # get news content
        contents = driver.find_element(By.ID, "news-content").find_elements(By.TAG_NAME, "p")
        contentList = []
        for zhContent in contents:
            contentList.append(zhContent.text)

        return self.dataFilter([title] + contentList)

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