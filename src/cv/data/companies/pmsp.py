from datetime import date

from cv.models import Company, Position

PMESP = Company(
    name="Diretoria de Tecnologia e Informação da PMESP",
    one_liner="Orgão de tecnologia da Polícia Militar do Estado de São Paulo",
    positions=(
        Position(
            title="Desenvolvedor Full Stack",
            start=date(2022, 3, 1),
            end=date(2025, 2, 1),
            location="São Paulo, SP",
            remote=False,
            description="""- Participei do desenvolvimento ágil de um sistema de gestão de estoque com PHP/Laravel/MySQL, garantindo auditoria e rastreabilidade de suprimentos.
- Implementei testes automatizados unitários e de integração, pipelines CI/CD e revisão de código para aumentar a confiabilidade das entregas.
- Gerenciei infraestrutura Linux e Windows Server, solucionei integrações entre sistemas e mantive SLA em um ambiente ágil.
- Contribuí para documentação de arquitetura e práticas de observabilidade, antecipando e resolvendo problemas de performance, segurança e escalabilidade.
- Trabalhei de forma colaborativa para entregar software de qualidade e operação confiável.""",
            keywords=(
                "PHP",
                "MySQL",
                "Laravel",
                "TDD",
                "CI/CD",
                "Git",
                "Linux",
                "Docker",
                "Observabilidade",
                "Arquitetura de Software",
                "Design Patterns",
            ),
        ),
    ),
)
