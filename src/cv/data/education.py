from datetime import date

from cv.models import Education

EDUCATION = (
    Education(
        institution="SENAC Piracicaba",
        degree="Bacharelado",
        field="Análise e Desenvolvimento de Sistemas",
        start=date(2022, 1, 1),
        end=date(2024, 12, 1),
    ),
)
