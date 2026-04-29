from datetime import date

from cv.models import Company, Position

UNHIDE = Company(
    name="UNHIDE School",
    one_liner="Online learning platform, Rio de Janeiro",
    positions=(
        Position(
            title="Backend Developer",
            start=date(2016, 8, 1),
            end=date(2022, 1, 1),
            location="Rio de Janeiro, Brazil",
            description="""
                Owned the backend API for UNHIDE School's website and associated products: API design, database optimization, server deployments on Amazon RDS, DevOps for frontend and backend teams, and backup tooling for data integrity.
            """,
            keywords=(
                "AWS",
                "Nginx",
                "uWSGI",
                "Python",
                "Flask",
                "SQLAlchemy",
                "PostgreSQL",
                "SQLite",
                "Git",
                "Node.js",
            ),
        ),
    ),
)
