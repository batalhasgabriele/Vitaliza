# ADR 008: Diagnóstico de Multiplicação de Dados e Prevenção de Fan-Out em JOINs

- **Data:** 29/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Agente 2 (Worktree Cluster)
- **Branch / Worktree:** `cluster-v1`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
Na engenharia de dados e modelagem analítica, a "multiplicação de dados" pode se manifestar tanto por anomalias transacionais (cobranças duplicadas) quanto por erros de modelagem relacional (explosão cartesiana / *fan-out* ao cruzar tabelas de granularidades distintas). Foi realizada uma auditoria estrutural para mapear a ocorrência de multiplicações de dados no *data room* e definir diretrizes técnicas estritas para os pipelines de feature store e clustering.

---

## 2. Decisão Adotada

### 2.1 Diagnóstico de Multiplicação nas Tabelas Brutas
1. **Duplicação Física Integral (Full-Row Duplicates):**
   - **Inexistente (0%).** Nenhuma das 12 tabelas brutas possui linhas idênticas duplicadas.
   - Chaves primárias e naturais (`user_id`, `assinatura_id`, `pagamento_id`, `atividade_id`, etc.) possuem **0 colisões**.

2. **Multiplicação Transacional (Cobranças Duplicadas em `pagamentos.csv`):**
   - **Existente.** Identificou-se que falhas transitórias de processamento seguidas de retentativas automáticas nos gateways geraram cobranças aprovadas em duplicidade no mesmo dia e ciclo para o mesmo usuário.
   - Foram detectados **3.882 registros de cobranças aprovadas duplicadas no mesmo dia/usuário/valor** em todo o histórico de `pagamentos.csv`.
   - Especificamente no mês de corte (setembro/2026), foram comprovados **93 casos de cobranças duplicadas** somando **R$ 6.830,40 indevidos**, que devem ser expurgados da receita líquida (reiterando a Decisão 003).

3. **Múltiplas Respostas em `pesquisa_saida.csv`:**
   - Apenas 2 usuários responderam à pesquisa de saída duas vezes ao longo do tempo (4 registros no total).

### 2.2 Mapeamento de Granularidade e Risco de *Fan-Out* em JOINs
Fica formalizada a separação de granularidades entre as tabelas do projeto:
- **Tabelas 1:1 (Exatamente 1 linha por usuário na história):**
  - `usuarios.csv` (64.948 linhas, 64.948 usuários únicos).
  - `assinaturas.csv` (32.643 linhas, 32.643 usuários únicos — **cada assinante possui estritamente 1 registro histórico de assinatura**).
  - `onboarding.csv` (63.929 linhas, 63.929 usuários únicos).
  - `campanha_ago26.csv` (14.120 linhas, 14.120 usuários únicos).
- **Tabelas 1:N (Séries Temporais e Logs Transacionais):**
  - `atividades.parquet`: até 476 treinos/usuário (média de 34,3).
  - `uso_mensal.csv`: até 21 meses/usuário (média de 9,3).
  - `eventos_assinatura.csv`: até 31 eventos/usuário (média de 5,3).
  - `pagamentos.csv`: até 32 pagamentos/usuário (média de 5,2).
  - `feed_posts.csv`: até 28 posts/usuário (média de 4,4).
  - `tickets_suporte.csv`: até 4 tickets/usuário (média de 1,1).
- **Tabela N:N (Grafo Social):**
  - `amizades.csv` (113.480 conexões entre seguidores e seguidos).

### 2.3 Regras Mandatórias de Engenharia para Pipelines
1. **Proibição de JOINs Diretos 1:N sem Agregação:** Fica expressamente vedado realizar `LEFT JOIN` ou `INNER JOIN` direto entre tabelas 1:1 e tabelas 1:N/N:N sem sumarização prévia.
2. **Agregação Prévia a Nível de `user_id`:** Qualquer variável originada de tabelas 1:N deve ser pré-agregada no nível de granularidade do usuário (`GROUP BY user_id`), computando métricas consolidadas (ex: médias mensais, contagens, somas de receita ou medianas).
3. **Deduplicação de Pagamentos:** Toda rotina de cálculo de LTV, faturamento e receita líquida deve aplicar expurgo de duplicidades aprovadas no mesmo ciclo/dia.
4. **Deduplicação da Pesquisa de Saída:** Ao relacionar `pesquisa_saida.csv`, selecionar exclusivamente o último registro por usuário (`keep='last'`).

---

## 3. Consequências e Impacto no Case
- **Blindagem Matemática das Features:** Evita-se a multiplicação acidental de assinantes no dataset de modelagem e segmentação, assegurando que o total de assinantes ativos no corte permaneça estritamente nos **14.753 usuários**.
- **Acurácia Financeira:** Protege as métricas de receita contra a inflação artificial decorrente de cobranças duplicadas de retentativa.
