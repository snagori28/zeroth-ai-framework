from neo4j import GraphDatabase
from config import Config
import logging
import spacy
from .llm_agent import LLM_Agent

logger = logging.getLogger(__name__)

class MemoryAgent:
    """Persist and retrieve facts using a Neo4j graph database."""

    def __init__(self, llm_agent=None):
        """Create a new memory agent and connect to Neo4j."""

        self.llm_agent = llm_agent or LLM_Agent()

        logger.info("Connecting to Neo4j at %s", Config.NEO4J_URI)
        try:
            self.driver = GraphDatabase.driver(
                Config.NEO4J_URI,
                auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD),
            )
            self._ensure_schema()
        except Exception as e:
            logger.error("Failed to connect to Neo4j: %s", e)
            self.driver = None

        self.nlp = spacy.load("en_core_web_sm")

    def close(self):
        """Close the underlying Neo4j driver connection."""
        logger.info("Shutting down MemoryAgent driver")
        if self.driver is not None:
            self.driver.close()

    def _ensure_schema(self):
        """Create basic index/constraints if database is empty."""
        if not self.driver:
            return
        try:
            with self.driver.session() as session:
                session.run(
                    "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Fact) REQUIRE f.name IS UNIQUE"
                )
        except Exception as e:
            logger.error("Schema initialization failed: %s", e)

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
        if not self.driver:
            return None
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Fact {name: $name}) RETURN n.value AS value",
                name=query,
            )
            record = result.single()
            if record:
                return record["value"]

            # Try synonyms from LLM before fuzzy matching
            synonyms = []
            try:
                prompt = f"Provide synonyms or rephrasings for: {query}. Return as comma-separated list"
                resp = self.llm_agent.query(prompt, mode="factual")
                synonyms = [s.strip() for s in resp.split(',') if s.strip()]
            except Exception as e:
                logger.error("LLM synonym lookup failed: %s", e)
            for syn in synonyms:
                result = session.run(
                    "MATCH (n:Fact {name: $name}) RETURN n.value AS value",
                    name=syn,
                )
                rec = result.single()
                if rec:
                    return rec["value"]

            # Fallback: fuzzy match using spaCy similarity
            all_facts = session.run("MATCH (n:Fact) RETURN n.name AS name, n.value AS value").data()
            doc_q = self.nlp(query)
            best = (0, None)
            for rec in all_facts:
                sim = doc_q.similarity(self.nlp(rec["name"]))
                if sim > best[0]:
                    best = (sim, rec["value"])
            if best[0] > 0.75:
                logger.debug("Fuzzy matched fact with similarity %.2f", best[0])
                return best[1]
        return None

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
        if not self.driver:
            logger.error("Cannot store fact; Neo4j unavailable")
            return
        try:
            with self.driver.session() as session:
                session.run(
                    "MERGE (n:Fact {name: $name}) SET n.value = $value, n.source = $source",
                    name=fact,
                    value=value,
                    source=source,
                )
        except Exception as e:
            logger.error("Failed to store fact: %s", e)
