# Guia de Referência: Resumo das Aulas de Negócios (Módulo 2 — MBA Inteli)

> **Propósito deste Documento:** Consolidar os conceitos, frameworks estratégicos, aprendizados, critérios de decisão e alertas metodológicos apresentados nas **Aulas 1, 2 e 3 da Trilha de Negócios** (Prof. Fábio Cássio de Souza e Tutora Natália Kloekner).
>
> **Regra de Uso no Projeto:** Este material deve ser **consultado sempre que necessário** para fundamentar nossas análises, escolhas de segmentação, formulação de hipóteses e construção dos artefatos das Semanas 5 e 10. Ele funciona como **base conceitual e metodológica**, sem nos restringir — podemos (e devemos) ir além dele combinando-o com as 12 tabelas reais do *data room* da Vitaliza e técnicas avançadas de Ciência de Dados e IA Generativa.
>
> **Regra de Atualização Contínua (Documento Vivo):** **Este arquivo DEVE ser atualizado SEMPRE que um novo arquivo de aula de Negócios for adicionado na pasta [`materiais-aulas/`](../materiais-aulas/)** (assim como [`docs/resumo_aulas_tecnologia.md`](resumo_aulas_tecnologia.md) deve ser atualizado sempre que entrar uma nova aula de Tecnologia).

---

## 📌 Nota de Alinhamento: Dados Ilustrativos das Aulas vs. Data Room Oficial do Case
Nos slides das aulas de Negócios, alguns exemplos didáticos utilizam recortes ilustrativos (ex.: base de `n = 4.000` de academia/fitness com colunas em inglês como `Avg_class_frequency_total`, `Near_Location`, ou o cenário executivo de `27.901` assinantes).
* **Conceitos e Frameworks das Aulas:** 100% aplicáveis e obrigatórios (Sistema 1 vs. 2, Vieses, Caminho A vs. B, Sleeping Dogs, Hipóteses em 3 partes, Árvore MECE, 5 Critérios de Segmentação, Comportamento vs. Demografia, LGPD).
* **Números Oficiais da Entrega do Grupo:** Devem sempre vir das **12 tabelas do Data Room da Vitaliza** e do **Enunciado Oficial do Case** (`64.948` contas cadastradas, `14.753` pagantes ativos no corte de `30/09/2026`, churn subindo de `5,6%` em 2025 para `6,6%` em 2026).

---

## 🏛️ Aula 1 — Inteligência de Mercado, Tomada de Decisão e Engenharia de Contexto com IA

### 1. O Território do Módulo: Do Dado à Decisão
* **O verdadeiro gargalo:** *"O problema não é só ter ou não ter dados. O problema é o que acontece entre o dado existir e a decisão ser tomada."*
* **Três pilares conectados:**
  1. **Inteligência:** Não é dado bruto; é o ponto em que o dado ganha contexto suficiente para influenciar uma decisão real.
  2. **Modelagem Preditiva:** Predizer não é adivinhar. É usar comportamento observável para antecipar risco, oportunidade e prioridade de ação antes que o problema vire fato consumado.
  3. **Crescimento:** Retenção é crescimento (provado com números de *unit economics*: LTV, CAC, MRR e Payback).

### 2. Psicologia da Decisão Executiva e Vieses Cognitivos
* **Intuição + Dados são complementares (Daniel Kahneman):**
  * **Sistema 1 (Rápido, Automático, Intuitivo):** Responsável por 90–95% das decisões diárias. Funciona bem em contextos familiares, mas traz o risco do executivo que *"já sabe"* como o cliente se comporta e decide antes de olhar o dado.
  * **Sistema 2 (Lento, Deliberado, Analítico):** Exige esforço consciente para estruturar critérios, dados e evidências que reduzem o ruído.
  * **Regra de Ouro de Kahneman:** *Avaliação estruturada de critérios (dados/evidências) + intuição calibrada no final = melhor preditor de desempenho.*
* **As 4 Armadilhas dos Vieses na Decisão (McKinsey — *Biases in Decision-Making*):**
  1. **Ancoragem:** Decisões distorcidas pelo primeiro número disponível (ex.: *"O churn do ano passado foi X%, então este ano deve ser parecido"*).
  2. **Viés de Confirmação:** Buscar apenas dados que confirmam a crença prévia e ignorar variáveis contrárias (ex.: cada diretor da Vitaliza culpando uma causa diferente).
  3. **Groupthink (Pensamento de Grupo):** O consenso sufoca a análise crítica; a harmonia da reunião vira prioridade sobre a qualidade da decisão.
  4. **Excesso de Otimismo:** Subestimar riscos técnicos e superestimar prazos e taxas de conversão.
  * *Evidência:* Decisões com debate estruturado têm **2,3x mais chance de dar certo**.

### 3. O Dilema Executivo da Vitaliza (Visão C-Level e Stakeholders)
* **Múltiplos Olhares (Política de Decisão Real):** O mesmo dado pode ser usado para defender lados opostos conforme o interesse do stakeholder:
  * **Rita Fontes (CFO):** Foco em ROI, razão LTV/CAC (piso saudável $\ge 3,0$), impacto no fluxo de caixa e viabilidade da captação da Série B. Avessa a premissas não declaradas.
  * **Marcelo Tavares (Head de Produto):** Foco em personalização, falta de diferenciação da experiência (*"tratamos corredor de maratona e quem quer perder 5kg como a mesma pessoa"*) e ameaça competitiva do **Strava Premium** (que lançou camada preditiva de engajamento personalizado no Brasil).
  * **Patrícia Marques (Head de CS):** Foco operacional imediatista (*"estancar a sangria primeiro"*), capacidade da equipe e contas recuperáveis no curto prazo.
  * **Diego Almeida (CTO):** Foco em viabilidade técnica, integração de sistemas dispersos, tempo de engenharia de dados e custo de infraestrutura.
* **Caminho A vs. Caminho B (e por que nenhum isoladamente basta):**
  * **Caminho A — *Win-Back* Reativo ("O Bombeiro"):** Dispara oferta quando o usuário clica em "Cancelar". É rápido, mas tem um **ponto cego estrutural**: não enxerga quem cancela silenciosamente fora do app (lojas Apple/Google, falha de pagamento/chargeback).
  * **Caminho B — *Engagement Forecasting* ("O Detector de Fumaça"):** Score preditivo que detecta desengajamento semanas antes. É o novo **piso competitivo** frente ao Strava, mas traz o risco de acordar ***Sleeping Dogs*** (clientes inativos que pagam por inércia e cancelam ao receberem comunicação).

### 4. Os 3 Pilares dos Artefatos de Negócios e Boas Práticas
1. **Segmentação Estratégica:** Transformar clusters estatísticos em interpretação de negócio (nomear e qualificar com tamanho, churn rate e receita).
2. **Criação de Personas Baseadas em Dados:** *Persona de dados $\neq$ Persona de marketing.* Toda persona deve ter âncora em variáveis da EDA: **quem é $\cdot$ o que faz $\cdot$ por que sai $\cdot$ custo financeiro da perda**.
3. **Valor Estratégico:** Calcular o **Valor em Risco** ($\text{Churn Rate} \times \text{Receita Média}$) e priorizar por **Impacto $\times$ Acionabilidade**.
* **Erros Comuns a Evitar:**
  * ❌ Persona sem âncora em dados $\rightarrow$ ✅ Todo atributo deve ter variável correspondente na EDA.
  * ❌ Segmentos genéricos demais $\rightarrow$ ✅ Nomear com intenção estratégica (ex.: *"O Entusiasta Frustrado"*).
  * ❌ Ignorar o valor financeiro $\rightarrow$ ✅ Sempre incluir **receita em risco** no documento final.
  * ❌ Documento feito só para cientistas de dados $\rightarrow$ ✅ Linguagem e visual acessíveis para C-level e Produto.

### 5. IA Generativa como Parceiro Metodológico (Engenharia de Prompt vs. Contexto)
* *"IA sem método é o viés de confirmação com velocidade de processamento."* (O efeito "espelho caro").
* **Plausível $\neq$ Evidência:** A IA gera hipóteses plausíveis (Sistema 1) em segundos, mas só os dados reais testam e derrubam ou confirmam essas hipóteses (Sistema 2). *"O julgamento é seu. A geração é dela."*
* **Engenharia de Prompt vs. Engenharia de Contexto:**
  * *Prompt:* Sintaxe, tom e formato do pedido no chat.
  * *Contexto:* O que você sabe sobre o problema antes de abrir o chat (hipóteses, variáveis, objetivos de decisão e quem vai usar o output).
* **Framework CREATE para Prompts Executivos:**
  * **C — Character (Papel):** Especialidade exata que a IA deve assumir.
  * **R — Request (Pedido):** Ação específica e clara.
  * **E — Examples (Exemplos):** O que incluir e o que evitar no raciocínio.
  * **A — Additions (Ajustes):** Audiência (CFO, CS, CTO, Board), tom e restrições.
  * **T — Type of Output (Formato):** Tabela, memo, 3 bullets executivos, JSON tipado.
  * **E — Extras:** Dados concretos do case, benchmarks e exigência de declarar premissas explicitamente.

---

## 🔬 Aula 2 — Traduzindo Problemas de Negócio em Hipóteses Analíticas

### 1. A Anatomia de uma Hipótese Testável (As 3 Partes Obrigatórias)
Para sair do achismo (*HIPPO — Highest Paid Person's Opinion*, ex.: *"O preço está alto demais"*), toda hipótese do projeto precisa ter:
1. **Afirmação Causal:** Diz o que causa o quê e em que direção (*"X faz Y acontecer"*).
2. **Métrica:** Qual variável, coluna ou taxa específica do dataset vai medir isso (*"Medido por..."*).
3. **Critério de Refutação Pré-definido:** O resultado numérico ou comparativo que derruba a hipótese, definido **antes** de olhar os dados (*"Cai se..."*).
   * *Lição central:* Sem critério de refutação, a hipótese se ajusta a qualquer resultado (opinião com cara de análise).
   * *Ausência de dados também é informação:* Se a base não tem variação ou histórico para testar uma hipótese diretamente, registrar o que os dados **não permitem testar** é um achado analítico obrigatório.

### 2. Árvore MECE de Hipóteses de Churn (4 Galhos)
Os fatores de cancelamento devem ser organizados em **4 galhos mutuamente exclusivos e coletivamente exaustivos (MECE)**:
1. **Características de Entrada:** Quem entrou? (idade, perfil demográfico, localização/CEP, canal de aquisição, objetivos declarados no onboarding).
2. **Comportamento de Uso:** O que a pessoa faz no app? (frequência de treinos, desaceleração recente, duração, uso de funcionalidades, gastos extras).
3. **Ciclo de Vida e Contrato:** Há quanto tempo está na base (*lifetime/tenure*) e com qual vínculo contratual (mensal vs. anual, canal de pagamento, proximidade de renovação)?
4. **Comunidade e Social:** Está conectada a outras pessoas? (participação em desafios/grupos, indicação de amigos, interações no feed social, parcerias/convênios).
* **Exercício Crítico Obrigatório:** Para cada coluna analisada, sempre responder: **"O que essa coluna NÃO mede?"** (ex.: frequência zero não distingue lesão física de insatisfação com o app).

### 3. As 3 Grandes Armadilhas Analíticas
1. **Vazamento de Dados (*Data Leakage* — "Toda variável tem data"):**
   * Variáveis medidas após ou durante o próprio evento de saída (ex.: frequência do mês corrente zerada porque o usuário já cancelou no início do mês, ou *lifetime* calculado até a data do cancelamento sem ancorar num corte fixo).
   * *Regra:* Usar apenas variáveis que já existiam **antes** do período de previsão (até a data de corte `30/09/2026`).
2. **Sinal do Contrato Mascarado:**
   * Variáveis como "meses até o fim do contrato" valem sempre 1 no plano mensal. Não são sinais puros de engajamento, mas sim um reflexo mecânico da modalidade contratual. Devem ser interpretadas junto com o contrato.
3. **Confusão entre Correlação, Causalidade e Viés de Seleção (Endogeneidade):**
   * Exemplo clássico: *"Quem participa de desafios cancela menos (6,7% vs. 18,6%)"* ou *"Quem está no plano anual cancela menos"*.
   * *Pergunta de negócio:* O desafio/plano anual **causa** retenção, ou usuários que já são motivados **escolhem** o plano anual e entram em desafios (efeito de seleção)?
   * *Como separar seleção de efeito causal:* Através de experimentos controlados (sorteio / Teste A/B, como a campanha de `10/08/2026` da Vitaliza) ou controlando por variáveis de engajamento prévio.

### 4. Ética, Poder Preditivo e Conformidade com a LGPD
* **Entender $\neq$ Decidir:**
  * Uma variável demográfica como **idade** pode apresentar alto poder preditivo univariado (mesmo controlando por tempo de casa), pois captura indiretamente renda, rotina ou maturidade que não estão no arquivo.
  * Contudo, **prever não é autorizar ação**: usar idade para definir preços, negar descontos ou restringir suporte pode configurar discriminação ilícita ou abusiva (**LGPD, Art. 6º, IX — Princípio da Não Discriminação**).
  * Além disso, o titular tem direito à revisão de decisões tomadas unicamente com base em tratamento automatizado (**LGPD, Art. 20**).
* **Descarte de Variáveis Sem Sinal:** Variáveis sensíveis ou cadastrais com AUC próximo de `0,50` (como gênero e telefone) não têm poder preditivo além do acaso e devem ser descartadas por parcimônia e governança.

---

## 🎯 Aula 3 — Comportamento vs. Demografia: O Valor Estratégico da Segmentação

### 1. O Que a Média Esconde
* Olhar apenas para o churn médio da base esconde grupos com comportamentos diametralmente opostos (grupos que vão de quase 0% a mais de 75% de churn).
* **Segmentar é o primeiro passo de qualquer decisão:** A pergunta deixa de ser *"qual variável prevê churn?"* e passa a ser **"qual grupo de clientes exige qual ação?"**.

### 2. As Três Lentes para Olhar o Mesmo Cliente
Dois assinantes com **cadastro demográfico idêntico** (mesma idade, mesmo gênero, mesma região) frequentemente apresentam comportamentos e desfechos opostos. Por isso, avaliamos o cliente sob **3 lentes**:

| Lente | Pergunta Central | Exemplos de Variáveis | Características e Limitações |
| :--- | :--- | :--- | :--- |
| **1. Demografia** | *Quem é?* | Idade, gênero, região/CEP, parceria de entrada | Estável e disponível no Dia 1 (*onboarding*), mas **não diz o que a pessoa faz nem como agir**. Tem baixo ganho marginal quando já temos comportamento. |
| **2. Comportamento** | *O que faz?* | Tempo de casa (*lifetime*), frequência de treinos, participação em desafios/grupos, plano, gastos extras | Muda ao longo do tempo e leva semanas para se formar, mas **prevê muito mais o churn** e **onde está a alavanca de ação**. |
| **3. Necessidade (*Jobs-to-be-Done*)** | *Por que contratou? Que progresso busca?* | Textos livres de metas no onboarding, posts no feed, motivos em tickets de suporte | Não vem pronta em colunas numéricas tradicionais; **exige extração de texto/imagem** (onde entra a IA Generativa no nosso projeto!). |

* **Três motivos para NÃO segmentar/agir pela idade (ou demografia pura):**
  1. Não diz o que fazer (qual intervenção oferecer).
  2. Não muda com a ação da empresa (a Vitaliza não muda a idade de ninguém, mas pode mudar a frequência de treinos ou a participação em desafios).
  3. Risco legal e ético de discriminação (LGPD, Art. 6º, IX).
  * *Síntese:* **Use a demografia para entender e controlar a análise (ou no Dia 1). Use o comportamento e a necessidade para segmentar e agir.**

### 3. O Paradoxo do Início (*Cold Start Problem*)
* Grande parte do churn (especialmente no plano mensal) ocorre nos **primeiros 30 a 90 dias de casa**, justamente quando o histórico comportamental ainda está se formando.
* **Estratégia em Camadas Temporais para a Vitaliza:**
  * **Na Entrada (Dia 1 / Mês 1):** Usar vínculo contratual (mensal vs. anual), canal de aquisição (indicação, parceria, influenciador) e **necessidade declarada no onboarding** (extraída via IA).
  * **Nas Primeiras Semanas:** Monitorar a formação de hábito (primeiros treinos por semana e entrada em desafios/comunidade).
  * **Após o Estabelecimento:** Usar o histórico comportamental completo e tendências de desaceleração (recência e variação de frequência).

### 4. Os 5 Critérios de Utilidade de um Segmento
Para validar se um segmento construído pelo grupo é realmente útil para o negócio, ele deve passar no **Checklist dos 5 Critérios** (Kotler / Frameworks de Segmentação):
1. **Mensurável:** É possível medir com precisão o tamanho ($n$ e $\%$ da base), o churn e a receita em risco do grupo?
2. **Substancial:** O grupo é grande ou valioso o bastante para justificar o custo de criar uma ação dedicada?
3. **Diferenciável:** O grupo apresenta comportamento e taxa de saída claramente distintos dos demais segmentos?
4. **Acessível:** A empresa consegue alcançar esse grupo por um canal viável no momento certo (ex.: Push, E-mail, WhatsApp, CS)?
5. **Acionável:** Existe uma intervenção clara (oferta, desafio, conteúdo, pausa) capaz de alterar o comportamento e reter esse cliente?
   * *Regra prática:* **Um segmento que prevê, mas não permite agir (não é acionável), serve apenas para diagnóstico — não serve para campanha.**

### 5. Cardápio de Técnicas de Segmentação e Cuidados Metodológicos
* **Técnica 1 — Regras de Negócio / Cortes Cruzados (ex.: Matriz Tempo de Casa $\times$ Frequência / RFM adaptado):**
  * *Vantagem:* Transparente, fácil de explicar ao Board e imediata de operar no CRM.
  * *Cuidado:* Diferenciar **frequência média histórica** (vida toda) de **recência / frequência recente** (últimas semanas antes do corte). No caso da Vitaliza, temos logs com datas que permitem medir recência e desaceleração!
* **Técnica 2 — Clusterização Estatística (*K-Means* e algoritmos não supervisionados):**
  * *Vantagem:* Descobre agrupamentos naturais combinando múltiplas variáveis sem cortes arbitrários prévios (e **sem usar a variável target de churn** para formar os grupos).
  * *Cuidados críticos com o K-Means:*
    1. O algoritmo **sempre** entrega grupos, mesmo que a separação seja fraca (sempre avaliar métricas como *Silhouette Score* e interpretabilidade).
    2. **Colunas binárias (0/1) e diferenças de escala dominam a distância euclidiana** se não houver padronização adequada.
    3. **Quem dá nome e sentido de negócio ao cluster é o analista, não o algoritmo** (ex.: transformar centroides em personas como *"Sozinhos em Risco"*, *"Turma dos Desafios"*, *"Veteranos Fiéis"*).
* **Técnica 3 — Microsegmentação (Múltiplos Scores: Risco $\times$ Valor/LTV $\times$ Uplift):**
  * Ideal para a fase prescritiva (Semana 10), cruzando probabilidade do modelo preditivo, efeito incremental da campanha A/B e valor financeiro.
* **Técnica 4 — Embeddings (Representação Vetorial de Histórico/Texto/Imagem):**
  * Conecta-se à extração via IA Generativa para enriquecer o perfil do usuário com dados não estruturados.

### 6. Governança de Dados Comportamentais (LGPD e Ecossistema Digital)
Mesmo dados comportamentais exigem governança rigorosa:
* **Base Legal (LGPD, Art. 7º):** Todo tratamento de dados exige base legal clara (consentimento ou legítimo interesse aplicável).
* **Princípio da Finalidade (LGPD, Art. 6º, I):** Dado coletado estritamente para prestar o serviço (ex.: rota GPS do treino) exige transparência e adequação de finalidade para ser usado em campanhas comerciais.
* **Dependência de Terceiros (ex.: Apple ATT e Lojas de App):** Mudanças nas políticas da Apple/Google restringem rastreamento externo e ocultam a tela de cancelamento. Por isso, **dados primários (*first-party data*) de uso dentro do próprio app da Vitaliza** são o ativo mais seguro e resiliente da empresa.

---

## 🧭 Síntese Operacional: Como Aplicar este Guia nas Entregas

1. **Na Análise Exploratória (EDA) e Hipóteses (Semana 5):**
   - Estruturar todas as hipóteses nos **4 galhos MECE** com **Afirmação Causal + Métrica + Critério de Refutação**.
   - Explicitar o que cada variável **não mede** e blindar a análise contra **vazamento temporal** (corte estrito em `30/09/2026`).
2. **No `Customer Segmentation Report` (Semana 5):**
   - Priorizar variáveis de **comportamento e ciclo de vida** (e necessidades extraídas) sobre demografia pura.
   - Construir **3 a 4 segmentos/personas** sem usar a variável *target* de saída na clusterização, mas validando depois o churn rate e a **receita em risco** de cada grupo.
   - Avaliar os segmentos criados contra os **5 Critérios de Utilidade** (Mensurável, Substancial, Diferenciável, Acessível, Acionável) e resumir cada persona no formato: **"Quem são $\cdot$ O que fazem $\cdot$ Por que saem $\cdot$ Custo da perda $\cdot$ O que a Vitaliza deve fazer"**.
3. **No Plano de Intervenção e App Preditivo-Generativo (Semana 10):**
   - Resolver o dilema **Caminho A vs. Caminho B** mostrando como a arquitetura preditiva-generativa contorna o ponto cego dos cancelamentos em loja e evita acordar *Sleeping Dogs* (via análise de *uplift* da campanha de agosto).
   - Traduzir os achados para a linguagem de cada executivo do Board (CFO, Produto, CS e CTO) com cálculo rigoroso de ROI dentro do orçamento de `R$ 40.000/mês`.

