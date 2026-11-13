# 14 — Auditoria do deck executivo (Customer Segmentation Report)

**Autora:** Lorena · **Branch:** `dev` · **Data:** 12/11/2026 · **Corte:** 30/09/2026
**Decisão:** [ADR 024](../decisoes/024-auditoria-deck-executivo.md) · **Código:** [`src/numeros_deck_executivo.py`](../src/numeros_deck_executivo.py) · **Tabelas:** [`saidas/deck_executivo/auditoria/`](../saidas/deck_executivo/auditoria/)

O deck "Vitaliza — Diagnóstico de Churn" (7 slides) usa como fonte principal a consolidação da [ADR 020](../decisoes/020-consolidacao-temporal-semana5.md) (`saidas/semana5_consolidada/tabelas/`). Este notebook audita cada número: de onde vem, como foi calculado, se confere com a fonte e com os outros slides, e o que foi corrigido.

## 1. Como reproduzir

```powershell
.\.venv\Scripts\python.exe src\consolidar_semana5.py          # números consolidados (ADR 020)
.\.venv\Scripts\python.exe src\numeros_deck_executivo.py      # números complementares e auditoria
```

| Fonte | Abreviação | Conteúdo |
|---|---|---|
| `dados/processados/prata/` | Prata | Tabelas limpas (registro de tratamentos) |
| `dados/processados/ouro/churn_mensal_*` | Ouro | Série mensal de churn (EVT-004) |
| `saidas/semana5_consolidada/tabelas/` | Consolidação | Perfis, coortes, prioridades, cenários (ADR 020) |
| `saidas/deck_executivo/auditoria/` | Auditoria | Receita de 12 meses, entropia, evento, poder, público ampliado |

## 2. Glossário de métricas

| Métrica | Definição | Onde aparece |
|---|---|---|
| Receita de caixa | Pagamentos aprovados, sem duplicatas, após taxas, no mês | Slide 2 (12 meses) |
| Receita equivalente | Último pagamento líquido; anual ÷ 12. Não é margem nem receita em risco | Slides 1, 3, 6 |
| Margem | Receita equivalente − R$ 4,20 de custo de servir | Slide 6 |
| Churn mensal | Perdas ÷ ativos no início do mês (série Ouro) | Slides 2, 4 |
| Saída em 60 dias | Ativos em uma data de corte que perderam o acesso em 60 dias (coorte) | Slides 1, 3, 4 |
| Saída em 90 dias | Entradas com 90 dias completos, por plano cadastral (coorte) | Slides 1, 5, 7 |

## 3. Auditoria por slide

Legenda: ✅ confere · ⚠️ confere, mas exige rótulo ou ressalva · ❌ corrigido nesta revisão.

### Slide 1 — Resumo executivo

| Item | Origem e cálculo | Situação |
|---|---|---|
| 2.255 com renovação desligada · R$ 51 mil/mês | Consolidação, `prioridades.csv` (prioridade 1) | ✅ Igual ao slide 6 |
| 76% no Hábito Fraco | 1.715 ÷ 2.255 (`perfil_personas.csv`) | ✅ |
| 19,8% contra 10,5% | `coortes_60d.csv`, ativos em 31/07, perda de acesso | ⚠️ Perfis da coorte vêm do modelo de maio; não são os 2.847 de setembro |
| 28,5% contra 0,9% | `coorte_90d.csv` | ⚠️ Plano cadastral; não estima efeito de trocar de plano |
| "Piloto de 400, R$ 2" | ADR 020 | ❌ 200 por braço só detecta ≥ 6,9 p.p.; corrigido para os 2.255 elegíveis (≥ 2,9 p.p.) |

### Slide 2 — Visão geral

| Item | Origem e cálculo | Situação |
|---|---|---|
| R$ 5,2 mi/ano | Setembro × 12 | ❌ Setembro concentra renovações anuais; trocado por **R$ 4,7 mi** (receita de caixa out/25–set/26) |
| +28% | Receita de jan–set/26 ÷ jan–set/25 (R$ 3,63 mi ÷ R$ 2,84 mi) | ✅ |
| 64,9 mil contas | Prata de usuários (64.948) | ⚠️ Inclui 60 internas e 1.918 com e-mail repetido; registrado no rodapé |
| 14.753 pagantes, 57% anual | POP-001 | ✅ |
| 6,7% (5,7% em 2025) | Série Ouro | ✅ |
| "travou a carteira" | Base +12% em 2026 contra +54% em 2025 | ❌ Trocado por "desacelerou" |
| 1,24 mi treinos · 119 mil posts | Prata | ❌ 24% dos treinos e 36% dos posts são de não pagantes; agora explícito |
| Idade, gênero, regiões, nível, origem | Prata, 14.753 pagantes | ✅ Motivação com 33% sem resposta |

### Slide 3 — Personas

| Item | Origem e cálculo | Situação |
|---|---|---|
| 6.797 / 5.109 / 2.847; 46 / 35 / 19% | `perfil_personas.csv` | ✅ |
| Receita 48 / 36 / 16% | Receita equivalente ÷ R$ 405,5 mil | ✅ |
| Treinos, semanas, ar livre, renovação desligada | `perfil_personas.csv` | ✅ 319 + 221 + 1.715 = 2.255 |
| "Saem em 60 dias" 8,8 / 7,1 / 19,8% | `coortes_60d.csv`, 31/07 | ⚠️ Outra população; rodapé corrigido. Em maio, a ordem Atleta × Hábito Fraco se inverte na saída composta |
| Participação nas perdas 39 / 38% | `coortes_60d.csv` | ✅ |

### Slide 4 — Churn

| Item | Origem e cálculo | Situação |
|---|---|---|
| Novas +9%, saídas +47% | Prata, médias mensais 2025 × jan–set/26 | ✅ Soma de 8.399 igual à série Ouro |
| Pico de abril | Série Ouro | ❌ "Pós-reajuste" sugeria causa; agora "concentrado no mensal" |
| % da incerteza explicada | `entropia_fatores.csv` | ✅ Reproduzível; o peso do plano vai de 7,2% (maio) a 1,9% (julho) |
| Treinos antes de sair | `treinos_antes_da_saida.csv`, assinaturas em vigor em 2026 | ⚠️ Retrospectivo, independe de perfil |

### Slide 5 — Hipóteses

| Item | Origem e cálculo | Situação |
|---|---|---|
| H1: 28,5% e 27,6% | `coorte_90d.csv` e `coortes_60d.csv` (n=228) | ✅ Amostra pequena |
| H2: 1.715 e 19% × 2% | Consolidação | ✅ |
| H3: 18–22% × 10–12% | `evento_corte_fixo.csv` (31/05 e 31/07) | ⚠️ Datas sem validação humana |
| H4: 58% × 47% | `numeros_deck.json`, anuais de 01/2024 a 08/2025 | ❌ Antes sem censura e sem comparação; corrigido |
| H5: 703 involuntárias | Prata, falha de pagamento ou chargeback em 2026 | ⚠️ Chargeback isolado nem sempre tira acesso |
| H6: vínculo social | `entropia_fatores.csv` | ❌ Contava conexões até a saída (vazamento); no corte, ≈ 0%. Virou "sem evidência" |

### Slide 6 — Estratégia

| Item | Origem e cálculo | Situação |
|---|---|---|
| Públicos 2.255 / 208 / 924 / 11.366 | `prioridades.csv` | ✅ Somam 14.753 e R$ 405,5 mil |
| Poder do piloto | `numeros_deck.json`: taxa base de 6,4% de religamento em 60 dias | ❌ Novo: ≥ 6,9 p.p. com 200 por braço; ≥ 2,9 p.p. com ~1.127 |
| Público ampliado de hábito | `numeros_deck.json`: 1.783 mensais com ≤ 90 dias e renovação ligada | ⚠️ Proposta; sobrepõe públicos 2 e 4 |
| Cenários +R$ 277 / −R$ 281 | `cenarios_financeiros.csv` | ✅ Hipóteses, não previsão |

### Slide 7 — Orçamento

| Item | Origem e cálculo | Situação |
|---|---|---|
| Plano em fases | Premissas do case: e-mail R$ 0,01, CS R$ 18, WhatsApp R$ 0,40, mês grátis R$ 25, desconto R$ 11,97 | ❌ A versão anterior somava ofertas e canais que a estratégia não usava |
| Fase 0 R$ 47 | 1.127 e-mails (R$ 11) + 892 × 4 e-mails (R$ 36) | ✅ |
| Máximo sem IA R$ 17.138 a 24.320 | 47 + 6.000 + 11.091 (1º mês) ou 18.273 (3º) | ✅ Folga de R$ 15,7 a 22,9 mil para IA |

## 4. Inconsistências entre slides e tratamento

| # | Inconsistência | Tratamento |
|---|---|---|
| 1 | Duas receitas (caixa × equivalente) sem explicação | Glossário no slide 7; rótulos em cada slide |
| 2 | Três medidas de churn | Glossário; rodapés com a medida |
| 3 | Cartões misturam setembro com a coorte de julho | Rodapé do slide 3 declara a outra população |
| 4 | Gráfico "antes de sair" de outra base | Recalculado no script novo, sem depender de perfil |
| 5 | Orçamento com ofertas e canais fora da estratégia | Orçamento em fases condicionadas à evidência |
| 6 | Iniciativa de hábito com evidência ampla e público de 208 | Proposta de ampliar para 1.783 mensalistas novos |
| 7 | Cenários de ±2 a 5 p.p. indetectáveis com n=200 | Poder calculado e piloto redimensionado |
| 8 | R$ 5,2 mi (set × 12) | Receita de 12 meses, R$ 4,7 mi |

## 5. Entropia dos fatores

Desfecho: perda de acesso em 60 dias entre ativos na data de corte; atributos medidos só até o corte. A métrica é a informação mútua dividida pela entropia do desfecho (cerca de 0,5 bit): a parcela da incerteza que o fator elimina sozinho.

| Fator | 31/05 | 31/07 |
|---|---:|---:|
| Renovação desligada | 7,1% | 11,7% |
| Constância (84 dias) | 0,8% | 3,6% |
| Treinos (84 dias) | 1,3% | 3,4% |
| Tempo de casa | 2,0% | 2,0% |
| Plano | 7,2% | 1,9% |
| Evento do objetivo | 0,8% | 0,9% |
| Motivação | 0,5% | 0,9% |
| Conexões no corte | 0,1% | 0,0% |
| Sexo, idade, UF, relógio, nível | ≤ 0,2% | ≤ 0,1% |

Leitura: nenhum fator isolado passa de 12%; razão de risco alta (o evento chega a 2×) não significa muita informação quando o grupo é pequeno; renovação desligada é quase o próprio desfecho no mensal e serve como gatilho, não como explicação.

## 6. Melhorias pendentes

1. Redefinir na consolidação os públicos de prioridade para incluir os mensalistas novos sem perder a exclusividade.
2. Validar as datas de evento numa amostra rotulada de cerca de 200 textos (também por GenAI).
3. Mostrar as taxas por perfil na população de setembro quando houver desfecho observável, ou manter a coorte como quadro separado.
4. Calcular o custo de IA pela tabela oficial do provedor antes da Fase 1.
5. Usar o sinal exploratório da campanha (no mensal, cupom com −5,1 p.p. na saída composta) para desenhar o braço de oferta da Fase 2.
