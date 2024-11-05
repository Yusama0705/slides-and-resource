from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def crawl(self, url):
        self.driver.get(url)
        # 在这里添加数据提取逻辑，例如：
        title = self.driver.title
        print(f'Title: {title}')

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    crawler = SeleniumCrawler()
    crawler.crawl('https://example.com')
    crawler.close()

