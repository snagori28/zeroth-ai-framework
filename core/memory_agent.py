from neo4j import GraphDatabase
from config import Config

class MemoryAgent:
    def __init__(self):
        self.driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))

    def retrieve(self, query):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Fact {name: $name}) RETURN n.value AS value", name=query)
            record = result.single()
            return record["value"] if record else None

    def store(self, fact, value, source="user"):
        with self.driver.session() as session:
            session.run(
                "MERGE (n:Fact {name: $name}) SET n.value = $value, n.source = $source",
                name=fact, value=value, source=source
            )
