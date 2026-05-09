from datetime import date

from cv.models import Company, Position

TELEMONT = Company(
    name="Telemont",
    one_liner="Empresa de engenharia especializada em soluções de telecomunicações",
    positions=(
        Position(
            title="Desenvolvedor Full Stack",
            start=date(2025, 2, 1),
            end=None,
            location="Remoto",
            remote=True,
            description="""- Participei do desenvolvimento ágil de software, entregando soluções confiáveis e escaláveis para integrações de sistemas.
- Construí APIs REST/SOAP seguras para comunicação entre microserviços, com autenticação, tratamento de erros e foco em confiabilidade.
- Modernizei aplicações legadas PHP 5.3 para PHP 8.3/Laravel usando arquitetura limpa, MVC, padrões SOLID e boas práticas de Design Patterns.
- Implementei testes automatizados e pipelines CI/CD com revisão de código; mantive observabilidade e monitoramento em produção.
- Apoiei a documentação de arquitetura, antecipei problemas de performance e escalabilidade e resolvi incidentes com o time.""",
            keywords=(
                "PHP",
                "Python",
                "Laravel",
                "Azure",
                "MySQL",
                "Docker",
                "CI/CD",
                "TDD",
                "Observability",
                "REST APIs",
                "Microservices",
                "Arquitetura de Software",
                "Design Patterns",
                "Git",
            ),
        ),
    ),
)
