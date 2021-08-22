from itemadapter import ItemAdapter
import json


class ScrapyPipeline(object):

    def __init__(self):
        self.file = open('result.json', 'w')

    def process_item(self, item):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

    def close_spider(self):
        self.file.close()
