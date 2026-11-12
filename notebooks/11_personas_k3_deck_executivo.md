# 11 — Personas k=3 e deck executivo (Customer Segmentation Report)

**Autora:** Lorena · **Branch:** `dev` · **Data:** 11/11/2026 · **Corte:** 30/09/2026
**Código:** [`src/personas_k3_deck.py`](../src/personas_k3_deck.py) · **Tabelas:** [`saidas/deck_executivo/tabelas/`](../saidas/deck_executivo/tabelas/) · **Decisão:** [ADR 019](../decisoes/019-personas-k3-deck-executivo.md)

Este notebook registra o racional do deck executivo "Vitaliza — Diagnóstico de Churn" (7 slides), para que qualquer pessoa do time consiga recalcular cada número.

## 1. Pergunta

Quem são os clientes da Vitaliza, como o churn evoluiu, o que explica as saídas e onde agir primeiro, com orçamento de CRM de R$ 40 mil/mês?

## 2. Como reproduzir

```powershell
.\.venv\Scripts\python.exe src\personas_k3_deck.py
```

O script lê só a camada Prata (e o segmento oficial da Ouro, para comparação) e grava apenas tabelas agregadas. Nenhum arquivo por cliente é publicado (GOV-004).

| Tabela | Conteúdo | Slides |
|---|---|---|
| `resumo_deck.json` | Qualidade da segmentação, números da empresa e impacto estimado | 1, 2, 4, 6 |
| `perfil_personas.csv` | Tamanho, receita, churn, comportamento e renovação por persona | 1, 3 |
| `categorias_personas.csv` | Motivação, modalidade, canal, nível, sexo, UF e relógio por persona | 3 |
| `fatores_churn.csv` | Churn por mês observado em cada categoria de cada fator | 4, 5 |
| `treinos_antes_da_saida.csv` | Treinos por janela de 30 dias antes da saída | 4 |
| `niveis_prioridade.csv` | Clientes e receita dos 4 níveis (segmento × renovação) | 1, 6 |
| `personas_vs_segmentos_time.csv` | Cruzamento com a segmentação oficial (ADR 011) | notas do slide 3 |
| `centroides_z.csv` | Centroides em z-score | notas do slide 3 |

## 3. População e tratamentos

A base é a mesma da proposta da base inteira (ADR 018), montada por `segmentacao_base_inteira.construir()`:

- **População:** 23.152 pagantes (sem contas internas nem cortesia, POP-002) com assinatura em vigor em algum momento de jan–set/2026, ativos ou não no corte. Inclui os 8.399 que saíram em 2026.
- **Ajuste:** 21.024 clientes com pelo menos 30 dias observados. Os 2.128 mais novos recebem o grupo mais próximo.
- **Comportamento por mês de assinatura observado** (ANA-001), com treinos de todas as origens (ATV-001 a ATV-010), limitados ao período de vigência (ANA-003).
- **Renovação no corte** reconstruída pelos eventos (EVT-003); **receita** pelo último pagamento aprovado, sem duplicatas e líquido de taxas (CLU-006, PAG-003 a PAG-005).

## 4. Segmentação

### Por que k=3 com 5 variáveis

As tabelas salvas da proposta k=4 (rodada de 11/11, 8 variáveis, sem `min_por_treino`) não sustentam mais os nomes do relatório: os grupos "Ar Livre" e "Indoor" quase não diferem em % de treinos ao ar livre (η² 0,006). A variável, porém, é claramente bimodal na base: cerca de 37% dos clientes têm menos de 30% de treinos ao ar livre e cerca de 60% têm mais de 60%.

Testei três conjuntos de variáveis com k de 3 a 5:

| Conjunto | k | Silhueta | Resultado |
|---|---:|---:|---|
| C, 8 variáveis (proposta k=4) | 4 | 0,187 | Separa por intensidade; ar livre não separa |
| Só comportamento, sem posts e conexões | **3** | **0,329** | Ar livre, casa e hábito fraco bem separados |
| Só comportamento | 4 | 0,316 | Divide o ar livre por intensidade |

**Escolha:** k=3 com `dias_semana_pretendidos`, `treinos_mes`, `regularidade`, `n_modalidades` e `pct_ar_livre`. Tratamento: teto no P99, log1p nas contagens e z-score (CLU-003). Churn, plano, renovação, receita, pesquisa e campanha ficam fora do modelo.

### Qualidade

| Medida | Valor |
|---|---:|
| Silhueta | 0,33 (0,23 com colunas embaralhadas) |
| Davies–Bouldin | 1,17 |
| ARI com outra semente | 1,00 |
| ARI bootstrap (médio · mínimo) | 0,996 · 0,993 |
| ARI ajustando só com ativos · só com quem saiu | 0,94 · 0,93 |
| ARI unindo hiit e funcional | 0,96 |
| ARI com MinMaxScaler | 0,97 |
| ARI com RobustScaler · sem log1p | 0,20 · 0,26 |

A estrutura é estável, mas depende de log1p + z-score: essa escolha é premissa declarada.

**Concordância com o time (ativos):** 100% dos "guiados por vídeo" caem no Treino em Casa e 92% dos "ao ar livre" caem no Atleta ao Ar Livre. O grupo "Treina em Companhia" (~5%) da proposta k=4 vira subsegmento: é instável a outras normalizações.

## 5. Personas

| | Atleta ao Ar Livre | Treino em Casa Guiado | Hábito Fraco |
|---|---:|---:|---:|
| Ativos no corte | 7.514 (51%) | 5.419 (37%) | 1.820 (12%) |
| Receita líquida/mês | R$ 208 mil (51%) | R$ 154 mil (38%) | R$ 43 mil (11%) |
| Churn/mês (mensal · anual) | 5,1% (9,4% · 1,0%) | 4,4% (7,6% · 0,9%) | 11,5% (44% · 8,4%) |
| Peso nas saídas de 2026 | 39% | 24% | 37% |
| Treinos/mês (mediana) | 9,7 | 9,3 | 1,1 |
| Custo de cada saída | R$ 333/ano + R$ 118 de CAC | R$ 341/ano + R$ 118 | R$ 285/ano + R$ 118 |

Notas: churn e comportamento usam os 21.024 da janela (o "77% no anual" do Hábito Fraco é dessa base; entre os ativos no corte são 83%). Ativos, receita e custo de saída usam os 14.753 do corte. Sexo, idade, UF, relógio e canal de cobrança não diferenciam os perfis.

## 6. Churn e fatores

- **Série** (Ouro, EVT-004): 5,68% ao mês em 2025 e 6,68% em jan–set/2026, pico de 8,13% em abril.
- **Carteira:** em 2025 entraram 12.233 e saíram 7.633; em jan–set/2026, 10.012 e 8.399 (84% das novas).
- **Fatores** (`fatores_churn.csv`, razão entre o grupo de maior e o de menor risco): evento do objetivo a ±60 dias, constância e plano mensal chegam a 3,4×; motivação estética 2,0×; sem conexões 1,8×; pagamento recusado 1,7×; influenciador 1,5×; sexo, idade, UF e relógio até 1,2×.
- **Antes da saída** (`treinos_antes_da_saida.csv`): o mensalista que sai mantém cerca de 11 treinos por 30 dias e cai para 4,8 no último mês; o anual que sai vai de 3,1 para 1,1 em 4 meses.

O objetivo com data vem de regex sobre o texto do onboarding (`src/objetivo_onboarding.py`), sem validação manual.

## 7. Priorização e impacto

Níveis por segmento × renovação desligada (`niveis_prioridade.csv`):

| Nível | Público | Clientes | Receita/mês |
|---|---|---:|---:|
| 1 · Imediata | Hábito Fraco com renovação desligada + mensalistas | 1.060 | R$ 26,9 mil |
| 2 · Leve | Atleta e Casa com renovação desligada | 1.486 | R$ 34,4 mil |
| 3 · Monitorar | Atleta e Casa com renovação ligada | 11.447 | R$ 327,8 mil |
| 4 · Não perturbe | Anuais do Hábito Fraco que ainda renovam | 760 | R$ 16,4 mil |

Impacto estimado (premissas de eficácia de 20–30%, a validar em piloto com controle): ~44 saídas/mês evitadas com hábito nos 90 primeiros dias, ~17 com próximo objetivo, ~13 com resgate da renovação anual e ~23 com recuperação de pagamento. Total ~97/mês (−0,66 p.p.), ~1.160 clientes/ano, R$ 0,38 mi de receita líquida recorrente e R$ 0,14 mi de CAC evitado.

Orçamento no pior caso (aceite máximo das ofertas): R$ 17.651 no 1º mês e R$ 24.833 no 3º, dentro do teto de R$ 40 mil, com reserva de R$ 15 a 22 mil para a IA Generativa.

## 8. Limitações

- Associações descritivas; só a campanha de 10/08 é randomizada.
- O efeito do cupom (−4,0 p.p.) só é significativo entre quem renovava até 30/09; na leitura oficial de 30 dias não é.
- Treinos de todas as origens só existem desde jan/2026.
- A pesquisa de saída cobre só a Web.
- Renovação desligada é intenção de sair, não churn.
- A taxa real de aceite das ofertas é desconhecida.
- LGPD: idade, sexo e UF não definem grupos nem ofertas.
