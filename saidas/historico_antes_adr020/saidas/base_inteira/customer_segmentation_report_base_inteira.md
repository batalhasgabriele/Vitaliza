> HISTORICO SUPERADO PELA ADR 020. Contém resultados/interpretações não vigentes. Não usar na entrega.

# Customer Segmentation Report — Vitaliza (Semana 5)
### Versão base inteira: proposta para discussão com o time

**Data de corte:** 30/09/2026 · **Janela de comportamento:** jan–set/2026
**População:** 23.151 clientes pagantes com assinatura em vigor na janela, ativos ou não. 21.023 com 30 dias ou mais observados formam os grupos; 2.128 recém-chegados recebem o grupo mais próximo de forma provisória.
**Código:** `src/segmentacao_base_inteira.py` · **Tabelas:** `saidas/base_inteira/tabelas/`

---

## 1. Resumo executivo

Os clientes da Vitaliza se dividem pelo **modo de treinar**: ao ar livre, em casa com vídeo, sem constância ou em companhia. Idade, sexo, UF e relógio praticamente não mudam entre os grupos.

| Persona | Clientes | % base | % receita | Churn mensal | Saídas esperadas por mês | Prioridade |
|---|---:|---:|---:|---:|---:|---|
| **Ativo ao Ar Livre** | 9.432 | 44,9% | 49,9% | 5,0% | ~470 | Imediata para quem tem evento próximo; monitorar o restante |
| **Treino Indoor Guiado** | 6.643 | 31,6% | 35,6% | 4,6% | ~300 | Monitoramento, com foco em falha de pagamento |
| **Hábito Fraco** | 3.894 | 18,5% | 8,9% | **11,4%** | ~440 | **Imediata** |
| **Treina em Companhia** | 1.054 | 5,0% | 5,6% | 4,6% | ~50 | Monitoramento; alavanca de indicação |

*Churn mensal = saídas na janela ÷ meses de assinatura observados. A média da base é 5,9%.*

Três achados guiam a priorização:

1. **Hábito Fraco é o grupo de maior risco.**
   - Churn de 11,4% ao mês na média e de **39,9% ao mês no plano mensal**: o mensalista sem hábito fica, em mediana, 1,8 mês.
   - Entre os anuais ainda ativos, **750 já desligaram a renovação**.
2. **Ativo ao Ar Livre perde quase tantos clientes por mês quanto o Hábito Fraco**, mesmo treinando muito. Boa parte sai porque **o objetivo terminou**: quem tinha evento nos ±60 dias saiu 62,5% das vezes, contra 34,0% de quem não tinha prazo.
3. **A segmentação confirma a do time e a amplia.**
   - Entre os ativos, os perfis do time são recuperados: 92% dos ativos classificados aqui como Ar Livre estão no segmento “ao ar livre” do time, e 94% dos Indoor estão no “guiados por vídeo”.
   - O grupo de baixo hábito passa a incluir mensalistas.
   - Surge um quarto grupo social.

---

## 2. Por que refazer com a base inteira

A versão anterior clusterizou só os **14.753 ativos em 30/09**. Isso deixa de fora os **8.399 clientes que saíram em 2026** e enviesa os grupos.

| Indicador | Ativos no corte | Saídas de 2026 |
|---|---:|---:|
| % plano anual | 57,5% | 28,2% |
| % sem treino nos 30 dias antes de sair | — | 27,8% |

O mensalista que para de treinar cancela antes do corte. Por isso, na versão anterior, o grupo adormecido era 98% anual.

### Regras desta versão

- **Sem informação de saída na formação dos grupos.** Churn, status, renovação, motivo de fim, pesquisa de saída, campanha, tickets, plano e receita não entram no K-Means. São usados só depois, para descrever os grupos.
- **Taxas por mês observado.** O comportamento é medido por mês de assinatura dentro da janela, para que o tempo de casa não pese.
- **Treinos de todas as origens** (app, Garmin, Apple Health). `hiit` e `funcional` são unidos, porque os relógios não usam o rótulo `hiit`.
- **Sem variáveis de dispositivo.** Sessões de app e % via relógio medem o aparelho, e não o hábito: quem usa relógio treina igual, mas abre menos o app. Testei com e sem essas variáveis, e a versão sem elas separa melhor (silhueta 0,206 contra 0,159) e é mais estável.

### Variáveis do modelo

Normalização: log1p nas variáveis de cauda longa e z-score em todas.

| Variável | η² entre grupos |
|---|---:|
| % treinos acompanhados | 0,77 |
| % treinos ao ar livre | 0,73 |
| Regularidade (% das semanas com treino) | 0,63 |
| Treinos por mês | 0,62 |
| Modalidades distintas | 0,53 |
| Posts por mês | 0,14 |
| Minutos por treino | 0,09 |
| Dias por semana declarados no onboarding | 0,02 |
| Conexões sociais | 0,01 |

### Escolha de k e qualidade

**Escolhi k = 4**, que tem a melhor silhueta e o melhor Davies-Bouldin entre k=3 e k=6. Com k=3, o grupo “Treina em Companhia” se dissolve nos outros.

| Medida | Valor |
|---|---|
| Silhueta | 0,206 (dados com colunas embaralhadas: 0,134). A separação existe, mas é moderada. |
| Estabilidade em reamostragem | Jaccard médio de 0,94 a 0,99 por grupo |
| Reajuste só com ativos ou só com quem saiu | ARI 0,92 e 0,94: os grupos não dependem de quem saiu |
| Sensibilidade | O resultado depende da normalização (ver Limitações) |

![Centróides](01_centroides.png)

---

## 3. Cartões de persona

> Os nomes descrevem comportamento observado. As motivações são hipóteses: os dados mostram o que o cliente faz, não por que faz.
> Valores em mediana, com P25–P75 entre parênteses.

### 🟢 Ativo ao Ar Livre — 9.432 clientes (44,9%) · 49,9% da receita

**Quem é:** corre, caminha e pedala com regularidade, e usa o app para registrar e acompanhar a evolução.

| Comportamento | Valor |
|---|---|
| Treinos por mês | 9,8 (7,0–13,6) |
| Semanas com treino | 87% |
| Treinos ao ar livre | 80% |
| Modalidades | 5 |
| Modalidade principal | corrida (66%) ou pedal (17%) |
| Motivação mais citada acima da base | performance (18,8% contra 13,6%) |

| Risco | Valor |
|---|---|
| Churn mensal | 5,0%; 9,2% no plano mensal e 1,0% no anual |
| Saídas involuntárias (falha de pagamento, chargeback) | 9,0% |
| Objetivo com prazo | 19,6%; quem estava a ±60 dias do evento saiu **62,5%** das vezes |

**Hipóteses de driver:**
- **Objetivo cumprido:** a prova ou o evento passa e o motivo de pagar acaba.
- **Falha de pagamento no plano mensal.**

**O que tende a precisar:** um próximo objetivo antes do atual acabar (nova prova, desafio de distância) e cobrança que não falhe.

### 🔵 Treino Indoor Guiado — 6.643 clientes (31,6%) · 35,6% da receita

**Quem é:** treina em casa com vídeo, em sessões mais curtas.

| Comportamento | Valor |
|---|---|
| Treinos por mês | 9,2 (6,4–12,7) |
| Semanas com treino | 86% |
| Treinos ao ar livre | 15% |
| Treinos do app em vídeo | 89% |
| Modalidade principal | funcional (71%) ou força (25%) |
| Minutos por treino | 41,7 (o menor) |
| Motivações acima da base | saúde mental (12,5% contra 7,4%) e saúde física (19,4% contra 17,1%) |
| Motivação abaixo da base | performance (5,4%) |

| Risco | Valor |
|---|---|
| Churn mensal | 4,6% (o menor); 7,9% no plano mensal |
| Saídas involuntárias | **10,2%**, a maior entre os grupos |
| Pagamento recusado na janela | 7,6% |
| Pesquisa de saída | “outro app” 7,7%, contra 5,2% na base |

**Hipóteses de driver:**
- **Churn involuntário** por falha de pagamento.
- **Troca por outro app de vídeo**, num mercado com mais concorrentes.

**O que tende a precisar:** conteúdo novo e variado, além de recuperação de pagamento (nova tentativa e lembrete de cartão).

### 🟠 Hábito Fraco — 3.894 clientes (18,5%) · 8,9% da receita

**Quem é:** assinou com intenção, mas não criou rotina.

| Comportamento | Valor |
|---|---|
| Treinos por mês | 1,1 (0,3–2,6) |
| Semanas com treino | 21% |
| Modalidades | 2 |
| Sem nenhum treino na janela | 13,6% |
| Dias por semana declarados | 3, o que daria ~13 dias por mês contra ~1 realizado |
| Plano anual | 75% |
| Motivação acima da base | estética (18,1% contra 13,8%) |
| Objetivo com prazo | 24,3% |

| Risco | Valor |
|---|---|
| Churn mensal | **11,4%** no total, **39,9%** no plano mensal e 8,2% no anual |
| Mensalistas: permanência mediana | 1,8 mês |
| Anuais ativos com renovação desligada | **48,5% (750 de 1.546)** |
| Sem treino nos 30 dias antes de sair | 47% |
| Pesquisa de saída | “não uso” 18,9% e problema técnico 9,4% (base: 12,6% e 4,2%) |

**Hipóteses de driver:**
- **Falta de hábito nas primeiras semanas:** o mensalista cancela na primeira ou segunda cobrança.
- **O anual sem uso não vê valor na renovação.**
- **Atrito técnico.**

**O que tende a precisar:** uma primeira rotina curta e guiada, metas pequenas e contato antes da renovação anual.

**Atenção:** 1.006 dos 2.128 clientes provisórios (menos de 30 dias de casa) caem aqui. Isso reforça que é o perfil do começo de jornada.

### 🟡 Treina em Companhia — 1.054 clientes (5,0%) · 5,6% da receita

**Quem é:** treina com outras pessoas e chegou por indicação.

| Comportamento | Valor |
|---|---|
| Treinos acompanhados | **15% (12–20%)**, contra 0% nos demais |
| Conexões | 5, contra 3 |
| Treinos por mês | 8,6 |
| Chegaram por indicação | **34,9%**, contra 14,7% na base |
| Motivação social | 23,9%, contra 11,3% |

| Risco | Valor |
|---|---|
| Churn mensal | 4,6%; 7,8% no plano mensal |
| Pesquisa de saída | “preço” 48,6%, mas só 37 respostas |

**Hipóteses de driver:**
- **Saída do parceiro de treino.** Ainda não testada; pode ser medida pelas conexões que saíram.
- **Sensibilidade a preço.**

**O que tende a precisar:** desafios em grupo, benefício de indicação e plano para duas pessoas.

**Atenção:** é o grupo menos robusto. Ele some com outras formas de normalizar, mas é sustentado pelo canal e pela motivação, que não entraram no modelo.

![Distribuições](05_distribuicoes.png)

---

## 4. Drivers de churn por segmento

![Tamanho, receita e churn](02_tamanho_receita_churn.png)

| Driver (hipótese) | Evidência | Ar Livre | Indoor | Hábito Fraco | Companhia |
|---|---|:-:|:-:|:-:|:-:|
| Falta de hábito no início | 39,9% ao mês no mensal sem hábito; 47% sem treino 30 dias antes de sair | | | ●●● | |
| Objetivo cumprido | Saem 62% com evento nos ±60 dias, contra 34% sem prazo | ●●● | ●● | ● | ●● |
| Renovação anual sem valor percebido | 48,5% dos anuais com renovação desligada | | | ●●● | |
| Falha de pagamento | Saída involuntária de 9–10% e 7–8% com recusa | ●● | ●●● | | ● |
| Concorrência de outro app | 7,7% citam “outro app” | | ●● | | |
| Saída do parceiro de treino | Não testado | | | | ●● |

![Churn por fase do objetivo com prazo](03_churn_objetivo_prazo.png)

---

## 5. Priorização preliminar

| Ação | Público | Tamanho no corte | Tipo |
|---|---|---:|---|
| Contato antes da renovação com rotina curta; oferta de pausa ou mês grátis só se não houver retomada | Hábito Fraco anual com renovação desligada | 750 | **Imediata** |
| Onboarding das primeiras 8 semanas com metas pequenas | Hábito Fraco e provisórios (mensal novo) | ~1.000 novos por mês | **Imediata** |
| Gatilho “próximo objetivo” antes do evento | Ativos com evento nos ±60 dias, em todas as personas | 495 | **Imediata** |
| Recuperação de pagamento | Indoor Guiado e Ar Livre com recusa | ~7% de cada grupo | Monitoramento com regra automática |
| Conteúdo novo e personalizado | Indoor Guiado | 4.794 ativos | Monitoramento |
| Indicação e desafios em grupo | Treina em Companhia | 757 ativos | Monitoramento e alavanca de crescimento |

**Evidência do experimento de 10/08:** entre os elegíveis (quem tinha renovação até 30/09):
- O **cupom de 1 mês grátis** reduziu o churn em **4,0 p.p.** (IC 95%: −6,5 a −1,4).
- O **desafio** reduziu em 2,6 p.p., no limite da significância.

São bons candidatos para o piloto da Semana 10.

---

## 6. Comparação com a versão anterior (só ativos)

![Personas × segmentos do time](04_personas_vs_segmentos_time.png)

| | Versão do time | Esta versão |
|---|---|---|
| População | 14.753 ativos em 30/09 | 23.151 clientes de jan–set/2026, ativos e ex-clientes |
| Variáveis | 16, incluindo plano, canal e tempo de casa | 9, só comportamento e declaração |
| Segmentos | 3 | 4 |
| Baixo hábito | 13,4%, sendo 98% anual | 18,5%, sendo 75% anual, com os mensalistas que saem cedo |
| Silhueta | 0,164 | 0,206 |
| Concordância nos ativos | — | ARI 0,71; 92% dos Ar Livre e 94% dos Indoor caem no segmento equivalente do time |

---

## 7. Visualizações da EDA usadas

- **Churn mensal 2025–2026** (`../churn_mensal_2025_2026.png`), com os marcos de 2026 (`../marcos_2026.png`), do time.
- **Gráficos de segmentação** desta pasta (`01` a `05`).
- **Efeito da campanha por janela** (`06_campanha_janelas.png`).

---

## 8. Limitações

- **Janela de nove meses.** Treinos de todas as fontes só existem a partir de 01/2026. Ficam fora os 7.633 clientes que saíram em 2025 e os 1.798 de 2024, cujo comportamento não é observável da mesma forma.
- **Separação moderada.** Com silhueta de 0,206, os grupos resumem um contínuo e quem está na fronteira pode mudar de grupo.
- **Dependência da normalização.** Com RobustScaler ou sem log1p, os grupos mudam: “Treina em Companhia” e a separação ar livre × indoor se perdem. Hábito Fraco aparece em todos os cenários.
- **Independência parcial do churn.** Nenhuma variável de saída entra no modelo, mas quem vai sair costuma reduzir o uso antes. Parte do Hábito Fraco é o “pré-churn”.
- **Objetivo com prazo vem de regex sobre texto livre**, sem validação manual, e a motivação fica sem dado para 33% dos clientes.
- **Receita é caixa líquido na janela:** anuais pagos antes de 2026 aparecem com receita zero.
- **Churn por persona é descritivo.** Não é modelo preditivo nem efeito causal; a validação prospectiva fica para a Semana 10.
- **Os clientes provisórios** (2.128, com menos de 30 dias) não formam os grupos e têm atribuição instável.
