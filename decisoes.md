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

---

## Como registrar uma nova decisão
1. Crie um novo arquivo na pasta `decisoes/` seguindo a nomenclatura `NNN-titulo-sucinto.md` (utilize o modelo em [`decisoes/TEMPLATE.md`](decisoes/TEMPLATE.md)).
2. Preencha os campos obrigatórios: **Data**, **Autor(a)**, **Branch/Worktree**, **Status**, **Contexto**, **Decisão** e **Consequências**.
3. Adicione uma linha na tabela acima com o link para o novo arquivo.
