# Registro de Limpeza e Tratamento de Dados

**Projeto:** Vitaliza — Módulo 2 MBA Inteli
**Data de corte:** 30/09/2026 23:59:59, Horário de Brasília
**Última consolidação:** 05/11/2026
**Branch:** `codex/plano-mestre-vitaliza`
**Responsável pela consolidação:** Igor / Codex

## 1. Objetivo e uso do registro

Este documento é o catálogo operacional das regras de limpeza, padronização, exclusão, preservação e transformação aplicadas às bases do projeto. Ele complementa, sem substituir:

- os ADRs em [`decisoes/`](../decisoes/), que explicam por que decisões relevantes foram adotadas;
- o manifesto técnico [`saidas/auditoria_bronze/manifesto_bronze.json`](../saidas/auditoria_bronze/manifesto_bronze.json), que registra a auditoria de uma execução;
- os scripts em [`src/`](../src/), que são a implementação executável das regras;
- os notebooks em [`notebooks/`](../notebooks/), que registram o racional analítico e a reprodução dos resultados.

O registro deve ser atualizado sempre que uma regra de tratamento for criada, alterada, removida ou tiver seu impacto quantitativo recalculado. Números desta versão representam a reprodução realizada em 04–05/11/2026 sobre a Bronze disponível.

## 2. Convenções

### 2.1 Status

| Status | Significado |
|:---|:---|
| **Implementado** | Regra presente no pipeline e materializada na camada indicada. |
| **Implementado na análise** | Regra aplicada no cálculo analítico, mas sem tabela Prata própria para a fonte. |
| **Preservado deliberadamente** | Dado atípico ou ausente foi mantido por possuir significado válido. |
| **Monitorado** | Divergência conhecida, sem correção automática por falta de evidência. |
| **Pendente de alinhamento** | Regra aprovada ou necessária, mas ainda não aplicada de forma consistente em todos os consumidores. |

### 2.2 Tipos de ação

- **Excluir:** a linha não entra no produto derivado indicado; a Bronze permanece intacta.
- **Anular:** o valor inválido vira nulo, preservando a linha e as demais colunas.
- **Padronizar:** valor ou tipo é convertido para representação canônica.
- **Sinalizar:** cria-se uma flag sem apagar a informação original.
- **Filtrar temporalmente:** somente fatos observáveis até o corte ou desfecho são utilizados.
- **Preservar:** nenhuma correção é aplicada porque a ocorrência é legítima ou não há base para alterá-la.

## 3. Linhagem e controles gerais

| ID | Camada/fonte | Situação | Regra e ação | Impacto observado | Status | Implementação e evidência |
|:---|:---|:---|:---|:---|:---|:---|
| GOV-001 | Bronze — `dados/brutos/` | Risco de alteração da fonte original | Manter a Bronze estritamente somente leitura. Qualquer tratamento gera novo artefato na Prata ou no Ouro. | 12 fontes tabulares e 2 ZIPs preservados. | Implementado | [ADR 001](../decisoes/001-politica-imutabilidade-dados-brutos.md), [ADR 014](../decisoes/014-arquitetura-medalhao-dados.md) |
| GOV-002 | Bronze | Necessidade de provar integridade e reprodutibilidade | Gerar SHA-256, contagens, schema, nulos, chaves candidatas e cobertura temporal antes do processamento; reconferir hashes após o pipeline. | Todas as fontes tabulares conferiram com o dicionário; Bronze inalterada. | Implementado | [`src/auditar_bronze.py`](../src/auditar_bronze.py), [manifesto](../saidas/auditoria_bronze/manifesto_bronze.json), [ADR 015](../decisoes/015-gate-reprodutibilidade-bronze-prata.md) |
| GOV-003 | Bronze → Prata → Ouro | Mistura de níveis de tratamento | Usar a Prata para tabelas tipadas, limpas, deduplicadas e temporalmente harmonizadas; usar o Ouro para métricas, feature stores e tabelas analíticas. | Doze Parquets Prata e produtos Ouro reproduzidos. | Implementado | [ADR 014](../decisoes/014-arquitetura-medalhao-dados.md) |
| GOV-004 | Todas as fontes | Risco de exposição de dados pessoais | Publicar apenas contagens, schemas, métricas agregadas e identificadores técnicos; não incluir amostras de e-mail, texto livre, GPS ou imagens nos relatórios. | Inventário e relatórios sem conteúdo pessoal de linha. | Implementado | [`docs/source_inventory.md`](source_inventory.md), [ADR 015](../decisoes/015-gate-reprodutibilidade-bronze-prata.md) |

## 4. Registros por domínio

### 4.1 Usuários e população elegível

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| USR-001 | `usuarios.email` | Contas internas não representam clientes pagantes | Identificar e sinalizar e-mails terminados em `@vitaliza.com.br`; excluí-los das tabelas de assinaturas e fontes temporais usadas nas análises. | 60 contas internas identificadas. | `usuarios_limpo.parquet` mantém as linhas com `flag_conta_interna`; `assinaturas_limpas.parquet` as exclui. | Implementado | [`src/limpeza_qualidade_dados.py`](../src/limpeza_qualidade_dados.py), ADR 009 |
| USR-002 | `usuarios.data_cadastro` | Campo temporal lido como texto | Converter com `errors='coerce'` para `data_cadastro_dt`. | 64.948 valores processados. | `usuarios_limpo.parquet` | Implementado | `auditar_populacao_e_contas_internas()` |
| USR-003 | `usuarios.data_nascimento` | Datas sentinela ou futuras geram idades inválidas | Converter anos `<= 1900` ou `>= 2026` em `NaT`; calcular idade no corte usando 365,25 dias por ano. | 606 datas anômalas identificadas segundo ADR 007. | `usuarios_limpo.parquet` | Implementado | ADR 007; `auditar_populacao_e_contas_internas()` |
| USR-004 | `usuarios.sexo` | Categorias heterogêneas | Normalizar caixa e mapear `f`, `fem`, `feminino` para `F`; `m`, `masc`, `masculino` para `M`; preservar ausências. | Categorias canônicas para análise. | `usuarios_limpo.parquet` | Implementado | ADR 007; `auditar_populacao_e_contas_internas()` |
| USR-005 | `usuarios.sistema` | Diferenças apenas de caixa | Converter para minúsculas. | Campo padronizado. | `usuarios_limpo.parquet` | Implementado | ADR 007; `auditar_populacao_e_contas_internas()` |
| USR-006 | `usuarios.cep_prefixo` | Exportação numérica remove zeros à esquerda; há 1.894 nulos | Converter valores presentes para string de três posições com `zfill(3)` e restaurar os nulos como nulos, inclusive no consumidor Ouro. | 1.894 ausências preservadas, sem criar CEP fictício. | `usuarios_limpo.parquet` e feature stores | Implementado | ADR 004; `auditar_populacao_e_contas_internas()` |
| USR-007 | `usuarios.data_cadastro` | 119 cadastros posteriores ao corte, chegando a 2027 | Preservar a dimensão completa na Prata, mas criar `flag_cadastro_apos_corte`; consumidores temporais devem impedir o uso desses fatos. | 119 registros sinalizados sem apagar a origem. | `usuarios_limpo.parquet` | Implementado | ADR 007; `auditar_populacao_e_contas_internas()` |
| POP-001 | `assinaturas` | Definição da população oficial | Excluir contas internas e plano `cortesia`; considerar `status_atual == 'ativa'` para o retrato de pagantes ativos. | 14.813 ativas brutas − 60 internas/cortesia = **14.753 pagantes ativos**; 12.503 com renovação ligada e 2.250 desligada. | `assinaturas_limpas.parquet` | Implementado | ADR 009; [gate Bronze→Prata](../notebooks/00_gate_reprodutibilidade_bronze.md) |
| POP-002 | `assinaturas` | A tabela bruta contém todo o histórico elegível, não apenas ativos | Excluir apenas contas internas/cortesia na materialização Prata; preservar expiradas e reembolsadas para análises históricas. | 32.643 → **32.583 linhas**. | `assinaturas_limpas.parquet` | Implementado | `auditar_populacao_e_contas_internas()` |

### 4.2 Onboarding e completude

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| ONB-001 | `onboarding.dias_por_semana` | Entrada livre como `3x`, `3 vezes` etc. | Extrair o primeiro número inteiro com regex; manter nulo quando não houver número. | 63.929 linhas preservadas; 6.368 ausências originais documentadas. | `onboarding_limpo.parquet` | Implementado | ADR 004; `auditar_dimensao_1_completude()` |
| ONB-002 | `onboarding.objetivo_texto` | Campo opcional com ausência válida | Não imputar texto nem excluir linhas; criar `flag_onb_objetivo_preenchido`. | 5.467 vazios (8,6%) preservados. | `onboarding_limpo.parquet` | Preservado deliberadamente | ADR 009 |
| ONB-003 | `onboarding.nivel` | Ausência não declarada como opcional | Não imputar categoria; criar `flag_onb_nivel_preenchido`. | 4.513 vazios (7,1%) preservados e sinalizados. | `onboarding_limpo.parquet` | Implementado | ADR 009 |
| ONB-004 | `onboarding.dias_por_semana` | Ausência não declarada como opcional | Criar `flag_onb_dias_preenchido`; não aplicar `dropna`. | 6.368 vazios (10,0%) preservados e sinalizados. | `onboarding_limpo.parquet` | Implementado | ADR 009 |
| ONB-005 | `onboarding.como_conheceu` | Ausência em campo descrito como obrigatório | Criar `flag_onb_como_conheceu_preenchido`; não inventar canal. | 4.586 vazios (7,2%) preservados e sinalizados. | `onboarding_limpo.parquet` | Implementado | ADR 009 |

### 4.3 Atividades

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| ATV-001 | `atividades.tipo` | 11 rótulos em português e inglês representam 7 modalidades | Mapear `run→corrida`, `walk→caminhada`, `strength→forca`, `ride→pedal`; preservar `funcional`, `hiit` e `yoga`. | 376.930 treinos em inglês integrados; 162.108 `run` não são perdidos. | `atividades_limpas.parquet.tipo_canonico` | Implementado | ADR 009; `MAPA_MODALIDADES` |
| ATV-002 | `atividades.inicio`, origem `garmin` | Garmin grava horário em UTC | Subtrair três horas antes da deduplicação e criar `inicio_dt_br`. | Alinha o pareamento de app e relógio ao horário de Brasília. | `atividades_limpas.parquet` | Implementado | ADR 009; `auditar_e_limpar_atividades()` |
| ATV-003 | Registro app + relógio | Mesmo treino pode aparecer duas vezes | Após harmonizar horário, marcar como duplicata o segundo registro com mesmo usuário, modalidade, duração, distância e início em até cinco minutos, desde que as origens sejam diferentes; excluir da Prata. | 9.383 pares: 5.199 Garmin e 4.184 Apple Health. | `atividades_limpas.parquet` | Implementado | ADR 009 |
| ATV-004 | `atividades.duracao_min` | Duração zero ou negativa é inválida para métricas de treino | Criar `flag_duracao_zero` e excluir essas linhas da Prata analítica. | 3.649 ocorrências sinalizadas. | `atividades_limpas.parquet` | Implementado | ADR 007 e ADR 009 |
| ATV-005 | `atividades.distancia_km` e `ritmo_min_km` | Distâncias acima de 200 km refletem erro de GPS | Criar flag; anular distância e ritmo, preservando o treino e sua duração. | 951 treinos; nas corridas, remoção de 555 distâncias anômalas eleva a correlação duração×distância de aproximadamente 0,12 para 0,89. | `atividades_limpas.parquet` | Implementado | ADR 009 |
| ATV-006 | `atividades.distancia_km` nula | Treinos indoor legitimamente não possuem GPS | Manter a linha e a distância nula; não imputar zero e não excluir. | 574.835 treinos preservados. | `atividades_limpas.parquet` | Preservado deliberadamente | ADR 009 |
| ATV-007 | `atividades.inicio` | Fatos após 30/09/2026 causam vazamento temporal | Criar `flag_apos_corte` e excluir da Prata. | 34 treinos pós-corte identificados segundo ADR 007. | `atividades_limpas.parquet` | Implementado | ADR 007; `auditar_e_limpar_atividades()` |
| ATV-008 | `atividades.treino_com` | Ausência de parceiro foi exportada como string vazia, não nulo | Classificar treino em dupla somente quando o texto, após `strip`, não for vazio; não preencher string vazia com identificador. | 1.240.338 vazios no bruto (98,87%) interpretados corretamente como treino individual. | Feature store Ouro | Implementado na análise | ADR 004; `src/processar_eda.py` |
| ATV-009 | Base completa | Necessidade de preservar rastreabilidade das exclusões | Manter flags de duplicata, duração inválida, distância anômala e pós-corte antes de gerar o subconjunto válido. | 1.254.475 linhas brutas → **1.241.461 atividades válidas**; categorias de remoção podem se sobrepor e não devem ser somadas. | `atividades_limpas.parquet` | Implementado | [gate Bronze→Prata](../notebooks/00_gate_reprodutibilidade_bronze.md) |
| ATV-010 | Outliers estatísticos de distância | A regra global de Tukey mistura modalidades com escalas distintas | Usar Tukey somente como diagnóstico; não remover automaticamente. Interpretar por modalidade antes de qualquer regra adicional. | Limiar global 17,08 km marca 81.775 treinos, dos quais 73.120 são pedal. | Tabela e gráfico agregados da EDA | Preservado deliberadamente | [`src/analisar_eda_marcos.py`](../src/analisar_eda_marcos.py), ADR 010 |

### 4.4 Eventos, uso mensal, campanha e pesquisa

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| EVT-001 | `eventos_assinatura.data_hora` | Lojas gravam UTC com `Z`; Web grava Brasília | Converter valores com `Z` de UTC para `America/Sao_Paulo`; interpretar os demais como horário local sem fuso. | Datas harmonizadas para uma única referência contábil. | `eventos_assinatura_limpos.parquet.data_hora_br` | Implementado | `harmonizar_data_utc_para_br()`; ADR 009 |
| EVT-002 | `eventos_assinatura` | Contas internas e fatos futuros não podem alimentar métricas | Excluir contas internas e filtrar `data_hora_br <= corte`. | **275.565 linhas** materializadas. | `eventos_assinatura_limpos.parquet` | Implementado | `materializar_fontes_temporais_prata()` |
| EVT-003 | Estado histórico da renovação | `assinaturas.csv` é fotografia de 30/09 e não deve ser usada retrospectivamente | Reconstruir o estado vigente em cada corte passado a partir da sequência de eventos. | Evita vazamento em 823 dos 2.250 ativos com renovação desligada no retrato: 754 ainda estavam ligados e 69 nem assinavam em 31/07. | Cálculos históricos/feature store | Implementado na análise | ADR 009 |
| EVT-004 | Expirações para churn mensal | Pode haver mais de um evento de expiração por usuário | Ordenar temporalmente e manter a última expiração por usuário antes de calcular perdas mensais. | Série mensal reproduzida sem multiplicação de usuários. | `churn_mensal_2025_2026.parquet` | Implementado no Ouro | [`src/analisar_eda_marcos.py`](../src/analisar_eda_marcos.py), ADR 010 |
| USO-001 | `uso_mensal.mes` | Mês armazenado como texto | Acrescentar dia 01, converter para data e filtrar até o corte. | **591.662 linhas** materializadas. | `uso_mensal_limpo.parquet.mes_dt` | Implementado | `materializar_fontes_temporais_prata()` |
| USO-002 | Regra de gravação 2025×2026 | Em 2025 só aparecem usuários com uso; em 2026 passam a existir linhas com zero | Não comparar médias brutas sem indicar o denominador. Calcular separadamente média sobre todos os registros e média entre meses/contas com `minutos > 0`. | Dez/2025: 13.624 linhas e zero zeros; jan/2026: 25.697 zeros em 41.130 linhas. | Métricas analíticas | Implementado na análise | ADR 009 |
| USO-003 | Uso após saída | Eventos comportamentais posteriores ao desfecho geram vazamento | Restringir `uso_mensal` à janela `mes_inicio <= mes <= mes_desfecho` de cada assinatura. | Métricas limitadas ao período de vigência. | `features_eda_corte_set2026.parquet` | Implementado no Ouro | `src/processar_eda.py` |
| USO-004 | `sessoes_app` × `minutos` | Correlação aparente é dominada pelo volume de atividades | Controlar pelo número de atividades antes da interpretação; não excluir variáveis apenas pela correlação bruta. | Correlação cai de aproximadamente 0,88 entre ativos para 0,02 após controle. | Tabela agregada de EDA | Implementado na análise | ADR 010 |
| CAM-001 | `campanha_ago26.enviado_em` | Timestamp precisa ser harmonizado; controle não recebeu mensagem e possui nulo legítimo | Harmonizar valores presentes; preservar nulos do grupo controle. Excluir contas internas. | **14.120 linhas**; 3.579 nulos de envio correspondem ao controle. | `campanha_ago26_limpa.parquet` | Implementado | `materializar_fontes_temporais_prata()` |
| CAM-002 | Avaliação da campanha | Usar abertura ou clique para selecionar usuários introduz viés pós-tratamento | Aplicar análise por intenção de tratar, usando 10/08/2026 como data comum de atribuição e horizonte completo de 30 dias para todos os braços. | Nenhum braço apresentou diferença significativa contra o controle a 5%. | `campanha_ago26_itt_30d.csv` | Implementado na análise | ADR 010 |
| PES-001 | `pesquisa_saida.respondido_em` | Data armazenada como texto; contas internas não devem entrar | Converter com validação estrita e excluir contas internas. | **643 respostas** materializadas. | `pesquisa_saida_limpa.parquet` | Implementado | `materializar_fontes_temporais_prata()` |
| PES-002 | Múltiplas respostas por usuário | Contagem de pessoas pode ser inflada | Para cobertura por pessoa, ordenar e manter a resposta mais recente por usuário; preservar as respostas no arquivo Prata. | 643 respostas, 641 respondentes únicos. | Métrica agregada da EDA | Implementado na análise | ADR 010 |
| PES-003 | Cobertura da pesquisa | Pesquisa cobre apenas Web e não representa clientes de lojas | Não imputar motivo para não respondentes nem generalizar os motivos declarados às lojas; reportar cobertura separadamente. | 3.389 expirações jun–set: 2.271 lojas e 1.118 Web; respondentes 100% Web. | Relatórios da EDA e de negócios | Preservado deliberadamente | ADR 010 |

### 4.5 Pagamentos e reconciliação financeira

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| PAG-001 | `pagamentos.valor` | Valores misturam `R$ 39,90` e `39.90` | Remover `R$` e espaços, trocar vírgula por ponto e converter para número. | 19.750 valores Web em formato brasileiro tratados. | `pagamentos_limpos.parquet.valor_num` | Implementado | ADR 004; `limpar_valor_monetario()` |
| PAG-002 | `pagamentos.data_hora` | Mistura de UTC nas lojas e horário local na Web | Harmonizar para Brasília e filtrar até 30/09/2026 23:59:59. | Corrige o pertencimento ao mês contábil no limite do corte. | `pagamentos_limpos.parquet.data_hora_br` | Implementado | ADR 003; `harmonizar_data_utc_para_br()` |
| PAG-003 | `pagamentos.status` | Nem toda transação é receita | Para receita, considerar somente `status == 'aprovado'`; preservar recusas, estornos e chargebacks na Prata para auditoria e métricas próprias. | Set/2026: R$ 509.588 em todas as linhas → R$ 499.503 aprovados no fuso original. | Prata completa; receita filtrada nas análises | Implementado | ADR 003 e ADR 007 |
| PAG-004 | Aprovações repetidas | Retentativas aprovadas no mesmo ciclo/dia duplicam receita | Ordenar por usuário, data/hora e tentativa; sinalizar como duplicata após a primeira aprovação com mesmo `user_id`, valor e dia em Brasília; atribuir receita líquida zero à duplicata. | 93 casos em setembro, somando R$ 6.830,40; bruto deduplicado **R$ 492.571,70**. | `pagamentos_limpos.parquet.flag_duplicata_aprovada_dia` | Implementado | ADR 003; `auditar_funil_faturamento_setembro2026()` |
| PAG-005 | Taxas por canal | Receita bruta não corresponde ao valor retido pela Vitaliza | Aplicar 15% a App Store/Google Play, 3,5% a cartão e 0,99% a Pix Automático. | Receita líquida oficial de setembro: **R$ 436.442,35**. | `pagamentos_limpos.parquet.taxa_canal` e `valor_liquido` | Implementado | ADR 003 |
| PAG-006 | Funil contábil | Diferenças entre áreas exigem reconciliação explícita | Registrar cada estágio: total sem filtro → aprovado → fuso Brasília → deduplicado → líquido após taxas. | R$ 509.588 → R$ 499.503 → R$ 499.402 → R$ 492.572 → R$ 436.442. | Log do pipeline e relatórios | Implementado | ADR 009; [gate Bronze→Prata](../notebooks/00_gate_reprodutibilidade_bronze.md) |

### 4.6 Fontes sociais, suporte e proteção temporal na feature store

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| SOC-001 | `amizades.desde` | Há 273 relações posteriores ao corte e relações posteriores ao desfecho individual | Converter data e filtrar pelo corte global na Prata; consumidores históricos ainda restringem pelo `data_desfecho` individual. | 113.480 → **113.207 relações**. | `amizades_limpas.parquet` | Implementado | ADR 007; `materializar_fontes_temporais_prata()` |
| SOC-002 | `feed_posts.data_hora` | Há 122 posts posteriores ao corte e posts posteriores ao desfecho individual | Converter data e filtrar pelo corte global na Prata; consumidores históricos ainda restringem pelo desfecho. | 119.309 → **119.187 posts**. | `feed_posts_limpos.parquet` | Implementado | ADR 007; `materializar_fontes_temporais_prata()` |
| SUP-001 | `tickets_suporte.aberto_em` | Tickets posteriores ao desfecho podem revelar o futuro | Tipar abertura e resolução; filtrar aberturas pelo corte; sinalizar resoluções posteriores e criar versão observável até o corte. | **4.422 tickets** materializados. | `tickets_suporte_limpos.parquet` | Implementado | `materializar_fontes_temporais_prata()` |
| ANA-001 | Métricas acumuladas | Clientes antigos acumulam mais eventos apenas por exposição | Dividir atividades, minutos, sessões, posts, curtidas e treinos em dupla pelos meses de vigência; manter mínimo de um mês. | Métricas comparáveis por tempo de exposição. | `features_eda_corte_set2026.parquet` | Implementado no Ouro | `src/processar_eda.py`, ADR 006 |
| ANA-002 | Métricas ausentes após `left join` | Ausência de evento agregado significa contagem zero em campos de ocorrência | Preencher com zero somente listas explícitas de contagens/flags; não imputar variáveis descritivas ou demográficas da mesma forma. | Evita perda de assinantes sem atividade, post, ticket ou pagamento observado. | `features_eda_corte_set2026.parquet` | Implementado no Ouro | `fill_zero_cols` em `src/processar_eda.py` |
| ANA-003 | Comportamento após cancelamento | Dados posteriores à saída vazam o desfecho | Definir `data_desfecho` como data de fim para saídos e corte para ativos; restringir uso, atividades, relações, posts e tickets a essa data. | Feature store histórica sem fatos posteriores ao desfecho. | `features_eda_corte_set2026.parquet` | Implementado no Ouro | `src/processar_eda.py`, ADR 006 |
| ANA-004 | Recência de comportamento | Totais acumulados ocultam desaceleração recente | Criar janelas D-30 e D-60 relativas ao desfecho/corte e razão do uso recente sobre a média da vigência. | Features de recência usadas na EDA sem olhar além do desfecho. | `features_eda_corte_set2026.parquet` | Implementado no Ouro | `src/processar_eda.py`, ADR 006 |

### 4.7 Pacotes de heatmaps

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| IMG-001 | `heatmaps_2026-07-31.zip` | O pacote físico contém cinco imagens a mais que o dicionário | Preservar integralmente o ZIP, registrar hash e contagem física e não apagar nem escolher arquivos sem regra semântica. | 12.431 PNGs únicos observados versus 12.426 documentados. | Manifesto Bronze; nenhuma imagem processada | Monitorado | [manifesto](../saidas/auditoria_bronze/manifesto_bronze.json), ADR 004 e ADR 015 |
| IMG-002 | `heatmaps_2026-09-30.zip` | Necessidade de validar integridade antes de uso futuro de imagem | Registrar hash, contagem, tamanho compactado/descompactado e maior arquivo, sem extrair ou modificar a Bronze. | 13.047 imagens, em conformidade com o dicionário. | Manifesto Bronze; nenhuma imagem processada | Implementado | [`src/auditar_bronze.py`](../src/auditar_bronze.py), ADR 015 |

### 4.8 Feature store e segmentação dos ativos

| ID | Fonte/campo | Problema ou regra | Tratamento | Impacto observado | Saída | Status | Evidência |
|:---|:---|:---|:---|:---|:---|:---|:---|
| CLU-001 | População ativa | Clusterização não pode usar clientes internos, cortesia ou saídos | Partir de `assinaturas_limpas.parquet`, filtrar `status_atual == ativa` e exigir unicidade de `user_id`. | **14.753 usuários únicos**, sem multiplicação em joins. | `features_segmentacao_ativos_set2026.parquet` | Implementado | [`src/segmentacao_clientes.py`](../src/segmentacao_clientes.py), ADR 011 |
| CLU-002 | Features de cluster | Risco de utilizar target, pós-tratamento ou atributo discriminatório | Excluir churn, saída, pesquisa, campanha, abertura/clique, renovação automática e demografia da matriz de distância. | 16 features comportamentais, sociais, contratuais e de onboarding utilizadas. | Metadados da segmentação | Implementado | ADR 011; `metadados_segmentacao.json` |
| CLU-003 | Contagens assimétricas e extremos | Escalas e caudas podem dominar a distância euclidiana | Aplicar limite no P99 quando cabível, `log1p` em contagens assimétricas e `StandardScaler` em todas as features. | Matriz comparável em z-score. | Pipeline de clusterização | Implementado | `preparar_matriz()` |
| CLU-004 | Número de clusters | K-Means sempre produz grupos, mesmo sem separação natural | Comparar k=3 e k=4 por silhouette, Calinski–Harabasz, Davies–Bouldin, estabilidade ARI e tamanho mínimo; manter k=5 apenas como diagnóstico. | Selecionado k=3: silhouette 0,164; DB 2,007; ARI 0,998; menor grupo 13,4%. | `metricas_clusterizacao.csv` | Implementado | ADR 011 |
| CLU-005 | Interpretação dos grupos | IDs numéricos não possuem significado de negócio | Nomear após a formação pelos centroides: Ativos ao ar livre, Ativos guiados por vídeo e Adormecidos sem hábito. | 7.457, 5.317 e 1.979 clientes, respectivamente. | `segmentos_ativos_set2026.parquet` | Implementado | ADR 011 |
| CLU-006 | Receita representada | Comparar mensal e anual diretamente distorce valor corrente | Usar o último pagamento aprovado e deduplicado, líquido de taxas; dividir o anual por 12 e aplicar fallback de tabela quando ausente. | R$ 405.551,09/mês representados nos três segmentos. | Perfil agregado dos segmentos | Implementado | `_agregar_receita()` |

## 5. Pendências e dívida técnica futura

| ID | Prioridade | Lacuna | Risco | Ação requerida |
|:---|:---:|:---|:---|:---|
| LIN-004 | Média | A regra de deduplicação de atividades depende de comparação apenas com a linha anterior após ordenação. | Grupos com três ou mais registros semelhantes podem exigir validação adicional. | Criar teste de cenário com múltiplas origens e confirmar a cardinalidade do algoritmo antes da Semana 10. |
| LIN-005 | Baixa | O catálogo é manual e o pipeline imprime métricas no console, mas ainda não gera um log estruturado por execução. | Comparações entre execuções dependem de leitura manual. | Em evolução futura, gerar `saidas/logs/tratamentos_<timestamp>.jsonl` com ID da regra, entrada, saída, contagens, duração, versão do código e resultado. |

As pendências LIN-001, LIN-002 e LIN-003 foram resolvidas na Etapa 4 pela materialização das fontes sociais/suporte, preservação correta do CEP nulo e flag explícita de cadastro futuro.

## 6. Inventário das materializações atuais

| Camada | Artefato | Linhas reproduzidas | Observação |
|:---|:---|---:|:---|
| Prata | `usuarios_limpo.parquet` | 64.948 | Contas internas sinalizadas, não excluídas. |
| Prata | `assinaturas_limpas.parquet` | 32.583 | Contas internas/cortesia excluídas. |
| Prata | `onboarding_limpo.parquet` | 63.929 | Ausências preservadas com flags. |
| Prata | `atividades_limpas.parquet` | 1.241.461 | Deduplicada, válida e limitada ao corte. |
| Prata | `pagamentos_limpos.parquet` | 165.548 | Histórico preservado com flags e valores derivados. |
| Prata | `eventos_assinatura_limpos.parquet` | 275.565 | Datas harmonizadas. |
| Prata | `uso_mensal_limpo.parquet` | 591.662 | Mês tipado. |
| Prata | `campanha_ago26_limpa.parquet` | 14.120 | Nulos do controle preservados. |
| Prata | `pesquisa_saida_limpa.parquet` | 643 | Respostas preservadas; deduplicação ocorre apenas em métricas por pessoa. |
| Prata | `amizades_limpas.parquet` | 113.207 | Relações posteriores ao corte removidas do derivado. |
| Prata | `feed_posts_limpos.parquet` | 119.187 | Posts posteriores ao corte removidos do derivado. |
| Prata | `tickets_suporte_limpos.parquet` | 4.422 | Abertura/resolução tipadas e flags temporais incluídas. |
| Ouro | `features_eda_corte_set2026.parquet` | 32.583 | Feature store histórica da EDA; não é ainda a feature store dos 14.753 ativos da segmentação. |
| Ouro | `churn_mensal_2025_2026.parquet` | 21 meses | Série de jan/2025 a set/2026. |
| Ouro | `churn_mensal_por_plano_2025_2026.parquet` | 42 linhas | Série mensal separada por plano. |
| Ouro | `features_segmentacao_ativos_set2026.parquet` | 14.753 | Uma linha por pagante ativo, com features e segmento. |
| Ouro | `segmentos_ativos_set2026.parquet` | 14.753 | Mapeamento interno entre usuário, cluster e nome executivo. |

## 7. Validações automatizadas existentes

| Controle | Cobertura atual | Local |
|:---|:---|:---|
| Conversão UTC→Brasília e preservação de horário local | Teste unitário com timestamp no limite de virada do dia. | [`tests/test_limpeza_qualidade_dados.py`](../tests/test_limpeza_qualidade_dados.py) |
| Conversão monetária brasileira e decimal | Teste unitário para `R$ 39,90` e `299.90`. | [`tests/test_limpeza_qualidade_dados.py`](../tests/test_limpeza_qualidade_dados.py) |
| Inventário, chaves e manifesto Bronze | Testes do auditor e contratos mínimos. | [`tests/test_auditar_bronze.py`](../tests/test_auditar_bronze.py) |
| Churn, campanha, outliers e correlação controlada | Testes das funções analíticas da Etapa 3. | [`tests/test_analisar_eda_marcos.py`](../tests/test_analisar_eda_marcos.py) |
| Divisão segura e escolha de k elegível | Testes unitários das regras centrais da Etapa 4. | [`tests/test_segmentacao_clientes.py`](../tests/test_segmentacao_clientes.py) |

## 8. Processo de atualização

Ao criar ou alterar um tratamento:

1. incluir ou atualizar um registro neste documento, mantendo o ID estável;
2. alterar o script responsável e adicionar teste proporcional ao risco;
3. reexecutar o pipeline a partir da Bronze e registrar as novas contagens;
4. verificar os hashes da Bronze;
5. atualizar ADRs, notebooks, gráficos e relatórios impactados;
6. registrar em novo ADR qualquer mudança de regra técnica ou de negócio, e não apenas uma correção mecânica de implementação.

## 9. Referências de decisão

- [ADR 001 — Imutabilidade dos dados brutos](../decisoes/001-politica-imutabilidade-dados-brutos.md)
- [ADR 003 — Metodologia de faturamento](../decisoes/003-metodologia-faturamento-setembro-2026.md)
- [ADR 004 — Auditoria e inconsistências](../decisoes/004-auditoria-dados-brutos-inconsistencias.md)
- [ADR 007 — Auditoria das 12 tabelas](../decisoes/007-auditoria-qualidade-12-tabelas.md)
- [ADR 009 — Pipeline pelas cinco dimensões](../decisoes/009-pipeline-5-dimensoes-qualidade-aula2.md)
- [ADR 010 — EDA Parte 2](../decisoes/010-eda-parte2-churn-marcos-2026.md)
- [ADR 014 — Arquitetura medalhão](../decisoes/014-arquitetura-medalhao-dados.md)
- [ADR 015 — Gate Bronze→Prata](../decisoes/015-gate-reprodutibilidade-bronze-prata.md)

## Complemento de validação — 08/11/2026

### Engenharia de dados e conservação dos resultados

| Registro | Tratamento/controle | Evidência |
|---|---|---|
| ENG-001 | Migração de todas as leituras da EDA para Prata; chaves e população verificadas | `src/processar_eda.py` |
| ENG-002 | Baseline privada, duas execuções em staging e comparação por usuário/atributo | `src/validar_engenharia_dados.py`, `saidas/tabelas/qa_engenharia_dados.json` |
| ENG-003 | Preservação da coluna numérica legada de CEP na Ouro; texto canônico preservado na Prata e em cep_prefixo_str | ADR 017 |
| ENG-004 | Auditoria agregada de datas, exposição e candidatos a cobranças duplicadas; sem exclusão automática | `src/auditar_temporalidade.py` |

O resultado de ENG-002 precisa ser lido no JSON da execução: `aprovado` e `publicado` indicam estados distintos. A comparação trata ausente como diferente de zero. Logs e baseline individuais ficam em pastas ignoradas pelo Git. Visão didática: [pipeline ETL e Data Quality](../notebooks/00_pipeline_etl_data_quality.md).

| Registro | Alteração | Camadas afetadas | Evidência |
|---|---|---|---|
| VAL-001 | Sensibilidade em três especificações, k=2…8 e bootstrap com reposição | Somente agregados em saídas; Ouro preservada | `src/validar_entrega_semana5.py`, `saidas/validacao_semana5.md` |
| VAL-002 | ICs de diferenças ITT e correção de três testes | Nova tabela agregada; experimento original preservado | `saidas/tabelas/campanha_ago26_incerteza.csv` |
| DOC-001 | Personas, orçamento do piloto e qualificações de receita/AUC/sobrevivência | Relatório, documento mestre, mini deck | ADRs 012 e 013 |

Não houve nova limpeza, exclusão de pessoas ou edição dos dados brutos neste fechamento. Validação suplementar não certifica reexecução integral da cadeia.
