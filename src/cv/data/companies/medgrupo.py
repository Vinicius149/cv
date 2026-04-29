from datetime import date

from cv.models import Company, Position

MEDGRUPO = Company(
    name="MEDGRUPO",
    one_liner="Medical-education publisher, Rio de Janeiro",
    positions=(
        Position(
            title="Freelance Software Developer",
            start=date(2012, 1, 1),
            end=date(2022, 1, 1),
            location="Rio de Janeiro, Brazil",
            description="""
                Built and operated a portfolio of always-on internal backend systems for the publisher's video post-production and customer-support workflows: secure content-aware file exchange, customer-inquiry email routing into Zendesk/Freshdesk, mass S3 upload tooling with a DSL-driven configuration system, and seamless Samba uploads for video creators.
            """,
            keywords=(
                "Python 2.x/3.x",
                "AWS",
                "SQLite3",
                "web.py",
                "Boto",
                "PLY",
                "IMAPLIB",
                "Google APIs",
                "C",
                "SAMBA",
            ),
        ),
        Position(
            title="Software Engineering Coordinator",
            start=date(2011, 6, 1),
            end=date(2011, 12, 1),
            location="Rio de Janeiro, Brazil",
            description="""
                Led a mobile-application project that decoded smart tags on printed educational materials. Wrote a custom iOS port of LIBDMTX through an Objective-C wrapper and a custom C89 data-compression algorithm that ported to Windows, Linux, OS X, Android, and iOS as static builds, with a Python ctypes API for internal services.
            """,
            keywords=(
                "C89",
                "Objective-C",
                "LIBDMTX",
                "Datamatrix",
                "iOS",
                "Android",
                "Python 2.x ctypes",
            ),
        ),
    ),
)
