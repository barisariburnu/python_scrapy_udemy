# -*- coding: utf-8 -*-

import logging
from scrapy.exceptions import DropItem
from udemy.settings import MONGO_USERNAME, MONGO_PASSWORD
from pymongo import MongoClient

client = MongoClient(
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@ac-dczxfng-shard-00-00.latzb7l.mongodb.net:27017,ac-dczxfng-shard-00-01.latzb7l.mongodb.net:27017,ac-dczxfng-shard-00-02.latzb7l.mongodb.net:27017/?ssl=true&replicaSet=atlas-bwqagz-shard-0&authSource=admin&retryWrites=true&w=majority"
)
db = client.udemy
logger = logging.getLogger(__name__)


class UdemyPipeline(object):
    def __init__(self):
        self.post_seen = set()

    def process_item(self, item, spider):
        if item['_id'] in self.post_seen:
            raise DropItem(f"Duplicate item found: {item['_id']}")

        try:
            if str(db.course.insert_one(item)):
                logger.info('Successful course id: {0}'.format(item['_id']))
                self.post_seen.add(item['_id'])
            else:
                logger.error('Error course id: {0}'.format(item['_id']))
                raise DropItem(f"Error item: {item['_id']}")
        except Exception as ex:
            raise DropItem(ex)

        return item
