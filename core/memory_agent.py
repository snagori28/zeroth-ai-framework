from neo4j import GraphDatabase
from config import Config
import logging

logger = logging.getLogger(__name__)

class MemoryAgent:
    def __init__(self):
        logger.info("Connecting to Neo4j at %s", Config.NEO4J_URI)
        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD),
        )

    def close(self):
        """Close the underlying Neo4j driver connection."""
        logger.info("Shutting down MemoryAgent driver")
        if self.driver is not None:
            self.driver.close()

    def retrieve(self, query):
        logger.debug("Retrieving fact '%s'", query)
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Fact {name: $name}) RETURN n.value AS value",
                name=query,
            )
            record = result.single()
            return record["value"] if record else None

    def store(self, fact, value, source="user"):
        logger.debug("Storing fact '%s' from %s", fact, source)
        with self.driver.session() as session:
            session.run(
                "MERGE (n:Fact {name: $name}) SET n.value = $value, n.source = $source",
                name=fact,
                value=value,
                source=source,
            )
