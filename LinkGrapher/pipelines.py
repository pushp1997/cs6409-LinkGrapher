from os import getenv
from neo4j import GraphDatabase
import networkx as nx


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
        G = self.create_networkx_graph()
        page_ranks = nx.pagerank(G)
        for url, rank in page_ranks.items():
            print(f"URL: {url} - PageRank: {rank:.4f}")
        self.driver.close()

    def process_item(self, item, spider):
        with self.driver.session() as session:
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

    def create_networkx_graph(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (source:Page)-[:LINKS_TO]->(target:Page)
                RETURN source.url as source_url, target.url as target_url
            """
            )
            G = nx.DiGraph()
            for record in result:
                G.add_edge(record["source_url"], record["target_url"])
        return G
