from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from elasticsearch import Elasticsearch
import warnings
from datetime import datetime
from dao import es_dao

class Crawling():
    def crawl_stock_one():
        warnings.filterwarnings('ignore')
        es = Elasticsearch()
        res = es.search(index="stock_info", body={"size":0,"aggs":{"code":{"terms":{"field":"code.keyword"}}}})
        
        stock=[]
        for stock_num in res['aggregations']['code']['buckets']:
            driver = webdriver.Chrome('C:/driver/chromedriver')
            main_url = "https://m.stock.naver.com/index.html#/domestic/stock/"+ stock_num['key'] +"/price"
            driver.get(main_url)

            html = driver.page_source
            soup=BeautifulSoup(html, 'html.parser')
            
            for i in soup.select_one('tbody'):
                company=[]
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').text[:6])
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[2]').text)

            for i in soup.select('#content > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div > div.VTablePrice_article__DfdmT > table > tbody > tr:nth-child(1)'):
                company.append(i.select('.VTablePrice_td__PZi0o')[0].text)
                company.append(int(i.select('.VTablePrice_td__PZi0o')[1].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[4].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[5].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[6].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[7].text.replace(',','')))

            stock.append(company)

            time.sleep(1)
        
        driver.close()

        col=['code','name','date','close','open','high','low','volume']
        df = pd.DataFrame(stock,columns=col)
        print(df)
        df.to_csv("C:/ELKStack/dataset/stock.csv", mode='a',header=False,index=False)  

    def crawl_stock_all():
        warnings.filterwarnings('ignore')
        driver = webdriver.Chrome("C:/driver/chromedriver")
        driver.get('https://m.stock.naver.com/index.html#/domestic/capitalization/KOSPI')
        stock=[]
        for i in range(1,11):

            driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div[2]/div[1]/table/tbody/tr[{}]/td[1]/span[1]'.format(i)).click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="common_component_tab"]/div/ul/li[4]/a').click()
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            time.sleep(1)
            html = driver.page_source
            soup=BeautifulSoup(html, 'html.parser')

            for i in soup.select_one('tbody'):
                company=[]
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').text[:6])
                company.append(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/span[2]').text)
                company.append(i.select('.VTablePrice_td__PZi0o')[0].text)
                company.append(int(i.select('.VTablePrice_td__PZi0o')[1].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[4].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[5].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[6].text.replace(',','')))
                company.append(int(i.select('.VTablePrice_td__PZi0o')[7].text.replace(',','')))
                
                stock.append(company)
            driver.back()

            driver.back()
            time.sleep(1)
        
        driver.close()

        col = ['code', 'name', 'date', 'close',
               'open', 'high', 'low', 'volume']
        df = pd.DataFrame(stock, columns=col)
        df
        df.to_csv("C:/ELKStack/dataset/stock.csv", header=False, index=False)

    def crawl_news_one():
        warnings.filterwarnings('ignore')
        stock = []
        es = Elasticsearch()
        res = es.search(index="stock_info", body={"size": 0, "aggs": {
                        "code": {"terms": {"field": "code.keyword"}}}})

        stock = []
        for stock_num in res['aggregations']['code']['buckets']:
            try:
                main_url = "https://m.stock.naver.com/index.html#/domestic/stock/" + \
                    stock_num["key"] + "/news/title"
                driver = webdriver.Chrome("C:/driver/chromedriver")
                driver.get(main_url)
                time.sleep(2)

                for page_num in range(1, 21):
                    news = []
                    time.sleep(1)
                    try:
                        boxItem = driver.find_element_by_css_selector(
                            f"#content > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div > div.VNewsList_article__1gx6H > ul > li:nth-child({page_num}) > a")
                    except:
                        print("Pass")
                        continue
                    boxItem.click()
                    time.sleep(2)

                    # ?????? ????????? ?????? ?????? ????????? ????????? ?????? ????????? ?????? ?????? ???????????? ????????? ?????? ?????? ????????? ??????
                    if datetime.today().strftime("%Y.%m.%d") != driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[1]/div[1]/time').text[:10]:
                        break

                    news.append(driver.find_element_by_xpath(
                        '//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').text[:6])
                    news.append(driver.find_element_by_xpath(
                        '//*[@id="content"]/div[2]/div[1]/div[1]/span[2]').text)
                    news.append(driver.find_element_by_xpath(
                        '//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[1]/div[1]/time').text[:10])
                    news.append(driver.find_element_by_xpath(
                        '//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[1]/strong').text)
                    news.append(driver.find_element_by_xpath(
                        '//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[2]/div[1]').text)

                    time.sleep(2)
                    driver.back()
                    stock.append(news)
                # driver.close()

            except Exception as e:
                print("driver ?????? ?????? ??????", e)
            finally:
                time.sleep(2)
                driver.close()

        col = ['code', 'name', 'date', 'subject', 'content']
        df = pd.DataFrame(stock, columns=col)

        d_records = df.to_dict('records')
        es_dao.save_news(d_records)
        df.to_csv("C:/ELKStack/dataset/news.csv",
                  mode='a', header=False, index=False)

    def crawl_news_all():
        driver = webdriver.Chrome("C:/driver/chromedriver")
        stock = []
        driver.get(
            'https://m.stock.naver.com/index.html#/domestic/capitalization/KOSPI')
        for i in range(1, 11):

            # ??? ?????? ????????????
            driver.find_element_by_xpath(
                '//*[@id="content"]/div[4]/div[2]/div[2]/div[1]/table/tbody/tr[{}]'.format(i)).click()
            time.sleep(1)

            # ???????????? ????????????
            driver.find_element_by_xpath(
                '//*[@id="common_component_tab"]/div/ul/li[3]/a/span').click()
            time.sleep(1)

            # ?????? ??????
            for i in range(3):
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            for i in range(1, 61):

                time.sleep(3)
                news = []
                try:
                    driver.find_element_by_xpath(
                        '//*[@id="content"]/div[4]/div[3]/div[2]/div/div[4]/ul/li[{}]/a'.format(i)).click()
                except:
                    print("Pass")
                    continue
                time.sleep(2)

                news.append(driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div[1]/div[1]/span[1]').text[:6])
                news.append(driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div[1]/div[1]/span[2]').text)
                news.append(driver.find_element_by_xpath(
                    '//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[1]/div[1]/time').text[:10])
                news.append(driver.find_element_by_xpath(
                    '//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[1]/strong').text)
                news.append(driver.find_element_by_xpath(
                    '//*[@id="content"]/div[4]/div[3]/div[2]/div/div[1]/div[2]/div[1]').text)

                time.sleep(2)
                driver.back()
                time.sleep(2)
                stock.append(news)

            driver.back()
            time.sleep(2)
            driver.back()
            time.sleep(2)

        col = ['code', 'name', 'date', 'subject', 'content']
        df = pd.DataFrame(stock, columns=col)
        d_records = df.to_dict('records')
        es_dao.save_news(d_records)
        df.to_csv("C:/ELKStack/dataset/news.csv", header=False, index=False)
    

# if __name__ == '__main__':
    # Crawling.crawl_stock_all()
    # Crawling.crawl_stock_one()
    # Crawling.crawl_news_all()
    # Crawling.crawl_news_one()
    # pass
