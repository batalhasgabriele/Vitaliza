# Guia Consolidado — Aulas de Tecnologia (Módulo 2 MBA IA e Dados — Inteli)

> Atualização cruzada em 12/11/2026: inclusão de `Negócio_M2_MBA_IA_Dados_Aula4.pdf`. O resumo completo está na abertura de `resumo_aulas_negocios.md`; implicações técnicas e conteúdo da nova aula seguem abaixo. O enunciado atual usa setembro/2026 e 14.753 ativos; a comparação antiga com narrativa de 2025 mais abaixo é histórica, não descreve o PDF vigente.

## Integração da Aula 4 de Negócios — storytelling e personas
A aula (03/11/2026, Prof. Fábio Cássio-de-Souza) diferencia persona arquetípica de persona baseada em dados; exige avaliar separação e cobertura do churn e comunicar seis campos: setup, conflito, resolução, evidência, decisão e limite. O exemplo de Roberto demonstra que condição de entrada não mede efeito de mudança e que recortes pequenos não sustentam inferência. Cada atributo precisa de data de disponibilidade.

Para cada hipótese, produzir n, taxa de quem atende à regra, taxa do restante, diferença em pontos percentuais e cobertura das saídas. Combinar critérios pode aumentar separação e reduzir cobertura; nenhum dos dois substitui avaliação de incerteza. Personas devem nascer da análise, ter nome comportamental e não inferir biografia. Idade/gênero não são gatilho de ação. Efeito de uma ação deve ser formulado como hipótese testável, sem converter associação em causalidade. Frequência durante o desfecho e informações futuras de contrato precisam ser excluídas da previsão.

Formatos: mini deck técnico de 3–5 slides, cartão executivo por persona e relatório de 4–6 páginas. Cartão deve ser lido rapidamente, com número verificável, gatilho/ação e limite explícito. A tarefa final pede 3–4 personas com indicador de valor ao lado do churn; a aula seguinte cruza valor/risco (proteger, priorizar, manter, monitorar).

Aplicação técnica na ADR 020: construir atributos em cortes anteriores ao seguimento; ajustar transformações e clusters antes do desfecho; gerar tabelas e apresentação da mesma fonte; separar denominadores de coorte, carteira ativa e pessoa-tempo. Cinco slides e cartões preservam narrativa e evidência. A avaliação histórica de segmentos não substitui o modelo supervisionado da Semana 10.

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

## Aula 3 — Clusterização com k-Means (`29/10/2026`)
**Fonte:** `materiais-aulas/Tech_M2_MBA_IA_Dados_Aula3.pdf` (Prof. Cesar Almiñana — 107 slides) + Notas de Aula

> **Objetivos de Aprendizagem da Aula 3:**
> 1. Descrever a base pela qualidade, pela granularidade e pela estatística descritiva;
> 2. Explicar o k-means passo a passo e preparar/padronizar as variáveis que entram nele;
> 3. Avaliar um agrupamento por **quatro lentes**: **inércia**, **silhueta**, **estabilidade** e **leitura de negócio**;
> 4. Transformar *cluster* em *segmento*, com perfil em medianas, tamanho e consequência prática.

---

### 1. Governança de Código e Git para Experimentos de Modelagem (Slides 6–12)
1. **Git como Rede de Segurança ("Um commit antes de cada pedido grande"):**
   - Um commit é uma foto do projeto inteiro. Antes de cada comando grande ao agente, fazer um commit permite voltar à foto anterior caso o agente estrague algo (*Caso real citado: Replit, julho de 2025, onde o agente apagou o banco de produção por falta de ponto de volta e ambiente isolado*).
2. **Branch Dedicado e Worktrees (`cluster-v1`):**
   - A `main` (ou `dev` consolidada) preserva a base limpa e a análise exploratória intocadas; o experimento do k-means nasce num branch paralelo (`cluster-v1`) com um commit por passo.
   - Com `git worktree` (ex.: `claude --worktree cluster-v1`), cada branch pode ter sua própria pasta para dois agentes trabalharem em paralelo sem pisar um no outro.
3. **Pull Request (PR) e Papel do Auditor:**
   - O branch só volta para a branch principal via Pull Request revisado pelo **Auditor** do grupo (alguém que não escreveu o código lê, pergunta, confere contagens/sementes e aprova).

---

### 2. Capítulo 1 da Aula 3: Revisão da Descrição da Base (Slides 13–50)
*(Consolida na prática os conceitos da Aula 2 aplicáveis antes de agrupar)*
- **Detetive antes do Juiz (Tukey, 1977):** Análise exploratória (*o detetive*) procura o que os dados mostram; análise confirmatória (*o juiz*) testa o que já se suspeita. O agente acelera a parte mecânica (`Dado` $\rightarrow$ `Resposta`), mas escolher a `Pergunta` e julgar a `Pergunta seguinte` continua 100% com o grupo.
- **5 Dimensões da Qualidade (Wang & Strong, 1996) e Gabaritos Oficiais:**
  - *Completude (`onboarding.csv`):* `63.929` respostas; `objetivo_texto` tem `5.467` vazias (`8,6%`), todas nulas (opcional no dicionário junto com `como_conheceu`). Armadilha: `nivel` (`7,1%`) e `dias_por_semana` (`10,0%`) também têm vazios não marcados como opcionais.
  - *Validade (`atividades.parquet`):* `1.254.475` treinos (`679.640` com distância; os `574.835` sem distância não são erro, são treinos sem GPS). Mediana `6,47 km`; `951` acima de `200 km` (maior: `10.012,75 km`, pedal de 160 min do `apple_health`); `3.649` com duração zero (nenhum negativo).
  - *Consistência (`atividades.parquet`):* `11` valores para `7` tipos canônicos (`corrida`/`run`, `caminhada`/`walk`, `forca`/`strength`, `pedal`/`ride`). Os `376.930` nomes em inglês (`30%`) vêm todos da origem `app`. Contar só `corrida` deixa de fora `162.108` corridas (`run`).
  - *Unicidade (`atividades.parquet`):* `9.383` pares em dobro (mesma conta, tipo, duração e distância, início em até 5 min): `4.184` com `apple_health` e `5.199` com `garmin` (que grava 3h à frente em UTC).
  - *Temporalidade (`uso_mensal.csv`):* Em 2025 nenhum mês tem linha zerada (`dez/2025` tem `13.624` linhas); em `jan/2026` são `41.130` linhas (`25.697` com zero), derrubando a média aparente de `265` para `118` minutos (contando só quem treinou, `jan/2026` dá `314` min).
- **Granularidade e Junção ("Juntar sem multiplicar", Wickham, 2014):**
  - `usuarios.csv` (`64.948` contas) + `atividades.parquet` (`1.254.475` treinos): juntar direto gera `1.282.872` linhas repetidas; resumindo antes por `user_id`, mantém `64.948` linhas (`36.551` com treino e `28.397` com zero).
- **Amostra, Centro, Dispersão e Correlação:**
  - *Sorteio vs. Viés de Seleção:* 20 sorteios aleatórios de 500 contas em `set/2026` (`56.565` contas, $\mu = 82,6\text{ min}$) variam entre `60,2` e `109,5 min` (fixar a semente *fora* do laço!). Já a pesquisa de saída (`jun–set/2026`, `3.389` fins de assinatura: `36,2%` Google Play, `30,8%` App Store, `22,3%` Cartão, `10,7%` Pix) teve `641` respostas **100% Web** (`68,0%` Cartão e `32,0%` Pix; `0%` das lojas, que são `67%` dos fins).
  - *Centro e Posição (`set/2026`):* `72,3%` das contas têm zero treino $\rightarrow$ `mediana = 0 min`, `moda = 0 min`, `média = 82,6 min` ($p75 = 40$, $p90 = 284$, $p99 = 1.074$, máx `4.294 min`). *"A média sozinha descreve uma conta que quase não existe."*
  - *Desvio Padrão e CV (`set/2026`):* Base inteira tem $s = 221,3\text{ min}$ e $CV = 268\%$; só quem treinou (`15.685` contas) tem média `298 min`, mediana `173 min`, $s = 335,2\text{ min}$ e $CV = 112\%$. Em `atividades.parquet`, duração tem $CV = 51\%$ (`46,4 ± 23,8 min`) e frequência cardíaca tem $CV = 17\%$ (`130,3 ± 22,3 bpm`).
  - *Quartis e Extremos (`679.640` treinos com GPS):* $Q_1 = 4,58\text{ km}$, mediana $= 6,47\text{ km}$, $Q_3 = 9,58\text{ km}$, $IQR = 5,00\text{ km}$. Acima de $Q_3 + 1,5 \times IQR = 17,08\text{ km}$ há `81.775` treinos (`12,0%`), sendo **`73.120` de pedal** (`8.355` corrida, `300` caminhada). Por $|z| > 3$ (acima de `191,6 km`), há `956` treinos. *"A regra marca; o grupo decide."*
  - *Correlação e Terceira Variável:* Nas corridas, os `555` treinos impossíveis `> 200 km` derrubam o $r$ de `0,88` para `0,12`. Em `set/2026` (`15.685` contas ativas), `sessoes_app` $\times$ `minutos` tem $r = 0,88$ (`0,92` na base toda), mas controlando pelo número exato de `atividades` (ou $r$ parcial), cai para **`r = 0,02`** (faixas largas deixam a 3ª variável vazar com $r$ de `0,36` a `0,67`).

---

### 3. Capítulo 2 da Aula 3: CRISP-DM, Paradigmas de Aprendizado e o K-Means Passo a Passo (Slides 51–78)

#### A. O CRISP-DM no Módulo 2 (Chapman et al., 2000; Wirth & Hipp, 2000)
Ciclo iterativo de 6 fases que vão e voltam em torno dos Dados:
1. **Entendimento do negócio:** A pergunta e o critério de sucesso (*Aulas 1 e 10*);
2. **Entendimento dos dados:** Limpeza, descrição e exploração (*Aulas 2 e 4*);
3. **Preparação dos dados:** Integração, corte, rótulo e variáveis (*Aulas 2 e 5*);
4. **Modelagem:** Segmentos e modelos preditivos (*Aulas 3, 6, 7 e 8*);
5. **Avaliação:** Métricas e o desfecho real (*Aulas 3, 7 e 8*);
6. **Implantação:** O modelo disponibilizado na rotina da empresa (*Aula 9 · entrega final*).

#### B. Paradigmas de Aprendizado de Máquina (Hastie, Tibshirani & Friedman, 2009)
- **Supervisionado ("aprende com a resposta"):** Exemplos do passado já trazem o rótulo (`saiu` vs. `ficou`). Traça uma fronteira de decisão (*Regressão logística e árvores na Aula 6; Avaliação na Aula 7; Bagging e boosting na Aula 8*).
- **Não Supervisionado ("acha grupos sem resposta"):** Sem rótulo de quem saiu; os pontos parecidos se juntam sozinhos apenas pela distância (*Clusterização na Aula 3*).
- **Outros dois (para o mapa conceitual):** *Por reforço* (tentativa e recompensa — Sutton & Barto, 2018) e *Autossupervisionado* (o próprio texto vira gabarito: *"Quem treina não [cancela]"* — base dos LLMs).

#### C. Exemplo Didático: 12 Assinantes (`A` a `L`) Agrupados por Comportamento (Slides 58–59)
Olhando para `treinos/semana`, `% ar livre`, `dias parado` e `tempo de casa` (sem usar idade nem plano), 12 assinantes em `31/07/2026` se separam naturalmente em 4 perfis:
1. **Ativos, Ar Livre (`A, E, G`):** `2,1 a 3,4 treinos/sem`, `79% a 84% ar livre`, `0–1 dia parado`;
2. **Ativos, Fechado (`B, C, L`):** `1,1 a 2,4 treinos/sem`, `4% a 27% ar livre`, `0–7 dias parado`;
3. **Parados (`F, H, K`):** `0 treinos/sem`, `0% ar livre`, `200 dias parado`;
4. **Veteranos (`D, I, J`):** `2,4 a 3,3 treinos/sem`, alto tempo de casa.

#### D. As Três Decisões Humanas Antes do Algoritmo e a Geometria da Distância (Slides 60–64)
1. **Três decisões do grupo antes de rodar (e Hierarquia de Impacto):**
   - **(1) Quais variáveis (O fator de MAIOR impacto):** Cadastro ou comportamento? Cada escolha conta uma história diferente sobre as mesmas pessoas.
     > **Regras de Ouro sobre Escolha de Variáveis e Escopo da Semana 5 vs. Semana 10 (Destaques do Professor em Aula):**
     > 1. **Hierarquia de impacto:** O que mais impacta a qualidade da clusterização são as **variáveis escolhidas** para criar os clusters. O método específico de padronização importa menos — o fundamental é **SEMPRE lembrar de padronizar os dados quando houver diferença de escala**.
     > 2. **Foco da Entrega da Semana 5 (`13/11`) vs. Semana 10 (`18/12`):**
     >    - **Na Semana 5 (`13/11` — "Até a segmentação"):** O foco principal **não é prever/otimizar o churn**, e sim **criar ótimos clusters comportamentais** (bem separados, estáveis, interpretáveis pelas medianas e acionáveis, independentemente de explicarem ou não o churn neste primeiro momento; a taxa de saída histórica entra apenas como leitura descritiva de cada grupo formado).
     >    - **Na Semana 10 (`18/12` — "O modelo preditivo de saída"):** Aí sim o foco passa a ser selecionar as variáveis que mais explicam/impactam o churn para treinar, avaliar e disponibilizar o modelo supervisionado de saída.
     >    - **Os 3 pilares exigidos nas duas entregas de Tech:** (1) **Repositório** (código do grupo versionado), (2) **Documentação** (as decisões e o motivo de cada uma em `decisoes.md`) e (3) **Apresentação executiva** (o processo analítico e os insights).
   - **(2) O que é parecido:** Uma régua de distância entre dois assinantes (depende da unidade de cada variável).
   - **(3) Quantos grupos ($k$):** O algoritmo forma os grupos; quantos, o grupo decide.
2. **Objetivo do Agrupamento e Distância Euclidiana:**
   - **Objetivo:** Indivíduos próximos entre si dentro de cada grupo (baixa distância interna) e grupos distantes entre si (alta distância entre grupos).
   - **Distância Euclidiana:** $d = \sqrt{\Delta x^2 + \Delta y^2}$ (com 4 variáveis, é a mesma raiz com 4 diferenças ao quadrado: $\sqrt{\Delta x_1^2 + \Delta x_2^2 + \Delta x_3^2 + \Delta x_4^2}$). O K-Means só enxerga essa distância.
3. **Obrigação de Padronizar antes de Calcular a Distância Euclidiana:**
   - **O problema das escalas diferentes:** `Treinos por semana` vai de `0 a 6`; `Treinos ao ar livre` vai de `0 a 1`; `Tempo de casa` vai de `0 a 2.152 dias`. Na mesma régua, 1 treino/semana pesa igual a 1 dia de casa.
   - **Evidência empírica ("Sem padronizar, o tempo de casa decide sozinho"):** Com $k=4$ nas unidades originais, **`Tempo de casa` responde por `94,1%`** da separação (`Dias sem treino` `2,6%`, `Treinos/semana` `0,2%`, `Treinos ao ar livre` `0,2%`), criando apenas 4 faixas de antiguidade (`até 343d`, `338–876d`, `879–1.554d`, `1.552–2.152d`).
   - **Padronização Z-Score (`StandardScaler`):** Coloca cada variável em desvios-padrão a partir da própria média ($z = \frac{x - \text{média}}{\text{desvio}}$, tipicamente entre $-3$ e $+3$).
   - **Tratamento prévio de cauda longa (`decisoes.md`):** Aplicar `log` ou teto (*capping*) em variáveis de cauda longa (`dias sem treino`, `km`) antes do Z-score é decisão do grupo e deve ir para `decisoes.md`.

#### E. Funcionamento Interno do K-Means (Algoritmo de Lloyd, 1982) e seus Limites (Slides 65–78)
1. **Passo a Passo Iterativo (Exemplo de 240 assinantes e $k=3$):**
   - **Início:** Escolhemos $k=3$ e sorteamos 3 centros iniciais.
   - **Passo 1 (Atribuir):** Cada ponto é atribuído ao centro mais próximo (inércia inicial = `613,7`).
   - **Passo 2 (Mover):** Cada centro desliza para a **média** dos pontos que ficaram com ele.
   - **Volta 2 em diante (Repetir até convergir):** Com os centros no lugar novo, alguns pontos trocam de grupo e a inércia cai para `182,1`. O algoritmo repete até nenhum ponto trocar de grupo (na **volta 11**, para com inércia = `167,8`).
   - **Inércia:** $\text{inércia} = \sum \|x - c\|^2$ (soma das distâncias ao quadrado de cada ponto $x$ ao centro $c$ do próprio grupo). Ela nunca sobe entre uma volta e a seguinte.
2. **Mínimo Local, `k-means++` e Reprodutibilidade:**
   - **Mínimo local:** O algoritmo para onde não consegue melhorar, não necessariamente no melhor resultado global (30 sorteios iniciais nos mesmos 240 pontos geram 8 inércias finais diferentes, de `166,8` a `194,1`).
   - **`k-means++` (Arthur & Vassilvitskii, 2007):** Sorteia o 1º centro e escolhe os seguintes longe dos já escolhidos (converge em 7 voltas em vez de 11 e acha a menor inércia; é o padrão do `scikit-learn`).
   - **`n_init = 10` e `random_state = 0`:** Roda 10 sorteios independentes e guarda o de menor inércia; o `random_state` fixo deve ser registrado em `decisoes.md` para qualquer pessoa repetir o exato mesmo resultado.
3. **Dois Limites Estruturais do K-Means (Slide 76):**
   - **Valores extremos:** Um único treino de `10.013 km` puxa o centro do grupo para longe de todos (exige limpeza, teto ou log antes de agrupar).
   - **Variáveis binárias (`0/1`) e formato dos grupos:** Uma variável `0/1` padronizada pesa demais na distância euclidiana, forçando os grupos a coincidirem com a categoria binária. Além disso, o K-Means só enxerga grupos redondos (esféricos) em torno de médias.
4. **Como Ler o Resultado ("O k-means devolve um número; o perfil sai das medianas"):**
   - O algoritmo devolve apenas `Grupo 1, 2, 3...`. O perfil de cada grupo deve ser lido pelas **medianas nas unidades originais** (nunca em z-score!), e a **taxa de saída em 60 dias** — que o algoritmo nunca viu — é a **primeira leitura de negócio**.
5. **Quatro das Seis Etapas são Decisões do Grupo (Slide 77):**
   - `1. Escolher variáveis` (**Decisão**) $\rightarrow$ `2. Transformar (teto/log, 0/1)` (**Decisão**) $\rightarrow$ `3. Padronizar (StandardScaler)` (Código) $\rightarrow$ `4. Rodar KMeans (k=2..8, n_init=10, random_state=0)` (Código) $\rightarrow$ `5. Escolher o k` (**Decisão**) $\rightarrow$ `6. Registrar no decisoes.md` (**Decisão**).

---

### 4. Capítulo 3 da Aula 3: Avaliar o Agrupamento pelas Quatro Lentes (Slides 79–92)

Nenhuma métrica decide sozinha o número de grupos $k$; a escolha combina **4 lentes** e vai para o `decisoes.md`:

#### Lente 1 — Inércia e Método do Cotovelo (Slides 80–82)
- A inércia sempre cai quando $k$ aumenta (com $k = N$, cada ponto é seu próprio centro e a inércia é zero). Inércia menor não significa agrupamento melhor.
- **O Cotovelo:** É onde a curva dobra e o próximo grupo reduz pouco a inércia.
- **Números na base da Vitaliza (`11.688` pagantes ativos em `31/07/2026`, 4 variáveis padronizadas):**
  - $k=2$: `34.009` $\rightarrow$ $k=3$: cai `-9.940` $\rightarrow$ $k=4$: cai `-7.520` (para `16.549`) $\rightarrow$ $k=5$: cai `-4.331` $\rightarrow$ $k=6$: cai `-1.811`.
  - Na Vitaliza, **a dobra fica entre $k=4$ e $k=5$** (*"A inércia sugere; não decide"*).

#### Lente 2 — Coeficiente de Silhueta (Rousseeuw, 1987; Kaufman & Rousseeuw, 1990 — Slides 83–85)
- Compara a distância média do ponto ao próprio grupo ($a$) com a distância média ao grupo vizinho mais próximo ($b$):
  $$s = \frac{b - a}{\max(a, b)} \quad \in [-1, +1]$$
  - Perto de `+1`: bem colocado no próprio grupo; Perto de `0`: na fronteira entre dois grupos; `Negativo`: provavelmente no grupo errado.
- **Régua de Kaufman & Rousseeuw (1990):** Até `0,25` = sem estrutura substancial; `0,25 a 0,50` = estrutura fraca; `0,50 a 0,70` = razoável; acima de `0,70` = forte.
- **Números na Vitaliza (`11.688` pagantes):**
  - Em $k=2$, a silhueta é a maior (**`0,61`**, razoável), mas divide a base apenas no óbvio: *quem treina vs. quem parou*.
  - Em **$k=4$, a silhueta média é `0,44`** (faixa fraca/moderada na régua pura, mas separa 4 grupos que o negócio trata de forma distinta).

#### Lente 3 — Estabilidade por Reamostragem / Índice de Rand Ajustado (Hubert & Arabie, 1985 — Slide 86)
- **Como funciona:** Sorteia a base de novo com reposição (*bootstrap*, ex.: 5 a 10 reamostras), roda o K-Means novamente e compara cada partição com a original pelo **Índice de Rand Ajustado (`adjusted_rand_score`)**, onde `1,00` = idêntico à original e `0,00` = puro acaso.
- **Números na Vitaliza (10 reamostras):**
  - $k=3$: Rand médio = **`1,000`** (mín. `1,000`)
  - **$k=4$: Rand médio = `0,999` (mín. `0,998`)** $\rightarrow$ até $k=4$, os cortes se repetem quase sempre!
  - $k=5$: Rand médio = `0,970` (mín. `0,931`) e $k=6$: `0,984` (mín. `0,960`) $\rightarrow$ a partir de $k=5$, a partição começa a oscilar entre sorteios.

#### Comparação com Outras Réguas de Distância em $k=4$ (Slide 87)
- **Euclidiana ($\sqrt{\sum(x-y)^2}$ — escolhida na aula):** Eleva diferenças ao quadrado (diferença grande pesa muito). Separa nitidamente os **Parados (`28,6%` de saída)** e os **Veteranos (`5,5%` de saída)**, com estabilidade **Rand = `0,999`**.
- **Manhattan ($\sum|x-y|$ — K-Medianas):** O extremo pesa menos; divide o ar livre em intenso (`11,2%` saída) e leve (`14,6%`), mas **some com os veteranos** e derruba o Rand para `0,80`.
- **Cosseno ($1 - \cos(x,y)$):** Olha direção e não volume; tem maior silhueta (`0,56`), mas **mistura parados e veteranos**, achatando a saída de todos os grupos entre `11%` e `15%`.

#### Lente 4 — Leitura de Negócio: De Cluster a Segmento ($k=4$ na Vitaliza — Slides 88–92)
- **Gabarito de Referência da Aula (`k = 4` em `11.688` pagantes ativos em `31/07/2026`, medianas nas unidades originais e saída em 60 dias pós-corte, cuja média geral é `12,5%`):**

| Grupo | Nome de Negócio (Hipótese) | Assinantes ($n$) | Mediana `Treinos/Semana` | Mediana `Dias sem Treino` | Mediana `Tempo de Casa (Dias)` | Mediana `% Ao Ar Livre` | Saída Histórica em 60d (Média: `12,5%`) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Grupo 1** | **Parados** | `472` (`4,0%`) | `0,0` | `200` | `558` | `1%` | **`28,6%`** *(+129% acima da média)* |
| **Grupo 2** | **Ativos ao ar livre** | `5.927` (`50,7%`) | `2,0` | `2` | `207` | `81%` | **`13,9%`** |
| **Grupo 3** | **Ativos em ambiente fechado** | `4.215` (`36,1%`) | `2,0` | `2` | `212` | `15%` | **`10,7%`** |
| **Grupo 4** | **Veteranos** | `1.074` (`9,2%`) | `2,2` | `2` | `1.750` | `56%` | **`5,5%`** *(-56% abaixo da média)* |

- **Quando um Cluster vira Segmento ("Cluster vira segmento quando tem consequência" — Slide 91):**
  1. **Distinto:** O perfil se lê em uma frase e não se confunde com o vizinho (*ex.: Parados têm 200 dias sem treino*).
  2. **Estável:** Os cortes se repetem em outra amostra (*$k=4$: Índice de Rand `0,999`*).
  3. **Grande o bastante:** Vale uma ação própria (*`472` parados; `1.074` veteranos; nenhum grupo com meia dúzia de pessoas*).
  4. **Acionável:** A Vitaliza faria algo diferente com ele (*Parados: `28,6%` de saída*).
- **Decisão pelas 4 Lentes (Slide 92):** $k=4$ é o ponto ótimo porque atende simultaneamente **Inércia/Cotovelo ($\checkmark$)**, **Estabilidade ($\checkmark$)** e **Leitura de Negócio ($\checkmark$)**, enquanto $k=2$ só vence em Silhueta pura mas é pobre para o negócio.

---

### 5. Capítulo 4 da Aula 3: Rito Prático de 7 Passos e Auditoria Crítica (Slides 93–106)

1. **Os 7 Passos da Execução Prática:**
   - **Passo 1 — Escolher as variáveis:** As 4 variáveis base da aula (`treinos por semana nas 12 semanas até o corte`, `dias desde o último treino`, `tempo de casa em dias` e `% dos treinos ao ar livre [corrida, caminhada e pedal]`), mais até 2 variáveis adicionais escolhidas e justificadas pelo grupo. Salvar base original e padronizada (`StandardScaler`).
   - **Passo 2 — Padronizar:** Cada variável em desvios-padrão (`StandardScaler`), aplicando teto ou log antes se decidido pelo grupo.
   - **Passo 3 — Rodar de $k = 2$ a $8$:** Com `n_init = 10` e `random_state = 0` fixo, extraindo inércia e silhueta de cada $k$.
   - **Passo 4 — Ler as duas curvas:** Identificar onde a inércia dobra e onde a silhueta cai (`saidas/k.png`).
   - **Passo 5 — Estabilidade e perfis:** Rodar reamostragem com reposição (5 a 10 vezes) no $k$ escolhido e calcular `adjusted_rand_score` (média e mínimo, esperando $> 0,90$); gerar tabela com tamanho, medianas na unidade original e taxa de saída (`saidas/perfis.md`).
   - **Passo 6 — Registrar as decisões:** Documentar variáveis, escala, semente (`random_state`) e $k$ com o motivo em `decisoes.md`.
   - **Passo 7 — Nomear e abrir o PR:** Dar um nome e uma frase de negócio por grupo, defender o $k$ pelas 4 lentes numa frase e revisar pelo **Auditor** (que confere se os tamanhos somam a base, se cada grupo cabe numa frase e se outra semente gera os mesmos grupos).
2. **Dica Complementar de Prompt para Refinamento do Algoritmo:**
   > *"Quero separar k-grupos para separar minha base de uma forma otimizada e eficiente; e também quero que gere perguntas que podem ser feitas para melhorar o algoritmo (por exemplo: as variáveis escolhidas segregam bem os grupos?)."*
   - Sempre auditar se todas as variáveis escolhidas realmente mudam de mediana entre os grupos (poder de segregação), se há redundância/colinearidade ou se alguma variável binária/extrema está distorcendo a distância euclidiana.
3. **Referências Bibliográficas da Aula 3 (Slides 104–106):**
   - **Arthur, D.; Vassilvitskii, S.** (2007) — *k-means++: the advantages of careful seeding* (SODA).
   - **Chapman, P. et al.** (2000) / **Wirth, R.; Hipp, J.** (2000) — *CRISP-DM 1.0*.
   - **Hastie, T.; Tibshirani, R.; Friedman, J.** (2009) / **James, G. et al.** (2023) — *An Introduction to Statistical Learning with Applications in Python* (Cap. 12: *Unsupervised Learning / k-means*).
   - **Hubert, L.; Arabie, P.** (1985) — *Comparing partitions* (*Journal of Classification* — Índice de Rand Ajustado).
   - **Kaufman, L.; Rousseeuw, P. J.** (1990) — *Finding Groups in Data: An Introduction to Cluster Analysis* (Faixas da silhueta).
   - **Lloyd, S. P.** (1982) — *Least squares quantization in PCM* (*IEEE Transactions on Information Theory* — Algoritmo k-means).
   - **Rousseeuw, P. J.** (1987) — *Silhouettes: a graphical aid to the interpretation and validation of cluster analysis*.
   - **Soto, J. et al.** (2024) — *Sports center customer segmentation: a case study* (*arXiv:2405.17467*).

---

*Nota de governança: Sempre que novos arquivos `Tech_M2_MBA_IA_Dados_AulaX.pdf` forem adicionados em `materiais-aulas/`, adicione ou complemente a seção correspondente mantendo a numeração e o padrão analítico deste guia.*

