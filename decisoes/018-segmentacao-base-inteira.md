# ADR 018 — Segmentação sobre a base inteira de clientes (proposta)

> **Escopo após 12/11/2026:** Proposta histórica preservada com autoria original. A [ADR 020](020-consolidacao-temporal-semana5.md) consolida e corrige população, temporalidade e interpretação para a entrega vigente.

- **Status:** Proposta, aguardando discussão com o time
- **Autora:** Lorena
- **Branch:** dev
- **Data:** 11/11/2026

## Contexto

A segmentação publicada (ADR 011) agrupa os 14.753 pagantes ativos em 30/09/2026. Filtrar pelos sobreviventes usa, de forma indireta, a informação de quem saiu, e enviesa o grupo de baixo engajamento para o plano anual (98%).

## Decisão proposta

1. **População:** clusterizar todos os pagantes com assinatura em vigor em jan–set/2026, ativos ou não (23.151; 21.023 no ajuste).
2. **Variáveis:** usar só comportamento e declaração, medidos por mês de assinatura observado. Ficam fora plano, canal, tempo de casa e variáveis de dispositivo.
3. **Modalidades:** unir hiit e funcional, porque a taxonomia depende da fonte.
4. **Modelo:** k=4, com log1p e z-score como premissa declarada.
5. **Churn:** usar só após a clusterização, para hipóteses e priorização.

## Consequências

- **Personas:** Ativo ao Ar Livre, Treino Indoor Guiado, Hábito Fraco e Treina em Companhia.
- **Documentos a atualizar se aprovada:**
  - `customer_segmentation_report_semana5.md`;
  - `mini_deck_eda_semana5.md`;
  - `segmentacao_etapa4.md`;
  - `docs/plano_entrega_semana5.md`;
  - `decisoes.md`.
- **Evidência:** `saidas/base_inteira/` e `notebooks/10_segmentacao_base_inteira.md`.
