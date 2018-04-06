# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from olx.items import OlxItem


class ElectronicsSpider(CrawlSpider):
    name = "electronics"
    allowed_domains = ["www.olx.ro"]
    start_urls = [
        'https://www.olx.ro/hobby-sport-turism/echipamente-sportive-si-turism/q-fenix/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='.pageNextPrev')),
        Rule(LinkExtractor(allow=('oferta/',)),
             callback="parse_item",
             follow=False),)

    def parse_item(self, response):
        title = response.css('.offer-titlebox > h1::text').extract()[0].strip()
        details = response.css('.descriptioncontent > .clr > p::text').extract()[0].strip()
        price = response.css('.pricelabel > strong::text').extract()[0]

        item = OlxItem()
        item['title'] = title
        item['details'] = details
        item['price'] = price
        item['url'] = response.url
        yield item
