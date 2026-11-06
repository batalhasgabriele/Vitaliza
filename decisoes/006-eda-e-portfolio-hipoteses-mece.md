# ADR 006: Metodologia e Resultados da EDA e Portfólio de Hipóteses MECE

- **Data:** 25/10/2026 *(Revisada e sincronizada pós-limpeza Etapa 1 em 01/11/2026)*
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
Executar uma Análise Exploratória de Dados (EDA) quantitativa e estruturada sobre os usuários elegíveis da Vitaliza no corte de 30/09/2026 para responder às causas da subida do churn mensal e criar o portfólio de hipóteses testáveis. Em `01/11/2026`, todos os cálculos, gráficos e tabelas foram reexecutados sobre as bases higienizadas pelas 5 Dimensões da Qualidade ([ADR 009](009-pipeline-5-dimensoes-qualidade-aula2.md)).

## 2. Decisão Adotada
1. **Adoção de Mediana e IQR na Vigência e nas Janelas Relativas (`D-30` e `D-60` Antes do Cancelamento) Sem Vazamento Pós-Cancelamento:**
   - Todas as métricas de uso mensal são calculadas estritamente dentro da janela de vigência de cada assinatura (`inicio` até a data de cancelamento — ou até `30/09/2026` para os ativos), expurgando meses inativos posteriores ao cancelamento.
   - Durante a vigência, a frequência mensal mediana é de `4,79` treinos/mês nos ativos (`média 6,41`, IQR `7,38`) contra `2,54` treinos/mês nos cancelados (`média 4,66`, IQR `6,67`, queda de `-46,9%`).
   - Nas janelas móveis anteriores ao cancelamento (`D-60` e `D-30`), os ativos mantêm mediana de `8,00` treinos, enquanto os cancelados despencam para mediana de `0,00` treino (`média 2,99` em `D-60` e `1,78` em `D-30`, queda de `-100,0%` na mediana).
   - A duração individual do treino na base limpa (`atividades_limpas.parquet`) permanece estável (`40,70 min` nos ativos vs. `41,15 min` nos cancelados).
2. **Identificação do Vale da Morte Contratual (M2/M3):**
   - Assinantes do plano mensal sofrem evasão massiva: `64,71%` no 1º mês, `76,55%` de churn no 2º mês e `79,29%` no 3º mês de vida, atingindo `67,91%` de churn geral acumulado.
   - Assinantes do plano anual registram apenas `34,92%` de churn no mesmo horizonte.
3. **Mapeamento do Ponto Cego dos Cancelamentos:**
   - `98,02%` de todos os cancelamentos históricos (`17.477` de `17.830`) ocorrem sem qualquer interação com a pesquisa de saída do aplicativo (`353` respostas = `1,98%`).
   - `100%` dos cancelamentos originários das lojas Apple (`5.775`) e Google (`5.984`) não passam pela pesquisa do app.
   - `9,05%` dos cancelamentos são involuntários (`1.321` falhas definitivas de pagamento = `7,41%` e `292` chargebacks = `1,64%`).
4. **Ranking Univariado de Sinais Preditivos Sem Vazamento Pós-Cancelamento e Normalizado por Vigência (AUC-ROC):**
   - Foram expurgadas variáveis fixas no calendário de fim de período (`atividades_set26`, `atividades_ago26`) — que mediam inatividade *após* o cancelamento para quem havia saído antes —, o próprio evento de saída (`desligou_renovacao`) e variáveis acumuladas pelo tempo de duração do contrato (`lifetime_dias`, `total_pago_bruto`, `total_renovacoes`, `total_posts`, `total_curtidas`), substituídas por variáveis puras de contrato (`eh_plano_anual`, `receita_bruta_mensal`, `eh_canal_loja`) e médias mensais na vigência (`media_posts_mes`, `media_curtidas_mes`).
   - Maiores sinais preditivos reais: Diversidade de modalidades canônicas (`n_modalidades_distintas`, `AUC 0,8653`), treinos nos últimos 30 dias antes do cancelamento (`atividades_ultimos_30d`, `AUC 0,8488`), razão de uso recente `D-30` vs. média da vigência (`razao_uso_ultimo_mes`, `AUC 0,8458`), treinos entre 31 e 60 dias antes do cancelamento (`atividades_31_a_60d`, `AUC 0,7636`), média mensal de posts no feed (`media_posts_mes`, `AUC 0,6753`), tipo de plano anual vs. mensal (`eh_plano_anual`, `AUC 0,6598`) e média mensal de curtidas recebidas (`media_curtidas_mes`, `AUC 0,6592`).
   - Menores sinais / descartadas como preditoras: Demográficas e de entrada (`idade` higienizada com `AUC 0,5088`, `dias_semana_pretendidos` com `AUC 0,5050` e `tem_relogio` com `AUC 0,5009`).
5. **Artefatos Entregues:**
   - Notebook reprodutível em `notebooks/02_eda_e_hipoteses.ipynb`.
- Feature store analítica em `dados/processados/ouro/features_eda_corte_set2026.parquet`.
   - Relatório executivo completo em `saidas/eda_e_hipoteses_vitaliza.md` com 4 gráficos comprobatórios.

## 3. Consequências e Impacto no Case
- Define as features prioritárias para as fases de segmentação e modelagem preditiva, embasando a recomendação estratégica para o Conselho de Administração.
