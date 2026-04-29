from datetime import date

from cv.models import Company, Position

CAVAGUTI = Company(
    name="Cavaguti Caminhões",
    one_liner="Heavy-vehicle dealership, Rio de Janeiro",
    hidden=True,
    positions=(
        Position(
            title="IT Manager",
            start=date(2010, 3, 1),
            end=date(2011, 5, 1),
            location="Rio de Janeiro, Brazil",
            description="""
                Coordinated IT and governance for ~100 workstations across five geographically dispersed sites interconnected via high-speed leased lines.

                - Oversaw IT staff: service-desk management, task assignment and prioritization, and project coordination.
                - Provided ERP support to ensure smooth operation and resolve user issues.
                - Provisioned and maintained servers across RedHat, CentOS, Debian, and Windows Server 2003.
                - Provisioned VPN and remote access for secure remote connectivity.
                - Wrote internal tools and automation in Python 2.x, shell, and PHP: scripts, backup routines, and IT process automation.
            """,
        ),
    ),
)
