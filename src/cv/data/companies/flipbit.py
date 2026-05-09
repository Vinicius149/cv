from datetime import date

from cv.models import Company, Position

FLIPBIT = Company(
    name="Flipbit Consulting",
    one_liner="Consultoria independente de engenharia de software",
    hidden=True,  # personal CNPJ shell; nothing meaningful happens here
    positions=(
        Position(
            title="Engenheiro de Software Sênior",
            start=date(2022, 1, 1),
            end=None,
            location="Rio de Janeiro, Brazil",
            description="""
                Engenharia de software e consultoria em problemas complexos de backend para empresas e indivíduos. Engajamentos abrangem serviços em Python e Rust, modernização de dados e infraestrutura, melhorias em segurança de tipos, testes e observabilidade, além de revisões arquiteturais.
            """,
        ),
    ),
)
