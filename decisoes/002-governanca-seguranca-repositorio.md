# ADR 002: Governança e Segurança do Repositório

- **Data:** 22/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
O repositório Git do projeto será compartilhado entre 5 integrantes da equipe, agentes de IA e repositório remoto. Faz-se necessário evitar vazamento de credenciais de ambientes e prevenir o commit de arquivos de dados pesados que excederiam o limite do GitHub e degradariam a performance do Git.

## 2. Decisão Adotada
1. A pasta completa `dados/` (incluindo `dados/brutos/` e `dados/processados/`) foi adicionada ao `.gitignore`.
2. Arquivos de ambiente e segredos (`.env`, chaves de API) foram adicionados ao `.gitignore`.
3. O repositório versiona estritamente: códigos-fonte (`src/`), notebooks metodológicos (`notebooks/`), documentação (`docs/`), relatórios (`saidas/`) e logs de decisão (`decisoes/`).

## 3. Consequências e Impacto no Case
- Repositório leve, ágil e seguro para clonagem e sincronização rápida em worktrees.
- Cada membro da equipe mantém os arquivos de dados brutos localmente sem sobrecarregar o histórico Git.
