from datetime import date

from cv.models import Company, Position

PMESP = Company(
    name="Diretoria de Tecnologia e Informação da PMESP",
    display_name="PMESP",
    one_liner="São Paulo public-sector agency",
    positions=(
        Position(
            title="Full Stack Developer",
            start=date(2022, 3, 1),
            end=date(2025, 2, 1),
            location="São Paulo, SP",
            remote=False,
            description="""Built a complete inventory management system in PHP/Laravel/MySQL with auditability and traceability for supply tracking. Implemented automated unit and integration tests to reduce regressions and improve release confidence. Managed Linux and Windows Server infrastructure and resolved integration issues between systems, helping maintain SLA compliance and operational continuity in an agile delivery environment.""",
            keywords=("PHP", "Python", "WordPress", "MySQL", "Laravel", "TDD", "Git", "Linux", "Docker"),
        ),
    ),
)