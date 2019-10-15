# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from urllib.parse import urljoin
from urllib.parse import unquote
from quotesbot.items import QuotesbotItem

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            author_page_url = '/author/' + quote.css("small.author::text").get()

            # 항목 정의
            item = QuotesbotItem()
            item['text'] = quote.css("span.text::text").get().strip()
            item['tags'] = quote.css("div.tags > a.tag::text").getall()

            # 콜백 요청
            yield scrapy.Request(urllib.parse.unquote(response.urljoin(author_page_url)), meta={'item':item}, callback=self.parse_author)

        next_page_url = response.css("li.next > a::attr(href)").get().strip()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    # author 정보 크롤링
    def parse_author(self, response):  
        author = {
            'name': response.css("h3.author-title::text").get().strip(),
            'born': response.css("span.author-born-date::text").get().strip() + response.css("span.author-born-location::text").get().strip(),
            'description': response.css("div.author-description::text").get().strip()
        }

        item = response.request.meta['item']
        item['author'] = author

        yield item