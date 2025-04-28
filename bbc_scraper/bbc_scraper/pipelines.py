# Define your item pipelines here
#
import os
import psycopg2
from psycopg2.extras import execute_values

class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT", 5432),
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        # Insert the record; if URL exists, update timestamp_scraped only
        self.cur.execute(
            """
            INSERT INTO bbc_headlines (headline, url, summary, category)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE
              SET headline = EXCLUDED.headline,
                  summary  = EXCLUDED.summary,
                  category = EXCLUDED.category,
                  timestamp_scraped = NOW()
            """,
            (item["headline"], item["url"], item["summary"], item["category"])
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
