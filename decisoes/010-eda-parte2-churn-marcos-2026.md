# ADR 010: EDA Parte 2 — Churn e Marcos de 2026

- **Data:** 05/11/2026
- **Autor(a) / Responsável:** Igor / Codex
- **Branch / Worktree:** `codex/plano-mestre-vitaliza`
- **Status:** Implementada

---

## 1. Contexto e Motivação

A Semana 5 exige investigar a subida do churn em 2026 e os marcos de reajuste em 01/03, pesquisa de saída em 01/06 e campanha randomizada em 10/08. O snapshot de assinaturas não pode ser tratado como histórico, eventos em lojas usam UTC e respostas/engajamento da campanha possuem riscos de viés e pós-tratamento.

## 2. Decisão Adotada

1. Definir perda mensal pelo evento `assinatura_expirada`, harmonizado para `America/Sao_Paulo` e deduplicado por usuário.
2. Calcular churn como perdas do mês divididas pelos pagantes ativos no início do mês, usando `assinaturas.csv` apenas para identidade, início e atributos contratuais.
3. Preservar a divergência entre a reconstrução (5,68% em 2025; 6,68% em 2026; 1.158 perdas em abril) e a referência executiva (5,6%; 6,6%; 1.154), sem ajuste artificial.
4. Tratar o reajuste como análise observacional antes/depois, sem alegação causal.
5. Tratar a pesquisa como fonte Web com viés de canal e seleção; respostas de usuários ativos não equivalem a perdas.
6. Avaliar a campanha por intenção de tratar em 30 dias a partir da data comum de sorteio, incluindo o controle sem `enviado_em`; abertura e clique não entram como filtros.
7. Avaliar outliers por modalidade e controlar a correlação entre sessões e minutos pelo número de atividades.

## 3. Consequências e Impacto no Case

- O pico reconstruído foi 8,13% em abril, seguido de 5,99% em agosto e 5,01% em setembro.
- No plano mensal, a média passou de 10,22% em jan–fev para 12,97% em mar–abr, sem identificação causal.
- Entre jun–set houve 3.389 expirações: 2.271 em lojas e 1.118 Web; os 641 respondentes únicos são 100% Web.
- No ITT de 30 dias: controle 5,48%, desafio 5,18%, cupom 4,64% e conteúdo 6,13%. Nenhum braço diferiu do controle a 5%; cupom apresentou direção favorável de −0,84 p.p. com p=0,108.
- A regra global de Tukey marcou 81.775 treinos, dos quais 73.120 são pedal, confirmando que outliers devem ser avaliados por modalidade.
- A correlação sessões × minutos caiu de 0,88 para 0,02 após controlar atividades, impedindo interpretação causal ingênua.

Os resultados são reproduzidos por `src/analisar_eda_marcos.py` e documentados em `saidas/eda_etapa3_marcos_2026.md`.
