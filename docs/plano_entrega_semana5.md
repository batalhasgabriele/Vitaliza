# Roadmap e Controle de Execução — Entregáveis da Semana 5 (Vitaliza)

> **Prazo Oficial de Submissão (Adalove):** `15/11/2026 até 23:59` (Avaliação Formativa / Feedback)
> **Regra de Governança Operacional:** Este documento é o **painel central de controle da Semana 5**. O agente de IA deve **obrigatoriamente consultar e atualizar este arquivo sempre que concluir uma etapa e/ou antes de iniciar uma nova etapa**, garantindo rastreabilidade ponta a ponta sem perda de contexto.

---

## 1. Visão Geral dos Artefatos Exigidos na Semana 5

> **Diretriz Oficial do Professor sobre o Escopo das Entregas de Tecnologia (`13/11` vs. `18/12`):**
> - **Semana 5 (`13/11` — Entrega Parcial: *"Até a segmentação"*):** A análise exploratória e os segmentos, com perfil, tamanho e saída histórica de cada um. **O foco da Semana 5 é criar ótimos clusters comportamentais** (bem separados, estáveis, interpretáveis pelas medianas e acionáveis, **independentemente de explicarem ou não o churn neste momento**; a taxa de saída histórica em 60 dias entra apenas como leitura descritiva pós-agrupamento).
> - **Semana 10 (`18/12` — Entrega Final: *"O modelo preditivo de saída"*):** O modelo de churn treinado, avaliado e disponibilizado (onde o foco central será prever o churn e selecionar as variáveis que mais impactam/explicam a saída).
> - **Os 3 Pilares Obrigatórios nas Duas Entregas de Tech:**
>   1. **Repositório:** O código do grupo, versionado;
>   2. **Documentação (`decisoes.md`):** As decisões e o motivo de cada uma;
>   3. **Apresentação executiva:** O processo analítico e os insights.

| Trilha | Artefato Oficial | Requisitos Obrigatórios (Guia do Aluno + Aulas 1–4) |
| :--- | :--- | :--- |
| **Tecnologia** | **Análise Exploratória de Dados (EDA)**<br>*(Repositório + Documentação `decisoes.md` + Apresentação Executiva / Mini Deck)* | 1. Carregar, limpar e auditar as 12 tabelas pelas 5 Dimensões da Qualidade;<br>2. Identificar padrões e correlações na base (investigando a subida de 2026 e os 3 marcos: `01/03/2026`, `01/06/2026` e `10/08/2026`), aplicando variáveis de controle e prevenindo vazamento temporal;<br>3. Gerar os gráficos executivos que entram no relatório;<br>4. Sustentar empiricamente a segmentação (**foco em criar ótimos clusters comportamentais não supervisionados**, apresentando perfil em medianas, tamanho e saída histórica de cada grupo);<br>5. Contar a história analítica em uma **Apresentação Executiva (Mini Deck)** no padrão *"1 Tabela + 1 Gráfico + 3 Frases"*, com repositório versionado e `decisoes.md` atualizado. |
| **Negócios** | **Customer Segmentation Report**<br>*(Relatório Executivo Descritivo)* | 1. Descrever **3 a 4 segmentos** de clientes com **Cartões de Persona** (construídos sobre os `14.753` pagantes ativos sem usar a informação de quem saiu) e validados nos 5 Critérios de Segmentação;<br>2. Formular **hipóteses estruturadas de *drivers* de churn** por segmento (formato *Ação + Público + Resultado Esperado* cobrindo os 5 galhos da Árvore MECE);<br>3. Definir **priorização preliminar** (*Intervenção Imediata vs. Monitoramento vs. Não Perturbe*), respeitando os tetos operacionais (300 CS, 1.500 WhatsApp e R$ 40.000/mês);<br>4. Incorporar as **visualizações de dados** vindas da EDA;<br>5. Redigir **seção robusta de limitações da análise** (ponto cego dos 70% em lojas, viés Web da pesquisa de saída, mudança de regra em `uso_mensal`, confundidores e conformidade com a **LGPD**). |

---

## 2. Quadro Geral de Status das Etapas (Checklist Mestre)

| Etapa | Trilha / Responsável | Nome da Etapa | Status Atual | Arquivos Principais (Isolados por Frente) | ADR Associado |
| :---: | :---: | :--- | :---: | :--- | :---: |
| **Etapa 1** | 💻 Tech *(Base Comum)* | **Inventário, Auditoria e Pipeline das 5 Dimensões da Qualidade de Dados + Reconciliação Contábil** | ✅ **Concluído** | `src/limpeza_qualidade_dados.py`<br>`notebooks/01_inventario_dados.ipynb`<br>`dados/processados/*_limpo(s).*` | [ADR 001](../decisoes/001-politica-imutabilidade-dados-brutos.md), [003](../decisoes/003-metodologia-faturamento-setembro-2026.md), [004](../decisoes/004-auditoria-dados-brutos-inconsistencias.md), [007](../decisoes/007-auditoria-qualidade-12-tabelas.md), [009](../decisoes/009-pipeline-5-dimensoes-qualidade-aula2.md) |
| **Etapa 2** | 💻 Tech & 📊 Negócios *(Base Comum)* | **EDA Parte 1: Perfilamento Robusto (Mediana/IQR), Curva de Sobrevivência (Vale da Morte M2/M3), Ponto Cego das Lojas e Ranking AUC-ROC + Árvore MECE Inicial** | ✅ **Concluído** | `src/processar_eda.py`<br>`src/gerar_graficos_eda.py`<br>`notebooks/02_eda_e_hipoteses.ipynb`<br>`saidas/eda_e_hipoteses_vitaliza.md`<br>4 gráficos em `saidas/` | [ADR 005](../decisoes/005-diretrizes-modelagem-e-hipoteses.md), [ADR 006](../decisoes/006-eda-e-portfolio-hipoteses-mece.md) |
| **Etapa 3** | 💻 **Dupla Tech** (Código/Gráficos)<br>+ 📊 **Trio Negócios** (Análise Marcos/LGPD) | **EDA Parte 2: Investigação da Subida do Churn em 2026, Análise dos 3 Marcos (`01/03`, `01/06`, `10/08`), Correlações com Variáveis de Controle e Padrão *"1 Tabela + 1 Gráfico + 3 Frases"*** | ⏳ **Próxima Etapa (A Iniciar)** | **Tech:** `notebooks/02_eda_e_hipoteses.ipynb`, `src/`, gráficos `.png` em `saidas/` e `saidas/eda_e_hipoteses_vitaliza.md`<br>**Negócios:** Rascunho de marcos e limitações em `saidas/customer_segmentation_report_semana5.md` | `ADR 010` *(a criar)* |
| **Etapa 4** | 🤝 **Ponte Tech + Negócios**<br>*(Sincronização Obrigatória)* | **Engenharia de Atributos dos `14.753` Pagantes Ativos e Clusterização Não Supervisionada (3 a 4 Segmentos sem Target)** *(Alinhado com Aula 3 de Negócios e Aula 3 de Tech)* | 🔲 **Pendente** | **Tech:** `src/segmentacao_clientes.py`, `notebooks/03_segmentacao_clusters.ipynb`, `dados/processados/features_segmentacao_ativos_set2026.parquet`, gráficos em `saidas/`<br>**Negócios:** Validação nos 5 Critérios e nomes das Personas | `ADR 011` *(a criar)* |
| **Etapa 5** | 📊 **Trio Negócios** *(Líder)*<br>+ 💻 Tech *(Apoio Gráficos)* | **Redação Executiva do *Customer Segmentation Report* (Semana 5)** *(Cartões de Persona, Hipóteses de Drivers por Segmento, Priorização de Canais/Tetos, Visualizações da EDA e Limitações/LGPD)* | 🔲 **Pendente** | **Exclusivo Negócios:**<br>`saidas/customer_segmentation_report_semana5.md` | `ADR 012` *(a criar)* |
| **Etapa 6** | 💻 **Dupla Tech** *(Líder)*<br>+ 📊 Negócios *(Revisão QA)* | **Construção do *Mini Deck de EDA* e Revisão Final de Qualidade (QA) para Entrega da Semana 5** *(Alinhado com Aula 4 de Tech)* | 🔲 **Pendente** | **Exclusivo Tech:**<br>`saidas/mini_deck_eda_semana5.md`<br>Checklist final dos notebooks `01`, `02` e `03` | `ADR 013` *(a criar)* |

---

## 3. Organização do Grupo (Dupla Tech vs. Trio Negócios) e Pontos de Atenção contra Conflitos

O grupo está dividido em duas frentes complementares:
- **💻 Dupla de Tecnologia (2 integrantes):** Responsável pelo pipeline de dados, notebooks (`01`, `02` e `03`), geração de gráficos em `saidas/` e construção do **Mini Deck de EDA** (`saidas/mini_deck_eda_semana5.md`).
- **📊 Trio de Negócios (3 integrantes):** Responsável pela interpretação estratégica dos dados, validação dos segmentos nos 5 critérios de negócio, construção dos Cartões de Persona, hipóteses de *drivers* de churn, matriz de alocação de canais/orçamento (`R$ 40.000/mês`), seção de limitações/LGPD e redação do **Customer Segmentation Report** (`saidas/customer_segmentation_report_semana5.md`).

### ⚠️ Os 3 Pontos Críticos de Atenção para Evitar Conflitos

1. **Conflito 1 — Desalinhamento de Segmentos e Personas (Etapa 4 é o Ponto de Encontro):**
   - **Risco:** O Trio de Negócios criar personas hipotéticas "no papel" antes ou separadamente dos clusters gerados pelo código da Dupla de Tech, gerando contradição entre o *Customer Segmentation Report* e a *EDA*.
   - **Regra de Blindagem:** As Personas de Negócios **devem nascer exatamente dos 3 a 4 clusters gerados na Etapa 4** sobre os `14.753` pagantes ativos. A Dupla de Tech roda o algoritmo e entrega a tabela com o perfil estatístico de cada cluster (tamanho $n$ e %, mediana de treinos, modalidade, plano, canal, engajamento social); o Trio de Negócios batiza cada grupo, monta os Cartões de Persona e desenha a estratégia de retenção.
2. **Conflito 2 — Divergência de Números entre o Relatório de Negócios e o Mini Deck de Tech:**
   - **Risco:** Integrantes fazerem contas paralelas (ex.: em planilhas separadas sobre dados brutos sem aplicar o expurgo das 60 contas de cortesia, deduplicação de cobranças/treinos ou fuso horário) e reportarem percentuais diferentes nos dois entregáveis.
   - **Regra de Blindagem (Fonte Única da Verdade):** Nenhum número deve ser calculado fora das bases limpas em `dados/processados/`. Todos os números citados no relatório de Negócios e no Mini Deck de Tech devem vir das tabelas oficiais geradas nos notebooks e documentadas em `saidas/` e nos ADRs em `decisoes/`.
3. **Conflito 3 — Conflitos de Merge no Git (Edição Simultânea do Mesmo Arquivo):**
   - **Risco:** Duas pessoas editarem o mesmo arquivo `.md` ou `.ipynb` simultaneamente na branch `dev`.
   - **Regra de Blindagem (Isolamento de Arquivos):**
     - **Arquivos exclusivos da Dupla Tech:** `src/*.py`, `notebooks/*.ipynb`, `saidas/*.png`, `saidas/eda_e_hipoteses_vitaliza.md` e `saidas/mini_deck_eda_semana5.md`.
     - **Arquivos exclusivos do Trio Negócios:** `saidas/customer_segmentation_report_semana5.md`.
     - **ADRs (`decisoes/NNN-titulo.md`):** Cada subgrupo cria seu próprio arquivo numerado individual quando registrar uma decisão nova.

---

## 4. Detalhamento de Cada Etapa e Critérios de Pronto (*Definition of Done*)

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
- **Divisão de Trabalho sem Conflito:**
  - **💻 Dupla Tech (2 pessoas):**
    1. Reconstruir e plotar a série mensal de perda (jan/2025 a set/2026) com denominador correto ($\text{perdas no mês} / \text{ativos no início do mês}$), validando `5,6%/mês` em 2025, `6,6%/mês` em 2026 e o pico de **`8,1%` (`1.154` saídas) em abril/2026** (`5,9%` em ago, `5,0%` em set).
    2. Calcular e plotar os números dos **3 Marcos de 2026**: `01/03/2026` (reajuste mensal `R$ 34,90` $\rightarrow$ `R$ 39,90` e fim do 1º ano de cupom `R$ 239,90` $\rightarrow$ `R$ 299,90`), `01/06/2026` (`pesquisa_saida.csv`: `3.389` saídas jun–set/2026, sendo `2.271` lojas vs. `1.118` web; `641` respondentes 100% Web: `68% Cartão` e `32% Pix`) e `10/08/2026` (`campanha_ago26.csv`: `14.120` sorteados entre `desafio`, `cupom`, `conteudo` e `controle`).
    3. Executar a análise de outliers por modalidade (`corrida` vs. `pedal`, onde `73.120` dos `81.775` treinos acima de $Q_3 + 1,5 \times IQR = 17,08\text{ km}$ são ciclismo) e correlações controladas por terceira variável (`sessoes_app` $\times$ `minutos` controlado pelo número exato de `atividades`: `0,88` $\rightarrow$ `0,02`).
    4. Atualizar `notebooks/02_eda_e_hipoteses.ipynb` e `saidas/eda_e_hipoteses_vitaliza.md` no formato **"1 Tabela + 1 Gráfico + 3 Frases"**.
  - **📊 Trio Negócios (3 pessoas — em paralelo):**
    1. Analisar as implicações estratégicas dos 3 marcos para retenção (elasticidade ao preço, cegueira da pesquisa de saída nas lojas e separação entre *Persuadíveis* e *Não Perturbe / Sleeping Dogs* no experimento de agosto).
    2. Redigir a seção de **Limitações da Análise e Governança (LGPD)** em `saidas/customer_segmentation_report_semana5.md`.

---

### 🔲 Etapa 4 — Engenharia de Atributos e Clusterização com K-Means (Sem Target) — 🤝 *Ponto de Encontro Obrigatório*
- **Status:** **Pendente (iniciar após Etapa 3 — Incorporando diretrizes das Aulas 3 e 4 de Tech e o escopo de `13/11` vs. `18/12`)**
- **Divisão de Trabalho e Sincronização:**
  - **💻 Dupla Tech (2 pessoas):**
    1. **Foco da Semana 5 (`13/11` — *"Até a segmentação"*): Criar Ótimos Clusters Comportamentais:** Conforme orientação do professor, na entrega parcial da Semana 5 não precisamos otimizar os clusters para prever o churn (o modelo preditivo de saída e a seleção de variáveis otimizada para explicar o churn são o foco da Semana 10 em `18/12`). O objetivo aqui é formar **grupos comportamentais muito bem segregados, estáveis, interpretáveis e acionáveis** — partindo das **4 variáveis base da Aula 3 de Tech** (`treinos por semana nas 12 semanas até o corte`, `dias desde o último treino`, `tempo de casa em dias` e `% dos treinos ao ar livre [corrida, caminhada e pedal]`) e avaliando até 1–2 variáveis comportamentais adicionais se melhorarem a coesão/separação dos grupos, **sem jamais colocar a variável de `churn`/saída dentro do K-Means**.
    2. Avaliar tratamento de cauda longa (teto ou `log` em variáveis assimétricas como `dias sem treino` ou `km`) e **padronizar obrigatoriamente** com `StandardScaler` ($z = (x - \text{média})/\text{desvio}$) antes de calcular a distância euclidiana.
    3. Rodar o **K-Means** de $k = 2$ a $8$ (`n_init = 10`, `random_state = 0` fixo) e avaliar o agrupamento pelas **4 Lentes da Aula 3 de Tech**:
       - *Lente 1:* **Inércia / Método do Cotovelo** (onde a curva dobra, ex.: entre $k=4$ e $k=5$);
       - *Lente 2:* **Coeficiente de Silhueta** (`silhouette_score` na régua de Kaufman & Rousseeuw);
       - *Lente 3:* **Estabilidade por Reamostragem** (`adjusted_rand_score` em 5 a 10 reamostras com reposição, validando $\text{Rand} > 0,90$, onde $k=4$ atinge `0,999`);
       - *Lente 4:* **Leitura de Negócio** (tamanho $n$, **perfil em medianas na unidade original** e cruzamento descritivo pós-agrupamento com a **saída histórica em 60 dias** de cada grupo, como nos 4 grupos de referência da aula: *Parados*, *Ativos ao ar livre*, *Ativos em ambiente fechado* e *Veteranos*).
    4. Incluir no notebook `03_segmentacao_clusters.ipynb` a seção de **Perguntas Diagnósticas para Melhoria do Algoritmo** e registrar todas as escolhas (variáveis, escala, `random_state` e $k$) em `decisoes/` e `decisoes.md`.
  - **📊 Trio Negócios (3 pessoas):**
    1. Validar os 3 a 4 clusters gerados por Tech frente aos **4 Critérios da Aula 3 de Tech** (*Distinto, Estável, Grande o bastante e Acionável*) e aos **5 Critérios de Negócios** (*Acionabilidade, Diferenciação de Resposta, Estabilidade no Tempo, Viabilidade Econômica e Mensurabilidade*).
    2. Traduzir os números frios dos grupos (`Grupo 1, 2, 3, 4`) para **nomes executivos de perfil e uma frase de negócio por grupo** (*"O nome resume o perfil e é uma hipótese a testar"*), garantindo que os mesmos segmentos alimentem tanto o *Customer Segmentation Report* quanto o *Mini Deck*.

---

### 🔲 Etapa 5 — Redação do *Customer Segmentation Report* (Artefato de Negócios da Semana 5)
- **Status:** **Pendente (iniciar após Etapa 4)**
- **Responsável Principal:** **📊 Trio de Negócios (3 pessoas)** *(editando exclusivamente `saidas/customer_segmentation_report_semana5.md`)*
- **Escopo Obrigatório:**
  1. Descrição executiva dos **3 a 4 segmentos** com **Cartões de Persona** completos (quem são, tamanho $n$ e %, receita líquida representada, comportamento de uso, canal e vínculo contratual — usando os números exatos da Etapa 4).
  2. **Hipóteses de *drivers* de churn por segmento** estruturadas em 3 partes (*Ação + Público + Resultado Esperado*) e organizadas pela Árvore MECE.
  3. **Matriz de Priorização Preliminar** (*Intervenção Imediata vs. Monitoramento vs. Não Perturbe*), alocando os canais (300 atendimentos CS, 1.500 msgs WhatsApp, E-mail e Push) dentro do teto de R$ 40.000/mês.
  4. Integração das **visualizações da EDA** geradas pela Dupla Tech nas Etapas 2, 3 e 4.
  5. **Seção de Limitações da Análise e Governança (LGPD):** Ponto cego dos 70% em lojas, viés Web da pesquisa de saída, mudança de regra em `uso_mensal.csv`, risco de confundimento/causalidade reversa e princípios da LGPD.

---

### 🔲 Etapa 6 — Construção do *Mini Deck de EDA* (Artefato de Tecnologia) e QA Final da Semana 5
- **Status:** **Pendente (iniciar após Etapa 5 e/ou Aula 4 de Tech)**
- **Responsável Principal:** **💻 Dupla de Tecnologia (2 pessoas)** *(editando exclusivamente `saidas/mini_deck_eda_semana5.md`)* + **Revisão Cruzada com Negócios**
- **Escopo Obrigatório:**
  1. Estruturar o **Mini Deck analítico** contando a história completa dos dados (Qualidade e Limpeza $\rightarrow$ Subida do Churn em 2026 e os 3 Marcos $\rightarrow$ Padrões de Comportamento e Correlações Controladas $\rightarrow$ Sustentação Empírica dos Segmentos).
  2. Aplicar o checklist de QA entre Dupla Tech e Trio Negócios: reprodutibilidade dos notebooks `01`, `02` e `03` e conferência cruzada garantindo que todos os números citados no *Customer Segmentation Report* e no *Mini Deck* sejam idênticos.

