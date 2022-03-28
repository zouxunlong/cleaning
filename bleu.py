from multiprocessing import Process, Queue
import scrapy
import json
from scrapy.crawler import CrawlerRunner,CrawlerProcess
import scrapy.crawler as crawler
from twisted.internet import reactor
from pymongo import MongoClient
import datetime
from bs4 import BeautifulSoup
import configuration

client = MongoClient(configuration.MONGO_CONNECTION_STRING)


class CNASpider(scrapy.Spider):
    name = 'CNA'

    # set USER_AGENT to avoid CNA web Anti-crawler technique
    custom_settings = {
        "USER_AGENT": "PostmanRuntime/7.28.4",
    }

    # set urls, start from 1, to unlimited number, as large as it can reach to the history new data
    start_urls = [
        'https://www.channelnewsasia.com/api/v1/infinitelisting/94f7cd75-c28b-4c0a-8d21-09c6ba3dd3fc?_format=json&viewMode=infinite_scroll_listing&page=%d' % n for n in range(1, 200)]

    # parse start url to get news page links
    def parse(self, response):
        data = json.loads(response.body)
        for item in data['result']:
            absolute_url = item['absolute_url']
            author = item['author']
            release_date = datetime.datetime.strptime(item['release_date'], '%Y-%m-%dT%H:%M:%S%z')
            title = item['title']
            result = client['CNA']['news'].update_one(
                {'_id': absolute_url}, {'$setOnInsert': {'user_id': author, 'created_at': release_date}}, upsert=True)
            print(result.upserted_id)
            if result.matched_count != 0:
                continue
            yield scrapy.Request(url=absolute_url, callback=self.parse_article, dont_filter=True, meta={'title': title})

    # parse each news link to get the article text
    def parse_article(self, response):
        text = response.meta['title']
        paragraphs = response.xpath(
            '//*[@id="block-mc-cna-theme-mainpagecontent"]/article[1]/div[1]/div[4]/div[1]/section[1]//div/div/div/div/p')

        for paragraph in paragraphs:
            # text += ''.join(paragraph.xpath('.//text()').extract()) + '\n'

            t = BeautifulSoup(paragraph.get(), "lxml").text
            text += t + '\n'
        client['CNA']['news'].update_one({'_id': response.url}, {'$set': {'text': text}})


def search_new_cna():
    runner = CrawlerRunner()
    d = runner.crawl(CNASpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    result=client.get_database('CNA').get_collection('news').delete_many({'text': {'$eq':None}})
    print(result.deleted_count)
    return "cna search finished"


def search_new_cna_stop():
    try:
        reactor.stop()
        return "cna search stopped"
    except:
        return "cna search isn't running"