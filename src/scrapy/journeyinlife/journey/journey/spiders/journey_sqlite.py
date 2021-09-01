import sqlite3

from src.scrapy.journeyinlife.journey.journey.items import JourneyItem


class journey_sqlite:
    connect = None

    def __init__(self):
        self.connect = sqlite3.connect('journey.db')
        self.init_db()

    def init_db(self):
        cur = self.connect.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS JOURNEY (
                    key text primary key,
                    title text,
                    link text,
                    thumb text,
                    content text,
                    image_url text
                )
        ''')
        self.connect.commit()

    def close(self):
        self.connect.close()

    def import_data(self, row):
        self.connect = sqlite3.connect('journey.db')
        cur = self.connect.cursor()
        cur.execute("insert or IGNORE INTO JOURNEY (key,title,link,thumb,content, image_url) values (?, ?, ?, ?, ?, ?)",
                    (row.key, row.title, row.link, row.thumb, row.content, row.image_url))
        self.connect.commit()
        self.connect.close()


if __name__ == '__main__':
    jr_sqlite = journey_sqlite()
    jr_sqlite.init_db()
    jr_sqlite.close()
