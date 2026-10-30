# ADR 006: Metodologia e Resultados da EDA e Portfólio de Hipóteses MECE

- **Data:** 25/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
Executar uma Análise Exploratória de Dados (EDA) quantitativa e estruturada sobre os usuários elegíveis da Vitaliza no corte de 30/09/2026 para responder às causas da subida do churn mensal e criar o portfólio de hipóteses testáveis.

## 2. Decisão Adotada
1. **Adoção de Mediana e IQR para Tendência Central:** Em virtude da assimetria extrema das métricas de uso digital e presença de caudas longas, rejeitou-se a média aritmética. A frequência mensal de treino típica cai de 5,39 (ativos) para 1,50 treino/mês (cancelados), uma queda de -72,2%, enquanto a duração por treino permanece estável (~41 min).
2. **Identificação do Vale da Morte Contratual (M2/M3):**
   - Assinantes do plano mensal sofrem evasão massiva: 76,55% de churn no 2º mês e 79,29% no 3º mês de vida, atingindo 67,91% de churn geral acumulado.
   - Assinantes do plano anual registram apenas 34,92% de churn no mesmo horizonte.
3. **Mapeamento do Ponto Cego dos Cancelamentos:**
   - 98,02% de todos os cancelamentos ocorrem sem qualquer interação com a pesquisa de saída do aplicativo.
   - 100% dos cancelamentos originários das lojas Apple e Google não passam pelo app.
   - 9,05% dos cancelamentos são involuntários (falhas definitivas de cartão, expiração de Pix e chargeback).
4. **Ranking Univariado de Sinais Preditivos (AUC-ROC):**
   - Maior sinal preditivo: Desaceleração de treinos em set/2026 (AUC 0,9158) e ago/2026 (AUC 0,8760), seguido de desligamento de auto-renovação (AUC 0,8485).
   - Menor sinal / descartadas: Demográficas (idade, sexo, smartwatch) com AUC próximo a 0,50.
5. **Artefatos Entregues:**
   - Notebook reprodutível em `notebooks/02_eda_e_hipoteses.ipynb`.
   - Feature store tratada em `dados/processados/features_eda_corte_set2026.parquet`.
   - Relatório executivo completo em `saidas/eda_e_hipoteses_vitaliza.md` com 4 gráficos comprobatórios.

## 3. Consequências e Impacto no Case
- Define as features prioritárias para as fases de segmentação e modelagem preditiva, embasando a recomendação estratégica para o Conselho de Administração.
