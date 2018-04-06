# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class KeywordsPipeline(object):

    KEYWORDS = ["garmin", "fenix"]

    def process_item(self, item, spider):
        info = (item['title'] + " " + item['details']).lower()
        if all(k in info for k in KeywordsPipeline.KEYWORDS):
            return item
        raise DropItem
