# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from os import getenv
from neo4j import GraphDatabase


class Neo4jPipeline:
    def __init__(self):
        self.neo4j_uri = (
            f"bolt://{getenv('NEO4J_HOST', 'localhost')}:{getenv('NEO4J_PORT', '7687')}"
        )
        self.neo4j_user = getenv("NEO4J_USERNAME", "neo4j")
        self.neo4j_password = getenv("NEO4J_PASSWORD", "password")
        self.driver = None

    def open_spider(self, spider):
        self.driver = GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)
        )

    def close_spider(self, spider):
        self.driver.close()

    def process_item(self, item, spider):
        with self.driver.session() as session:
            # Handle the case when item is None, i.e., when the current
            # link has already been crawled.
            if item:
                session.execute_write(self._create_node, item["url"])
                for link in item["links"]:
                    session.execute_write(self._create_node, link)
                    session.execute_write(self._create_relationship, item["url"], link)
        return item

    @staticmethod
    def _create_node(tx, url):
        tx.run("MERGE (n:Page {url: $url})", url=url)

    @staticmethod
    def _create_relationship(tx, source_url, target_url):
        tx.run(
            """
            MATCH (source:Page {url: $source_url})
            MATCH (target:Page {url: $target_url})
            MERGE (source)-[:LINKS_TO]->(target)
        """,
            source_url=source_url,
            target_url=target_url,
        )
