from datetime import date

from cv.models import Company, Position

PUZZL_SOFTWARE_HOUSE = Company(
    name="Puzzl Software House",
    one_liner="Multi-product software studio, Rio de Janeiro (now closed)",
    positions=(
        Position(
            title="Technical Director",
            start=date(2019, 11, 1),
            end=date(2023, 5, 1),
            location="Rio de Janeiro, Brazil",
            description="""
                Provided daily mentoring and technical guidance to developers: task prioritization, technology-stack selection, and best-practice implementation across the studio's portfolio.

                - Built a distributed video-transcoding solution in Python (Django) with PostgreSQL, AWS, Linux, and FFmpeg, enabling efficient and scalable transcoding for client applications.
                - Developed a high-throughput event aggregator in Rust + Diesel, with a WebSocket façade that gave front-ends real-time access to the event stream.
                - Led the from-scratch development of several custom LMS-like products in Python (FastAPI), SQLAlchemy, PostgreSQL, Docker, AWS, and Linux.
                - Architected and operated a 16TB+ Perforce server for a video/art client, ensuring efficient version control and collaboration on large-scale projects.
                - Provided support, maintenance, and improvements on legacy C# codebases.
            """,
            keywords=(
                "Python",
                "FastAPI",
                "Django",
                "Flask",
                "C#",
                "Node",
                "Rust",
                "PostgreSQL",
                "MS SQL Server",
                "Redis",
                "Docker",
                "Linux",
                "AWS",
                "Digital Ocean",
                "Linode",
            ),
        ),
    ),
)
