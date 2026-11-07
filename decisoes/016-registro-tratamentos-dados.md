# ADR 016: Registro Consolidado de Limpeza e Tratamento de Dados

- **Data:** 05/11/2026
- **Autor(a) / Responsável:** Igor / Codex
- **Branch / Worktree:** `codex/plano-mestre-vitaliza`
- **Status:** Implementada

---

## 1. Contexto e Motivação

As regras de limpeza e tratamento do projeto estavam distribuídas entre scripts, notebooks, relatórios e diferentes ADRs. Essa distribuição preservava o racional de cada decisão, mas dificultava responder de forma rápida quais tratamentos foram efetivamente aplicados, qual foi o impacto quantitativo, onde a regra está implementada e quais lacunas ainda permanecem.

## 2. Decisão Adotada

Instituir [`docs/registro_limpeza_tratamento_dados.md`](../docs/registro_limpeza_tratamento_dados.md) como catálogo operacional versionado das regras de dados.

O catálogo deve:

1. manter um identificador estável para cada tratamento;
2. distinguir exclusão, anulação, padronização, sinalização, filtro temporal e preservação deliberada;
3. registrar fonte, campo, regra, impacto observado, camada de saída, status e evidência técnica;
4. diferenciar regras implementadas de decisões pendentes ou aplicadas somente em análises;
5. apontar para o código, testes e ADRs correspondentes;
6. ser atualizado sempre que uma regra ou seu impacto quantitativo mudar.

O Markdown é a fonte de verdade humana por permitir revisão de diferenças, autoria e histórico no Git. Um log estruturado de execução em JSONL poderá ser adicionado futuramente, mas não substituirá o catálogo nem os ADRs.

## 3. Consequências e Impacto no Case

O projeto passa a ter uma visão consolidada e auditável da linhagem Bronze→Prata→Ouro, útil para a entrega acadêmica, revisão do grupo e reprodução futura. O levantamento também torna explícitas dívidas técnicas antes da segmentação, em especial fontes sociais ainda consumidas diretamente da Bronze, tratamento divergente de CEP nulo e ausência de uma regra materializada para cadastros futuros.

O documento não altera dados nem regras existentes; ele consolida o estado efetivamente observado e separa com clareza o que já foi implementado do que ainda requer alinhamento.
