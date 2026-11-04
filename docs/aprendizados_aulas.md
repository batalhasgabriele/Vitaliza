# Síntese de Aprendizados dos Materiais de Aula - Case Vitaliza

Este documento consolida os aprendizados teóricos, metodológicos e práticos extraídos dos materiais de aula do **Módulo 2 do MBA em IA e Dados para Negócios (Inteli)** (*Negócio Aulas 1 e 2, Tech Aulas 1 e 2 Extra*). Ele serve como guia de referência obrigatório para as etapas de análise exploratória, engenharia de atributos, modelagem preditiva e tomada de decisão estratégica do projeto **Vitaliza**.

---

## 1. Visão Geral Estratégica: O Dilema de Negócio da Vitaliza

* **Contexto do Negócio:**
  * App freemium brasileiro de saúde e bem-estar (treinos outdoor com GPS, vídeos guiados e feed social).
  * 27.901 assinantes pagantes ativos; ticket médio mensal de R$ 39,90.
  * O churn mensal aumentou de 5,6% para 6,6% em 2026 (ou 10,2% no segmento de contratos mensais vs. meta contratual de 6,0%).
  * Razão LTV/CAC caiu para 2,02 (abaixo do piso de 3,0 exigido para a rodada de Série B), gerando perda recorrente de ~R$ 113.000,00/mês em MRR.
* **Os Dois Caminhos em Conflito (O Dilema de Camila Ferraz):**
  * **Caminho A – Win-Back Reativo (Abordagem "Bombeiro"):**
    * Dispara ofertas/descontos no momento em que o usuário clica em "Cancelar".
    * Rápido de implementar (MVP em 4 semanas), porém possui um **ponto cego fatal**: **32,9% dos cancelamentos (349 de 1.060)** ocorrem *sem qualquer clique no botão* (sumiço silencioso, cancelamento direto na loja de aplicativos da Apple/Google, bloqueio de cartão ou chargeback). Quem cancela fora do app nunca é impactado pelo Caminho A.
  * **Caminho B – Engagement Forecasting (Abordagem Estrutural/Preditiva):**
    * Modelagem preditiva diária/semanal para detectar desengajamento e risco de saída semanas antes do churn acontecer.
    * Inicialmente visto como mais complexo (60% do orçamento consumido em infraestrutura e dados), tornou-se um **requisito competitivo obrigatório de mercado** após o Strava Premium anunciar para o Q1/2026 uma camada de engajamento preditivo hiperpersonalizado para o Brasil.

---

## 2. A Definição Formal da Pergunta do Case (As 3 Dimensões)

A ciência de dados aplicada ao negócio vai além de estimar probabilidades abstratas; ela responde a três perguntas conectadas:

1. **Prever (Classificação / Risco):**
   * *Qual é a probabilidade de cada assinante sair até 29/11/2026?*
   * Gera uma pontuação de risco contínua (probabilidade entre 0,0 e 1,0) para a base ativa.
2. **Decidir (Prescrição / Uplift):**
   * *Quem contatar, com qual oferta/mensagem, e quem deixar quieto?*
   * Ter alto risco de churn não justifica contato automático. Deve-se priorizar o grupo que **só permanece se receber a intervenção**, evitando impactar clientes que não querem ser incomodados ("cães adormecidos" que cancelam ao serem lembrados da assinatura).
3. **Valorar (Impacto Financeiro Líquido):**
   * *Quanto a estratégia de intervenção gera de retorno financeiro real?*
   * Respeitar o limite de capacidade operacional (ex.: 1.500 contatos/mês) e calcular:
     $$\text{Retorno Líquido} = \text{Receita Salva} - \text{Custo Operacional de Contato} - \text{Custo dos Benefícios/Cupons Concedidos}$$

---

## 3. População Elegível e Janela de Corte Temporal

Para evitar contaminação e discrepâncias entre análises:
* **Data de Corte Oficial:** `30/09/2026`.
* **População Elegível:** Usuários pagantes ativos em `30/09/2026` com opção de renovação automática ligada.
* **Janela de Desfecho (Target):** 60 dias (até `29/11/2026`).
* **Definição Operacional de Churn (Saída):** Estar em `29/11/2026` com renovação desligada ou sem assinatura ativa (contempla desligamento voluntário, falhas definitivas de cobrança não recuperadas, estornos e chargebacks).

---

## 4. Metodologia de Formulação e Teste de Hipóteses

### 4.1 A Estrutura em Três Partes de uma Hipótese Testável
Para não cair na armadilha de "opiniões com cara de análise", toda hipótese precisa conter:
1. **Afirmação Causal:** Relação clara de causa e efeito e seu sentido (*"X faz Y acontecer"*).
2. **Métrica Objetiva:** Indicador ou coluna específica dos dados que mensura o fenômeno (*"Medido por..."*).
3. **Critério de Refutação Pré-definido:** O valor ou padrão de corte que invalida a hipótese se não for observado nos dados (*"Cai se..."*). Se o critério não for definido antes da análise, a hipótese será amoldada a qualquer resultado encontrado.

### 4.2 Árvore MECE de Hipóteses de Churn
A formulação deve cobrir 4 galhos mutuamente exclusivos e coletivamente exaustivos:
* **Galho 1: Características de Entrada:** Quem entrou? (idade, sexo, prefixo de CEP, canal de aquisição, objetivos declarados no onboarding).
* **Galho 2: Comportamento de Uso:** O que faz no app? (frequência de treinos, volume de minutos, gastos extras em desafios/loja, padrão de rotas GPS).
* **Galho 3: Ciclo de Vida e Vínculo Contratual:** Há quanto tempo está ativo e com que contrato? (tempo de casa/*lifetime*, plano mensal vs. anual, método de pagamento).
* **Galho 4: Comunidade e Conexões Sociais:** Está conectado na rede? (amizades ativas, treinos em dupla/grupo, comentários e posts no feed).

> **Atenção:** Para cada coluna utilizada, a equipe deve explicitar: *"O que essa coluna NÃO mede?"* (ex.: 0 treinos num mês pode significar lesão física, frustração ou falha no upload de dados de GPS). Se uma variável de negócio não existe na base (ex.: sensibilidade a preço sem histórico de testes de preço), essa ausência é um fato analítico a ser registrado e contornado.

---

## 5. Armadilhas Metodológicas e Vazamento de Dados (*Data Leakage*)

1. **Vazamento Temporal (*Toda variável tem data*):**
   * Nunca utilizar variáveis cujos valores foram gerados ou influenciados pelo próprio evento de cancelamento (ex.: `frequência do mês corrente` para quem cancelou no início do mês é zero em decorrência do cancelamento, e não causa dele).
   * Somente utilizar informações geradas estritamente até a data de corte (`30/09/2026`).
2. **Sinal do Contrato mascarado de Engajamento:**
   * A variável `meses até o fim do contrato` em planos mensais vale invariavelmente 1; tratá-la como indicador contínuo de engajamento gera multicolinearidade espúria com a variável `plano`.
3. **Causalidade Falsa vs. Viés de Seleção (Endogeneidade):**
   * Usuários participantes de desafios têm menor churn não necessariamente porque o desafio os reteve, mas porque usuários inerentemente disciplinados procuram desafios. Correlação não prova causalidade sem controle ou grupo de comparação.

---

## 6. Boas Práticas Estatísticas e de Limpeza de Dados

* **Média vs. Mediana em Distribuições Assimétricas:**
  * Métricas de uso de produto digital e gastos adicionais possuem distribuições fortemente assimétricas com presença de *outliers*.
  * A média é facilmente distorcida por caudas longas; a **mediana**, **IQR** (intervalo interquartil) e visualizações via **boxplots/histogramas** devem ser priorizados para descrever o cliente típico da Vitaliza.
* **Tidy Data e Granularidade:**
  * Respeitar rigorosamente a granularidade dos arquivos antes dos cruzamentos (`user_id` único em `usuarios.csv`; relacionamento 1:N com logs em `pagamentos.csv` e `atividades.parquet`).
  * Não fazer junções ingênuas que multipliquem linhas e inflem valores monetários ou contagens de treinos.

---

## 7. Governança, Ética e Conformidade com a LGPD

* **Poder Preditivo vs. Autorização de Ação:**
  * Análises univariadas revelam que a **idade** tem forte correlação com churn (usuários de 18 a 22 anos cancelam mais que faixas acima de 30 anos, mesmo controlando por tempo de casa).
  * No entanto, criar regras automáticas de preços, exclusão de suporte ou ofertas desvantajosas baseadas em idade pode violar o **Princípio da Não Discriminação da LGPD (Art. 6º, IX)**.
  * O usuário tem o direito legal de solicitar revisão humana sobre decisões puramente automatizadas (**Art. 20 da LGPD**).
* **Variáveis Irrelevantes ou de Risco Ético Desnecessário:**
  * Gênero e telefone apresentam AUC próximo de 0,50 (poder discriminatório igual ao acaso) e devem ser descartadas do pipeline preditivo.

---

## 8. Estrutura dos Artefatos de Entrega

* **Artefato 1 – Customer Segmentation Analysis Report:**
  * Pelo menos 3 a 4 clusters estatísticos transformados em **Personas Estratégicas de Negócio** (ex.: *"O Entusiasta Frustrado"*).
  * Tabelas contendo: tamanho do segmento, churn rate médio, receita líquida em risco, drivers comportamentais de saída e proposta de intervenção imediata vs. monitoramento.
  * Seção obrigatória destacando as **limitações dos dados** (ex.: ausência de logs de cliques de tela do Mixpanel).
* **Artefato 2 – Board Recommendation Deck (6 Slides Executivos):**
  * Apresentação executiva simulada de Camila Ferraz para o Conselho da Vitaliza.
  * Diagnóstico do problema (evolução do churn, LTV/CAC e MRR em risco).
  * Recomendação justificada entre Caminho A e Caminho B com base em ROI financeiro líquido, prazo de implementação, riscos técnicos e posicionamento estratégico contra o avanço do Strava no Brasil.

---

## 9. Metodologia de Trabalho com IA Generativa (Framework CREATE)

* **O Novo Papel do Profissional em 2026:**
  * A IA generativa escreve códigos, consolida logs e processa texto livre em alta velocidade. O diferencial competitivo e gargalo do time reside em **revisar, aplicar método, evitar vieses cognitivos e tomar decisões estratégicas**.
  * *"IA sem método é o viés de confirmação com velocidade de processamento."*
* **Framework CREATE para Prompts de Alto Impacto:**
  * **C - Character (Papel):** Delimitar com precisão a especialidade da IA (ex.: consultora de unit economics, especialista em retenção de produto).
  * **R - Request (Pedido):** Solicitação analítica objetiva e delimitada.
  * **E - Examples (Exemplos):** Padrões desejados de saída e o que deve ser explicitamente evitado.
  * **A - Additions (Ajustes):** Tom, audiência-alvo (C-level, time técnico) e restrições.
  * **T - Type of Output (Formato de Saída):** Saídas tipadas e estruturadas (tabelas markdown, schemas JSON/Pydantic rígidos).
  * **E - Extras:** Considerações complementares e diretrizes de refutação.
* **Processamento de Dados Não Estruturados:**
  * Utilizar LLMs e modelos multimodais com *schemas tipados* para converter textos livres do onboarding/feed e imagens de heatmaps de GPS em variáveis tabulares (booleanas, numéricas e categóricas) prontas para o modelo de Machine Learning.
