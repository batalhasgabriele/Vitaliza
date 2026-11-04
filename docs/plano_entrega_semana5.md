# Roadmap e Controle de Execução — Entregáveis da Semana 5 (Vitaliza)

> **Prazo Oficial de Submissão (Adalove):** `15/11/2026 até 23:59` (Avaliação Formativa / Feedback)
> **Regra de Governança Operacional:** Este documento é o **painel central de controle da Semana 5**. O agente de IA deve **obrigatoriamente consultar e atualizar este arquivo sempre que concluir uma etapa e/ou antes de iniciar uma nova etapa**, garantindo rastreabilidade ponta a ponta sem perda de contexto.

---

## 1. Visão Geral dos Artefatos Exigidos na Semana 5

| Trilha | Artefato Oficial | Requisitos Obrigatórios (Guia do Aluno + Aulas 1–4) |
| :--- | :--- | :--- |
| **Tecnologia** | **Análise Exploratória de Dados (EDA)**<br>*(Código + Visualizações + Mini Deck)* | 1. Carregar, limpar e auditar as 12 tabelas pelas 5 Dimensões da Qualidade;<br>2. Identificar padrões e correlações com churn (investigando a subida de 2026 e os 3 marcos: `01/03/2026`, `01/06/2026` e `10/08/2026`), aplicando variáveis de controle e prevenindo vazamento temporal;<br>3. Gerar os gráficos executivos que entram no relatório;<br>4. Sustentar empiricamente a segmentação (Clusterização não supervisionada sem usar o target de saída);<br>5. Contar a história analítica em um **Mini Deck** no padrão *"1 Tabela + 1 Gráfico + 3 Frases"*. |
| **Negócios** | **Customer Segmentation Report**<br>*(Relatório Executivo Descritivo)* | 1. Descrever **3 a 4 segmentos** de clientes com **Cartões de Persona** (construídos sobre os `14.753` pagantes ativos sem usar a informação de quem saiu) e validados nos 5 Critérios de Segmentação;<br>2. Formular **hipóteses estruturadas de *drivers* de churn** por segmento (formato *Ação + Público + Resultado Esperado* cobrindo os 5 galhos da Árvore MECE);<br>3. Definir **priorização preliminar** (*Intervenção Imediata vs. Monitoramento vs. Não Perturbe*), respeitando os tetos operacionais (300 CS, 1.500 WhatsApp e R$ 40.000/mês);<br>4. Incorporar as **visualizações de dados** vindas da EDA;<br>5. Redigir **seção robusta de limitações da análise** (ponto cego dos 70% em lojas, viés Web da pesquisa de saída, mudança de regra em `uso_mensal`, confundidores e conformidade com a **LGPD**). |

---

## 2. Quadro Geral de Status das Etapas (Checklist Mestre)

| Etapa | Trilha | Nome da Etapa | Status Atual | Arquivos Principais Gerados / Atualizados | ADR Associado |
| :---: | :---: | :--- | :---: | :--- | :---: |
| **Etapa 1** | 💻 Tech | **Inventário, Auditoria e Pipeline das 5 Dimensões da Qualidade de Dados + Reconciliação Contábil** | ✅ **Concluído** | `src/limpeza_qualidade_dados.py`<br>`notebooks/01_inventario_dados.ipynb`<br>`dados/processados/*_limpo(s).*` | [ADR 001](../decisoes/001-politica-imutabilidade-dados-brutos.md), [003](../decisoes/003-metodologia-faturamento-setembro-2026.md), [004](../decisoes/004-auditoria-dados-brutos-inconsistencias.md), [007](../decisoes/007-auditoria-qualidade-12-tabelas.md), [009](../decisoes/009-pipeline-5-dimensoes-qualidade-aula2.md) |
| **Etapa 2** | 💻 Tech & 📊 Negócios | **EDA Parte 1: Perfilamento Robusto (Mediana/IQR), Curva de Sobrevivência (Vale da Morte M2/M3), Ponto Cego das Lojas e Ranking AUC-ROC + Árvore MECE Inicial** | ✅ **Concluído** | `src/processar_eda.py`<br>`src/gerar_graficos_eda.py`<br>`notebooks/02_eda_e_hipoteses.ipynb`<br>`saidas/eda_e_hipoteses_vitaliza.md`<br>4 gráficos em `saidas/` | [ADR 005](../decisoes/005-diretrizes-modelagem-e-hipoteses.md), [ADR 006](../decisoes/006-eda-e-portfolio-hipoteses-mece.md) |
| **Etapa 3** | 💻 Tech & 📊 Negócios | **EDA Parte 2: Investigação da Subida do Churn em 2026, Análise dos 3 Marcos (`01/03`, `01/06`, `10/08`), Correlações com Variáveis de Controle e Padrão *"1 Tabela + 1 Gráfico + 3 Frases"*** | ⏳ **Próxima Etapa (A Iniciar)** | Atualização de `notebooks/02_eda_e_hipoteses.ipynb`<br>Novos gráficos dos marcos e controle em `saidas/`<br>Atualização de `saidas/eda_e_hipoteses_vitaliza.md` | `ADR 010` *(a criar)* |
| **Etapa 4** | 💻 Tech & 📊 Negócios | **Engenharia de Atributos dos `14.753` Pagantes Ativos e Clusterização Não Supervisionada (3 a 4 Segmentos sem Target)** *(Alinhado com Aula 3 de Negócios e Aula 3 de Tech)* | 🔲 **Pendente** | `src/segmentacao_clientes.py`<br>`notebooks/03_segmentacao_clusters.ipynb`<br>`dados/processados/features_segmentacao_ativos_set2026.parquet`<br>Gráficos de perfil dos clusters em `saidas/` | `ADR 011` *(a criar)* |
| **Etapa 5** | 📊 Negócios | **Redação Executiva do *Customer Segmentation Report* (Semana 5)** *(Cartões de Persona, Hipóteses de Drivers por Segmento, Priorização de Canais/Tetos, Visualizações da EDA e Limitações/LGPD)* | 🔲 **Pendente** | `saidas/customer_segmentation_report_semana5.md` | `ADR 012` *(a criar)* |
| **Etapa 6** | 💻 Tech | **Construção do *Mini Deck de EDA* e Revisão Final de Qualidade (QA) para Entrega da Semana 5** *(Alinhado com Aula 4 de Tech)* | 🔲 **Pendente** | `saidas/mini_deck_eda_semana5.md`<br>Checklist final de reprodutibilidade dos notebooks | `ADR 013` *(a criar)* |

---

## 3. Detalhamento de Cada Etapa e Critérios de Pronto (*Definition of Done*)

### ✅ Etapa 1 — Inventário, Auditoria e Pipeline das 5 Dimensões da Qualidade de Dados
- **Status:** **Concluído em 01/11/2026**
- **O que foi feito:**
  - Validação da população oficial no corte (`30/09/2026`): `64.948` contas cadastradas, exclusão das `60` contas `@vitaliza.com.br`, resultando em **`14.753` assinantes pagantes ativos** (`12.503` com renovação automática ligada e `2.250` com renovação desligada).
  - Validação da regra *"Juntar sem multiplicar"* (`64.948` linhas preservadas após `JOIN` agregado com `atividades.parquet`: `36.551` com treino e `28.397` sem treino).
  - Tratamento completo das **5 Dimensões da Qualidade de Dados**:
    1. *Completude:* Flags de preenchimento em `onboarding_limpo.csv` (`5.467` vazios opcionais em `objetivo_texto` vs. `6.368` em `dias_por_semana` e `4.513` em `nivel`).
    2. *Validade:* Preservação dos `574.835` treinos *indoor* sem GPS; tratamento dos `951` treinos `> 200 km` (recuperando o $r$ de Pearson nas corridas de `0,12` para `0,89`) e expurgo dos `3.649` treinos com duração zero.
    3. *Consistência:* Padronização dos 11 rótulos para 7 modalidades canônicas (`376.930` treinos em inglês da origem `app`, resgatando `162.108` corridas `run`).
    4. *Unicidade:* Conversão de fuso `UTC` $\rightarrow$ `UTC-3` do `garmin` e remoção dos `9.383` pares duplicados (`5.199` `garmin` + `4.184` `apple_health`).
    5. *Temporalidade e Vazamento:* Tratamento da mudança de regra de `uso_mensal.csv` entre 2025 (`0` zeros) e 2026 (`25.697` zeros em jan/26) e comprovação do vazamento temporal de `823` assinantes (`37%`) em `31/07/2026` se usado o retrato de `assinaturas.csv`.
  - Reconciliação do faturamento de setembro/2026 em `pagamentos.csv`: `R$ 509.588` $\rightarrow$ `R$ 499.503` $\rightarrow$ `R$ 499.402` $\rightarrow$ **`R$ 492.572` (Bruto)** $\rightarrow$ **`R$ 436.442` (Líquido)**.

---

### ✅ Etapa 2 — EDA Parte 1: Perfilamento Robusto, Sobrevivência, Ponto Cego e Hipóteses MECE
- **Status:** **Concluído e Sincronizado em 01/11/2026 (Reexecutado sobre as bases limpas da Etapa 1)**
- **Arquivos atualizados e sincronizados:**
  - Notebook executado: [`notebooks/02_eda_e_hipoteses.ipynb`](../notebooks/02_eda_e_hipoteses.ipynb)
  - Relatório executivo: [`saidas/eda_e_hipoteses_vitaliza.md`](../saidas/eda_e_hipoteses_vitaliza.md)
  - ADR sincronizado: [`decisoes/006-eda-e-portfolio-hipoteses-mece.md`](../decisoes/006-eda-e-portfolio-hipoteses-mece.md)
  - 4 Gráficos regerados: [`saidas/boxplot_assimetria_uso.png`](../saidas/boxplot_assimetria_uso.png), [`saidas/curva_sobrevivencia_lifetime.png`](../saidas/curva_sobrevivencia_lifetime.png), [`saidas/ponto_cego_cancelamentos.png`](../saidas/ponto_cego_cancelamentos.png), [`saidas/auc_roc_ranking.png`](../saidas/auc_roc_ranking.png)
- **Principais resultados consolidados pós-limpeza (sem vazamento pós-cancelamento e normalizados por vigência):**
  - Expurgo de variáveis fixas no calendário de fim de período (`atividades_set26`, `atividades_ago26`), do evento de saída (`desligou_renovacao`) e de variáveis acumuladas pelo tempo de duração do contrato (`lifetime_dias`, `total_pago_bruto`, `total_renovacoes`, `total_posts`, `total_curtidas`), substituindo-as por métricas calculadas estritamente por mês de vigência (`inicio` até o cancelamento/corte: mediana de `4,79` vs. `2,54` treinos/mês, `-46,9%`), nas janelas móveis anteriores ao cancelamento (`D-30` e `D-60`: mediana de `8,00` vs. `0,00` treinos, `-100,0%`) e variáveis puras de contrato (`eh_plano_anual`, `receita_bruta_mensal`).
  - Maiores preditores univariados reais: **diversidade de modalidades canônicas** (`n_modalidades_distintas`: `AUC = 0,8653`), **treinos nos últimos 30 dias antes do cancelamento (`D-30`)** (`atividades_ultimos_30d`: `AUC = 0,8488`), **razão de uso recente (`D-30` vs. média da vigência)** (`razao_uso_ultimo_mes`: `AUC = 0,8458`), **treinos entre 31 e 60 dias antes do cancelamento (`D-60`)** (`atividades_31_a_60d`: `AUC = 0,7636`), **média mensal de posts no feed** (`media_posts_mes`: `AUC = 0,6753`), **tipo de plano anual vs. mensal** (`eh_plano_anual`: `AUC = 0,6598`) e **média mensal de curtidas** (`media_curtidas_mes`: `AUC = 0,6592`).
  - Confirmação do "Vale da Morte" do plano mensal (`64,71%` no M1, `76,55%` no M2 e `79,29%` no M3) e do ponto cego de `98,02%` geral (`100%` nas lojas Apple e Google).

---

### ⏳ Etapa 3 — EDA Parte 2: Subida do Churn em 2026, 3 Marcos, Correlações Controladas e Formato *"1 Tabela + 1 Gráfico + 3 Frases"*
- **Status:** **Próxima Etapa (Plano elaborado, aguardando início da execução)**
- **Escopo Obrigatório:**
  1. Reconstruir e plotar a série mensal de perda (jan/2025 a set/2026) com denominador correto ($\text{perdas no mês} / \text{ativos no início do mês}$), validando `5,6%/mês` em 2025, `6,6%/mês` em 2026 e o pico de **`8,1%` (`1.154` saídas) em abril/2026** (`5,9%` em ago, `5,0%` em set).
  2. Investigar empiricamente os **3 Marcos de 2026**:
     - `01/03/2026`: Reajuste do plano mensal (`R$ 34,90` $\rightarrow$ `R$ 39,90`) e fim de primeiro ano de cupom (`R$ 239,90` $\rightarrow$ `R$ 299,90`);
     - `01/06/2026`: Pesquisa de saída (`pesquisa_saida.csv`) nas `3.389` saídas de jun–set/2026 (`2.271` lojas vs. `1.118` web; `641` respondentes 100% Web: `68% Cartão` e `32% Pix`);
     - `10/08/2026`: Experimento A/B (`campanha_ago26.csv`, `14.120` sorteados entre `desafio`, `cupom`, `conteudo` e `controle`), medindo efeito na retenção e identificando *Persuadíveis* vs. *Sleeping Dogs*.
  3. Analisar outliers por modalidade (`corrida` vs. `pedal`, onde `73.120` dos `81.775` treinos acima de $Q_3 + 1,5 \times IQR = 17,08\text{ km}$ são ciclismo) e correlações controladas por terceira variável (`sessoes_app` $\times$ `minutos` controlado pelo número exato de `atividades`: `0,88` $\rightarrow$ `0,02`).
  4. Consolidar todas as seções em `notebooks/02_eda_e_hipoteses.ipynb` e `saidas/eda_e_hipoteses_vitaliza.md` no formato **"1 Tabela + 1 Gráfico + 3 Frases"**.

---

### 🔲 Etapa 4 — Engenharia de Atributos dos `14.753` Pagantes Ativos e Clusterização (Sem Target)
- **Status:** **Pendente (iniciar após Etapa 3 e/ou Aula 3 de Tech)**
- **Escopo Obrigatório:**
  1. Construir a matriz de atributos comportamentais, contratuais e sociais exclusivamente para os **`14.753` assinantes pagantes ativos em `30/09/2026`**, **sem utilizar nenhuma variável de desfecho/saída** (aprendizado não supervisionado puro).
  2. Selecionar e padronizar variáveis com alto sinal e baixo ruído (excluindo demografia pura com AUC ~ 0,50 e variáveis colineares identificadas na Etapa 3).
  3. Executar clusterização para encontrar **3 a 4 segmentos acionáveis**, validando coesão/separação técnica e os **5 Critérios de Segmentação de Negócios** (*Acionabilidade, Diferenciação de Resposta, Estabilidade no Tempo, Viabilidade Econômica e Mensurabilidade*).

---

### 🔲 Etapa 5 — Redação do *Customer Segmentation Report* (Artefato de Negócios da Semana 5)
- **Status:** **Pendente (iniciar após Etapa 4)**
- **Escopo Obrigatório:**
  1. Descrição executiva dos **3 a 4 segmentos** com **Cartões de Persona** completos (quem são, tamanho $n$ e %, receita líquida representada, comportamento de uso, canal e vínculo contratual).
  2. **Hipóteses de *drivers* de churn por segmento** estruturadas em 3 partes (*Ação + Público + Resultado Esperado*) e organizadas pela Árvore MECE.
  3. **Matriz de Priorização Preliminar** (*Intervenção Imediata vs. Monitoramento vs. Não Perturbe*), alocando os canais (300 atendimentos CS, 1.500 msgs WhatsApp, E-mail e Push) dentro do teto de R$ 40.000/mês.
  4. Integração das **visualizações da EDA** geradas nas Etapas 2, 3 e 4.
  5. **Seção de Limitações da Análise e Governança (LGPD):** Ponto cego dos 70% em lojas, viés Web da pesquisa de saída, mudança de regra em `uso_mensal.csv`, risco de confundimento/causalidade reversa e princípios da LGPD.

---

### 🔲 Etapa 6 — Construção do *Mini Deck de EDA* (Artefato de Tecnologia) e QA Final da Semana 5
- **Status:** **Pendente (iniciar após Etapa 5 e/ou Aula 4 de Tech)**
- **Escopo Obrigatório:**
  1. Estruturar o **Mini Deck analítico** contando a história completa dos dados (Qualidade e Limpeza $\rightarrow$ Subida do Churn em 2026 e os 3 Marcos $\rightarrow$ Padrões de Comportamento e Correlações Controladas $\rightarrow$ Sustentação Empírica dos Segmentos).
  2. Aplicar o checklist de QA (reprodutibilidade dos notebooks `01`, `02` e `03`, conferência cruzada de todos os números entre relatório, deck e `decisoes.md`).

