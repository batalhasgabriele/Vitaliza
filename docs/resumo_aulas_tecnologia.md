# Guia Consolidado — Aulas de Tecnologia (Módulo 2 MBA IA e Dados — Inteli)

> **Diretriz de Uso deste Documento:**
> 1. **Base de Referência:** Este arquivo consolida toda a fundamentação técnica, metodológica, estatística e os achados empíricos oficiais das aulas da trilha de **Tecnologia** (Prof. Cesar Almiñana) aplicadas ao case **Vitaliza**. Ele deve ser consultado sempre que necessário como **base de referência para o projeto** (regras de limpeza, auditoria de dados, estatística descritiva, prevenção de vazamento temporal e arquitetura preditiva/generativa), **sem restringir ou limitar** investigações, hipóteses e análises adicionais.
> 2. **Regra de Atualização Contínua (Documento Vivo):** **Este arquivo DEVE ser atualizado SEMPRE que um novo arquivo de aula de Tecnologia for adicionado na pasta [`materiais-aulas/`](../materiais-aulas/)** (assim como [`docs/resumo_aulas_negocios.md`](resumo_aulas_negocios.md) deve ser atualizado sempre que entrar uma nova aula de Negócios).

---

## Sumário Executivo da Trilha de Tecnologia (4 Movimentos em 10 Semanas)

| Movimento | Aulas | Foco Técnico e Metodológico | Conexão com Entregáveis |
| :--- | :--- | :--- | :--- |
| **1. Entender** | **Aulas 1 e 2** | Metodologia (CRISP-DM/CRISP-ML(Q), 4 tipos de análise), ambiente com agentes de código, 5 dimensões de qualidade de dados, limpeza e Análise Exploratória de Dados (EDA). | Base da **Entrega da Semana 5** (`15/11/2026`): Código + Visualizações + Mini Deck de EDA. |
| **2. Segmentar e Comunicar** | **Aulas 3 e 4** | Aprendizado não supervisionado (Clusterização sem usar a variável resposta de quem saiu) e Visualização de Dados executiva. | Sustenta empiricamente os 3–4 segmentos do *Customer Segmentation Report* (Semana 5). |
| **3. Preparar e Prever** | **Aulas 5 a 8** | Extração de dados não estruturados (texto/imagem) via LLM com schema tipado (Aula 5), Regressão Logística (Aula 6), Árvores e Avaliação/Trade-offs (Aula 7), Bagging, Boosting e Deep Learning (Aula 8). | Previsão de saída até `29/11/2026` (entrega da previsão em `08/12`; revelação do gabarito real em `10/12`). |
| **4. Implantar** | **Aulas 9 e 10** | Deploy do aplicativo web preditivo-generativo (Python + Marimo + API GenAI) e fechamento integrado com Negócios. | **Entrega Final da Semana 10** (`20/12/2026`): Aplicativo Web Preditivo-Generativo + Plano de Intervenção. |

---

## Aula 1 — Conceitos, Metodologia e o Desafio Vitaliza (`15/10/2026`)
**Fonte:** `materiais-aulas/Tech_M2_MBA_IA_Dados_Aula1.pdf` (Prof. Cesar Almiñana)

### 1. Evolução Histórica dos Gargalos ("Da Ideia ao Resultado")
A história da análise de dados é a história de qual era o gargalo de cada época e o que o destravou:
- **Anos 1950–1970 (Gargalo: Computar):** A máquina era rara e cara; cada conta exigia fila, cartão perfurado e operador $\rightarrow$ *Destravado por:* **Computador pessoal e planilha eletrônica** (`1979–1983`).
- **Anos 1970–1980 (Gargalo: Consultar):** Os dados existiam, mas cada pergunta virava um programa escrito sob encomenda pela TI $\rightarrow$ *Destravado por:* **Bancos relacionais e SQL** (`1970–1986`).
- **Anos 1990 (Gargalo: Integrar):** Cada área tinha seu sistema; os números não batiam na mesma reunião $\rightarrow$ *Destravado por:* **Data Warehouse** (`1992–1996`).
- **Anos 2000 (Gargalo: Escalar):** Cliques, buscas e logs da web não cabiam mais em uma única máquina $\rightarrow$ *Destravado por:* **Nuvem e Big Data** (`2004–2006`).
- **Anos 2010 (Gargalo: Codificar):** Os dados estavam na nuvem, mas tirar valor deles dependia de quem sabia programar $\rightarrow$ *Destravado por:* **IA Generativa para código** (`2021–2022`).
- **Hoje — 2026 (Gargalo: Revisar e Refletir):** **Gerar código ficou barato; perguntar bem, conferir e decidir continuam sendo trabalho humano.**

---

### 2. Os 4 Tipos de Análise de Dados
*(Referências: Davenport & Harris, 2007; Lepenioti et al., 2020; Siegel, 2013)*

1. **Análise Descritiva — *"O que aconteceu?"* (Relatórios / BI):**
   - Resume o passado em contagens, taxas e séries no tempo.
   - *Na Vitaliza:* Quantos assinantes pagantes saíram em cada mês? Mostra que a perda mensal subiu em 2026 (média de `5,6%/mês` em 2025 para `6,6%/mês` de jan a set/2026, com pico de `8,1%` em abril/2026).
2. **Análise Diagnóstica — *"Por que aconteceu?"* (Fronteira entre BI e Ciência de Dados):**
   - Compara grupos e cruza variáveis para testar hipóteses sobre a causa.
   - *Na Vitaliza:* Quem sai mais: plano mensal ou anual? Em 2025, a perda mensal média foi de **`9,0%/mês` no plano mensal** contra **`2,6%/mês` no plano anual**.
3. **Análise Preditiva — *"O que vai acontecer?"* (Ciência de Dados — Foco do Módulo):**
   - Usa um modelo treinado com casos cujo desfecho já é conhecido para calcular a **probabilidade individual** de um evento futuro. Ciência de dados começa onde entra um modelo.
   - *Na Vitaliza:* Qual a chance de cada assinante ativo em `30/09/2026` sair nos próximos 60 dias (`até 29/11/2026`)? Na distribuição típica da base: ~61% têm risco baixo (`<10%`), ~24% risco moderado (`10–20%`), ~11% risco alto (`20–40%`) e ~4% risco crítico (`≥40%`).
4. **Análise Prescritiva — *"O que fazer?"* (Ciência de Dados + Negócios):**
   - Combina a previsão de risco, o efeito incremental de cada ação (*uplift*) e o custo/restrição de agir para recomendar **quem contatar e com qual oferta**.
   - **Matriz de Decisão de Contato (2×2 de Uplift):**

| Se NÃO contatar \ Se CONTATAR | Fica se contatar | Sai se contatar |
| :--- | :--- | :--- |
| **Sai se não contatar** | **Persuadível** *(Alvo ideal da intervenção!)* | **Perdido** *(Sai nos dois casos — não gastar incentivo caro)* |
| **Fica se não contatar** | **Garantido** *(Fica nos dois casos — não gastar desconto)* | **Não perturbe / *Sleeping Dog*** *(O contato acorda a saída — nunca acionar!)* |

---

### 3. Ciclo CRISP-DM e a Evolução para CRISP-ML(Q) em 2026
*(Referências: Chapman et al., 2000; Studer et al., 2021; Shankar et al., 2024; Rewolinski & Yu, 2025)*

- **As 6 Fases Clássicas do CRISP-DM:**
  1. **Entendimento do Negócio:** Qual decisão vamos apoiar e como medir sucesso.
  2. **Entendimento dos Dados:** O que existe na base, o que falta e o que engana.
  3. **Preparação dos Dados:** Limpar, juntar tabelas e criar variáveis (*feature engineering*).
  4. **Modelagem:** Treinar e comparar algoritmos que aprendem com os dados.
  5. **Avaliação:** Testar se o modelo resolve o problema do negócio sem vazamento.
  6. **Implantação:** Colocar o resultado na mão de quem decide (App Web).
- **Regra Prática ("A linha anda pelo ciclo, não desce uma escada"):** Cada técnica nova obriga o grupo a voltar às fases de dados (ex.: na Aula 4 volta-se ao entendimento visual; na Aula 5 volta-se à preparação para transformar texto e imagem em colunas numéricas/categóricas).
- **O que muda em 2026 com Agentes de IA e LLMs (CRISP-ML(Q)):**
  - Em todas as 6 fases, **a IA executa** (escreve código de checagem, limpeza, extração estruturada de texto/imagem, treino e interface web) e **o grupo humano decide e audita**.
  - Nasce a **7ª Fase — Monitoramento:** Depois que o modelo entra no ar, o perfil dos clientes muda (*data/concept drift*); a IA vigia o acerto no tempo e o grupo decide quando retreinar.

---

### 4. O Desafio Vitaliza: PDF do Case vs. Base de Dados Oficial
> **Regra de Ouro:** *"No trabalho de dados, vale a base. O PDF dá o contexto."*

| Dimensão | Business Case em PDF (Narrativa de Set/2025) | Base de Dados Oficial (`dados/brutos/` em `30/09/2026`) |
| :--- | :--- | :--- |
| **Assinantes Pagantes Ativos** | 27.901 pagantes | **14.753 pagantes ativos** (excluindo 60 contas internas `@vitaliza.com.br`; 64.948 contas cadastradas no total) |
| **Planos** | 1, 6 e 12 meses | **57% Anual** (R$ 299,90/ano ou R$ 239,90 no 1º ano com cupom) e **43% Mensal** (R$ 39,90/mês desde `01/03/2026`; era R$ 34,90) |
| **Perda Mensal (Churn)** | 10,2% ao mês | Média de **5,6%/mês em 2025** $\rightarrow$ subiu para **6,6%/mês em jan–set/2026** (pico de **8,1% / 1.154 saídas em abr/2026**; 5,9% em ago; 5,0% em set) |
| **Canais de Pagamento e Saída** | 71% das saídas pela tela do app | **70,2% pagam via Loja** (App Store `36,6%`, Google Play `33,6%` — taxa de 15%) e **29,8% via Site Web** (Cartão `20,3%` — taxa 3,5%; Pix Automático `9,5%` — taxa 0,99%) |

#### O Ponto Cego Estrutural das Lojas e as 4 Perguntas em Aberto
- **Por que a empresa enxerga tão pouco das saídas?**
  - **70% (App Store / Google Play):** O cliente cancela nas configurações do celular. A Vitaliza recebe apenas um evento técnico (`renovacao_automatica_desligada` e depois `assinatura_expirada`), **sem tela própria e sem pesquisa de motivo**.
  - **30% (Site Web — Cartão e Pix):** Passam pela tela de cancelamento da Vitaliza. A pesquisa de saída (`pesquisa_saida.csv`) só começou em `01/06/2026` e é opcional: de `3.389` saídas entre jun e set/2026, `2.271` foram em loja (sem pesquisa) e `1.118` no site (gerando `641` contas respondentes / ~10% a 19% das saídas totais).
- **As 4 coisas que a Vitaliza ainda não sabe:**
  1. *Por que a perda subiu em 2026?* (Reajuste de preço em `01/03/2026`? Mudança de mix de planos ou canais? Fim de ano de cupom?).
  2. *Por que cada assinante saiu?* (A pesquisa cobre só uma fração enviesada para Web).
  3. *Se a campanha A/B de `10/08/2026` funcionou:* `14.120` pagantes ativos foram sorteados em 4 grupos (`desafio`: 3.515; `cupom`: 3.472; `conteudo`: 3.554; `controle`: 3.579).
  4. *Quem vale a pena contatar:* O time de CS só atende **300 pessoas/mês** (R$ 18/contato) e o WhatsApp tem teto de **1.500 mensagens/mês** (R$ 0,40/msg), dentro do orçamento global de **R$ 40.000/mês**.

#### Definição Oficial de População e Alvo (Target) Preditivo
- **População elegível:** Assinantes pagantes ativos em **`30/09/2026`**, com **renovação automática ligada** naquela data (excluindo as 60 contas de teste `@vitaliza.com.br`).
- **Definição de Saída (Target = 1):** Em **`29/11/2026`** (60 dias após o corte), estar com a **renovação automática desligada** ou **sem assinatura ativa** (engloba desligamento voluntário da renovação, falha de pagamento não recuperada, reembolso e chargeback).

---

### 5. Arquitetura do Data Room: As 3 Formas de Dado e o Caso Júlia Almeida
O pacote de dados (`dados/brutos/`) contém 12 tabelas/logs + 1 pasta de imagens, divididos em 3 naturezas:

| Tipo de Dado | O que é | Arquivos no Data Room Vitaliza | Como vira variável para o modelo |
| :--- | :--- | :--- | :--- |
| **1. Estruturado (Tabela)** | Linhas e colunas fixas; **1 linha por pessoa ou vínculo**. | `usuarios.csv` (64.948), `assinaturas.csv` (32.643), `amizades.csv` (113.480), `campanha_ago26.csv` (14.120). | Juntar pela chave (`user_id`) e copiar/codificar a coluna. |
| **2. Semiestruturado (Log de eventos)** | **1 linha por evento ou mês**, com carimbo de tempo; uma pessoa aparece dezenas de vezes. | `eventos_assinatura.csv` (275.565), `pagamentos.csv` (165.548), `uso_mensal.csv` (591.662), `atividades.parquet` (1.254.475). | **Resumir/agregar por pessoa e janela temporal** (contagens, médias, tendências) antes de juntar. |
| **3. Não Estruturado (Texto e Imagem)** | Conteúdo em linguagem natural ou pixels, sem colunas prontas para o modelo. | `onboarding.csv` (63.929), `pesquisa_saida.csv` (643), `feed_posts.csv` (119.309), `tickets_suporte.csv` (4.422), `heatmaps_90d/` (25.473 imagens PNG). | **Extrair campos estruturados via LLM com schema tipado** (ou métricas de pixels) na Aula 5. |

#### Por que o Dado Não Estruturado Importa? O Caso Júlia Almeida (`user_id = u_2722f848`)
- **O que as tabelas estruturadas mostravam em `31/07/2026`:** Mulher, 36 anos, São Paulo, plano anual via Google Play (renovação em `27/11/2026`), ativa no app com 7 corridas em julho (`376 min`, nota média `4,4`). Um modelo treinado apenas em tabelas dava a ela **6% de risco de saída** (metade da média de 12,5% da base).
- **O que aconteceu:** **35 dias depois (`04/09/2026`), ela desligou a renovação automática.**
- **O que estava escondido nos textos e imagens:**
  1. `onboarding.csv`: *"Quero completar minha primeira meia maratona até julho"* (tinha um objetivo com data de validade!).
  2. `feed_posts.csv`: Em `28/07/2026` postou *"Terminei minha meia maratona! Meta batida"*; em `06/08/2026` reclamou de *"repetir o mesmo treino sem planilha nova"*; em `19/08/2026` relatou *"lesão no ombro, duas semanas parada"*.
  3. `heatmaps_90d/u_2722f848.png`: Mostrava voltas repetidas exatamente nos mesmos dois parques (saturação de rota).
- **Contexto competitivo real:** Concorrentes diretos atacaram exatamente essa dor de progressão de treino (o Strava lançou o *Athlete Intelligence* em out/2024 e comprou o app de planilhas de corrida *Runna* em abr/2025).

---

### 6. Fundamentos de IA: Hierarquia, Modelo vs. Algoritmo e Paradigmas
- **Hierarquia Conceitual:**
  - **Inteligência Artificial (IA):** Campo amplo de sistemas que realizam tarefas associadas à inteligência humana.
  - **Aprendizado de Máquina (*Machine Learning*):** Sistemas que aprendem padrões a partir de dados (**foco preditivo do módulo**).
  - **Aprendizado Profundo (*Deep Learning*):** Redes neurais com múltiplas camadas (visto na Aula 8).
  - **IA Generativa e LLMs:** Modelos treinados em grandes volumes para gerar texto, código e imagem (**usados no módulo como ferramenta de apoio** para codificação, extração de variáveis de texto/imagem com schema tipado na Aula 5 e redação de mensagens personalizadas na Aula 9).
- **Modelo vs. Algoritmo:**
  - **Algoritmo** é a *receita* (procedimento matemático que lê os dados de treino).
  - **Modelo** é o *bolo pronto* (a função ajustada que recebe um cliente novo e devolve uma previsão). *"Todo modelo erra; a pergunta é se ele é útil"* (George Box, 1976).
- **Os 4 Paradigmas de Aprendizado de Máquina:**
  1. **Supervisionado:** Aprende com exemplos que já têm a resposta/rótulo (`saiu` vs. `ficou`) $\rightarrow$ *Regressão Logística (Aula 6), Árvores de Decisão (Aula 7), Bagging e Boosting (Aula 8).*
  2. **Não Supervisionado:** Agrupa clientes semelhantes **sem usar rótulo de resposta** $\rightarrow$ *Clusterização / Segmentação (Aula 3).*
  3. **Por Reforço:** Aprende por tentativa, erro e recompensa em ambiente dinâmico *(fora do escopo do módulo).*
  4. **Autossupervisionado:** O próprio dado bruto serve de gabarito (ex.: esconder a próxima palavra do texto para ensinar LLMs).

---

## Aula 2 — Limpeza e Análise Exploratória de Dados (EDA) (`22/10/2026`)
**Fontes:** `materiais-aulas/Tech_M2_MBA_IA_Dados_Aula2.pdf` e `materiais-aulas/Tech_M2_MBA_IA_Dados_Aula2_Extra.pdf` (Prof. Cesar Almiñana)

### 1. O Caso do Faturamento de Setembro/2026 ("O Número Importa Menos que o Caminho")
Ao perguntar *"Quanto a Vitaliza faturou em setembro de 2026 em `pagamentos.csv`?"*, respostas sem alinhamento de regras variam de R$ 310 mil a R$ 4,06 milhões. A reconciliação oficial exige **4 filtros sequenciais**:

| Etapa de Limpeza Contábil em `pagamentos.csv` (Setembro/2026) | Valor Resultante | Regra de Negócio / Técnica Aplicada |
| :--- | :---: | :--- |
| **0. Soma bruta ingênua das transações de set/2026** | `R$ 509.588` | Inclui cobranças recusadas, estornos e chargebacks. |
| **1. Filtrar apenas status aprovado (sem estorno/chargeback)** | `R$ 499.503` | Exclui tentativas recusadas e valores devolvidos. |
| **2. Harmonizar fuso horário para Brasília (`UTC-3`)** | `R$ 499.402` | Lojas (`App Store` e `Google Play`) gravam em `UTC` (terminado em `Z`); Web (`Cartão` e `Pix`) grava em `UTC-3`. Uma compra às 22h de `30/09` em Brasília aparece como `01/10` em UTC! |
| **3. Expurgar cobranças aprovadas em duplicidade** | **`R$ 492.572`** *(Bruto)* | Retentativas aprovadas em dobro para a mesma assinatura no mesmo ciclo/dia devem ser removidas. |
| **4. Descontar taxas de intermediação de canal** | **`R$ 436.442`** *(Líquido)* | Desconta `15,0%` nas lojas (Apple/Google), `3,5%` no Web Cartão e `0,99%` no Web Pix Automático. |

---

### 2. Governança do Ambiente e Trabalho com Agentes de Código
- **Modelo vs. Harness:** O modelo (LLM) é o cérebro que raciocina e gera texto/código; o *harness* (Claude Code, Codex, Antigravity) é o ambiente que lê arquivos, roda scripts no terminal, aplica permissões e mantém regras persistentes (`AGENTS.md`), operando no ciclo **Planejar $\rightarrow$ Executar $\rightarrow$ Conferir**.
- **Regras Inegociáveis de Governança:**
- `dados/brutos/` **nunca é editado** (somente leitura). Dados limpos vão para `dados/processados/prata/` e produtos analíticos para `dados/processados/ouro/`.
  - `.gitignore` protege `dados/` e `.env`. Chaves de API nunca entram em notebooks, scripts, chat ou `AGENTS.md`.
  - **Rede de segurança Git:** Fazer `git commit` na branch de trabalho (`dev`) antes de cada etapa grande.
- **Anatomia de um Pedido Completo de Análise (5 Elementos):**
  1. **A Pergunta:** O que queremos descobrir.
  2. **Os Arquivos:** Quais tabelas/colunas entram.
  3. **As Regras:** Filtros de população, fuso horário, tratamento de nulos/duplicatas.
  4. **O Formato de Saída:** Tabela, gráfico, caminho do arquivo salvo.
  5. **O Critério de Pronto (*Definition of Done*):** Como validar que deu certo (sempre exigindo o plano antes de rodar).
- **Protocolo de Auditoria ("Conferir antes de acreditar" — 4 Passos):**
  1. Ler o código gerado (especialmente filtros `WHERE`/`query` e tipo de `JOIN`);
  2. Rodar de novo do zero para garantir reprodutibilidade;
  3. Checar **três números ou casos individuais à mão**;
  4. Confrontar o total com o dicionário de dados (ex.: `14.813` assinantes ativos brutos menos `60` contas `@vitaliza.com.br` = **`14.753` pagantes ativos oficiais**).

---

### 3. As 5 Dimensões da Qualidade de Dados e Achados Oficiais na Base Vitaliza
*(Referência: Wang & Strong, 1996; Redman, 2016)*

Toda inspeção de tabela na EDA deve passar pelas 5 dimensões abaixo. Diante de qualquer anomalia, **limpar é decidir entre 3 caminhos: Corrigir, Remover ou Marcar** — registrando sempre em `decisoes.md`.

| Dimensão | Pergunta-Guia | Achado Oficial na Base Vitaliza (`dados/brutos/`) | Armadilha / Cuidado Técnico |
| :--- | :--- | :--- | :--- |
| **1. Completude** | O que está vazio é opcional ou falha de coleta? | Em `onboarding.csv` (`63.929` linhas), `objetivo_texto` tem `5.467` vazios (`8,6%`, campo opcional), mas `nivel` (`7,1%` vazio) e `dias_por_semana` (`10,0%` vazio) também têm nulos não documentados como opcionais. | Nunca apagar linhas com nulos (`dropna`) sem antes verificar se a ausência de resposta é, por si só, um sinal comportamental de desengajamento. |
| **2. Validade** | Os valores respeitam limites físicos e de negócio? | Em `atividades.parquet` (`1.254.475` treinos):<br>• `574.835` têm `distancia_km` nula (são treinos *indoor* legítimos: força, yoga, etc.);<br>• Nos `679.640` com GPS, há **`951` treinos acima de 200 km** (o maior tem **`10.012,75 km`** em 160 min vindo do `apple_health`);<br>• Há **`3.649` treinos com duração igual a zero**. | Não confundir nulo legítimo (treino sem GPS = `NaN` em distância) com erro, nem permitir que os 951 erros de GPS destruam médias e correlações. |
| **3. Consistência** | A mesma coisa está escrita de dois jeitos? | Em `atividades.parquet`, existem **11 rótulos para 7 modalidades**: `corrida` / `run`, `caminhada` / `walk`, `forca` / `strength`, `pedal` / `ride` (além de `yoga`, `natacao`, `funcional`). Os rótulos em inglês somam **`376.930` treinos (30% da base)** e vêm 100% da origem `app`. | Filtrar apenas `tipo == 'corrida'` deixa **`162.108` corridas (`run`) de fora**! É obrigatório padronizar os rótulos antes de qualquer agregação. |
| **4. Unicidade** | O mesmo fato foi gravado duas vezes? | Em `atividades.parquet`, há **`9.383` pares de treinos duplicados** (mesmo `user_id`, modalidade equivalente, mesma duração/distância e início em até 5 min: um gravado pelo `app` e outro sincronizado pelo relógio): **`4.184` com `apple_health`** e **`5.199` com `garmin`**. | **Armadilha de fuso do Garmin:** O `garmin` grava o timestamp **3 horas à frente (`UTC`)**. Se deduplicar sem antes converter o fuso do Garmin para `UTC-3`, o código só encontra os 4.184 pares da Apple e deixa passar os 5.199 do Garmin! |
| **5. Temporalidade** | A regra de gravação mudou ao longo do tempo? | Em `uso_mensal.csv`:<br>• Em **2025**, usuário sem treino no mês **não gerava linha** (`dez/2025` tem `13.624` linhas e `0` linhas zeradas);<br>• A partir de **jan/2026**, usuário sem treino passou a gerar **linha explícita com zero** (`jan/2026` salta para `41.130` linhas, sendo `25.697` zeradas). | Comparar a média bruta de `uso_mensal.csv` entre 2025 e 2026 cria uma **queda falsa de `265 min` (dez/25) para `118 min` (jan/26)**. Olhando apenas quem treinou (`minutos > 0`), a média de jan/2026 foi de **`314 min`**! |

---

### 4. Granularidade, *Tidy Data* e a Regra "Juntar sem Multiplicar"
*(Referência: Hadley Wickham — Tidy Data, Journal of Statistical Software, 2014)*

- **Cada tabela tem uma unidade de análise (grão):**
  - Conta (`usuarios.csv` = `64.948` linhas);
  - Assinatura (`assinaturas.csv` = `32.643` linhas — uma conta pode ter mais de uma assinatura ao longo da vida);
  - Evento (`eventos_assinatura.csv` = `275.565` linhas);
  - Mês por conta (`uso_mensal.csv` = `591.662` linhas);
  - Treino individual (`atividades.parquet` = `1.254.475` linhas).
- **Erro Clássico de Multiplicação de Linhas (*Fan-out*):** Fazer `LEFT JOIN` direto de `usuarios.csv` (`64.948` contas) com `atividades.parquet` (`1.254.475` treinos) gera uma tabela de **`1.282.872` linhas**, inflando artificialmente qualquer contagem ou média de clientes muito ativos.
- **Regra Obrigatória:** **Primeiro agregar no grão do destino (`GROUP BY user_id`), depois juntar (`JOIN`)**, conferindo sempre se o número de linhas antes e depois do `JOIN` permaneceu exatamente `64.948` (sendo `36.551` contas com ao menos 1 treino e `28.397` contas sem treino).

---

### 5. Estatística Descritiva, Distribuições Assimetricas e Outliers na Vitaliza
*(Referências: Tukey, 1977; Diez et al., OpenIntro Statistics; McKinney, 2022)*

1. **Viés de Seleção Amostral ("Amostra que não foi sorteada engana"):**
   - Entre jun e set/2026 ocorreram `3.389` fins de assinatura (Google Play `36,2%`, App Store `30,8%`, Cartão `22,3%`, Pix `10,7%`).
   - Porém, nas `641` contas de `pesquisa_saida.csv`, **68,0% são de Cartão e 32,0% de Pix (0,0% de lojas!)**. Conclusões tiradas da pesquisa de saída descrevem o cliente Web, não os 67% que saíram pelas lojas.
2. **Centro e Dispersão em Distribuições Assimétricas (`uso_mensal.csv` em Setembro/2026):**
   - Das `56.565` contas registradas no mês, **72,3% (`40.880` contas) tiveram `0 minutos` de treino**.
   - **Moda:** `0 min` | **Mediana ($Q_2$):** `0 min` | **Média ($\bar{x}$):** `82,6 min` (~83 min).
   - **Desvio Padrão Amostral ($s$, dividido por $n-1$):** `221,3 min` | **Coeficiente de Variação ($CV = s / \bar{x}$):** **`268%`**.
   - *Lição analítica:* *"Quando a distribuição é muito assimétrica ou cheia de zeros, a média sozinha descreve uma conta que quase não existe."* Sempre reportar **mediana + IQR (ou separar `% de ativos no mês` e `média/mediana entre os que treinaram`)**.
3. **Comparando Dispersão em Escalas Diferentes pelo Coeficiente de Variação ($CV$):**
   - Em `atividades.parquet` (jan–set/2026), a **duração do treino** tem $\bar{x} = 46,4\text{ min}$ e $s = 23,8\text{ min}$, enquanto a **frequência cardíaca (`fc_media`)** tem $\bar{x} = 130,3\text{ bpm}$ e $s = 22,3\text{ bpm}$.
   - Os desvios absolutos são quase iguais (~23), mas o **$CV$ da duração é `51%`** e o **$CV$ da frequência cardíaca é apenas `17%`** (a duração varia três vezes mais em termos relativos).
4. **Quartis, IQR e o Risco de Cortar Outliers Cegamente:**
   - Nos `679.640` treinos com GPS: $Q_1 = 4,58\text{ km}$, Mediana $= 6,47\text{ km}$, $Q_3 = 9,58\text{ km}$, $IQR = Q_3 - Q_1 = 5,00\text{ km}$, $P_{99} = 57,64\text{ km}$.
   - Pela **regra de Tukey ($Q_3 + 1,5 \times IQR = 17,08\text{ km}$)**, `81.775` treinos (`12,0%`) seriam marcados como outliers. Porém, **`73.120` deles são treinos de ciclismo (`pedal`/`ride`)**, onde pedalar 20 a 60 km é perfeitamente normal!
   - Pela **regra do Z-score ($|z| > 3$, equivalente a $> 191,6\text{ km}$)**, caem `956` treinos (quase todos erros de GPS acima de 200 km).
   - *Regra de Ouro:* **Avaliar outliers dentro de cada modalidade** (`corrida` separada de `pedal`). *"A regra estatística marca; o grupo decide."*

---

### 6. Correlação ($r$ de Pearson), Confundimento e Vazamento Temporal (*Data Leakage*)

#### A. Sensibilidade do $r$ de Pearson a Erros de Dados
- O coeficiente $r$ de Pearson mede apenas **associação linear** (de $-1$ a $+1$).
- Nas corridas (`corrida` + `run`), se calcularmos a correlação entre `duracao_min` e `distancia_km` na base bruta, encontramos um **$r = 0,12`** (quase zero!).
- Ao remover apenas os **`555` treinos impossíveis com mais de 200 km**, a correlação salta para **$r = 0,88$**. *Uma fração minúscula de erros de GPS (0,1%) destrói completamente o cálculo de correlação.*

#### B. Correlação Espúria e Variável de Controle (Terceira Variável)
- Em `uso_mensal.csv` (`set/2026`, `15.685` contas que treinaram), a correlação entre `sessoes_app` (abrir o app) e `minutos` treinados é altíssima: **$r = 0,88$** (ou $r = 0,92$ incluindo quem não treinou).
- Seria tentador concluir que *"fazer o usuário abrir mais o app aumenta os minutos de treino"*.
- Porém, quando controlamos pela **quantidade de atividades realizadas no mês (`atividades`)** — calculando a correlação dentro de cada número exato de atividades ou via correlação parcial —, o coeficiente despenca para **$r = 0,02$**!
- *Explicação:* Quem faz mais atividades naturalmente abre mais o app e acumula mais minutos. Para um mesmo número de treinos, abrir mais vezes o app não adiciona minutos. *(Nota técnica: controlar usando faixas largas de atividades, como "1 a 5 treinos", não limpa o efeito e deixa a terceira variável vazar com $r$ entre 0,36 e 0,67).*
- **5 Explicações Alternativas obrigatórias antes de falar em causa:**
  1. *Comparação injusta de janela:* O plano mensal tem 12 janelas de saída por ano; o anual tem 1 janela no aniversário.
  2. *Autosseleção:* Quem compra o plano anual já tinha maior intenção prévia de permanecer.
  3. *Terceira variável (confundidor):* Preço, canal de pagamento e cupom mudam juntos.
  4. *Causalidade reversa:* O usuário parou de treinar porque já tinha decidido cancelar, ou decidiu cancelar porque parou de treinar?
  5. *Coincidência / flutuação amostral.*

#### C. Retrato vs. Histórico e Prevenção de Vazamento Temporal (*Data Leakage*)
*(Referência: Kaufman et al., 2012 — Leakage in Data Mining)*
- **O problema:** A tabela `assinaturas.csv` é uma **foto tirada em `01/10/2026`** (corte `30/09/2026`). Ela mostra o estado *final* de `renovacao_automatica`, não como a assinatura estava meses antes.
- **Prova empírica na base Vitaliza:** Se quisermos estudar quem estava ativo em `31/07/2026` olhando a foto de `assinaturas.csv`, veremos `2.250` assinantes com `renovacao_automatica = nao`. Porém, reconstruindo a linha do tempo real em `eventos_assinatura.csv` até `31/07/2026`:
  - Apenas **`1.427`** já estavam com a renovação desligada em `31/07`;
  - **`754`** ainda estavam com a renovação **ligada** em `31/07` (só desligaram em agosto ou setembro!);
  - **`69`** nem sequer eram assinantes em `31/07`.
- Usar a coluna de `assinaturas.csv` para estudar uma data passada introduz **vazamento do futuro (*data leakage*) em `823` assinantes (`37%` de erro)**.
- **Regra Técnica de Reconstrução Histórica:** Para qualquer corte no passado, o estado da assinatura deve ser reconstruído a partir de `eventos_assinatura.csv` até aquela data. *(Atenção: assinaturas iniciadas antes de `01/07/2024` não possuem evento de início no log; se não houver evento de desligamento até a data consultada, a renovação estava ligada).*

---

### 7. Rito de Prática em Equipe e Padrão de Entrega de Achados da EDA
- **Divisão de Papéis Sugerida no Grupo:**
  - **Piloto:** Formula o pedido estruturado (5 partes), revisa o plano e conduz o agente de código.
  - **Auditor:** Confere contagens de linhas antes/depois de `JOINs`, valida fusos/duplicatas e checa 3 casos individuais à mão.
  - **Relator:** Documenta cada escolha de limpeza em `decisoes/` e `decisoes.md` e sintetiza os achados para o relatório/deck.
- **Formato Padrão de Comunicação de cada Achado na EDA ("1 Tabela + 1 Gráfico + 3 Frases"):**
  1. **1 Tabela comparativa:** Grupos lado a lado com tamanho ($n$), taxa (%), centro (média e mediana) e dispersão (desvio padrão e IQR).
  2. **1 Gráfico limpo:** Distribuição, série temporal com marcos anotados ou boxplot comparativo.
  3. **3 Frases com números:**
     - *Frase 1 — O que o dado diz* (o fato quantificado com precisão);
     - *Frase 2 — O que o dado NÃO diz* (limitação, viés de seleção ou variável de controle necessária);
     - *Frase 3 — A próxima pergunta* (como esse achado guia a segmentação ou a modelagem).

---

### 8. Leituras de Referência da Trilha (`Tech_M2_MBA_IA_Dados_Aula2_Extra.pdf`)
1. **Diez, D.; Cetinkaya-Rundel, M.; Barr, C. D.** — *OpenIntro Statistics* (4ª ed., Cap. 2: *Summarizing Data*): média, mediana, quartis, desvio padrão, IQR, boxplots e efeito de assimetria/valores extremos.
2. **McKinney, Wes** — *Python for Data Analysis* (3ª ed., Cap. 7: *Data Cleaning and Preparation*): tratamento de ausentes, duplicatas, padronização de categorias e detecção/filtragem de extremos em `pandas`.
3. **Shaibu, T.** — *Média vs. Mediana: Saiba a Diferença* (DataCamp, 2024): guia rápido de quando preferir mediana e IQR a média e desvio padrão.
4. **Dubiella, I.** — *Estatística Descritiva: Conceitos e Métricas Principais* (Alura, 2025): revisão em português de medidas de posição e dispersão.
5. **Wickham, Hadley** — *Tidy Data* (*Journal of Statistical Software*, v. 59, n. 10, 2014): organização tabular onde cada variável é uma coluna, cada observação é uma linha e cada unidade observacional forma uma tabela.

---

*Nota de governança: Sempre que novos arquivos `Tech_M2_MBA_IA_Dados_AulaX.pdf` forem adicionados em `materiais-aulas/`, adicione uma nova seção correspondente abaixo mantendo a numeração e o padrão analítico deste guia.*

