# ADR 002: Governança e Segurança do Repositório

- **Data:** 22/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
O repositório Git do projeto será compartilhado entre 5 integrantes da equipe, agentes de IA e repositório remoto. Faz-se necessário evitar vazamento de credenciais de ambientes e prevenir o commit de arquivos de dados pesados que excederiam o limite do GitHub e degradariam a performance do Git.

## 2. Decisão Adotada
1. A pasta de dados originais `dados/brutos/` foi mantida no `.gitignore` (permanecendo apenas localmente em cada máquina e em modo somente leitura), enquanto `dados/processados/` foi liberada para versionamento no Git (atualizado em `07/11/2026`) a fim de facilitar o compartilhamento direto das bases limpas e feature stores entre os integrantes do grupo.
2. Arquivos de ambiente e segredos (`.env`, chaves de API) foram adicionados ao `.gitignore`.
3. O repositório versiona: códigos-fonte (`src/`), dados processados (`dados/processados/`), notebooks metodológicos (`notebooks/`), documentação (`docs/`), relatórios (`saidas/`) e logs de decisão (`decisoes/`).

## 3. Consequências e Impacto no Case
- Compartilhamento imediato das tabelas tratadas (`dados/processados/`) entre a Dupla de Tech e o Trio de Negócios sem exigir que os dados brutos pesados (`dados/brutos/`) sejam enviados ao GitHub.
- Cada membro da equipe mantém os arquivos de dados brutos localmente sem sobrecarregar o histórico Git com `dados/brutos/`.
