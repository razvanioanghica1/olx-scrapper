# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from olx.items import OlxItem


class ElectronicsSpider(CrawlSpider):
    name = "electronics"
    allowed_domains = ["www.olx.ro"]
    start_urls = [
        'https://www.olx.ro/hobby-sport-turism/echipamente-sportive-si-turism/q-forerunner-235/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='.pageNextPrev')),
    )

    def parse(self, response):
        rows = response.css('table[summary="Anunt"]')
        for row in rows:
            title = (
                row.css('h3>a.detailsLink>strong::text').extract_first() or
                row.css('h3>a.detailsLinkPromoted>strong::text').extract_first()
            ).strip()
            price = row.css('.price > strong::text').extract_first().strip()
            href = row.css('h3>a.detailsLinkPromoted::attr(href),a.detailsLink::attr(href)').extract_first()
            id = href.split('-')[-1].split('.')[0]

            item = OlxItem()
            item['id'] = id
            item['title'] = title
            item['price'] = price
            item['url'] = href
            yield scrapy.Request(href, callback=self.parse_detail_page, meta={'item': item})

    def parse_detail_page(self, response):
        details = response.css('.descriptioncontent > .clr > p::text').extract_first().strip()
        state = response\
            .css('.descriptioncontent > .details')\
            .xpath('//th[contains(text(),"Stare")]/../td/strong/a/text()')\
            .extract_first().strip()

        item = response.meta.get('item')
        item['details'] = details
        item['state'] = state
        yield item
