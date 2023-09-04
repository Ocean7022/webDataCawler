from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

class webAspeedtechTW():
    zhUrl = "https://www.aspeedtech.com/tw/news"
    enUrl = "https://www.aspeedtech.com/news/"
    s = Service(executable_path='./chromedriver.exe')
    driverZh = webdriver.Chrome(service = s)
    #driverEn = webdriver.Chrome(service = s)

    def __init__(self):
        # news = {"date": "", "link": "", "linkText": ""}
        newsZh = []

    def startCawler(self):
        self.driverZh.get(self.zhUrl)
        #self.driverEn.get(self.url)

        time.sleep(10)
        zhData = self.getNews(self.driverZh)
        print(zhData)

        self.driverZh.close()
        #self.driverEn.close()

    def getNews(self, driver):
        haveNextPage = True
        newsList = []

        while haveNextPage:
            print("In While loop")
            time.sleep(10)
            newsElements = driver.find_element(By.ID, "news").find_elements(By.TAG_NAME, "tr")
            for newElement in newsElements:
                td = newElement.find_elements(By.TAG_NAME, "td")
                newsList.append({
                    "date": td[0].text, 
                    "link": td[1].find_element(By.TAG_NAME, "a").get_attribute("href"), 
                    "linkText": td[1].text
                })
            haveNextPage = self.nextPage(driver)
            print("Have Next Page", haveNextPage)
        return newsList
    
    def nextPage(self, driver):
        if driver.find_element(By.ID, "news-next").is_displayed():
            print("Check Next Page = Trun")
            driver.find_element(By.ID, "news-next").click()
            time.sleep(10)
            return True
        else:
            return False
