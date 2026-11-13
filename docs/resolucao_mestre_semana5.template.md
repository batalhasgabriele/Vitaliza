# Resolução mestre do case Vitaliza — Semana 5

**Leitura consolidada de negócios e tecnologia.** Corte dos dados: 30/09/2026. Versão metodológica: ADRs 020 e 021. Este documento explica o problema, o caminho analítico, os resultados e a decisão proposta. Os números pertencem à consolidação atual; as versões anteriores permanecem no histórico do projeto.

## 1. Resposta executiva ao desafio

### Atendimento explícito ao guia da Semana 5

O problema central é o **churn: a perda de assinantes e os sinais de descontinuidade da assinatura**. Os segmentos organizam a investigação desse problema. Este quadro mostra onde cada requisito é respondido na própria resolução.

| Área | Requisito do guia | Resposta nesta leitura |
|---|---|---|
| Negócios | 3–4 segmentos com cartões de persona | Seção 7: três personas, tamanho, comportamento, tensão, ação e limite |
| Negócios | Hipóteses de drivers de churn por segmento | Seção 7.4: matriz de hipóteses, evidências, lacunas e testes |
| Negócios | Priorização imediata versus monitoramento | Seção 10: públicos, gatilhos e ações preliminares |
| Negócios | Visualizações da EDA | Gráficos incorporados nas seções 5, 7, 8 e 9 |
| Negócios | Limitações da análise | Seção 12 e limites junto de cada achado |
| Tecnologia | Código para carregar, limpar e visualizar | Seções 4 e 15: engenharia, código e reprodução |
| Tecnologia | Padrões e correlações com churn | Seções 5 e 8: período, plano, comportamento e diferenças de saída; seção 9: campanha |
| Tecnologia | Gráficos gerados pelo código | Seção 5.4: ligação entre pergunta, evidência e implementação |
| Tecnologia | Sustentar empiricamente a segmentação | Seções 6–8: atributos, escolha de k, estabilidade, perfis e avaliação histórica |
| Tecnologia | História analítica em mini deck | Seção 15: sequência dos cinco slides e acesso ao artefato |

As hipóteses são **explicações candidatas para churn**, não causas comprovadas. Associação histórica ajuda a priorizar investigação, mas não demonstra, sozinha, que uma ação reduzirá perdas.

A Vitaliza precisa entender por que seus assinantes deixam de perceber valor no serviço e organizar uma estratégia de retenção que possa ser testada. A resolução da Semana 5 é dividir a carteira atual em três perfis comportamentais, verificar como perfis semelhantes se relacionaram com a saída em um período histórico e propor ações coerentes com as evidências disponíveis.

Encontramos **6.797 integrantes no perfil Atleta ao Ar Livre, 5.109 no perfil Treino em Casa Guiado e 2.847 no perfil Hábito Fraco**, totalizando os **14.753 pagantes ativos** no corte. O perfil de hábito fraco apresentou a maior taxa de saída composta na avaliação histórica, mas os outros perfis responderam pela maior parte das saídas em números absolutos. Portanto, priorizar retenção exige olhar conjuntamente comportamento, estado da assinatura e tamanho do público.

A recomendação é começar pelo diagnóstico de quem desligou a renovação, distinguir assinantes mensais com dificuldade de formar hábito dos demais públicos e testar ações pequenas antes de ampliar investimentos. O estudo não comprova o motivo individual da saída nem o retorno de uma campanha futura. Essa distinção orienta toda a resolução.

## 2. Empresa, problema e escopo da entrega

A Vitaliza é um aplicativo freemium brasileiro de bem-estar, com treinos ao ar livre, vídeos e recursos sociais. No retrato oficial, há **64.948 contas cadastradas** e **14.753 assinantes pagantes ativos**. A média de churn informada pelo enunciado aumenta de 5,6% ao mês em 2025 para 6,6% entre janeiro e setembro de 2026. Esse aumento torna necessário entender os padrões de uso e as diferenças entre clientes antes de escolher uma intervenção.

O plano mensal passou de R$ 34,90 para R$ 39,90 em 01/03/2026. O plano anual custa R$ 299,90, com possibilidade de preço promocional no primeiro ano. Além do preço, plano, canal de pagamento, tempo de relacionamento e frequência de treino podem influenciar a leitura dos dados. Um contrato anual, por exemplo, pode manter o acesso de alguém que já desligou a renovação futura.

A Semana 5 pede dois artefatos conectados: um relatório de segmentação com três ou quatro personas, hipóteses, prioridade e limitações; e uma EDA com código, visualizações e mini deck. Modelo supervisionado, aplicativo com IA generativa e ROI final são entregas da Semana 10. Esta resolução chega até a segmentação e a formulação de uma estratégia preliminar de aprendizado.

## 3. Quais dados foram usados e por que existem populações diferentes

### Definição de churn e dos sinais relacionados

| Medida | Definição e denominador | Uso na resolução |
|---|---|---|
| Churn mensal por expiração | Expirações no mês ÷ ativos no início do mês | Subida de 2026 e reajuste; não é uma coorte fechada, pois pode incluir perdas de entradas do próprio mês |
| Renovação desligada | Estado da renovação futura desligada no corte, mesmo com acesso ativo | Sinal para diagnóstico; não equivale a perda financeira já realizada |
| Saída composta em 60 dias | Sem acesso **ou** renovação desligada ao fim, entre ativos com renovação ligada no início | Comparação histórica dos perfis em horizonte comum |
| Expiração em 30 dias na campanha | Sorteados com expiração na janela ÷ todos os sorteados no braço | Comparação principal por intenção de tratar |

Logo, **23,70% de saída composta no perfil Hábito Fraco em julho não significa 23,70% de churn mensal**, nem previsão desse percentual para setembro. Toda taxa deve ser acompanhada de desfecho, horizonte e população.

### Fontes e populações

O data room reúne usuários, assinaturas, eventos de assinatura, pagamentos, uso mensal, atividades, onboarding, amizades, publicações, suporte, pesquisa de saída e campanha de agosto, além dos arquivos de mapas de calor. Cada fonte responde a uma pergunta diferente: pagamentos ajudam a calcular receita; atividades descrevem comportamento; eventos reconstroem o estado contratual; campanha permite comparar grupos sorteados.

As populações não são intercambiáveis:

| População | Papel na resolução |
|---|---|
| 64.948 contas cadastradas | Contexto geral, incluindo usuários gratuitos |
| 32.583 usuários da base histórica de EDA | Exploração de assinaturas após o tratamento das contas internas; inclui históricos que já saíram |
| 14.753 pagantes ativos em setembro | Carteira atual que recebe os segmentos e a priorização preliminar |
| 11.685 ativos com renovação ligada em julho | Público da avaliação histórica primária de saída composta em 60 dias |
| 14.120 sorteados na campanha de agosto | Público da comparação principal da campanha |

Quem já saiu não foi apagado da análise. Essas pessoas aparecem na EDA, nas coortes e nos desfechos históricos. A segmentação atual usa os ativos porque descreve a carteira sobre a qual uma ação de retenção poderia ser planejada no corte. Misturar antigos clientes com ativos em uma única contagem dificultaria interpretar o tamanho de cada público operacional.

## 4. Engenharia de dados: como a base se tornou confiável

O projeto adota arquitetura medalhão. A camada **Bronze**, em `dados/brutos/`, conserva os arquivos originais. A **Prata** guarda tabelas tratadas e padronizadas. A **Ouro** organiza atributos, segmentos e métricas para consumo analítico. Todo resultado deve poder ser reconstruído a partir da origem.

O trabalho de ETL inclui leitura das fontes, exclusão das contas internas do universo de clientes, padronização de modalidades, tratamento de atividades inválidas e duplicadas, conversão de valores monetários e harmonização de horários para Brasília. Treinos indoor sem GPS são preservados: falta de GPS nessa modalidade não significa necessariamente erro. Distâncias devem ser interpretadas por modalidade; aplicar o mesmo limite a corrida e ciclismo pode remover observações legítimas.

Na receita, cobranças aprovadas duplicadas pela regra de usuário, valor e dia são sinalizadas para evitar contagem em dobro. Essa regra é uma aproximação do ciclo de cobrança e continua documentada como limitação. Nas junções, as tabelas são agregadas na granularidade adequada para não multiplicar clientes ou receita.

Os controles de qualidade verificam presença de arquivos, contratos de colunas e chaves, duplicidades, datas, relacionamentos e integridade. Hashes permitem comprovar que a Bronze não foi alterada. O código reutilizável fica em `src/`; os notebooks explicam e demonstram as análises. A reprodução completa é responsabilidade do pipeline, não de executar células avulsas em uma ordem informal.

## 5. O que a EDA mostrou

### 5.1 A subida de churn exige investigação, mas não identifica uma causa isolada

A reconstrução pelos eventos de expiração encontra média mensal de **5,68% em 2025** e **6,68% em janeiro–setembro de 2026**. Abril apresenta **1.158 perdas sobre 14.237 ativos no início do mês**, ou aproximadamente **8,13%**. O enunciado informa 1.154 perdas. A auditoria encontrou 1.158 usuários distintos tanto nos eventos quanto no cadastro; a diferença foi preservada como ressalva de fonte.

![Série mensal de churn](churn_mensal_2025_2026.png)

No plano mensal, a média observada passou de 10,22% em janeiro–fevereiro para 12,97% em março–abril. Isso é compatível com uma hipótese de sensibilidade ao reajuste, mas não mede seu efeito causal: sazonalidade, composição dos clientes e vencimentos também mudam no período. A decisão adequada é investigar o preço junto dessas variáveis, sem atribuir toda a subida a ele.

### 5.2 A pesquisa de saída tem uma cobertura limitada

A pesquisa começou em junho. Entre junho e setembro, houve **3.389 saídas**; **353** dessas pessoas responderam, aproximadamente **10,4%**. Há **641 respondentes únicos no total**, mas 288 ainda estavam ativos no corte. Dividir todos os respondentes pelas saídas misturaria situações diferentes e exageraria a cobertura relevante para explicar perdas concluídas.

Os motivos observados são concentrados no canal Web e não representam automaticamente quem paga pelas lojas de aplicativos. Responder à pesquisa também é uma escolha do usuário, o que cria viés de seleção. Os relatos ajudam a formular hipóteses, mas não autorizam generalizar um motivo para toda a carteira.

![Cobertura da pesquisa](ponto_cego_cancelamentos.png)

### 5.3 Correlação e sobrevivência precisam de interpretação cuidadosa

Entre contas com treino, sessões e minutos apresentam correlação bruta próxima de 0,88. Após controlar linearmente o número de atividades, ela cai para cerca de 0,02. Parte importante da associação reflete o volume de treinos, e não um efeito independente de abrir o aplicativo. Esse exemplo mostra por que correlação bruta não basta para escolher uma ação.

A coorte de entrada com 90 dias completos de acompanhamento encontrou saída em até 90 dias de **28,47% no mensal** e **0,86% no anual**. Clientes que saíram cedo continuam no denominador. Esses percentuais não são churn mensal nem demonstram que migrar para o anual evita a saída: duração contratual e composição dos grupos afetam a comparação. O plano nessa análise auxiliar é cadastral, e não uma intervenção sorteada.

Também foram retiradas interpretações de AUC retrospectiva como se fossem desempenho de previsão futura. Para prever, os atributos precisam estar disponíveis antes do desfecho e a avaliação deve respeitar o tempo.

### 5.4 Padrões relacionados a churn: da pergunta à evidência

| Pergunta | Evidência e interpretação | Código / visualização |
|---|---|---|
| As perdas aumentaram em 2026? | Média mensal reconstruída de 5,68% para 6,68%; investigar composição e marcos | `src/analisar_eda_marcos.py`; série da seção 5.1 |
| O reajuste pode estar relacionado às perdas? | Aumento no mensal após março; antes/depois não isola causalidade | Mesmo script; EDA dos marcos |
| A pesquisa explica todos os cancelamentos? | 353 respondentes entre 3.389 perdas de junho–setembro; viés de canal e seleção | `src/gerar_graficos_eda.py`; gráfico da seção 5.2 |
| Quais perfis se associam à saída? | Na coorte de julho, saída composta de 12,25%, 9,80% e 23,70%; denominadores e intervalos na seção 8 | `src/consolidar_semana5.py`; gráfico histórico |
| A campanha reduziu expiração? | Cupom com −0,84 p.p. versus controle, mas comparação ainda inconclusiva quanto a efeito diferente de zero | Mesmo script; gráfico da seção 9 |

A correlação entre sessões e minutos da seção 5.3 avalia redundância de atributos; **não é uma correlação direta com churn**. A evidência específica sobre churn vem das comparações por período, plano e perfil e do experimento. A relação entre segmento e saída é uma associação entre grupos, não uma causa individual identificada.

## 6. Como os segmentos foram construídos

A segmentação usa cinco atributos comportamentais: dias de treino pretendidos no onboarding, treinos por mês observado, regularidade, número de modalidades e proporção de atividades ao ar livre. Churn, desligamento de renovação e desfecho futuro não entram no agrupamento.

As atividades são medidas em uma janela comum de **84 dias**, limitada ao início da assinatura. A frequência considera os dias efetivamente observados. A regularidade representa a proporção dos blocos semanais observáveis com treino. Usar uma janela comum evita comparar livremente clientes observados por poucos dias com outros acompanhados por muitos meses.

O pré-processamento trata ausência de intenção com mediana, limita extremos selecionados no percentil 99, aplica `log1p` à frequência e padroniza as escalas com z-score. Padronizar torna os atributos comparáveis; clusterizar agrupa perfis semelhantes. São etapas diferentes. Quando não há treino, a proporção ao ar livre é preenchida com zero apenas na matriz do modelo; isso não deve ser interpretado isoladamente como preferência por ambiente fechado.

O K-Means foi comparado para diferentes números de grupos. Entre três e quatro grupos, elegíveis pelo guia, três favoreceram a parcimônia e a silhueta. A silhueta de aproximadamente **0,350** indica separação parcial, não perfis totalmente distintos. Cinco reamostragens bootstrap, reajustando todo o pré-processamento, apresentaram ARI médio de aproximadamente **0,998**. É evidência exploratória de estabilidade, não garantia de generalização.

Os **1.119 clientes com menos de 30 dias** recebem classificação provisória. Eles não ajustam os centroides, mas permanecem nas contagens e nos desfechos. Assim, a solução não melhora artificialmente seus números excluindo clientes com pouca observação.

## 7. As três personas da carteira atual

| Persona | Ativos | Provisórios | Treinos/mês, mediana | Semanas com treino | Renovação desligada |
|---|---:|---:|---:|---:|---:|
| Atleta ao Ar Livre | 6.797 | 524 | 10,54 | 91,67% | 319 |
| Treino em Casa Guiado | 5.109 | 387 | 10,15 | 91,67% | 221 |
| Hábito Fraco | 2.847 | 208 | 0,36 | 8,33% | 1.715 |

![Tamanho dos segmentos atuais](semana5_consolidada/personas.png)

### Atleta ao Ar Livre

O perfil apresenta rotina de treino frequente e predominantemente ao ar livre. A tensão de negócio é que continuar treinando não garante perceber valor na assinatura. Uma hipótese é que a conclusão de uma meta reduza a necessidade percebida do serviço, mas essa motivação ainda não foi validada nos textos.

A proposta é monitorar a continuidade de uso e investigar os casos de renovação desligada. Para elegíveis, testar uma proposta de continuidade de treino contra um grupo controle, sem desconto automático. O resultado a observar é a permanência com assinatura ativa e renovação ligada em 60 dias. O nome da persona descreve comportamento registrado; não define biografia, saúde ou motivação individual.

### Treino em Casa Guiado

O perfil reúne treinos registrados predominantemente em ambiente fechado, com frequência e regularidade elevadas. O nome é um rótulo executivo: os dados usados no agrupamento não comprovam que todo integrante treine em casa ou utilize orientação guiada.

A hipótese de negócio é que conteúdo pouco relevante ou dificuldade em encaixar a rotina reduza a continuidade. Para pessoas elegíveis com queda de regularidade, pode-se testar seleção editorial de conteúdo. Retomada em 30 dias, saída em 60 dias e descadastro são medidas relevantes. A modalidade, sozinha, não comprova fadiga de catálogo ou falta de tempo.

### Hábito Fraco

O perfil apresenta pouca frequência e baixa regularidade nos registros. A hipótese é que a dificuldade de estabelecer uma rotina reduza o valor percebido. Entretanto, ausência de registro pode refletir atividade fora do aplicativo, cobertura incompleta ou outros fatores; não permite concluir lesão ou desinteresse pela atividade física.

A ação precisa separar mensais em formação de hábito, pessoas que já desligaram a renovação e anuais que continuam renovando. Um teste de rotina inicial pode medir retomada em 30 dias e continuidade em 60 dias. O contrato anual também exige cuidado: acesso ativo pode persistir mesmo quando a intenção de renovar já mudou.

### 7.4 Hipóteses de drivers de churn por segmento

Cada hipótese distingue **evidência observada**, **mecanismo possível** e **validação necessária**. A taxa histórica do perfil não valida automaticamente o motivo proposto.

| Persona | Hipótese de driver de churn | Evidência disponível | Limite da evidência | Ação e teste propostos |
|---|---|---|---|---|
| Atleta ao Ar Livre | **H1 — perda de valor após concluir uma meta:** continuar treinando não exige necessariamente manter a assinatura | Carteira atual: mediana de 10,54 treinos/mês e 319 renovações desligadas. Coorte de julho: 12,25% de saída composta | Não foi demonstrado que essas pessoas concluíram metas ou saíram por esse motivo | Validar motivos em amostra; para elegíveis com renovação desligada, testar continuidade de treino versus controle e medir permanência em 60 dias |
| Treino em Casa Guiado | **H2 — conteúdo perde relevância ou deixa de caber na rotina**, reduzindo valor percebido | Carteira atual: mediana de 10,15 treinos/mês e 221 renovações desligadas. Coorte de julho: 9,80% de saída composta | Modalidade não mede fadiga de catálogo, falta de tempo ou uso guiado. Frequência elevada não prova queda individual | Confirmar consumo de conteúdo, queda de regularidade e motivos; testar seleção editorial entre elegíveis, medindo retomada, saída e descadastro |
| Hábito Fraco | **H3 — dificuldade de formar hábito reduz valor percebido**, favorecendo descontinuidade | Carteira atual: 0,36 treino/mês, 8,33% de semanas com treino e 1.715 renovações desligadas. Coorte de julho: 23,70% de saída composta | Há associação entre perfil e saída, mas não prova do mecanismo; exercício fora do app e cobertura dos logs podem explicar parte do baixo uso | Verificar cobertura e separar plano/estado contratual; testar rotina inicial versus controle, com retomada em 30 dias e continuidade em 60 dias |

**H4 — hipótese transversal de sensibilidade a preço:** o reajuste pode reduzir a relação entre valor percebido e custo, sobretudo no mensal. O aumento observado após março justifica investigação, mas não identifica a persona afetada nem valida desconto generalizado. Comparar coortes, canal, tempo de casa e vencimento; a campanha de cupom também mantém incerteza.

As contagens atuais e as taxas históricas pertencem a **populações diferentes**, identificadas na tabela. H1 e H2 são mecanismos plausíveis ainda não validados. H3 tem associação observada com o perfil, mas a explicação causal permanece em aberto. Nenhuma das hipóteses deve ser apresentada como motivo comprovado de cancelamento.

## 8. O que a avaliação histórica acrescenta

Para verificar a relação entre perfis e saída sem usar o futuro para formar os grupos, ajustamos o modelo histórico em maio e aplicamos esse mesmo modelo aos clientes de julho. Depois observamos os 60 dias seguintes, até 29/09. O público primário são os ativos com renovação ligada no início.

O desfecho é **saída composta**: estar sem acesso ou com renovação desligada ao fim do horizonte. Portanto, não é sinônimo de expiração financeira. Perda de acesso é analisada separadamente nas tabelas completas.

| Perfil na coorte de julho | Pessoas | Saídas compostas | Taxa em 60 dias | IC95% | Participação nas saídas |
|---|---:|---:|---:|---|---:|
| Atleta ao Ar Livre | 5.957 | 730 | 12,25% | 11,45%–13,11% | 49,73% |
| Treino em Casa Guiado | 4.458 | 437 | 9,80% | 8,96%–10,71% | 29,77% |
| Hábito Fraco | 1.270 | 301 | 23,70% | 21,44%–26,12% | 20,50% |
| Total | 11.685 | 1.468 | 12,56% | 11,97%–13,18% | 100,00% |

![Saída composta na avaliação histórica](semana5_consolidada/coorte_60d.png)

Hábito Fraco tem a maior taxa, mas responde por apenas 20,50% das saídas dessa coorte. Atleta ao Ar Livre responde por 49,73%, em parte por seu tamanho. Taxa e cobertura respondem a perguntas distintas: a primeira indica frequência relativa; a segunda mostra quanto do problema o público representa.

O modelo de setembro foi ajustado separadamente para descrever a carteira atual. Não se deve multiplicar automaticamente a taxa de julho pelo segmento atual e chamar o resultado de previsão. O histórico também inclui as campanhas realmente realizadas, inclusive em agosto; não representa um cenário sem intervenção.

## 9. O que aprendemos com a campanha de agosto


A comparação principal usa todos os sorteados em 10/08, independentemente de terem aberto ou clicado na mensagem. Essa abordagem, chamada intenção de tratar, preserva a comparação criada pelo sorteio. O desfecho principal é expiração nos 30 dias de 10/08 até antes de 09/09.

| Grupo | Sorteados | Expirações | Taxa | Diferença versus controle | p ajustado |
|---|---:|---:|---:|---:|---:|
| Controle | 3.579 | 196 | 5,48% | Referência | — |
| Cupom | 3.472 | 161 | 4,64% | −0,84 p.p. | 0,32 |
| Desafio | 3.515 | 182 | 5,18% | −0,30 p.p. | 1,00 |
| Conteúdo | 3.554 | 218 | 6,13% | +0,66 p.p. | 0,71 |

Os valores de p foram ajustados para as três comparações contra controle. Os intervalos individuais das diferenças incluem zero. O cupom apresentou a menor taxa observada, mas a evidência não sustenta afirmar um efeito diferente de zero a 5% nessas comparações. Isso também não prova equivalência ou ausência de efeito.

![Comparação dos tratamentos](semana5_consolidada/campanha.png)

Abertura e clique acontecem depois da atribuição do tratamento; selecionar somente essas pessoas mudaria a comparação. Também não é possível identificar com essa tabela quais indivíduos são persuadíveis ou seriam prejudicados pelo contato. As análises por plano, por desfecho composto e por 51 dias estão separadas como sensibilidades exploratórias.

## 10. Priorização e proposta de ação

### Imediata versus monitoramento, conforme o guia

| Persona | Quando priorizar de imediato | Quando monitorar | Hipótese associada |
|---|---|---|---|
| Atleta ao Ar Livre | Renovação desligada: diagnosticar motivo, elegibilidade e preferência de contato | Renovação ligada e continuidade de uso: acompanhar sinais; não oferecer desconto automaticamente | H1 — possível perda de valor após uma meta |
| Treino em Casa Guiado | Renovação desligada: diagnóstico; queda de regularidade confirmada pode motivar elegibilidade a teste | Renovação ligada e rotina preservada: acompanhar consumo e dificuldades | H2 — relevância de conteúdo e rotina |
| Hábito Fraco | Renovação desligada: diagnóstico; mensal com renovação ligada: priorizar teste de formação de hábito | Anual com renovação ligada: investigar antes de contatar, pois baixo uso não prova urgência financeira | H3 — formação de hábito |

**Prioridade imediata significa agir no diagnóstico e preparar um teste elegível**, não executar disparos indiscriminados. A tabela por persona traduz a decisão de negócio; os totais operacionais abaixo usam regras mutuamente exclusivas para evitar dupla contagem. A hipótese H4 de preço só justifica oferta financeira após validação adicional.

A priorização atual é operacional. Primeiro vem o estado da renovação; depois, o perfil de hábito e o plano. As regras são aplicadas em ordem, sem colocar uma pessoa em dois públicos.

| Prioridade | Público | Pessoas | Receita líquida equivalente mensal |
|---|---|---:|---:|
| 1 — Diagnóstico imediato | Renovação desligada, qualquer persona | 2.255 | R$ 51.065,27 |
| 2 — Formação de hábito | Mensal, hábito fraco e renovação ligada | 208 | R$ 7.344,00 |
| 3 — Investigar antes de contatar | Anual, hábito fraco e renovação ligada | 924 | R$ 20.015,80 |
| 4 — Monitoramento | Demais ativos com renovação ligada | 11.366 | R$ 327.126,01 |

Diagnóstico imediato não significa oferecer desconto a todos. É preciso verificar elegibilidade, preferências de contato e o motivo conhecido antes de agir. Da mesma forma, monitoramento não significa negar atendimento necessário. Essas prioridades não equivalem às classes causais de resposta a tratamento.

Como primeiro aprendizado, propõe-se um piloto de viabilidade com até 400 elegíveis com renovação desligada, sorteados entre 200 e-mails editoriais e 200 controles, com estratificação por plano e persona. A medida primária é estar ativo com renovação ligada em 60 dias; retomada em 30 dias e reclamações são secundárias. Se faltarem elegíveis, ambos os braços devem ser reduzidos igualmente. A amostra precisa ser dimensionada antes de um teste confirmatório de pequenos efeitos.

## 11. Viabilidade econômica e o que ainda não é ROI

A receita equivalente usa o último pagamento aprovado não duplicado, líquido da taxa do canal; no anual, divide-se por 12. Há fallback de preço quando necessário. Essa medida permite comparar dimensão econômica, mas não é margem, receita em risco ou receita que uma campanha conseguiria salvar.

O piloto proposto custa **R$ 2 em e-mails**, sem desconto, API, WhatsApp ou CS proativo. O orçamento geral do case é R$ 40 mil por mês, com limites de 1.500 mensagens de WhatsApp e 300 atendimentos de CS. Qualquer expansão deve contabilizar canais, ofertas, API e compromissos futuros no mesmo orçamento.

Para mostrar como a hipótese de efeito afeta a economia, os cenários usam 200 tratados, receita líquida mensal assumida de R$ 27,49, custo de servir de R$ 4,20 e três meses de permanência incremental. A contribuição é calculada como `200 × efeito assumido × 3 × (27,49 − 4,20) − 2`.

| Efeito de retenção assumido | Contribuição incremental do cenário |
|---|---:|
| −2 pontos percentuais | −R$ 281,48 |
| Zero | −R$ 2,00 |
| +2 pontos percentuais | R$ 277,48 |
| +5 pontos percentuais | R$ 696,70 |

Esses valores são cenários, não retorno comprovado. Também não somamos CAC evitado automaticamente: seria necessário demonstrar redução real de aquisição. Nenhuma campanha proposta neste trabalho foi executada.

## 12. Limitações e decisões que precisam permanecer visíveis

| Limitação | Consequência para a interpretação |
|---|---|
| Enunciado informa 1.154 perdas em abril; eventos e cadastro indicam 1.158 | Manter a divergência e confirmar a definição com a fonte |
| Cinco registros divergem no estado de renovação | Há renovação após o último desligamento sem religamento explícito; eventos indicam 2.255 desligados, cadastro 2.250 |
| Plano/canal sem evento usam fallback cadastral | A reconstrução histórica não é perfeita em todos os atributos |
| Pesquisa concentrada em Web e respondentes voluntários | Motivos não representam automaticamente todos os cancelamentos |
| Texto sem amostra humana validada | Extrações não orientam listas de ação ou inferências causais |
| Deduplicação financeira por usuário/valor/dia | Aproxima o ciclo; um identificador de ciclo permitiria validação melhor |
| Cinco bootstrap e separação parcial dos grupos | Estabilidade exploratória não garante generalização ou tipos fixos de pessoa |
| Clientes novos têm menos observação | Atribuição provisória deve ser reavaliada posteriormente |
| Sem desfecho futuro completo para o corte de setembro | Não declarar previsão supervisionada validada para essa carteira |

Essas ressalvas não invalidam a entrega descritiva. Elas delimitam as conclusões e evitam que uma hipótese seja apresentada como fato ou que uma taxa de outra população seja usada como previsão individual.

## 13. Como verificamos a resolução

O fechamento da ADR 021 executou o projeto em diretório independente, começando com uma cópia da Bronze e sem Prata/Ouro anteriores, base histórica de segmentação ou histórico Git. Foram aprovados **28 testes** e executados os **três notebooks**. Os 14 arquivos brutos foram preservados; a Prata ficou idêntica; sete tabelas analíticas foram reproduzidas com equivalência numérica.

Os mesmos 14.753 ativos mantiveram suas atribuições e receita em relação à consolidação ADR 020. Isso é diferente da mudança metodológica anterior: ao passar da proposta de 11/11 para a janela comum de 84 dias, a composição dos grupos mudou. O histórico está preservado, mas seus números não devem ser misturados com os atuais.

O relatório executivo tem seis páginas e o mini deck cinco slides. Os PDFs foram renderizados e inspecionados, e seus hashes estão vinculados aos HTML correspondentes. O pacote de entrega inclui código, documentação e agregados, com notebooks sem outputs individuais e um manifesto de integridade.

## 14. Resultado entregue e continuidade do trabalho

A Semana 5 entrega uma base tratada e auditável, uma descrição coerente da carteira atual, três personas sustentadas por dados, uma avaliação histórica de saída, a leitura da campanha e uma priorização preliminar com hipóteses testáveis. A orientação de negócio é aprender antes de ampliar: usar os perfis para formular ações, verificar estado contratual e medir resultado incremental.

Na Semana 10, será necessário construir e avaliar o modelo supervisionado de churn, testar o ganho de variáveis de texto/imagem, desenhar a política de intervenção, aprofundar a economia e integrar a personalização por GenAI ao aplicativo. Esses passos exigem validação própria; não estão automaticamente resolvidos pela segmentação.

Para continuar com colegas ou outras IAs, manter as definições de população, janela e desfecho; consultar as ADRs vigentes; regenerar tabelas e apresentações juntas quando houver alteração; e nunca editar a Bronze. Publicação no Drive e submissão individual na Adalove são etapas externas, ainda não realizadas pelos scripts.

## 15. Referências e reprodução

### Como a tecnologia entrega a história analítica

O mini deck segue cinco passos: (1) três perfis da carteira; (2) como a qualidade dos dados muda a interpretação; (3) diferenças históricas de saída e cobertura; (4) o que a campanha permite concluir; (5) prioridade operacional e próximo teste. A leitura mestre explica o racional desses slides, mas não substitui os arquivos de código e a apresentação exigidos pelo guia.

| Parte da entrega técnica | Arquivo principal | Papel |
|---|---|---|
| Carga e qualidade | `src/auditar_bronze.py`, `src/limpeza_qualidade_dados.py` | Auditar e tratar entradas |
| EDA e marcos | `src/processar_eda.py`, `src/analisar_eda_marcos.py` | Explorar padrões, distribuições, períodos e relações |
| Segmentação e gráficos | `src/consolidar_semana5.py` | Formar perfis sem churn, avaliar coortes e gerar apresentações |
| Notebooks | `notebooks/01_inventario_dados.ipynb`, `02_eda_e_hipoteses.ipynb`, `03_segmentacao_clusters.ipynb` | Demonstrar inventário, EDA e evidência dos segmentos |
| Mini deck | [Cinco slides em PDF](semana5_consolidada/mini_deck.pdf) | Comunicar a história analítica |


As bases conceituais são o guia oficial de artefatos, o enunciado e o dicionário da Vitaliza, além dos resumos das aulas mantidos no repositório. As fontes numéricas são os agregados da consolidação, a EDA dos marcos e os registros de QA. Este texto não usa a pontuação de avaliação da Semana 10 como se fosse uma nota já obtida na Semana 5.

- [Relatório executivo](customer_segmentation_report_semana5.md) e [PDF](semana5_consolidada/relatorio_executivo.pdf).
- [EDA dos marcos](eda_etapa3_marcos_2026.md) e [mini deck](semana5_consolidada/mini_deck.pdf).
- [Método temporal](../notebooks/12_consolidacao_semana5.md) e [racional do fechamento](../notebooks/13_fechamento_entrega_semana5.md).
- [Qualidade e impacto](qa_entrega_semana5.md), [requisitos](../docs/matriz_requisitos_semana5.md) e [índice de decisões](../decisoes.md).

Para recalcular com acesso autorizado à Bronze, executar da raiz:

```powershell
uv run --with-requirements requirements-notebooks.txt python src/executar_semana5.py
uv run --with-requirements requirements-notebooks.txt python src/revisar_notebooks_semana5.py
```

Para editar somente esta leitura consolidada, alterar `docs/resolucao_mestre_semana5.template.md` e executar `python src/atualizar_documentacao_semana5.py`. Depois, montar novamente o pacote com `python src/montar_pacote_semana5.py`. Se houver mudança numérica ou metodológica, revisar este texto e as demais entregas antes de distribuir uma nova versão.
