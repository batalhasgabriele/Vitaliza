# Revisão de prontidão das entregas Vitaliza

> **Escopo após 12/11/2026:** Fechamento em 12/11: os ajustes autorizados desta revisão foram implementados na [ADR 020](../decisoes/020-consolidacao-temporal-semana5.md). Consultar [QA e limites restantes](../saidas/qa_entrega_semana5.md). A análise abaixo registra o diagnóstico anterior às correções.

Data: 12/11/2026. Autor: Codex, a pedido de Igor. Branch: dev. Commit examinado: `38961a7`.

## Pergunta e escopo

Verificar aderência ao enunciado e ao guia, qualidade dos artefatos, pendências e ordem de melhoria. Revisão documental, inspeção de código e gráficos, conferência agregada das bases existentes e execução dos testes. Não foram regenerados dados, clusters, gráficos ou relatórios. Este registro não aprova campanhas nem muda regras de negócio.

Critério de conclusão da revisão: separar requisito oficial, orientação das aulas, artefato existente e evidência de validação; registrar problemas verificáveis e recomendações. Não equivale à conclusão das correções ou à submissão da entrega.

## Fontes e requisitos oficiais

- [Guia de artefatos](../instrucoes-case/[Inteli%20MBA]%20Guia%20de%20Projeto%20-%20Entrega%20de%20Artefatos%20-%20Módulo%202%20(2026.2B).pdf): páginas 4–7, 10–13.
- [Enunciado](../instrucoes-case/Vitaliza%20-%20Enunciado%20do%20case.pdf): páginas 3–7.
- [Dicionário](../docs/Vitaliza%20-%20Dicionário%20de%20dados.pdf): snapshot de assinaturas e reconstrução histórica por eventos, páginas 3–6.
- [Resumo de Tecnologia](../docs/resumo_aulas_tecnologia.md), [resumo de Negócios](../docs/resumo_aulas_negocios.md) e [plano local](../docs/plano_entrega_semana5.md): complementam o guia, mas não substituem o texto oficial.

O guia fixa Semana 5 em 15/11/2026 às 23:59 e Semana 10 em 20/12/2026 às 23:59. Permite formato livre, exige pasta e arquivos públicos no Drive e envio individual do link na Adalove. A Semana 5 é formativa, sem nota. PDF e PPTX são recomendações de apresentação, não formatos obrigatórios.

O plano/resumos registram também datas de aulas de 13/11 e 18/12. Identificar como marcos de aula e distinguir dos prazos administrativos do guia; eventual alteração posterior deve ser confirmada na comunicação oficial da turma.

## Estado das entregas

| Semana | Área | Pedido | Evidência atual | Situação |
|---|---|---|---|---|
| 5 | Negócios | Relatório executivo com 3–4 personas | `saidas/customer_segmentation_report_semana5.md`, seções 3 e 6 | Existe em Markdown; três grupos empíricos, sem churn nas entradas |
| 5 | Negócios | Hipóteses de drivers | Mesmo relatório, seção 7 | Existem; aprofundar evidência, gatilhos e critérios de decisão |
| 5 | Negócios | Prioridade imediata vs. monitoramento | Mesmo relatório, seção 8 | Existe; piloto ainda proposto e não dimensionado para pequenos efeitos |
| 5 | Negócios | Visualizações e limitações | Mesmo relatório, seções 3, 5 e 9 | Existem; ressalvas não corrigem os erros preservados em outros documentos |
| 5 | Tecnologia | Código de carga, limpeza e EDA | `src/`, notebooks 01–03, Prata/Ouro e registro de tratamentos | Implementado; cadeia completa não reexecutada nesta revisão |
| 5 | Tecnologia | Padrões e correlações com churn | `saidas/eda_e_hipoteses_vitaliza.md`, `saidas/eda_etapa3_marcos_2026.md` | Parcial em qualidade: erros de interpretação e gráfico na EDA antiga |
| 5 | Tecnologia | Sustentação empírica da segmentação | `src/segmentacao_clientes.py`, `saidas/validacao_semana5.md` | Há comparação de k, estabilidade e sensibilidade; falta leitura histórica de saída por segmento em coorte temporal adequada, destacada nas orientações locais |
| 5 | Tecnologia | Mini deck | `saidas/mini_deck_eda_semana5.md` | Roteiro de oito slides com gráficos; não há apresentação exportada nesta versão |
| 5 | Ambas | Entrega pública | QA registra publicação pendente | Não verificada no Drive/Adalove nesta revisão; não tratar como entregue |
| 10 | Negócios | Plano de intervenção e ROI | Hipóteses e piloto preliminar | Plano final, política de contato por risco/efeito e modelo financeiro ainda pendentes |
| 10 | Tecnologia | Modelo supervisionado + aplicação web com API GenAI | Base de dados e segmentos como preparação | Não foram localizados modelo preditivo validado, aplicação ou integração de geração no código atual |

## Evidências verificadas nesta revisão

- `python -m pytest -q -p no:cacheprovider`, via ambiente de `requirements-data.txt`: **16 passed**, 21,12 s.
- Prata de assinaturas: 32.583 linhas; 14.753 ativas; 12.503 ativas com renovação ligada.
- Ouro de EDA: 32.583 linhas e 101 colunas.
- Ouro de segmentação: 14.753 linhas e 14.753 usuários distintos.
- Gráfico `ponto_cego_cancelamentos.png`: base de 17.830 cancelados, mas soma de fatias de 19.443; excesso de 1.613 cancelamentos involuntários.
- Inspeção visual também de `segmentacao_heatmap_perfis.png` e `segmentacao_pca.png`: perfis legíveis para anexo técnico; grupos ativos se sobrepõem na projeção. PCA mostra apenas parte da variância e não substitui métricas no espaço original.
- `git ls-files dados` inclui tabelas Prata/Ouro e cópias legadas fora das subcamadas. `usuarios_limpo.parquet` contém coluna de e-mail e `feed_posts_limpos.parquet` contém texto. O enunciado declara que os dados são fictícios; esta constatação é sobre escopo de publicação e coerência de governança, não uma afirmação de vazamento de dados reais.

Os registros de execução dos notebooks e da comparação/idempotência da EDA datam de 08/11. Foram lidos, não repetidos integralmente nesta revisão. Testes unitários aprovados não garantem validade das interpretações estatísticas.

## Melhorias em ordem de importância

### 1. Corrigir erros de análise que hoje aparecem como conclusões

**Local:** `src/gerar_graficos_eda.py`, aproximadamente linhas 143–205; `saidas/eda_e_hipoteses_vitaliza.md`, linhas 28 e 250.

O agrupamento por duração observada e média do indicador de cancelamento não estima sobrevivência nem a probabilidade de sair em cada ciclo. Não sustenta a afirmação de que quase oito em dez saem após 90 dias. Refazer por coortes e população em risco, com censura adequada, ou retirar essas conclusões da entrega.

A hipótese H3.1 exige taxa pelo menos duas vezes maior, mas usa 76,55%/79,29% contra 66,43% para declarar comprovação. Além de inadequadas para o estimando proposto, essas proporções não satisfazem o próprio limiar.

No gráfico de pizza, `lojas_sem + web_sem_pesq + pesq_web` já cobre toda a base; acrescentar `involuntario` duplica 1.613 casos. Substituir por categorias mutuamente exclusivas ou gráficos separados por canal e motivo. Rever cobertura da pesquisa no período em que ela existia: o enunciado informa 353 respondentes entre 3.389 saídas de junho a setembro, aproximadamente 10,4%; os 641 respondentes totais também incluem pessoas ainda ativas. A taxa histórica de 1,98% não mede cobertura desde o lançamento da pesquisa.

### 2. Definir consistentemente população, desfecho e janela

**Locais:** `src/analisar_eda_marcos.py:163`, relatórios e resumos de aulas.

Separar explicitamente expiração financeira, desligamento da renovação e alvo preditivo composto descrito nas orientações. A campanha atual mede apenas expiração em 30 dias em todos os sorteados. Isso é um estimando válido e limitado, mas não responde integralmente à resposta comportamental de anuais que desligaram a renovação e continuam com acesso. Não declarar ausência de efeito geral a partir desse resultado.

Reanalisar com desfechos separados e janela observável comum, comparar planos e perfis definidos antes da campanha, apresentar incerteza e tratar multiplicidade. Preservar ITT e não selecionar por abertura/clique. Um recorte elegível deve ser definido antes da atribuição. A base termina em setembro: não há 60 dias completos após 10/08.

### 3. Completar o vínculo histórico entre segmentos e saída

**Locais:** `saidas/customer_segmentation_report_semana5.md:9`, `saidas/qa_entrega_semana5.md`.

A ausência de futuro após setembro é uma limitação correta; ainda assim, é possível estudar uma coorte passada com 60 dias completos. Reconstruir estados e atributos numa data passada, formar grupos sem o target e só então medir saída futura. Não usar o snapshot atual como estado passado nem ajustar transformações ou clusters com informação futura para anunciar validação prospectiva. Descrever eventual análise retrospectiva com taxonomia atual como tal.

Entregar tabela por segmento com população, eventos, taxa, intervalo de confiança, plano e tempo de casa. Não escolher k para maximizar churn. A exigência de leitura histórica está nos complementos de aulas/plano, não explicitada com esse detalhamento na página 10 do guia.

### 4. Tornar a priorização de negócio mais justificável

O piloto de 200 e-mails e 200 controles, a R$ 2,00 de envio, é transparente e econômico, mas demonstra principalmente viabilidade. Não comprova retenção incremental pequena. É preciso explicar por que priorizar adormecidos em vez de mensais novos ou pessoas próximas à renovação.

Manter os três clusters como descrição; adicionar regras operacionais por plano, renovação ligada/desligada, vencimento e queda de uso. Incluir gatilho, elegibilidade, mensagem, mecanismo esperado, métrica, limiar de decisão e responsável. Os subgrupos operacionais não precisam ser novos clusters. Antes de ampliar, dimensionar amostra e distinguir comunicação experimental de serviço necessário.

### 5. Fechar exposição temporal e justificar a especificação de clusters

Há três grupos estáveis, mas silhouette de aproximadamente 0,164. A variante de quatro atributos tem aproximadamente 0,336 no próprio espaço e ARI de aproximadamente 0,931 frente à publicada. Isso motiva comparar simplicidade, interpretação e estabilidade temporal, sem promover automaticamente a maior silhueta entre espaços diferentes.

Definir 84 dias/12 semanas ou justificar 90 dias, distinguir observação antes da assinatura de uso pago e tratar entrantes com exposição curta. A auditoria existente registra 34.390 atividades anteriores à assinatura e 2.994 ativos com menos de 90 dias. Uso freemium pode ser legítimo e não deve ser eliminado sem definição do atributo.

### 6. Publicar uma narrativa única e um pacote apresentável

O aviso no topo da EDA antiga não resolve afirmações contraditórias no corpo, figuras e notebooks. Corrigir ou arquivar explicitamente versões substituídas e atualizar referências. O resumo de tecnologia ainda descreve o PDF como narrativa de setembro/2025 com 27.901 pagantes, enquanto o enunciado atual consultado informa 14.753 em setembro/2026.

Manter Markdown como fonte; recomendar relatório executivo em PDF/HTML e deck em PDF + PPTX/Slides, com revisão visual. Incluir legenda de população/janela/fonte, cartões de persona e decisões executivas. Não é obrigatório mudar de formato, mas o avaliador deve conseguir consumir a entrega sem montar ambiente Python ou abrir um editor.

### 7. Facilitar reprodução integral por outro colega

O teste de idempotência cobre a EDA; execução de notebooks sobre outputs prontos não equivale a Bronze → todos os artefatos. Criar entrada curta de reprodução, ambiente único coerente, comando de execução e verificação ponta a ponta em diretório isolado.

Há instrução no documento mestre para executar `src/gerar_graficos_eda.py` com `requirements-data.txt`, embora o script importe `seaborn`, declarado apenas em `requirements-notebooks.txt`. `requirements.txt` também diverge nas versões de pacotes presentes nos demais arquivos. Consolidar ou explicitar a finalidade e o ambiente suportado de cada arquivo.

### 8. Fechar reconciliações e publicação

Explicar a divergência de quatro perdas de abril (1.158 reconstruídas contra 1.154 do case) e confirmar a regra de duplicidade financeira por ciclo; a regra atual usuário/valor/dia é aproximação documentada. Não ajustar números para coincidir artificialmente.

Preparar lista explícita dos arquivos públicos. O repositório versiona dados processados apesar de textos que sugerem exclusão de dados. Como o case é fictício, isso não demonstra incidente; ainda assim, separar pacote executivo/agregado, dados de reprodução e histórico reduz ambiguidade. Não apagar histórico nem alterar compartilhamento sem instrução específica.

## Formato recomendado

- Negócios Semana 5: PDF/HTML com síntese, três cartões, evidências, hipóteses, priorização e limitações; Markdown mantido como fonte.
- Tecnologia Semana 5: repositório/código, notebooks, dependências, decisões, tabelas agregadas e instrução de reprodução; mini deck de oito slides em PDF e formato editável.
- Pasta pública no Drive com índice dos artefatos e link do código; testar abertura sem login; submissão individual do link na Adalove. Nenhuma dessas ações externas foi executada/verificada nesta revisão.
- Semana 10: relatório de intervenção + modelo financeiro auditável; modelo supervisionado avaliado temporalmente; extração de texto/imagem com avaliação de custo/qualidade; aplicação funcional com risco, decisão e geração personalizada. Não confundir essas pendências futuras com faltas obrigatórias da Semana 5.

## Referências metodológicas externas consultadas

- [Scikit-learn: prevenção de vazamento](https://scikit-learn.org/stable/common_pitfalls.html): separação de avaliação e ajuste de transformações. Aplicável à validação prospectiva, não uma proibição de ajustar clustering descritivo na população atual.
- [Gutierrez e Gérardy, PMLR: inferência causal e uplift](https://proceedings.mlr.press/v67/gutierrez17a.html): efeito incremental de uma ação é diferente de risco de saída.

## Encerramento desta revisão

O projeto cobre estruturalmente os artefatos da Semana 5 e tem boa rastreabilidade. Ainda não cabe atestar excelência: corrigir as conclusões e o gráfico, padronizar os desfechos, fortalecer a ligação histórica e a priorização, harmonizar documentos e verificar o pacote final. Os dados/modelos/resultados publicados permaneceram inalterados nesta revisão.

---

## Reavaliação após atualização — commit abfac49, 12/11/2026

Esta seção atualiza o diagnóstico acima, preservado como retrato do commit 38961a7. Foram revisados os commits be04895 e abfac49: inclusão da Aula 4 de Negócios, proposta de segmentação da base de 2026, alternativa k=3, scripts, tabelas, relatórios e ADRs 018/019. As ADRs seguem como propostas; não houve promoção da nova segmentação aos artefatos oficiais.

### Avanços que mudam a avaliação anterior

- Há uma alternativa concreta mais simples, com cinco atributos e três personas, além da segmentação oficial de 16 atributos.
- A população histórica é delimitada por cobertura de dados: 23.152 pagantes com vigência em jan–set/2026. Não corresponde a todas as 32.583 assinaturas históricas.
- O ajuste utiliza 21.024 pessoas com pelo menos 30 dias observados; 2.128 recebem classificação provisória. A proposta incorpora ex-clientes e mede frequência por exposição.
- Regularidade é calculada diretamente nos logs de treino de todas as origens, reduzindo dependência da cobertura de `uso_mensal`.
- As tabelas apresentam participação nas saídas, perfis por plano, sensibilidade a escala e quatro níveis de ação por renovação. Isso fortalece a discussão de negócio.
- Existe agora um relato de reprodução integral por Lorena em `saidas/base_inteira/pontos_de_atencao.md`, com hashes e métricas declarados iguais. Esse relato é evidência documental adicional, não execução independente desta revisão.
- A Aula 4 recomenda cartões com setup, conflito, resolução, evidência, decisão e limite; relatório de 4–6 páginas e mini deck analítico de 3–5 slides. São orientações de apresentação complementares ao formato livre do guia.

### Verificação independente desta atualização

Foi executada `segmentacao_base_inteira.construir()` e reproduzido em memória o K-Means k=3 com as cinco variáveis, parâmetros P99/log e StandardScaler da proposta, n_init=50 e seed=42. Nenhuma tabela foi sobrescrita.

| Controle | Resultado |
|---|---:|
| População e usuários únicos | 23.152 / 23.152 |
| Base de ajuste | 21.024 |
| Ativos: Ar Livre / Casa / Hábito Fraco | 7.514 / 5.419 / 1.820 |
| Saídas excluídas da base >=30 dias | 1.009 |
| Saídas usadas na taxa dessa base | 7.390 |
| Meses de exposição dessa base | 125.485,4954 |
| Ativos com renovação desligada reconstruída | 2.255 |
| Hábito Fraco anual com renovação desligada | 758 |
| Extremos de dias no grupo denominado evento recente ±60 | −60 / +30 |

Não foram repetidos os experimentos completos de robustez nem a geração financeira; suas métricas permanecem resultados publicados pelos scripts da proposta. Os testes existentes não foram modificados nos novos commits; a aprovação anterior de 16 testes não deve ser apresentada como cobertura específica dos novos cálculos.

### Pendências prioritárias atualizadas

1. **Unificar a versão de entrega.** Há três linhas coexistindo: oficial k=3/16 atributos, proposta k=4 e proposta k=3/5 atributos. O relatório k=4 está desatualizado: informa 23.151 pessoas e silhueta 0,206, enquanto `_meta.json` registra 23.152 e 0,187; os tamanhos das personas também diferem das tabelas. A própria ADR 019 reconhece a defasagem. O novo deck k=3 tem racional e tabelas, mas não foi localizado o arquivo da apresentação de sete slides. Não enviar versões conflitantes como uma entrega única.

2. **Distinguir taxa por pessoa-tempo de churn mensal.** `src/personas_k3_deck.py:44` divide saídas pela soma de meses observados. Isso é uma taxa de incidência por assinante-mês, não a métrica oficial de perdas do mês / ativos no início do mês, nem probabilidade de sair no mês. A taxa global de 5,89 e os 43,98 dos mensais de Hábito Fraco não devem ser comparados diretamente a 6,68% ou usados como probabilidades. O recorte >=30 dias elimina 1.009 saídas precoces dessas taxas; medir o tamanho desse viés e apresentar também resultados para população completa com exposição adequada.

3. **A validação temporal segue pendente.** `src/segmentacao_base_inteira.py:62` encerra atributos na data de saída dos cancelados e no corte dos ativos. Não há coluna churn no K-Means, mas a janela de atributos depende do desfecho. É uma descrição retrospectiva válida com ressalvas, não uma validação de sinais disponíveis numa data anterior à saída. Incluir ex-clientes amplia a pergunta; não torna automaticamente incorreta a segmentação da carteira atual nem resolve a previsão histórica. Para leitura prospectiva, construir cortes comuns anteriores ao desfecho.

4. **Corrigir a hipótese de objetivo com prazo.** Em `src/segmentacao_base_inteira.py:166`, a distância ao evento é medida contra a saída para cancelados e contra setembro para ativos; isso dificulta interpretar diferenças como risco comparável. Além disso, a faixa chamada ±60 é de −60 a +30. Corrigir o rótulo/regra, validar manualmente o extrator e testar a relação com janelas anteriores ao desfecho. A afirmação de que clientes saem porque o objetivo acabou excede a evidência. Menção por regex a prova/meta também não comprova que a meta foi cumprida.

5. **Reconciliar a campanha antes de adotar a oferta.** A nova sensibilidade usa `data_fim` e limite inclusivo; a oficial usa eventos de expiração e limite exclusivo. Até a janela de 30 dias muda (controle 5,70% vs. 5,48%). Separar efeito da janela, definição e elegibilidade. A tabela nova também mostra cupom significativo sem restringir aos que renovam até setembro: −1,91 p.p., IC95 [−3,24; −0,59]. Portanto, o notebook 11 erra ao dizer que só há significância no subconjunto elegível. O efeito de −3,98 p.p. mistura mensais e anuais: não deve ser chamado de efeito exclusivo de um mês grátis. Manter sensibilidades exploratórias, elegibilidade pré-tratamento, incerteza e multiplicidade explícitas.

6. **Tratar o impacto financeiro como cenário, não retorno demonstrado.** A redução de 97,2 saídas/mês soma premissas de eficácia de 20–30%, sem deduplicar públicos potencialmente sobrepostos. R$ 384.588 é calculado atribuindo 12 meses de receita a todos os clientes supostamente retidos ao longo de 12 meses: explicitar se é valor anualizado da carteira acumulada ou receita realizada no primeiro ano. CAC evitado depende de realmente evitar aquisições de reposição. Faltam sobrevivência futura, custo de servir, contatos, ofertas e IA na conta de retorno. Não foi localizado no script o detalhamento que reproduz os orçamentos de R$ 17.651 e R$ 24.833 declarados no notebook. Os 758 anuais foram confirmados, mas estão fixos no código e devem ser derivados da base.

7. **Não transformar cautela em classificação causal.** Os 760 anuais de Hábito Fraco com renovação ligada podem receber a regra operacional de não fazer campanha proativa. Isso não comprova que contato causaria sua saída nem identifica individualmente sleeping dogs. Preservar atendimento e explicitar a natureza da regra.

8. **Corrigir os problemas antigos ainda presentes.** `gerar_graficos_eda.py`, a EDA antiga e os relatórios oficiais não mudaram desde a revisão anterior. Permanecem o gráfico com sobreposição de categorias, a interpretação incorreta de sobrevivência e a hipótese declarada comprovada sem atingir o próprio critério. A nova taxa de saída em três meses usa uma coorte com acompanhamento mínimo e é um avanço, mas não substituiu nem corrigiu a narrativa antiga.

9. **Atualizar documentação e testar os novos cálculos.** Os resumos das aulas não foram atualizados após a inclusão da Aula 4, contrariando AGENTS.md. Reconciliar 2.255 renovações desligadas por eventos contra 2.250 do snapshot; não forçar igualdade sem explicar a diferença. Acrescentar testes focados em janelas, limites de datas, população/exposição, atribuição provisória e consistência relatório-tabela. A sensibilidade forte a RobustScaler/ausência de log e o bootstrap com pré-processamento fixo devem permanecer como limites.

### Parecer atualizado

Há progresso real na parcimônia, cobertura histórica e acionabilidade. A proposta k=3 de cinco atributos merece ser candidata à consolidação, mas não deve ser promovida só pela silhueta: população, período e espaço de atributos diferem da versão anterior. A entrega ainda exige corrigir métricas e interpretações e escolher uma única versão coerente. O problema principal deixou de ser falta de propostas; passou a ser sua validação e integração. Exportação, publicação e submissão externa continuam não verificadas.
