# ADR 014: Arquitetura Medalhão para a Camada de Dados

- **Data:** 04/11/2026
- **Autor(a) / Responsável:** Igor / Codex
- **Branch / Worktree:** `codex/plano-mestre-vitaliza`
- **Status:** Aprovada

---

## 1. Contexto e Motivação

O projeto precisa receber manualmente as fontes originais do data room e, ao longo das análises, gerar tabelas tratadas e produtos analíticos sem modificar os arquivos de origem. A estrutura anterior distinguia apenas dados brutos e processados, sem explicitar o nível de tratamento dos derivados.

## 2. Decisão Adotada

Adotar a arquitetura medalhão preservando os caminhos já usados pelo projeto:

- **Bronze:** `dados/brutos/`, destinada exclusivamente aos arquivos originais inseridos manualmente. Os arquivos dessa camada são imutáveis e não podem ser sobrescritos por scripts.
- **Prata:** `dados/processados/prata/`, destinada a tabelas limpas, tipadas, deduplicadas, normalizadas temporalmente, reconciliadas e historizadas.
- **Ouro:** `dados/processados/ouro/`, destinada a tabelas analíticas, métricas consolidadas, feature stores e datasets de consumo para EDA, segmentação, modelagem e relatórios.

Toda tabela Prata deve ser reproduzível a partir da Bronze, e toda tabela Ouro deve ser reproduzível a partir da Prata. A árvore `dados/` permanece excluída do Git pelo `.gitignore`; os dados serão adicionados localmente pelo operador e não baixados automaticamente do Drive.

## 3. Consequências e Impacto no Case

A decisão mantém compatibilidade com a regra existente de `dados/brutos/`, reduz o risco de edição acidental da fonte e torna explícita a linhagem dos produtos analíticos. Scripts, notebooks, relatórios e ADRs futuros deverão indicar a camada de entrada e de saída. Como as pastas vazias e seus conteúdos são ignorados pelo Git, cada ambiente deverá criá-las localmente antes da execução ou por um futuro comando de inicialização documentado.
