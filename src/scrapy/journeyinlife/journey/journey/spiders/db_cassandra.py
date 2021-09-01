import cassandra

from cassandra.cluster import Cluster, log
from cassandra.query import SimpleStatement

from src.scrapy.journeyinlife.journey.journey.items import JourneyItem

# keyspace only key lower
KEYSPACE = 'journey_in_life'


class db_cassandra:
    cluster = None
    session = None

    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect()

        self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
                """ % KEYSPACE)
        self.session.set_keyspace(KEYSPACE)

    def create_table_phrase(self):
        self.session.execute("""
                CREATE TABLE IF NOT EXISTS JOURNEY (
                    key text,
                    title text,
                    link text,
                    thumb text,
                    content text,
                    image_url text,
                    PRIMARY KEY (key)
                )
                """)

    query_insert = SimpleStatement("""
                  INSERT INTO JOURNEY (key, title, link, thumb, content, image_url)
                  VALUES (%(key)s, %(title)s, %(link)s, %(thumb)s, %(content)s, %(image_url)s)
                  """, consistency_level=cassandra.ConsistencyLevel.ONE)

    def insert_db(self, items):
        for journey in items:

            if journey is None or journey.key is None:
                return
            print(f'insert {journey.title}')
            self.session.execute(self.query_insert,
                                 dict(key=journey.key,
                                      title=journey.title,
                                      link=journey.link,
                                      thumb=journey.thumb,
                                      content=journey.str_content,
                                      image_url=journey.image))

    def get_db(self):
        future = self.session.execute_async("SELECT * FROM JOURNEY WHERE content ='' limit 10 ALLOW FILTERING")
        try:
            rows = future.result()
            return rows
        except Exception:
            log.exception("Error reading rows:")
            return None

        # for row in rows:
        #     print('\t'.join(row))
        #     # log.info('\t'.join(row))
        # return rows

    def drop_keyspace(self):
        pass
        # self.session.execute("DROP KEYSPACE " + KEYSPACE)


if __name__ == '__main__':
    db = db_cassandra()
    db.create_table_phrase()
    # item = JourneyItem()
    # item.key = '123'
    # item.title = '123title'
    # item.link = '123link'
    # item.thumb = '123thumb'
    # db.insert_db(item)
    # db.get_db()
    # db.drop_keyspace()
