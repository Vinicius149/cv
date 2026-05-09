from datetime import date

from cv.models import Company, Position

TELEMONT = Company(
    name="Telemont",
    one_liner="Infrastructure and telecom services company",
    positions=(
        Position(
            title="Full Stack Developer",
            start=date(2025, 2, 1),
            end=None,
            location="Remote",
            remote=True,
            description="""Designed and maintained scalable integrations by building secure REST APIs and applying SOLID and Clean Code principles. Modernized legacy PHP 5.3 applications to PHP 8.3/Laravel, following Clean Architecture and MVC; migrated on-premise infrastructure to Azure Cloud, improving performance by over 200% and enabling TDD adoption. Designed and maintained scalable REST/SOAP APIs for microservice integration, applying SOLID, DRY, and Clean Code. Supported observability, automated testing, CI/CD pipelines, and performance improvements for production services.""",
            keywords=(
                "PHP",
                "Python",
                "JavaScript",
                "NodeJS",
                "Redis",
                "Azure",
                "GCP",
                "AWS",
                "MySQL",
                "SQL Server",
                "Laravel",
                "Docker",
                "Linux",
                "Git",
                "Unit Testing",
            ),
        ),
    ),
)
