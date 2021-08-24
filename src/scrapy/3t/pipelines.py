from itemadapter import ItemAdapter
import json


class ScrapyPipeline():

    def __init__(self):
        self.file = open('shaman_king.json', 'w')
        self.__start_exporting()

    def process_item(self, item):
        line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
        self.file.write(line)
        return item

    def __start_exporting(self):
        self.file.write("{\"product\": [\n")

    def __finish_exporting(self):
        self.file.write("\n]}")

    def close_spider(self):
        self.__finish_exporting()
        self.file.close()
