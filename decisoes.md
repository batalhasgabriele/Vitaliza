# Registro de Decisões do Projeto - Vitaliza (Módulo 2)

Este repositório adota o padrão **ADR (Architecture Decision Records)** para registrar as escolhas metodológicas, de negócios, engenharia de dados e modelagem adotadas pela equipe.

Como o projeto é desenvolvido de forma concorrente por **5 integrantes e múltiplos agentes de IA** em diferentes branches e worktrees, cada decisão é mantida em um arquivo isolado na pasta [`decisoes/`](decisoes/), eliminando conflitos de merge no Git e garantindo rastreabilidade completa de autoria.

---

## Índice Executivo de Decisões

| ID | Título da Decisão | Data | Autor(a) / Responsável | Branch / Worktree | Status | Documento Detalhado |
|:---:|:---|:---:|:---|:---:|:---:|:---:|
| **001** | Política de Imutabilidade dos Dados Brutos | 22/10/2026 | Gabriele Batalha / Equipe | `dev` | Aprovada | [ADR 001](decisoes/001-politica-imutabilidade-dados-brutos.md) |
| **002** | Governança e Segurança do Repositório | 22/10/2026 | Gabriele Batalha / Equipe | `dev` | Aprovada | [ADR 002](decisoes/002-governanca-seguranca-repositorio.md) |
| **003** | Metodologia de Faturamento de Setembro de 2026 | 22/10/2026 | Gabriele Batalha / Equipe | `dev` | Aprovada | [ADR 003](decisoes/003-metodologia-faturamento-setembro-2026.md) |
| **004** | Auditoria de Dados Brutos e Tratamento de Inconsistências | 22/10/2026 | Gabriele Batalha / Equipe | `dev` | Aprovada | [ADR 004](decisoes/004-auditoria-dados-brutos-inconsistencias.md) |
| **005** | Diretrizes Metodológicas de Modelagem Preditiva e Hipóteses | 25/10/2026 | Gabriele Batalha / Equipe | `dev` | Aprovada | [ADR 005](decisoes/005-diretrizes-modelagem-e-hipoteses.md) |
| **006** | Metodologia e Resultados da EDA e Portfólio de Hipóteses MECE | 25/10/2026 | Gabriele Batalha / Equipe | `dev` | Aprovada | [ADR 006](decisoes/006-eda-e-portfolio-hipoteses-mece.md) |
| **007** | Diretrizes Técnicas da Auditoria de Qualidade de Dados (12 Tabelas) | 29/10/2026 | Gabriele Batalha / Agente 2 | `cluster-v1` | Aprovada | [ADR 007](decisoes/007-auditoria-qualidade-12-tabelas.md) |
| **008** | Consolidação do Guia de Artefatos (Semanas 5 e 10) e Premissas Oficiais do Case | 01/11/2026 | Gabriele Batalha / Gemininha | `dev` | Aprovada | [ADR 008](decisoes/008-guia-artefatos-e-premissas-oficiais-case.md) |
| **009** | Pipeline de Limpeza pelas 5 Dimensões da Qualidade de Dados e Reconciliação da Aula 2 de Tecnologia | 01/11/2026 | Gabriele Batalha / Antigravity AI | `dev` | Aprovada | [ADR 009](decisoes/009-pipeline-5-dimensoes-qualidade-aula2.md) |
| **010** | EDA Parte 2 — Churn e Marcos de 2026 | 05/11/2026 | Igor / Codex | `codex/plano-mestre-vitaliza` | Implementada | [ADR 010](decisoes/010-eda-parte2-churn-marcos-2026.md) |
| **011** | Segmentação Não Supervisionada dos Pagantes Ativos | 05/11/2026 | Igor / Codex | `codex/plano-mestre-vitaliza` | Implementada | [ADR 011](decisoes/011-segmentacao-pagantes-ativos.md) |
| **014** | Arquitetura Medalhão para a Camada de Dados | 04/11/2026 | Igor / Codex | `codex/plano-mestre-vitaliza` | Aprovada | [ADR 014](decisoes/014-arquitetura-medalhao-dados.md) |
| **015** | Gate de Reprodutibilidade Bronze → Prata | 04/11/2026 | Igor / Codex | `codex/plano-mestre-vitaliza` | Implementada | [ADR 015](decisoes/015-gate-reprodutibilidade-bronze-prata.md) |
| **016** | Registro Consolidado de Limpeza e Tratamento de Dados | 05/11/2026 | Igor / Codex | `codex/plano-mestre-vitaliza` | Implementada | [ADR 016](decisoes/016-registro-tratamentos-dados.md) |

---

## Como registrar uma nova decisão

### Fechamento de 08/11/2026

| ID | Decisão | Autor | Branch | Status |
|---|---|---|---|---|
| 012 | [Personas e priorização](decisoes/012-personas-e-priorizacao-semana5.md) | Igor / Codex | dev | Documentada; piloto não executado |
| 013 | [Validação e mini deck](decisoes/013-validacao-e-mini-deck-semana5.md) | Igor / Codex | dev | Implementada |
| 017 | [Prata e comparação de resultados](decisoes/017-engenharia-prata-e-comparacao-resultados.md) | Igor / Codex | dev | Implementada; ver QA da execução |
| 018 | [Segmentação sobre a base inteira](decisoes/018-segmentacao-base-inteira.md) | Lorena | dev | Proposta histórica; consolidada pela ADR 020 |
| 019 | [Personas k=3 e deck executivo](decisoes/019-personas-k3-deck-executivo.md) | Lorena | dev | Proposta histórica; consolidada pela ADR 020 |
| 020 | [Consolidação temporal Semana 5](decisoes/020-consolidacao-temporal-semana5.md) | Igor / Codex | dev | Implementada e validada localmente |
| 021 | [Fechamento e pacote de entrega](decisoes/021-fechamento-pacote-entrega-semana5.md) | Igor / Codex | dev | Implementada; reprodução independente aprovada |
| 022 | [Resolução mestre consolidada](decisoes/022-resolucao-mestre-consolidada.md) | Igor / Codex | dev | Implementada; alteração documental |
| 023 | [Mestre alinhado ao guia](decisoes/023-alinhamento-mestre-guia-semana5.md) | Igor / Codex | dev | Implementada; alteração documental |

1. Crie um novo arquivo na pasta `decisoes/` seguindo a nomenclatura `NNN-titulo-sucinto.md` (utilize o modelo em [`decisoes/TEMPLATE.md`](decisoes/TEMPLATE.md)).
2. Preencha os campos obrigatórios: **Data**, **Autor(a)**, **Branch/Worktree**, **Status**, **Contexto**, **Decisão** e **Consequências**.
3. Adicione uma linha na tabela acima com o link para o novo arquivo.
