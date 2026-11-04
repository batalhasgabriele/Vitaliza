# ADR 001: Política de Imutabilidade dos Dados Brutos

- **Data:** 22/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
Para assegurar a reprodutibilidade científica do projeto e manter a integridade inquestionável do *data room* da Vitaliza, a base original entregue pela equipe de engenharia precisa permanecer intocada ao longo de todo o ciclo de vida do projeto.

## 2. Decisão Adotada
1. Os arquivos da pasta `dados/brutos/` (12 tabelas/logs e pasta `heatmaps/`) são **estritamente somente leitura** (*read-only*).
2. É expressamente proibido editar, sobrescrever, reformatar ou deletar qualquer arquivo dentro de `dados/brutos/`.
3. Qualquer procedimento de limpeza, tipagem, imputação, enriquecimento ou engenharia de atributos deve obrigatoriamente persistir novos artefatos tratados na pasta `dados/processados/`.

## 3. Consequências e Impacto no Case
- Todas as análises podem ser reexecutadas do zero garantindo paridade total de resultados.
- Pipelines de feature store consumirão apenas arquivos validados e versionados em `dados/processados/`.
