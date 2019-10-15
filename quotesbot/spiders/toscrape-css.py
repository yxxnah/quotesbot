# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from urllib.parse import urljoin
from urllib.parse import unquote

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    # author 정보 크롤링
    def parse_author(self, response):  
        yield {
            'name': response.css("h3.author-title::text").extract(),
            'born': response.css("span.author-born-date::text").extract() + response.css("span.author-born-location::text").extract(),
            'description': response.css("div.author-description::text").extract()
        }

    def parse(self, response):
        for quote in response.css("div.quote"):
            author_page_url = '/author/' + quote.css("small.author::text").extract_first()
            test = scrapy.Request(urllib.parse.unquote(response.urljoin(author_page_url)), callback=self.parse_author)

            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': scrapy.Request(urllib.parse.unquote(response.urljoin(author_page_url)), callback=self.parse_author),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))