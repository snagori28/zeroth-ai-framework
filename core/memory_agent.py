from neo4j import GraphDatabase
from config import Config
import logging

logger = logging.getLogger(__name__)

class MemoryAgent:
    """Persist and retrieve facts using a Neo4j graph database."""

    def __init__(self):
        """Create a new memory agent and connect to Neo4j."""

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
        """Return the stored value for a fact name, if available.

        Parameters
        ----------
        query : str
            The fact name to search for.

        Returns
        -------
        str or None
            The stored value or ``None`` if the fact is missing.
        """

        logger.debug("Retrieving fact '%s'", query)
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Fact {name: $name}) RETURN n.value AS value",
                name=query,
            )
            record = result.single()
            return record["value"] if record else None

    def store(self, fact, value, source="user"):
        """Store a fact value in the database.

        Parameters
        ----------
        fact : str
            Name of the fact.
        value : str
            Value associated with the fact.
        source : str, optional
            Origin of the fact, e.g. ``"user"`` or ``"document"``.
        """

        logger.debug("Storing fact '%s' from %s", fact, source)
        with self.driver.session() as session:
            session.run(
                "MERGE (n:Fact {name: $name}) SET n.value = $value, n.source = $source",
                name=fact,
                value=value,
                source=source,
            )
