# ADR 019: Personas k=3 da base inteira e deck executivo

- **Data:** 11/11/2026
- **Autor(a) / Responsável:** Lorena
- **Branch / Worktree:** dev
- **Status:** Proposta, aguardando discussão com o time

---

## 1. Contexto e Motivação

A proposta da ADR 018 segmenta a base inteira de jan–set/2026 com k=4. Depois de retirar `min_por_treino` (regra ANA-002), as tabelas salvas em `saidas/base_inteira/` deixaram de bater com o relatório e o mini deck da proposta: os grupos "Ar Livre" e "Indoor" quase não diferem em % de treinos ao ar livre (η² 0,006), embora essa variável seja bimodal na base. O deck executivo pedia 3 personas.

## 2. Decisão Adotada

1. **População e tratamentos:** os mesmos da ADR 018 (23.152 pagantes de jan–set/2026; 21.024 no ajuste), montados por `segmentacao_base_inteira.construir()`.
2. **Variáveis:** só comportamento e declaração: `dias_semana_pretendidos`, `treinos_mes`, `regularidade`, `n_modalidades` e `pct_ar_livre`. Posts e conexões saem do modelo e ficam como descritivas.
3. **Modelo:** K-Means com k=3, P99 + log1p + z-score. Silhueta 0,33 (0,23 embaralhado), ARI bootstrap 0,99.
4. **Personas:** Atleta ao Ar Livre, Treino em Casa Guiado e Hábito Fraco. "Treina em Companhia" vira subsegmento.
5. **Priorização:** 4 níveis por segmento × renovação desligada, incluindo "não perturbe".
6. **Hipóteses:** formato da Aula 2, com critério de refutação.

## 3. Consequências e Impacto no Case

- **Novos arquivos:** `src/personas_k3_deck.py`, `saidas/deck_executivo/tabelas/` e `notebooks/11_personas_k3_deck_executivo.md`.
- **Deck executivo:** 7 slides; os números saem das tabelas acima.
- **Concordância com o time:** 100% dos "guiados por vídeo" e 92% dos "ao ar livre" (ADR 011) caem nos grupos equivalentes; a diferença está no Hábito Fraco, que passa a incluir mensalistas que saem cedo.
- **Trade-off:** os grupos mudam com RobustScaler ou sem log1p (ARI 0,20 e 0,26); a normalização é premissa declarada.
- **Pendências se aprovada:** substituir a proposta k=4 no relatório da base inteira e atualizar `customer_segmentation_report_semana5.md`, `mini_deck_eda_semana5.md` e o registro de tratamentos.
