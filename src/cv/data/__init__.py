"""Source-of-truth life data, assembled into a `CV` instance."""

from __future__ import annotations

from cv.data.education import EDUCATION
from cv.data.experience import COMPANIES
from cv.data.languages import LANGUAGES
from cv.data.open_source import OPEN_SOURCE_PROJECTS
from cv.data.personal import PERSONAL
from cv.models import CV


def build_cv() -> CV:
    return CV(
        personal=PERSONAL,
        companies=COMPANIES,
        education=EDUCATION,
        languages=LANGUAGES,
        open_source=OPEN_SOURCE_PROJECTS,
    )
