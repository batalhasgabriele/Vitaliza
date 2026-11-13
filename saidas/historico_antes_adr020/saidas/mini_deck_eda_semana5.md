> HISTORICO SUPERADO PELA ADR 020. Contém resultados/interpretações não vigentes. Não usar na entrega.

# Vitaliza — segmentação para orientar a retenção

Mini deck da Semana 5 • 08/11/2026 • Corte: 30/09/2026

Roteiro de apresentação: 8 slides, cerca de 8 minutos. Cada `---` inicia um slide. Abrir no preview Markdown para apresentar com os gráficos. Fonte: tabelas agregadas em `saidas/tabelas/`. Relatório completo: [Customer Segmentation Report](customer_segmentation_report_semana5.md).

## 1. Três segmentos descrevem os 14.753 pagantes

| Segmento | Pessoas | Base |
|---|---:|---:|
| Ao ar livre | 7.457 | 50,55% |
| Por vídeo | 5.317 | 36,04% |
| Adormecidos | 1.979 | 13,41% |

![Tamanho e receita equivalente](segmentacao_tamanho_receita.png)

1. O agrupamento usa dados disponíveis no corte, sem churn como entrada.
2. O grupo adormecido demanda investigação, sem presunção de resposta positiva ao contato.
3. A receita no gráfico é mensal equivalente estimada, não receita em risco.

---

## 2. A qualidade dos dados muda a leitura do comportamento

| Tratamento | Registros |
|---|---:|
| Pares de atividades duplicadas removidos | 9.383 |
| Atividades de duração zero removidas | 3.649 |
| Distâncias acima de 200 km tratadas como ausentes | 951 |

![Distâncias por modalidade](outliers_por_modalidade.png)

1. A camada Bronze permanece imutável e a Prata contém as transformações rastreáveis.
2. Uma régua global de outliers confunde pedais longos com erros.
3. Fuso de Brasília e deduplicação também afetam a reconciliação financeira.

Fonte: registro de tratamento e `tabelas/outliers_por_modalidade.csv`.

---

## 3. O churn aumentou, mas o reajuste não explica sozinho a mudança

| Período | Churn mensal médio reconstruído |
|---|---:|
| 2025 | 5,68% |
| Jan–set/2026 | 6,68% |
| Abril/2026 | 8,13% |

![Churn reconstruído](churn_mensal_2025_2026.png)

1. O denominador é a população ativa no início de cada mês.
2. Preço, sazonalidade e composição de contratos mudam simultaneamente.
3. Abril tem 1.158 perdas reconstruídas versus 1.154 no case, diferença ainda não reconciliada.

Fonte: `tabelas/churn_mensal_2025_2026.csv`. Médias aritméticas mensais, não taxa anual.

---

## 4. Pesquisa e campanha respondem perguntas diferentes

| Braço randomizado | Pessoas | Churn em 30 dias | Diferença para controle |
|---|---:|---:|---:|
| Controle | 3.579 | 5,48% | Referência |
| Desafio | 3.515 | 5,18% | −0,30 p.p. |
| Cupom | 3.472 | 4,64% | −0,84 p.p. |
| Conteúdo | 3.554 | 6,13% | +0,66 p.p. |

![Marcos de 2026](marcos_2026.png)

1. Os 641 respondentes únicos da pesquisa são Web e não representam as lojas.
2. Os intervalos de 95% das três diferenças experimentais incluem zero.
3. A análise mantém todos os sorteados e ainda não identifica uplift individual.

Fonte: `tabelas/campanha_ago26_incerteza.csv`. ICs não simultâneos, com p-valores corrigidos disponíveis no anexo.

---

## 5. A correlação depende da atividade que estamos controlando

| Sessões e minutos | Correlação |
|---|---:|
| Bruta entre ativos | 0,883 |
| Parcial, controlando atividades | 0,015 |

![Correlação controlada](correlacao_controlada.png)

1. Mais sessões acompanham maior volume de atividade.
2. Após o controle linear, a associação residual é pequena.
3. Esse ajuste não prova causalidade nem elimina confundidores não observados.

Fonte: `tabelas/correlacao_controlada.csv`.

---

## 6. Os grupos se repetem, mas há sobreposição

| Especificação, k=3 | Silhueta em amostra de 2.500 | ARI versus publicado |
|---|---:|---:|
| 16 atributos | 0,164 | 1,000 |
| Sem plano e canal | 0,193 | 0,988 |
| Quatro atributos comportamentais, proxy | 0,336 | 0,931 |

![Projeção dos grupos publicados](segmentacao_pca.png)

1. Testamos k de 2 a 8 em três especificações, sem selecionar pelo churn.
2. A solução compacta melhora a silhueta no seu próprio espaço, mas isso não prova superioridade operacional.
3. Mantemos a versão publicada rastreável e registramos a compacta como candidata a evolução após auditoria temporal.

Fonte: `tabelas/robustez_segmentacao_semana5.csv`. A projeção PCA representa a solução publicada de 16 atributos. ARI alto mede concordância, não separação.

---

## 7. As personas orientam testes diferentes

| Persona | Evidência de uso | Prioridade |
|---|---|---|
| Ao ar livre | 10 treinos/30d, mediana | Monitorar continuidade |
| Por vídeo | 10 treinos/30d, mediana | Monitorar relevância do conteúdo |
| Adormecidos | 0 treino/30d, mediana | Preparar piloto controlado |

![Perfis padronizados](segmentacao_heatmap_perfis.png)

1. Preferência observada sustenta a diferenciação da mensagem.
2. Motivação e eficácia da oferta permanecem hipóteses.
3. Dados demográficos, GPS e relatos pessoais não são necessários para esses cartões.

Fonte: `tabelas/perfil_segmentos.csv` e relatório executivo.

---

## 8. O próximo passo é aprender com um piloto limitado

| Proposta, ainda não executada | Limite |
|---|---:|
| Adormecidos elegíveis | Até 400 |
| Mensagem por e-mail / controle | 200 / 200 |
| Custo incremental de envios | R$ 2,00 |
| Orçamento mensal global do case | R$ 40.000,00 |

![População de referência do piloto](segmentacao_tamanho_receita.png)

1. Verificar elegibilidade e preferências de contato antes do sorteio.
2. Medir saída em 60 dias e retomada em 30 dias, preservando atendimento nos dois braços.
3. O piloto testa viabilidade, e uma expansão exige cálculo de poder e revisão de danos e custos.

Limites da entrega: churn futuro de setembro indisponível, causalidade do reajuste não identificada, exposição temporal ainda requer aprofundamento. Fonte: relatório executivo, seções 8 e 9. Repetição do gráfico é intencional para retomar a população de referência.
