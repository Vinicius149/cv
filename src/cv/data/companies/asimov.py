from datetime import date

from cv.models import Company, Position

ASIMOV = Company(
    name="Asimov",
    one_liner="Synthetic-biology platform company, Boston",
    positions=(
        Position(
            title="Senior Backend Engineer",
            start=date(2022, 1, 1),
            end=date(2023, 6, 1),
            location="Boston, MA, USA",
            remote=True,
            description="""
                Bootstrapped the Python/FastAPI backend that replaced the company's Hasura low-code backend for the *Kernel* product and became the foundation for adjacent Python systems. Shipped tested API endpoints with ADR-documented architectural decisions, co-designed a Google Pub/Sub layer for fault-tolerant queued computation between components, and integrated a scientist-authored Codon Optimization package, refactoring it and adding tests and type hints. Built ETL workflows on BigQuery and a SQLAlchemy Core data-migration system that supported stable, idempotent deployments. Mentored engineers across teams on algorithm design, testing, async frameworks, and type hinting.
            """,
            keywords=(
                "Python 3",
                "FastAPI",
                "SQLAlchemy",
                "PostgreSQL",
                "Docker",
                "Redis",
                "Oso",
                "Elasticsearch",
                "Google Pub/Sub",
                "BigQuery",
                "DataDog",
            ),
        ),
    ),
)
