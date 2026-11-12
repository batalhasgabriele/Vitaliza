# ADR 020: Consolidação temporal e editorial da Semana 5

- **Data:** 12/11/2026
- **Autor(a) / Responsável:** Igor (autorização) / Codex (implementação)
- **Branch / Worktree:** dev
- **Status:** Implementada e validada localmente; publicação externa pendente

## 1. Contexto e Motivação
Revisões registradas em notebooks/10_revisao_prontidao_entregas.md identificaram métricas incompatíveis, janela condicionada à saída, relatórios divergentes e projeções sem efeito incremental validado.

## 2. Decisão Adotada
Consolidar uma entrega gerada das tabelas. Segmentação descritiva com cinco atributos e três grupos; avaliação histórica em datas comuns anteriores ao desfecho, sem ajustar por churn. Comparar retrospectiva, taxa por pessoa-tempo, expiração e desligamento sem tratá-los como equivalentes. Não excluir saídas precoces do denominador por conveniência. Usar 84 dias para comportamento no corte, com exposição e classificação provisória explícitas. Retirar afirmações causais e financeiras não sustentadas. Não executar campanhas.

## 3. Consequências e Impacto no Case
ADRs 018/019 fornecem a base conceitual, mas a população/janela consolidada difere. Resultados anteriores estão identificados como históricos, com comparação de impacto. Bronze/Prata permanecem intactas. Artefatos de apresentação contêm agregados e uma orientação única de reprodução. Relatório e deck HTML portáveis acompanham fontes Markdown. Semana 10 e publicação externa permanecem fora da execução atual.

## 4. Validação e limites
Foram exportados também PDF do relatório (seis páginas) e do mini deck (cinco slides), com inspeção visual de todas as páginas. São derivados dos HTML; ao mudar a apresentação, repetir a exportação indicada no README.

24 testes aprovados, três notebooks executados, seis seções de relatório e cinco slides renderizados. Os 14 hashes Bronze foram preservados e a Prata foi reproduzida byte a byte. Os mesmos 14.753 ativos foram mantidos; a composição dos grupos mudou para 6.797/5.109/2.847 por alteração explícita de janela/atributos, não por perda de linhas na limpeza. A campanha primária reproduziu a apuração anterior.

Ver [QA e impacto](../saidas/qa_entrega_semana5.md), [método](../notebooks/12_consolidacao_semana5.md) e [plano atualizado](../docs/plano_entrega_semana5.md). Permanecem ressalvas de abril, cinco estados de renovação, deduplicação aproximada por ciclo e texto sem validação humana. Não há comprovação de retorno causal nem previsão atual de churn.
