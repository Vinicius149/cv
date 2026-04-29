from __future__ import annotations

import textwrap
from datetime import date
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, HttpUrl, model_validator


def _dedent_strip(v: str) -> str:
    """Normalize triple-quoted markdown blocks: strip common indent + leading/trailing whitespace."""
    return textwrap.dedent(v).strip() if isinstance(v, str) else v


# Use this annotation for any free-form markdown field authored as a triple-quoted string,
# so data files can write naturally indented blocks and the model strips the indentation.
MarkdownText = Annotated[str, BeforeValidator(_dedent_strip)]


class Personal(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    title: str
    location: str
    email: EmailStr
    phone: str | None = None
    github: HttpUrl
    linkedin: HttpUrl
    portfolio: HttpUrl | None = None
    summary: MarkdownText
    epigraph: str | None = None
    epigraph_attribution: str | None = None


class Position(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    start: date
    end: date | None = None
    location: str | None = None
    remote: bool = False
    description: MarkdownText
    keywords: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _check_dates(self) -> Position:
        if self.end is not None and self.end < self.start:
            raise ValueError(f"Position {self.title!r}: end {self.end} before start {self.start}")
        return self


class Company(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    display_name: str | None = None
    one_liner: str | None = None
    url: HttpUrl | None = None
    positions: tuple[Position, ...]
    hidden: bool = False  # if True, sort_companies() drops this company from the render

    @property
    def label(self) -> str:
        return self.display_name or self.name

    @property
    def latest_end(self) -> date:
        """For sorting: most recent end date across positions; ongoing roles → today."""
        return max((p.end or date.today()) for p in self.positions)

    @property
    def earliest_start(self) -> date:
        return min(p.start for p in self.positions)


class Education(BaseModel):
    model_config = ConfigDict(frozen=True)

    institution: str
    degree: str
    field: str | None = None
    start: date | None = None
    end: date | None = None


class Language(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    proficiency: str


class OpenSourceProject(BaseModel):
    """Author-time fields are required; metric fields are filled by `cv refresh-metrics`."""

    model_config = ConfigDict(frozen=True)

    name: str
    repo: str
    tagline: str
    description: MarkdownText
    keywords: tuple[str, ...] = ()
    # Sort key in the rendered Open Source section (ascending; smaller = earlier).
    # Default 100 means "no specific position"; assign 10/20/30/... to prioritize.
    order: int = 100
    language: str | None = None

    stars: int | None = None
    last_commit: date | None = None
    url: HttpUrl | None = None

    @property
    def derived_url(self) -> str:
        return str(self.url) if self.url else f"https://github.com/{self.repo}"


class CV(BaseModel):
    model_config = ConfigDict(frozen=True)

    personal: Personal
    companies: tuple[Company, ...]
    education: tuple[Education, ...]
    languages: tuple[Language, ...]
    open_source: tuple[OpenSourceProject, ...] = ()
