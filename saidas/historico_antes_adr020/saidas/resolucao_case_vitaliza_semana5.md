> HISTORICO SUPERADO PELA ADR 020. Contém resultados/interpretações não vigentes. Não usar na entrega.

# Resolução do Case Vitaliza — Semana 5

> **Documento mestre de leitura e continuidade**
> **Data de atualização:** 08/11/2026
> **Data de corte dos dados:** 30/09/2026
> **Branch da consolidação:** `dev` (versão inicial em `codex/plano-mestre-vitaliza`)
> **Status:** relatório de negócios e mini deck Markdown concluídos localmente. Validação suplementar e os três notebooks executados. Exportação para PDF/PPTX e submissão permanecem pendentes. Ver [QA e limites](qa_entrega_semana5.md).

## Fechamento executivo em 08/11/2026

Leia o [relatório executivo final](customer_segmentation_report_semana5.md), o [mini deck de oito slides](mini_deck_eda_semana5.md) e a [validação suplementar](validacao_semana5.md). Os três perfis publicados foram preservados. As personas distinguem comportamento observado de motivação hipotética. Propomos apenas um piloto controlado de até 400 elegíveis, com 200 e-mails e 200 controles, custo incremental de envio de R$ 2,00, ainda não executado.

**Correções de interpretação aplicáveis a todo este documento e às versões anteriores:** receita dos segmentos é mensal equivalente estimada, não faturamento de setembro ou receita em risco. AUCs da EDA são associações retrospectivas com janelas diferentes para quem saiu e quem ficou, não validação preditiva prospectiva. A curva por duração não é um estimador de sobrevivência com censura. A divergência de quatro perdas de abril continua sem causa reconciliada. Acessibilidade depende de elegibilidade de contato, não apenas do canal de cobrança.

Remover plano e canal preserva a estrutura (ARI 0,988). A variante compacta de quatro atributos alcança silhueta 0,336 no próprio espaço e ARI 0,931 frente à versão publicada, permanecendo candidata a evolução após auditoria de exposição temporal. Não transplantar a saída histórica do exemplo de julho da aula para as personas de setembro. Ainda não existe observação completa do churn em 60 dias destas personas.

## Como usar este documento

Para entender a engenharia que sustenta os resultados, começar pelo [mapa do pipeline](../notebooks/00_pipeline_etl_data_quality.md). Ele conecta contratos, linhagem, auditoria temporal, reconciliação e reprocessamento. A migração da EDA para Prata é validada contra baseline privada antes de publicar; evidência em `tabelas/qa_engenharia_dados.json` e ADR 017.

Este é o ponto de entrada para quem precisa entender o projeto sem ler primeiro todos os scripts, notebooks e decisões técnicas. Ele reúne:

- o problema de negócio;
- o caminho adotado para tratar e analisar os dados;
- os resultados já reproduzidos;
- a segmentação dos clientes ativos;
- as limitações;
- o mapa dos artefatos;
- as instruções para outro integrante ou outra IA continuar o trabalho.

Este documento é vivo e deve acompanhar o projeto. Ele não substitui os dois artefatos oficiais da Semana 5:

1. **Customer Segmentation Report**, da trilha de Negócios;
2. **EDA com código, visualizações e mini deck**, da trilha de Tecnologia.

Também não representa a resolução final da Semana 10. Modelo preditivo de churn, uplift individual, ROI completo e aplicação web pertencem à etapa futura.

---

## 1. Resumo executivo

A Vitaliza é um aplicativo brasileiro freemium de bem-estar, com treinos ao ar livre por GPS, vídeos guiados e recursos sociais. O desafio é construir uma arquitetura de retenção capaz de entender quem são os clientes, por que o churn aumentou e como priorizar ações sem desperdiçar orçamento ou abordar clientes que não responderiam positivamente.

No corte oficial de **30/09/2026**, a empresa possui:

- **64.948 contas cadastradas**;
- **14.753 assinantes pagantes ativos** após retirar 60 contas internas/cortesia;
- **12.503 ativos com renovação automática ligada**;
- **2.250 ativos com renovação desligada**;
- aproximadamente sete em cada dez pagantes nas lojas Apple e Google.

A reconstrução histórica observa churn médio de **5,68% ao mês em 2025** e **6,68% ao mês de janeiro a setembro de 2026**, com pico de **8,13% em abril/2026**. A referência executiva do case informa 5,6%, 6,6% e 1.154 perdas em abril; a reconstrução encontra 1.158. A diferença de quatro casos foi mantida e documentada, sem ajuste artificial.

Para a entrega da Semana 5, os 14.753 pagantes ativos foram agrupados sem usar churn ou informação de quem saiu. Foram encontrados três segmentos:

| Segmento | Clientes | Participação | Receita líquida mensal representada | Característica dominante |
|:---|---:|---:|---:|:---|
| **Ativos ao ar livre** | 7.457 | 50,55% | R$ 209.995,60 | Uso frequente, com 82,3% das atividades ao ar livre. |
| **Ativos guiados por vídeo** | 5.317 | 36,04% | R$ 152.203,80 | Uso frequente, com 92,2% das atividades em vídeo. |
| **Adormecidos sem hábito** | 1.979 | 13,41% | R$ 43.351,69 | Baixa regularidade, zero treino mediano em 30 dias e recência de 68 dias. |

O principal achado é que intensidade de uso separa claramente o grupo adormecido, enquanto o **modo de treino** separa os dois grupos ativos. A segmentação é muito estável, mas os grupos ativos apresentam sobreposição. Ela deve orientar hipóteses e comunicação, não ser tratada como um modelo de risco ou prova causal.

---

## 2. O problema que estamos resolvendo

### Pergunta executiva

Como a Vitaliza pode entender e organizar sua base de assinantes para preparar uma estratégia de retenção personalizada, financeiramente viável e respeitosa aos limites operacionais?

### Entrega da Semana 5

A Semana 5 é descritiva e diagnóstica. Ela deve:

1. carregar, limpar e auditar o data room;
2. explicar padrões relacionados ao churn e à subida de 2026;
3. investigar os marcos de março, junho e agosto;
4. construir três ou quatro segmentos sem usar a informação de saída;
5. transformar os segmentos em personas e hipóteses de drivers;
6. contar a história em um relatório executivo e um mini deck.

### O que fica para a Semana 10

- previsão de saída nos 60 dias posteriores ao corte;
- comparação de Regressão Logística, Árvores e ensembles;
- uplift individual e identificação de persuadíveis, garantidos, perdidos e “não perturbe”;
- racional financeiro completo com LTV, CAC, custos de contato, ofertas e IA;
- aplicação web preditivo-generativa.

---

## 3. Princípios que orientam a solução

### 3.1 Imutabilidade

`dados/brutos/` é a camada Bronze e nunca pode ser editada. Todos os tratamentos geram novos arquivos.

### 3.2 Arquitetura medalhão

```text
dados/brutos/                    Bronze: fontes originais, somente leitura
        ↓
dados/processados/prata/         Prata: tipagem, limpeza, deduplicação e harmonização
        ↓
dados/processados/ouro/          Ouro: feature stores, segmentos e métricas analíticas
        ↓
saidas/                          Relatórios, tabelas agregadas e gráficos
```

### 3.3 Uma fonte de verdade

Nenhum número final deve ser recalculado manualmente em uma planilha isolada. Relatórios e apresentações devem consumir as tabelas agregadas produzidas pelos scripts.

### 3.4 Proteção temporal

Somente informações observáveis até 30/09/2026 podem entrar nas análises. Em análises históricas, fatos também são limitados ao desfecho individual de cada assinatura.

### 3.5 Segmentação sem target

Churn, saída, pesquisa de saída, campanha, abertura, clique, renovação automática e demografia não participaram da formação dos clusters.

### 3.6 LGPD e minimização

Relatórios não publicam e-mail, texto livre, rota GPS, imagem ou identificador individual. Dados demográficos podem ser usados para auditoria de representação, mas não para determinar ofertas ou prioridade de atendimento.

---

## 4. Dados utilizados

O data room contém 12 fontes tabulares e dois pacotes de heatmaps.

| Domínio | Fontes principais | Uso no projeto |
|:---|:---|:---|
| Cadastro | `usuarios.csv`, `onboarding.csv` | Perfil cadastral, necessidade declarada e completude. |
| Contrato | `assinaturas.csv`, `eventos_assinatura.csv` | População, plano, canal e reconstrução histórica. |
| Receita | `pagamentos.csv` | Receita bruta/líquida, falhas e deduplicação de cobranças. |
| Uso | `uso_mensal.csv`, `atividades.parquet` | Frequência, recência, intensidade, modalidade e regularidade. |
| Social | `amizades.csv`, `feed_posts.csv` | Conexões, posts e curtidas. |
| Atendimento | `tickets_suporte.csv` | Volume e categoria de contato com suporte. |
| Pesquisa/experimento | `pesquisa_saida.csv`, `campanha_ago26.csv` | Motivos declarados e avaliação ITT da campanha. |
| Imagem | pacotes `heatmaps` | Auditados, mas ainda não usados na entrega da Semana 5. |

O inventário completo, com contagens, schemas, nulos e cobertura temporal, está em [`docs/source_inventory.md`](../docs/source_inventory.md).

---

## 5. Limpeza e preparação dos dados

### 5.1 População

- 64.948 usuários foram preservados na dimensão Prata;
- 60 contas `@vitaliza.com.br`/cortesia foram sinalizadas e excluídas da população pagante;
- 14.753 pagantes ativos formam a população oficial de segmentação.

### 5.2 Atividades

- 11 rótulos foram consolidados em sete modalidades canônicas;
- 376.930 atividades em inglês foram integradas às modalidades correspondentes;
- 9.383 pares app+relógio foram deduplicados após corrigir o fuso do Garmin;
- 3.649 atividades com duração zero foram excluídas do derivado válido;
- 951 distâncias acima de 200 km foram anuladas como erro de GPS, preservando as demais informações do treino;
- 574.835 treinos indoor sem distância foram preservados como nulos legítimos;
- 1.241.461 atividades válidas foram materializadas na Prata.

### 5.3 Datas e fusos

- eventos de lojas terminados em `Z` foram convertidos de UTC para `America/Sao_Paulo`;
- registros Web sem `Z` foram interpretados como horário de Brasília;
- fatos posteriores ao corte foram retirados dos derivados temporais;
- 119 cadastros futuros foram preservados na dimensão, mas receberam flag explícita.

### 5.4 Pagamentos

O fechamento de setembro foi reconciliado em cinco passos:

| Passo | Valor | Regra |
|:---|---:|:---|
| Todas as linhas de setembro | R$ 509.588 | Inclui todos os status. |
| Somente aprovados | R$ 499.503 | Remove recusas, estornos e chargebacks da receita. |
| Após harmonizar fuso | R$ 499.402 | Corrige pertencimento ao mês contábil. |
| Bruto deduplicado | R$ 492.572 | Remove 93 aprovações repetidas no mesmo dia/ciclo. |
| Líquido oficial | R$ 436.442 | Desconta taxas de Apple/Google, cartão e Pix. |

### 5.5 Completude

Campos ausentes do onboarding não foram apagados nem preenchidos com respostas inventadas. Foram criadas flags de preenchimento porque a ausência pode carregar sinal comportamental.

### 5.6 Registro completo

Cada regra, impacto, saída e evidência está documentada em [`docs/registro_limpeza_tratamento_dados.md`](../docs/registro_limpeza_tratamento_dados.md). Esse documento deve ser atualizado sempre que um tratamento mudar.

---

## 6. Análise exploratória e principais achados

### 6.1 Evolução do churn

![Churn mensal](churn_mensal_2025_2026.png)

- média de **5,68% ao mês em 2025**;
- média de **6,68% ao mês em jan–set/2026**;
- pico de **8,13% em abril/2026**;
- agosto encerra com aproximadamente 5,99% e setembro com 5,01%.

O aumento após o reajuste é uma associação observacional. Sazonalidade, composição da base e calendário de vencimentos mudam simultaneamente; não foi estimada elasticidade causal.

### 6.2 Marco de 01/03/2026 — reajuste

O plano mensal passou de R$ 34,90 para R$ 39,90. A média observada do churn mensal passou de **10,22% em jan–fev** para **12,97% em mar–abr** nesse plano. O dado sustenta uma hipótese de sensibilidade a preço, mas não prova que o reajuste causou a alta.

### 6.3 Marco de 01/06/2026 — pesquisa de saída

Entre junho e setembro foram observadas **3.389 expirações**:

- 2.271 nas lojas;
- 1.118 na Web.

A pesquisa possui 643 respostas e 641 respondentes únicos, todos Web. Portanto, os motivos declarados não podem ser generalizados para os clientes das lojas.

### 6.4 Marco de 10/08/2026 — campanha randomizada

| Braço | Sorteados | Churn em 30 dias | Diferença contra controle | p-valor |
|:---|---:|---:|---:|---:|
| Controle | 3.579 | 5,48% | 0,00 p.p. | — |
| Desafio | 3.515 | 5,18% | −0,30 p.p. | 0,576 |
| Cupom | 3.472 | 4,64% | −0,84 p.p. | 0,108 |
| Conteúdo | 3.554 | 6,13% | +0,66 p.p. | 0,235 |

Nenhum braço apresentou diferença estatisticamente significativa a 5%. Abertura e clique são pós-tratamento e não foram usados para selecionar participantes na análise principal.

### 6.5 Correlação não é causalidade

A correlação entre sessões no aplicativo e minutos treinados é 0,92 na base completa e 0,88 entre quem treinou. Após controlar pelo número de atividades, cai para aproximadamente **0,02**. Abrir mais o aplicativo não pode ser interpretado isoladamente como causa de mais minutos.

### 6.6 Outliers dependem do contexto

A regra global de Tukey marcaria 81.775 distâncias acima de 17,08 km como outliers, mas 73.120 são pedaladas. O resultado demonstra por que modalidades com escalas distintas não devem receber o mesmo corte automático.

Os detalhes estão em [`saidas/eda_e_hipoteses_vitaliza.md`](eda_e_hipoteses_vitaliza.md) e [`saidas/eda_etapa3_marcos_2026.md`](eda_etapa3_marcos_2026.md).

---

## 7. Segmentação dos pagantes ativos

### 7.1 Construção

A feature store possui uma linha por pagante ativo e consome exclusivamente a camada Prata. Foram utilizadas 16 variáveis relacionadas a:

- recência e frequência;
- tendência de uso entre D-30 e D-60;
- regularidade nos últimos três meses;
- diversidade e modo de treino;
- atividade social;
- tickets de suporte;
- tempo de casa;
- intensidade pretendida no onboarding;
- plano e canal.

Contagens assimétricas receberam `log1p`, extremos foram limitados no percentil 99 e todas as variáveis foram padronizadas. Foram comparados `k=3` e `k=4`; `k=5` foi mantido apenas como diagnóstico.

### 7.2 Escolha da solução

![Validação de clusters](segmentacao_validacao_k.png)

| k | Elegível | Silhouette | Davies–Bouldin | Estabilidade ARI | Menor grupo |
|---:|:---:|---:|---:|---:|---:|
| 3 | Sim | 0,164 | 2,007 | 0,998 | 13,41% |
| 4 | Sim | 0,160 | 1,898 | 0,954 | 12,95% |
| 5 | Diagnóstico | 0,167 | 1,784 | 0,786 | 8,70% |

Foi escolhido `k=3` por apresentar o melhor silhouette entre as soluções permitidas, estabilidade superior e grupos substanciais.

### 7.3 Perfis

![Perfis relativos](segmentacao_heatmap_perfis.png)

#### Ativos ao ar livre

- 7.457 clientes — 50,55% da base;
- receita líquida mensal equivalente: R$ 209.995,60;
- recência mediana: 2 dias;
- mediana de 10 treinos em 30 dias e 26 em 90 dias;
- 82,3% das atividades são ao ar livre;
- modalidade mais frequente: corrida;
- 9,47% estavam com renovação desligada no corte.

#### Ativos guiados por vídeo

- 5.317 clientes — 36,04% da base;
- receita líquida mensal equivalente: R$ 152.203,80;
- recência mediana: 2 dias;
- mediana de 10 treinos em 30 dias e 26 em 90 dias;
- 92,2% das atividades são vídeos;
- modalidade mais frequente: HIIT;
- 6,85% estavam com renovação desligada no corte.

#### Adormecidos sem hábito

- 1.979 clientes — 13,41% da base;
- receita líquida mensal equivalente: R$ 43.351,69;
- recência mediana: 68 dias;
- mediana de zero treino em 30 dias e um em 90 dias;
- regularidade média de apenas 12,3% nos três meses;
- 98,23% estão no plano anual;
- 59,63% estavam com renovação desligada no corte.

`renovacao_automatica` foi observada somente depois da formação dos clusters e não entrou no algoritmo.

### 7.4 Limitação estatística

![Projeção PCA](segmentacao_pca.png)

O silhouette de 0,164 é baixo. A PCA mostra que o grupo adormecido é relativamente distinto, mas os dois grupos ativos se sobrepõem bastante. A estabilidade elevada significa que o algoritmo repete a divisão; não significa que existam fronteiras humanas rígidas.

O relatório técnico completo está em [`saidas/segmentacao_etapa4.md`](segmentacao_etapa4.md).

---

## 8. Resolução de negócio até este ponto

### O que os dados permitem afirmar

1. A base ativa não deve receber uma única estratégia de retenção.
2. Existe um grupo de 1.979 assinantes sem hábito recente, com forte concentração de planos anuais e renovação desligada.
3. Os clientes ativos se dividem principalmente pela experiência de produto utilizada: ar livre/GPS ou vídeo guiado.
4. O aumento do churn em 2026 é real, mas o efeito causal do preço ainda não foi isolado.
5. A pesquisa de saída descreve clientes Web e não representa as lojas.
6. A campanha de agosto não oferece evidência suficiente para declarar um tratamento vencedor.

### Direções preliminares — ainda não são a priorização final

| Segmento | Direção a desenvolver na Etapa 5 | Cuidado principal |
|:---|:---|:---|
| Ativos ao ar livre | Monitorar manutenção do hábito e testar variedade de rotas, metas e progressão. | Não interromper uma experiência que já funciona. |
| Ativos guiados por vídeo | Trabalhar progressão, variedade e aderência de conteúdo. | Não presumir monotonia sem teste específico. |
| Adormecidos sem hábito | Avaliar reativação controlada, pausa ou conteúdo personalizado. | Risco de “acordar sleeping dogs”; contato deve ser testado, não disparado indiscriminadamente. |

Cartões de persona, hipóteses e piloto com orçamento estão concluídos no relatório executivo, seções 6 a 9.

---

## 9. Limitações e cuidados de interpretação

1. **Correlação não prova causa.** O reajuste e outros marcos coincidem com mudanças de composição e calendário.
2. **Pesquisa enviesada por canal.** Respondentes são 100% Web.
3. **Mudança de instrumentação.** Em 2025, usuários sem uso não geravam linha mensal; em 2026 passaram a gerar zeros.
4. **Snapshot não é histórico.** `assinaturas.csv` representa o estado final; cortes anteriores exigem reconstrução por eventos.
5. **Segmentação não é risco.** Clusters descrevem semelhança e não estimam probabilidade de saída.
6. **Segmentação não é uplift.** Um grupo aparentemente em risco pode não responder positivamente ao contato.
7. **Sobreposição entre ativos.** Ar livre e vídeo não formam fronteiras perfeitamente separadas.
8. **Heatmaps ainda não utilizados.** O pacote de julho possui cinco imagens acima do dicionário e permanece preservado para investigação futura.
9. **LGPD.** Textos, GPS, imagens e demografia exigem finalidade, minimização e revisão humana.

---

## 10. Estado atual da entrega da Semana 5

| Etapa | Status | Resultado principal |
|---:|:---:|:---|
| 1. Inventário e qualidade | Concluída | Bronze auditada e 12 materializações Prata. |
| 2. EDA Parte 1 | Concluída | Perfil, sobrevivência, ponto cego e hipóteses MECE. |
| 3. EDA Parte 2 | Concluída | Churn mensal, três marcos e controles estatísticos. |
| 4. Segmentação | Concluída | Três segmentos sobre 14.753 ativos. |
| 5. Relatório de negócios | Concluído localmente | Personas, hipóteses, priorização e orçamento documentados. |
| 6. Mini deck e QA | Pendente | Deve consolidar a história e validar todos os números. |

O painel operacional oficial é [`docs/plano_entrega_semana5.md`](../docs/plano_entrega_semana5.md).

---

## 11. Mapa de artefatos

### Documentos para leitura humana

| Arquivo | Para que serve |
|:---|:---|
| [`saidas/resolucao_case_vitaliza_semana5.md`](resolucao_case_vitaliza_semana5.md) | Documento mestre e manual de continuidade. |
| [`saidas/customer_segmentation_report_semana5.md`](customer_segmentation_report_semana5.md) | Artefato de Negócios em construção. |
| [`saidas/eda_e_hipoteses_vitaliza.md`](eda_e_hipoteses_vitaliza.md) | EDA consolidada e hipóteses. |
| [`saidas/eda_etapa3_marcos_2026.md`](eda_etapa3_marcos_2026.md) | Detalhamento dos marcos de 2026. |
| [`saidas/segmentacao_etapa4.md`](segmentacao_etapa4.md) | Relatório técnico da clusterização. |
| [`docs/registro_limpeza_tratamento_dados.md`](../docs/registro_limpeza_tratamento_dados.md) | Catálogo de todos os tratamentos. |
| [`decisoes.md`](../decisoes.md) | Índice dos ADRs e decisões. |

### Notebooks

| Notebook | Conteúdo |
|:---|:---|
| [`notebooks/00_gate_reprodutibilidade_bronze.md`](../notebooks/00_gate_reprodutibilidade_bronze.md) | Gate Bronze→Prata e números de controle. |
| [`notebooks/01_inventario_dados.ipynb`](../notebooks/01_inventario_dados.ipynb) | Inventário e qualidade. |
| [`notebooks/02_eda_e_hipoteses.ipynb`](../notebooks/02_eda_e_hipoteses.ipynb) | EDA e marcos. |
| [`notebooks/03_segmentacao_clusters.ipynb`](../notebooks/03_segmentacao_clusters.ipynb) | Segmentação e validação. |

### Scripts principais

| Script | Responsabilidade |
|:---|:---|
| [`src/auditar_bronze.py`](../src/auditar_bronze.py) | Inventário, contratos e hashes. |
| [`src/limpeza_qualidade_dados.py`](../src/limpeza_qualidade_dados.py) | Bronze→Prata. |
| [`src/processar_eda.py`](../src/processar_eda.py) | Feature store histórica da EDA. |
| [`src/analisar_eda_marcos.py`](../src/analisar_eda_marcos.py) | Churn e marcos de 2026. |
| [`src/segmentacao_clientes.py`](../src/segmentacao_clientes.py) | Feature store e clusterização dos ativos. |

### Saídas estruturadas

- `saidas/tabelas/churn_mensal_2025_2026.csv`;
- `saidas/tabelas/campanha_ago26_itt_30d.csv`;
- `saidas/tabelas/perfil_segmentos.csv`;
- `saidas/tabelas/metricas_clusterizacao.csv`;
- `saidas/tabelas/centroides_segmentos.csv`;
- `saidas/tabelas/metadados_segmentacao.json`.

---

## 12. Como reproduzir o projeto

Execute a partir da raiz do repositório, nunca dentro de `dados/brutos/`.

```powershell
$env:UV_CACHE_DIR='.uv-cache'

# 1. Testes
uv run --system-certs --with-requirements requirements-data.txt python -m pytest -q

# 2. Auditoria somente leitura da Bronze
uv run --system-certs --with-requirements requirements-data.txt python src/auditar_bronze.py

# 3. Materialização da Prata
uv run --system-certs --with-requirements requirements-data.txt python src/limpeza_qualidade_dados.py

# 4. Feature store e EDA histórica
uv run --system-certs --with-requirements requirements-data.txt python src/processar_eda.py
uv run --system-certs --with-requirements requirements-data.txt python src/gerar_graficos_eda.py

# 5. Churn e marcos
uv run --system-certs --with-requirements requirements-data.txt python src/analisar_eda_marcos.py

# 6. Segmentação
uv run --system-certs --with-requirements requirements-data.txt python src/segmentacao_clientes.py
uv run --system-certs --with-requirements requirements-data.txt python src/criar_notebook_segmentacao.py
```

### Números mínimos de conferência

Uma reprodução válida deve confirmar:

- 64.948 usuários;
- 60 contas internas;
- 14.753 pagantes ativos;
- 9.383 pares duplicados de atividades;
- 1.241.461 atividades válidas;
- R$ 492.572 de receita bruta deduplicada em setembro;
- R$ 436.442 de receita líquida em setembro;
- 14.753 linhas únicas na feature store de segmentação;
- segmentos com 7.457, 5.317 e 1.979 clientes;
- 11 testes aprovados na versão atual.

---

## 13. Protocolo de continuidade para colegas e IAs

### 13.1 Ordem obrigatória de leitura

Antes de alterar qualquer coisa:

1. leia [`AGENTS.md`](../AGENTS.md);
2. leia este documento;
3. consulte [`docs/plano_entrega_semana5.md`](../docs/plano_entrega_semana5.md);
4. consulte [`docs/registro_limpeza_tratamento_dados.md`](../docs/registro_limpeza_tratamento_dados.md);
5. consulte [`decisoes.md`](../decisoes.md) e o ADR relacionado à tarefa;
6. confira o script e a tabela estruturada que geram o número que será usado.

### 13.2 Regras que não podem ser quebradas

- nunca editar `dados/brutos/`;
- nunca trabalhar diretamente na `main`;
- não recalcular números finais fora da Prata/Ouro;
- não incluir churn ou saída na formação dos segmentos;
- não publicar dados pessoais ou amostras de texto/GPS;
- não alterar um número no relatório sem atualizar todos os artefatos impactados;
- atualizar o plano ao iniciar ou concluir uma etapa;
- registrar nova decisão técnica ou de negócio em ADR;
- atualizar o registro de tratamentos quando uma regra de dados mudar.

### 13.3 Formato recomendado para pedir trabalho a uma IA

Todo pedido deve especificar:

```text
Pergunta:
O que precisa ser respondido ou construído?

Arquivos:
Quais fontes, scripts e documentos são a fonte de verdade?

Regras:
Qual população, corte temporal, fuso, exclusões e proibições se aplicam?

Formato de saída:
Qual arquivo deve ser criado ou atualizado? Quais tabelas/gráficos são esperados?

Definition of Done:
Quais números, testes, links e validações provam que a tarefa terminou?
```

### 13.4 Checklist antes de entregar uma mudança

- [ ] A tarefa foi executada fora da `main`.
- [ ] A Bronze permaneceu intacta.
- [ ] Joins preservaram o grão esperado.
- [ ] O corte de 30/09/2026 foi respeitado.
- [ ] Não houve vazamento de target ou pós-tratamento.
- [ ] Testes passaram.
- [ ] Três números de controle foram conferidos.
- [ ] Plano, registro de tratamentos e ADRs foram atualizados quando aplicável.
- [ ] Relatórios e gráficos não divergem das tabelas estruturadas.
- [ ] Nenhum dado pessoal foi publicado.

---

## 14. Próximos passos objetivos

### Etapa 5 — concluída localmente em 08/11/2026

1. transformar os três segmentos em cartões de persona baseados somente em evidências;
2. formular hipóteses de drivers no formato ação + público + resultado esperado;
3. definir intervenção imediata, monitoramento e não perturbe;
4. distribuir preliminarmente canais dentro dos limites de 300 CS e 1.500 WhatsApps;
5. respeitar o orçamento mensal de R$ 40.000;
6. revisar limitações e LGPD;
7. finalizar o Customer Segmentation Report.

### Etapa 6 — mini deck e validação suplementar concluídos; empacotamento pendente

1. criar o mini deck;
2. aplicar o formato “1 tabela + 1 gráfico + 3 frases”;
3. executar QA cruzado de todos os números;
4. exportar relatório e apresentação;
5. organizar a pasta pública do Google Drive;
6. validar o link e submeter na Adalove.

---

## 15. Decisões centrais

- [ADR 001 — Imutabilidade da Bronze](../decisoes/001-politica-imutabilidade-dados-brutos.md)
- [ADR 003 — Faturamento de setembro](../decisoes/003-metodologia-faturamento-setembro-2026.md)
- [ADR 009 — Pipeline pelas cinco dimensões](../decisoes/009-pipeline-5-dimensoes-qualidade-aula2.md)
- [ADR 010 — EDA Parte 2 e marcos](../decisoes/010-eda-parte2-churn-marcos-2026.md)
- [ADR 011 — Segmentação dos pagantes ativos](../decisoes/011-segmentacao-pagantes-ativos.md)
- [ADR 014 — Arquitetura medalhão](../decisoes/014-arquitetura-medalhao-dados.md)
- [ADR 015 — Gate Bronze→Prata](../decisoes/015-gate-reprodutibilidade-bronze-prata.md)
- [ADR 016 — Registro consolidado de tratamentos](../decisoes/016-registro-tratamentos-dados.md)

---

## Conclusão

O projeto possui EDA documentada, três segmentos, personas, hipóteses, priorização e mini deck Markdown. A validação suplementar explicita separação baixa e incerteza experimental. Os três notebooks foram executados. Permanecem eventual exportação para formato de apresentação e publicação/submissão. Auditoria temporal adicional é necessária antes de promover a variante compacta ou afirmar desempenho prospectivo.

A regra para continuar é simples: **números vêm das tabelas estruturadas; interpretação vem dos documentos; decisões novas entram em ADR; e qualquer alteração deve permanecer reproduzível desde a Bronze.**
