from datetime import date

from cv.models import Company, Position

NUCLEP = Company(
    name="Nuclebras Equipamentos Pesados S.A. (Nuclep)",
    display_name="Nuclep",
    one_liner="State-owned heavy-equipment manufacturer, Rio de Janeiro",
    positions=(
        Position(
            title="Data Engineer",
            start=date(2012, 1, 1),
            end=date(2021, 11, 1),
            location="Rio de Janeiro, Brazil",
            description="""
                Built ETL and reporting pipelines on Python and SQL for workforce and project data, supporting Production Planning and Control. Drove data-quality work (validation, cleansing, enrichment).
            """,
            keywords=(
                "Python 2.x/3.x",
                "C#",
                "SQLAlchemy",
                "MS SQL Server",
                "SQLite",
                "ETL",
                "BI",
            ),
        ),
    ),
)
