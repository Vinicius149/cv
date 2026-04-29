from datetime import date

from cv.models import Company, Position

FLIPBIT = Company(
    name="Flipbit Consulting",
    one_liner="Independent software engineering consultancy",
    hidden=True,  # personal CNPJ shell; nothing meaningful happens here
    positions=(
        Position(
            title="Staff Software Engineer",
            start=date(2022, 1, 1),
            end=None,
            location="Rio de Janeiro, Brazil",
            description="""
                Software engineering and consulting on hard-to-crack backend problems for companies and individuals. Engagements span Python and Rust services, data and infra modernization, type-safety/testing/observability uplifts, and architectural reviews.
            """,
        ),
    ),
)
