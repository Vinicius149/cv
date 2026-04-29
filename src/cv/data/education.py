from datetime import date

from cv.models import Education

EDUCATION = (
    Education(
        institution="Universidade Estácio de Sá",
        degree="Bachelor's Degree",
        field="Information Systems (Computer Science)",
        start=date(2011, 1, 1),
        end=date(2017, 12, 1),
    ),
    Education(
        institution="Escola Técnica do Rio de Janeiro (ETERJ)",
        degree="Associate's Degree",
        field="Computer Software Technology",
        start=date(2001, 1, 1),
        end=date(2003, 12, 1),
    ),
)
