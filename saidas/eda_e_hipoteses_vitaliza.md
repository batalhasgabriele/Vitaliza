# Relatório Executivo: Análise Exploratória de Dados (EDA) e Portfólio de Hipóteses MECE

> **Qualificação metodológica — 08/11/2026:** este relatório preserva a EDA histórica. As AUCs abaixo são discriminações retrospectivas com janelas alinhadas ao cancelamento/corte; não demonstram acurácia prospectiva. A curva de proporção de cancelados por duração não estima sobrevivência com censura. “Efeito”, “protetor” e “causal” devem ser lidos como associação ou hipótese a testar. Para conclusões executivas vigentes, consultar [o relatório da Semana 5](customer_segmentation_report_semana5.md).

**Projeto:** Vitaliza - Arquitetura de Retenção Preditiva  
**Liderança:** Camila Ferraz (VP de Crescimento e Retenção) & Cientista de Dados Líder  
**Data de Corte Oficial:** 30/09/2026 às 23:59:59 (Horário de Brasília)  
**Artefatos Relacionados:**
- Notebook de Código Reproduzível: `notebooks/02_eda_e_hipoteses.ipynb`
- Feature Store Ouro: `dados/processados/ouro/features_eda_corte_set2026.parquet`
- Log de Governança e Decisões: `decisoes.md`

---

## 1. Sumário Executivo e Diagnóstico de Negócio

O aplicativo Vitaliza enfrenta uma escalada contínua do churn mensal ao longo de 2026, com a taxa global passando de **5,6%** no início do ano para **6,6%** no encerramento do 3º trimestre, atingindo o pico crítico de **10,2%** nos planos mensais. A perda acelerada de receita líquida e o aumento do Custo de Aquisição de Clientes (CAC) exigem uma transição da reação passiva para uma **Arquitetura de Retenção Preditiva e Prescritiva**.

Esta Análise Exploratória de Dados (EDA) auditou integralmente as **32.583 assinaturas pagas** (expurgadas as 60 assinaturas de cortesia interna) e seus 1,25 milhão de treinos, interações sociais e eventos de cobrança registrados até 30/09/2026.

### Principais Conclusões Analíticas (Sincronizadas e Sem Vazamento Pós-Cancelamento):
1. **Desaceleração Aguda em `D-60` e `D-30` Antes do Cancelamento (e Assimetria Severa):**
   - Medindo estritamente durante os meses de vigência da assinatura (sem misturar meses inativos pós-cancelamento), usuários ativos registram mediana de **4,79 treinos/mês** (`média 6,41`, IQR `7,38`), enquanto cancelados registram mediana de **2,54 treinos/mês** (`média 4,66`, IQR `6,67`) — uma retração de **-46,9%** na vigência geral (`-38,9%` nos meses com treino `> 0`, onde a mediana é `6,00` vs. `3,67`).
   - O sinal mais forte, porém, ocorre nas **janelas móveis que antecedem o cancelamento (`D-60` e `D-30`, comparadas aos últimos 60 e 30 dias antes do corte `30/09/2026` para os ativos)**: quem permanece ativo mantém mediana de **8,00 treinos** tanto em `D-60` quanto em `D-30`, enquanto quem cancela já cai para mediana de **0,00 treino (`média 2,99`) entre 31 e 60 dias antes de cancelar (`D-60`)** e **0,00 treino (`média 1,78`) nos 30 dias finais antes do cancelamento (`D-30`)** — queda de **-100,0% na mediana**!
   - Já a duração individual de cada treino realizado na base limpa permanece idêntica entre quem fica e quem sai (`40,70 min` vs. `41,15 min`). O abandono decorre da **quebra recente do hábito semanal e da baixa diversidade de modalidades (`5,0` vs. `0,0` modalidades canônicas)**, e não da duração do treino.
2. **O "Vale da Morte" do Plano Mensal no M2 e M3:**
   - Enquanto o plano anual apresenta churn acumulado de **34,92%** (concentrado na renovação de 12 meses), o plano mensal acumula **67,91% de churn**.
   - No plano mensal, o churn atinge **64,71% no 1º mês**, saltando para **76,55% no 2º mês** e o ápice de **79,29% no 3º mês**. Após o 90º dia, quase 8 em cada 10 assinantes mensais abandonam a base.
3. **Diagnóstico do Ponto Cego de Cancelamento:**
   - **98,02% dos cancelamentos (17.477 de 17.830) são invisíveis para a pesquisa de saída do app.** Apenas 353 cancelamentos (1,98%) possuem preenchimento voluntário em `pesquisa_saida.csv`.
   - Nas lojas de aplicativos (App Store e Google Play), que respondem por **66,0% dos cancelamentos** (11.759 usuários), **0% responderam à pesquisa**, pois o cancelamento ocorre externamente nos ajustes do iOS/Android.
   - Além disso, **9,05% dos cancelamentos são estritamente involuntários** (1.321 por falhas definitivas de pagamento em cartão/pix e 292 por chargebacks).
4. **Poder Discriminatório Univariado Sem Vazamento Pós-Cancelamento (AUC-ROC):**
   - Foram expurgadas variáveis fixas no calendário de fim de período (`atividades_set26`, `atividades_ago26`) — que criavam falso sinal pós-cancelamento porque quem cancelou meses antes naturalmente tem zero treinos em setembro — e o próprio evento de saída (`desligou_renovacao`).
   - **Maiores sinais preditivos reais:** Diversidade de modalidades canônicas (`n_modalidades_distintas`, **AUC 0,8653**), treinos nos últimos 30 dias antes do cancelamento (`atividades_ultimos_30d`, **AUC 0,8488**), razão de uso recente `D-30` vs. média da vigência (`razao_uso_ultimo_mes`, **AUC 0,8458**) e treinos entre 31 e 60 dias antes do cancelamento (`atividades_31_a_60d`, **AUC 0,7636**).
   - **Sinais sociais e contratuais protetores (AUC 0,71 a 0,73):** Volume de posts no feed (**AUC 0,7315**), LTV pago bruto (**AUC 0,7267**) e curtidas recebidas (**AUC 0,7131**).
   - **Sinais nulos (AUC ~ 0,50):** Idade higienizada (**AUC 0,5088**), meta declarada no onboarding (**AUC 0,5050**) e presença de smartwatch (**AUC 0,5009**).

---

## 2. Tabelas Comparativas da EDA (Sincronizadas e Sem Vazamento Pós-Cancelamento — `01/11/2026`)

### 2.1 Perfilamento Robusto Durante a Vigência: Média (±DP), Mediana e Intervalo Interquartil (IQR)

| Variável Analisada | Ativo: Média (±DP) | Ativo: Mediana (IQR) | Cancelado: Média (±DP) | Cancelado: Mediana (IQR) | Variação Mediana (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Treinos nos Últimos 30d Antes do Cancelamento (D-30)** | 9,42 (±7,52) | **8,00 (10,00)** | 1,78 (±3,79) | **0,00 (2,00)** | **-100,0%** |
| **Treinos entre 31d e 60d Antes do Cancelamento (D-60)** | 8,43 (±7,33) | **8,00 (11,00)** | 2,99 (±5,87) | **0,00 (4,00)** | **-100,0%** |
| **Média de Atividades/Mês (Na Vigência)** | 6,41 (±5,72) | **4,79 (7,38)** | 4,66 (±5,42) | **2,54 (6,67)** | **-46,9%** |
| **Média de Atividades/Mês (Meses Ativos >0)** | 7,25 (±5,78) | **6,00 (7,86)** | 5,24 (±5,07) | **3,67 (6,57)** | **-38,9%** |
| **Minutos de Treino/Mês (Na Vigência)** | 283,72 (±287,89) | **194,83 (313,73)** | 209,43 (±274,36) | **107,83 (277,83)** | **-44,7%** |
| **Minutos de Treino/Mês (Meses Ativos >0)** | 321,43 (±295,43) | **241,25 (335,60)** | 234,52 (±260,24) | **154,05 (277,19)** | **-36,1%** |
| **Dias Ativos/Mês (Na Vigência)** | 5,29 (±4,07) | **4,30 (5,90)** | 3,87 (±4,04) | **2,50 (5,73)** | **-41,9%** |
| **Sessões no App/Mês (Na Vigência)** | 10,72 (±8,60) | **8,29 (10,92)** | 10,61 (±11,51) | **6,80 (14,00)** | **-17,9%** |
| **Proporção de Meses Ativos na Vigência** | 0,84 (±0,25) | **1,00 (0,25)** | 0,64 (±0,40) | **0,81 (0,75)** | **-18,8%** |
| **Modalidades Canônicas Distintas (7 máx)** | 4,71 (±1,28) | **5,00 (2,00)** | 1,60 (±2,10) | **0,00 (4,00)** | **-100,0%** |
| **Valor Médio Pago/Mês na Vigência (R$)** | 30,48 (±7,25) | **24,99 (13,80)** | 32,93 (±5,16) | **34,90 (9,91)** | **+39,6%** |
| **Média de Posts no Feed/Mês (Na Vigência)** | 0,49 (±0,39) | **0,43 (0,46)** | 0,31 (±0,42) | **0,14 (0,50)** | **-67,6%** |
| **Média de Curtidas Recebidas/Mês (Na Vigência)** | 3,37 (±2,80) | **2,95 (3,45)** | 2,34 (±3,26) | **0,92 (3,70)** | **-68,9%** |
| **Média de Treinos em Dupla/Mês (Na Vigência)** | 0,09 (±0,38) | **0,00 (0,00)** | 0,02 (±0,20) | **0,00 (0,00)** | **0,0%** |
| **Número de Seguidores na Comunidade** | 1,66 (±1,51) | **1,00 (2,00)** | 1,67 (±1,47) | **1,00 (2,00)** | **0,0%** |
| **Duração do Treino (min - Base Limpa)** | 43,78 (±14,54) | **40,70 (7,70)** | 44,86 (±16,57) | **41,15 (10,35)** | **+1,1%** |
| **Distância do Treino (km - Base Limpa)** | 8,02 (±7,86) | **5,69 (2,21)** | 8,57 (±8,59) | **5,99 (2,74)** | **+5,3%** |
| **Idade (Higienizada)** | 47,99 (±11,08) | **46,99 (15,44)** | 48,39 (±11,23) | **47,30 (15,48)** | **+0,7%** |

---

### 2.2 Sobrevivência e Cohorts: Churn por Lifetime, Plano e Canal

#### A. Curva de Churn por Tempo de Casa (Lifetime) e Plano Contratado

| Faixa de Lifetime | Plano Anual: Base | Plano Anual: Churn (%) | Plano Mensal: Base | Plano Mensal: Churn (%) | Churn Geral (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **0 meses (< 30 dias)** | 532 | 16,73% | 904 | 22,01% | **20,06%** |
| **1 mês (30 a 59 dias)** | 366 | 0,00% | 1.876 | **64,71%** | **54,15%** |
| **2 meses (60 a 89 dias)** | 338 | 0,00% | 2.047 | **76,55%** | **65,70%** |
| **3 meses (90 a 119 dias)** | 297 | 0,00% | 1.748 | **79,29%** | **67,78%** |
| **4 a 5 meses** | 724 | 0,00% | 3.010 | **76,11%** | **61,36%** |
| **6+ meses** | 10.770 | 41,41% | 9.971 | **66,43%** | **53,44%** |
| **Total Consolidado** | **13.027** | **34,92%** | **19.556** | **67,91%** | **54,72%** |

#### B. Churn por Canal de Cobrança e Intermediação

| Canal de Cobrança | Grupo de Canal | Base Total | Total Cancelados | Taxa de Churn (%) | Taxa de Intermediação |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **App Store (Apple)** | Lojas (Mobile) | 11.170 | 5.775 | **51,70%** | 15,0% |
| **Google Play (Android)**| Lojas (Mobile) | 10.948 | 5.984 | **54,66%** | 15,0% |
| **Web - Cartão de Crédito**| Meios Próprios Web | 7.087 | 4.093 | **57,75%** | 3,5% |
| **Web - Pix Automático** | Meios Próprios Web | 3.378 | 1.978 | **58,56%** | 0,99% |

---

### 2.3 Diagnóstico do Ponto Cego de Cancelamento

| Canal de Cobrança | Total Cancelados | Respondeu Pesquisa Saída | % Cobertura da Pesquisa | Falhas de Pagamento (Involuntário) | Chargebacks | % Ponto Cego Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **App Store** | 5.775 | 0 | **0,00%** | 249 | 95 | **100,0%** |
| **Google Play** | 5.984 | 0 | **0,00%** | 272 | 88 | **100,0%** |
| **Web - Cartão** | 4.093 | 225 | **5,50%** | 671 | 69 | **94,50%** |
| **Web - Pix** | 1.978 | 128 | **6,47%** | 129 | 40 | **93,53%** |
| **Total Vitaliza** | **17.830** | **353** | **1,98%** | **1.321 (7,41%)** | **292 (1,64%)** | **98,02%** |

---

### 2.4 Ranking de Poder Discriminatório Univariado (AUC-ROC — Sem Vazamento Pós-Cancelamento e Normalizado por Vigência)

| Galho MECE | Variável Preditora | Descrição Operacional | AUC-ROC | Direção do Efeito |
| :--- | :--- | :--- | :---: | :--- |
| **Uso** | `n_modalidades_distintas` | Diversidade de modalidades praticadas (7 canônicas) | **0,8653** | Reduz Churn (Protetor) |
| **Uso** | `atividades_ultimos_30d` | Treinos nos últimos 30 dias antes do cancelamento (`D-30`) | **0,8488** | Reduz Churn (Protetor) |
| **Uso** | `razao_uso_ultimo_mes` | Razão de uso recente (`D-30` vs. média da vigência) | **0,8458** | Reduz Churn (Protetor) |
| **Uso** | `atividades_31_a_60d` | Treinos entre 31 e 60 dias antes do cancelamento (`D-60`) | **0,7636** | Reduz Churn (Protetor) |
| **Social** | `media_posts_mes` | Média mensal de posts no feed durante a vigência | **0,6753** | Reduz Churn (Protetor) |
| **Contrato** | `eh_plano_anual` | Tipo de plano contratado (`Anual` vs. `Mensal`) | **0,6598** | Reduz Churn (Protetor) |
| **Social** | `media_curtidas_mes` | Média mensal de curtidas recebidas no feed na vigência | **0,6592** | Reduz Churn (Protetor) |
| **Uso** | `prop_meses_ativos_vigencia` | Proporção de meses com treino ativo durante a vigência | **0,6322** | Reduz Churn (Protetor) |
| **Uso** | `media_dias_ativos_mes` | Frequência média mensal de dias ativos na vigência | **0,6287** | Reduz Churn (Protetor) |
| **Uso** | `media_atividades_mes` | Média mensal de sessões de treino na vigência | **0,6272** | Reduz Churn (Protetor) |
| **Uso** | `media_video_mes` | Média mensal de treinos guiados em vídeo na vigência | **0,6243** | Reduz Churn (Protetor) |
| **Uso** | `media_minutos_mes` | Minutos médios de exercício por mês na vigência | **0,6237** | Reduz Churn (Protetor) |
| **Uso** | `media_ar_livre_mes` | Média mensal de treinos ao ar livre com GPS na vigência | **0,5887** | Reduz Churn (Protetor) |
| **Uso** | `media_sessoes_mes` | Aberturas do aplicativo por mês na vigência | **0,5585** | Reduz Churn (Protetor) |
| **Social** | `media_treinos_dupla_mes` | Média mensal de treinos realizados com parceiro na vigência | **0,5404** | Reduz Churn (Protetor) |
| **Contrato** | `receita_bruta_mensal` | Valor médio mensal pago na vigência (ticket mensal equivalente) | **0,5386** | Aumenta Churn |
| **Contrato** | `teve_carencia` | Usuário entrou em grace period de cobrança | **0,5362** | Aumenta Churn |
| **Contrato** | `pagamentos_recusados` | Histórico de tentativas de cobrança recusadas | **0,5309** | Aumenta Churn |
| **Contrato** | `eh_canal_loja` | Canal de cobrança (`Lojas Mobile` vs. `Meios Próprios Web`) | **0,5213** | Reduz Churn (Protetor) |
| **Entrada** | `idade` | Idade cronológica do assinante (higienizada) | **0,5088** | Nulo / Ruído |
| **Entrada** | `dias_semana_pretendidos` | Meta semanal autodeclarada no onboarding | **0,5050** | Nulo / Ruído |
| **Social** | `num_seguidores` | Conexões recebidas na rede social | **0,5042** | Nulo / Ruído |
| **Entrada** | `tem_relogio` | Integração ativa com Apple Watch / Garmin | **0,5009** | Nulo / Ruído |

---

## 3. Matriz Consolidada da Árvore de Hipóteses MECE

A metodologia MECE (*Mutually Exclusive, Collectively Exhaustive*) garante que nenhuma dimensão causal seja sobreposta ou negligenciada.

```
                              ÁRVORE DE CAUSA RAIZ DO CHURN
                                            │
      ┌──────────────────┬──────────────────┴──────────────────┬──────────────────┐
      ▼                  ▼                                     ▼                  ▼
  [GALHO 1]          [GALHO 2]                             [GALHO 3]          [GALHO 4]
Características    Comportamento de                      Ciclo de Vida       Comunidade e
  de Entrada              Uso                             e Contrato           Social
      │                  │                                     │                  │
 ├─ H1.1 (Onboarding)├─ H2.1 (Queda D-30/60)               ├─ H3.1 (M2/M3)    ├─ H4.1 (Feed)
 └─ H1.2 (Canais/Cup)└─ H2.2 (GPS vs Vídeo)                └─ H3.2 (Involunt) └─ H4.2 (Duplas)
```

| ID | Galho MECE | Afirmação Causal Resumida | Mecanismo Central | AUC Esperado |
| :--- | :--- | :--- | :--- | :---: |
| **H1.1** | Características de Entrada | Gap de Expectativa no Onboarding gera frustração rápida | Frustração cognitiva por meta irrealista não atingida no M1 | 0,62 - 0,68 |
| **H1.2** | Características de Entrada | Desconto de Cupom atrai usuário oportunista sem retenção | Ausência de disposição a pagar após expirar o cupom | 0,60 - 0,65 |
| **H2.1** | Comportamento de Uso | Desaceleração de Atividades em D-30 e D-60 antecipa saída | Perda do hábito precede a tomada de decisão formal | **0,87 - 0,92** |
| **H2.2** | Comportamento de Uso | Exclusividade em Vídeo Guiado gera fadiga de catálogo | Monotonia de vídeos vs. dinâmica imprevisível de rua com GPS | 0,65 - 0,70 |
| **H3.1** | Ciclo de Vida e Contrato | Vale da Morte do Plano Mensal no 2º e 3º mês | Falta de barreira financeira permite corte de custo de impulso | **0,75 - 0,80** |
| **H3.2** | Ciclo de Vida e Contrato | Fricção de Cobrança gera cancelamento involuntário silencioso | Cartões expirados e falhas Pix sem régua ativa de recuperação | 0,55 - 0,60 |
| **H4.1** | Comunidade e Social | Engajamento no Feed cria laços de pertencimento protetores | Validação social pública aumenta custo psicológico de saída | **0,71 - 0,75** |
| **H4.2** | Comunidade e Social | Treinos em Dupla/Grupo estabelecem compromisso interpessoal | Accountability mútuo impede que o corredor falte aos treinos | 0,55 - 0,60 |

---

## 4. Fichas Detalhadas das Hipóteses Analíticas

---

### [FICHA 1] Hipótese H1.1: Gap de Expectativa e Desilusão no Onboarding
- **1. Galho da Árvore MECE:** Galho 1: Características de Entrada (Quem entrou?)
- **2. Afirmação Causal:** Usuários que declaram metas ambiciosas no onboarding ($\ge 4$ dias/semana), mas realizam menos de 2 treinos por semana nas primeiras 4 semanas de assinatura, sofrem dissonância cognitiva/frustração e apresentam probabilidade significativamente maior de cancelamento precoce ($\le 60$ dias).
- **3. Colunas Utilizadas:**
  - `onboarding.csv`: `dias_por_semana` (convertido para numérico), `nivel`, `respondido_em`.
  - `atividades.parquet`: `user_id`, `inicio`, `atividade_id`.
  - `assinaturas.csv`: `inicio`, `status_atual`, `data_fim`.
- **4. Métrica Objetiva:**
  $$\text{Gap de Cumprimento} = \text{Dias Pretendidos} - \text{Frequência Real M1}$$
  Comparação do churn rate entre assinantes com $\text{Gap} \ge 2$ versus assinantes com $\text{Gap} \le 0$ no primeiro ciclo.
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** O churn rate nos primeiros 60 dias dos usuários com $\text{Gap} \ge 2$ não for pelo menos **30% superior** ao dos usuários realistas/cumpridores ($\text{Gap} \le 0$), com $p\text{-valor} < 0,01$.
- **6. O que a variável NÃO mede:** Não mede fatores de saúde externa, lesões ortopédicas ou mudanças imprevistas na rotina de trabalho/pessoal do usuário.
- **7. Riscos e Governança:**
  - *Vazamento Temporal:* Métricas de frequência devem ser restritas exclusivamente aos primeiros 28 dias após a data de `inicio` da assinatura.
  - *Viés de Seleção vs. Causalidade:* Usuários que declaram metas altas podem ter perfil perfeccionista (variável omitida de personalidade).
  - *Conformidade LGPD:* A meta de treino é dado pessoal autodeclarado; seu uso deve ser restrito à customização da régua de boas-vindas do app (Art. 6º, I da LGPD).

---

### [FICHA 2] Hipótese H1.2: Oportunismo de Cupom e Sensibilidade de Preço
- **1. Galho da Árvore MECE:** Galho 1: Características de Entrada (Quem entrou?)
- **2. Afirmação Causal:** Assinantes atraídos via campanhas de influenciadores com cupom de desconto inicial (plano anual de R$ 239,90) possuem propensão desproporcionalmente maior ao cancelamento na primeira renovação (12 meses) devido à baixa disposição a pagar o valor integral (R$ 299,90).
- **3. Colunas Utilizadas:**
  - `pagamentos.csv`: `valor`, `data_hora`, `metodo`, `status`.
  - `assinaturas.csv`: `plano_atual`, `inicio`, `data_fim`, `status_atual`.
  - `usuarios.csv`: `canal_aquisicao`.
- **4. Métrica Objetiva:** Taxa de churn na renovação anual (lifetime 12 meses) comparando usuários com primeiro pagamento de R$ 239,90 (cupom) vs. R$ 299,90 (sem desconto).
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** O churn de 12 meses dos usuários de cupom não exceder o dos assinantes integrais em pelo menos **15 pontos percentuais** ($p < 0,05$).
- **6. O que a variável NÃO mede:** Não mede a capacidade financeira individual ou renda do assinante.
- **7. Riscos e Governança:**
  - *Vazamento Temporal:* O valor do 1º pagamento é estático na entrada; sem risco temporal.
  - *Conformidade LGPD:* Totalmente aderente (dado transacional e financeiro interno).

---

### [FICHA 3] Hipótese H2.1: Desaceleração Precoce da Frequência de Treino (D-30 a D-60)
- **1. Galho da Árvore MECE:** Galho 2: Comportamento de Uso (O que faz no app?)
- **2. Afirmação Causal:** O cancelamento formal da assinatura não é um evento súbito, mas o desfecho de um processo gradual de abandono de hábito caracterizado pela queda de $\ge 50\%$ na frequência mensal de treinos já em D-60 e D-30 antes da renovação.
- **3. Colunas Utilizadas:**
  - `uso_mensal.csv`: `atividades`, `dias_ativos`, `minutos`, `mes`.
  - `assinaturas.csv`: `data_fim`, `status_atual`, `plano_atual`.
- **4. Métrica Objetiva:**
  $$\Delta \text{Uso} = \frac{\text{Atividades}_{\text{Mês } t} - \text{Atividades}_{\text{Mês } t-1}}{\text{Atividades}_{\text{Mês } t-1} + 1}$$
  AUC univariado da variação relativa de treinos em relação ao churn do ciclo subsequente.
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** O AUC-ROC da frequência/variação de uso em `D-30` e `D-60` antes do desfecho for inferior a **0,75**, demonstrando que o abandono não emite sinal antecipado mensurável. (Na nossa EDA blindada contra vazamento pós-saída, `atividades_ultimos_30d` atingiu **AUC = 0,8488**, `razao_uso_ultimo_mes` atingiu **AUC = 0,8458** e `atividades_31_a_60d` atingiu **AUC = 0,7636**, validando fortemente a hipótese).
- **6. O que a variável NÃO mede:** Não diferencia inatividade por desmotivação de inatividade temporária por viagens de férias ou lesões.
- **7. Riscos e Governança:**
  - *Vazamento Temporal:* A janela de cálculo deve ser rigorosamente defasada ($t-1$ e $t-2$) em relação à data do desfecho.
  - *Causalidade Reversa:* O desinteresse causa a falta de treino, ou a falta de treino gera o desinteresse? Ambas convergem para o mesmo gatilho de CRM.

---

### [FICHA 4] Hipótese H2.2: Monotonia e Fadiga de Conteúdo em Treinos Guiados por Vídeo
- **1. Galho da Árvore MECE:** Galho 2: Comportamento de Uso (O que faz no app?)
- **2. Afirmação Causal:** Usuários cuja prática se restringe a vídeos guiados dentro de casa sofrem fadiga de catálogo e estagnação motora mais rapidamente do que praticantes de corrida ao ar livre com GPS, apresentando menor retenção no longo prazo.
- **3. Colunas Utilizadas:**
  - `uso_mensal.csv`: `atividades_ar_livre`, `atividades_video`, `minutos`.
  - `atividades.parquet`: `tipo`, `gps_ok`.
  - `assinaturas.csv`: `status_atual`, `lifetime_dias`.
- **4. Métrica Objetiva:** Proporção de atividades em vídeo:
  $$\text{Mix Vídeo} = \frac{\text{atividades\_video}}{\text{atividades\_ar\_livre} + \text{atividades\_video} + 0.01}$$
  Hazard Ratio de churn para usuários com $\text{Mix Vídeo} > 0,80$ vs. $\text{Mix Vídeo} < 0,20$.
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** Assinantes com dominância de vídeo ($\ge 80\%$) tiverem lifetime médio igual ou superior ao de corredores de rua com GPS ($p > 0,05$).
- **6. O que a variável NÃO mede:** Não avalia a satisfação com a qualidade da trilha sonora ou dos instrutores dos vídeos.
- **7. Riscos e Governança:**
  - *Vazamento Temporal:* O mix deve ser acumulado até a data de corte sem incorporar treinos futuros.

---

### [FICHA 5] Hipótese H3.1: O "Vale da Morte" do Plano Mensal no 2º e 3º Ciclos
- **1. Galho da Árvore MECE:** Galho 3: Ciclo de Vida e Contrato (Há quanto tempo e qual vínculo?)
- **2. Afirmação Causal:** A ausência de barreira de saída financeira no plano mensal faz com que qualquer atrito pontual de rotina resulte em cancelamento no 2º ou 3º ciclo de renovação (M2/M3), momento em que o entusiasmo inicial arrefece.
- **3. Colunas Utilizadas:**
  - `assinaturas.csv`: `plano_atual`, `inicio`, `data_fim`, `status_atual`.
  - `eventos_assinatura.csv`: `evento` (`renovacao`, `assinatura_expirada`).
- **4. Métrica Objetiva:** Churn rate condicional em cada ciclo mensal: $P(\text{Churn no Ciclo } k \mid \text{Sobreviveu até } k-1)$.
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** A taxa de churn no 2º e 3º ciclos do plano mensal não for pelo menos **o dobro** da taxa de churn do 6º ciclo em diante. (Na nossa EDA, o churn no M2 é de **76,55%** e no M3 é de **79,29%**, contra 66,43% em 6+ meses, comprovando a hipótese).
- **6. O que a variável NÃO mede:** Não mede elasticidade de preço unitário (R$ 39,90 vs. outros valores) por falta de grupo de controle de preços.
- **7. Riscos e Governança:**
  - *Vazamento Temporal:* Controlar pela data de contratação (cohort).

---

### [FICHA 6] Hipótese H3.2: Ponto Cego de Cancelamento Involuntário por Falhas de Gateway
- **1. Galho da Árvore MECE:** Galho 3: Ciclo de Vida e Contrato (Há quanto tempo e qual vínculo?)
- **2. Afirmação Causal:** Uma parcela expressiva dos cancelamentos na web e nas stores ocorre por expiração silenciosa de cartões de crédito e falhas no Pix Automático, sem que o assinante tenha demonstrado intenção consciente de cancelar.
- **2. Colunas Utilizadas:**
  - `assinaturas.csv`: `motivo_fim`, `canal_cobranca`.
  - `pagamentos.csv`: `status`, `tentativa`, `metodo`.
  - `eventos_assinatura.csv`: `periodo_carencia`.
- **4. Métrica Objetiva:** Proporção de cancelamentos com `motivo_fim == 'falha_pagamento'` e volume de retentativas recusadas em D-7 antes do encerramento.
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** As falhas definitivas de cobrança representarem menos de **5,0%** dos cancelamentos totais da base. (Na EDA, representam **7,41%**, com 1.321 casos confirmados, superando o critério).
- **6. O que a variável NÃO mede:** Não mede se o usuário deliberadamente bloqueou o cartão para forçar o cancelamento em vez de clicar na interface.
- **7. Riscos e Governança:**
  - *Segurança e Privacidade:* Respeito integral às normas PCI-DSS (não registrar CVV ou números de cartão) e LGPD.

---

### [FICHA 7] Hipótese H4.1: Blindagem de Retenção pelo Engajamento Social no Feed
- **1. Galho da Árvore MECE:** Galho 4: Comunidade e Social (Está conectado a outros?)
- **2. Afirmação Causal:** Assinantes que compartilham corridas no feed e recebem incentivo social (curtidas e comentários) constroem identidade de corredor e têm custo psicológico de abandono mais alto, reduzindo substancialmente o churn.
- **3. Colunas Utilizadas:**
  - `feed_posts.csv`: `post_id`, `user_id`, `curtidas`, `data_hora`.
  - `amizades.csv`: `seguidor_id`, `seguido_id`.
  - `assinaturas.csv`: `status_atual`, `churn`.
- **4. Métrica Objetiva:**
  $$\text{Interações Sociais} = \text{Total Posts} \times 2 + \text{Total Curtidas Recebidas}$$
  AUC-ROC da métrica em relação ao churn.
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** O AUC-ROC de curtidas e posts por mês na vigência for inferior a **0,65**, indicando que conexões sociais no feed são neutras em relação à longevidade do contrato. (Na nossa EDA normalizada pela vigência, `media_posts_mes` atingiu AUC de **0,6753** e `media_curtidas_mes` **0,6592**, confirmando o efeito protetor mesmo descontando o tempo de casa).
- **6. O que a variável NÃO mede:** Não mede interações em grupos de WhatsApp externos ao app Vitaliza.
- **7. Riscos e Governança:**
  - *Viés de Confundimento:* Usuários mais disciplinados postam mais (efeito seleção). Necessário pareamento por escore de propensão (Propensity Score Matching).
  - *LGPD:* Respeito ao Art. 6º, IX (não discriminação no feed social).

---

### [FICHA 8] Hipótese H4.2: Efeito Rede Operacional de Treinos em Dupla ou Grupo
- **1. Galho da Árvore MECE:** Galho 4: Comunidade e Social (Está conectado a outros?)
- **2. Afirmação Causal:** Corredores que realizam treinos acompanhados por outros assinantes (`treino_com != ""`) estabelecem compromisso interpessoal (*accountability*) que impede o abandono dos treinos e blindam a assinatura contra cancelamento.
- **3. Colunas Utilizadas:**
  - `atividades.parquet`: `treino_com`, `user_id`, `inicio`.
  - `assinaturas.csv`: `status_atual`, `lifetime_dias`.
- **4. Métrica Objetiva:** Churn rate entre assinantes com pelo menos 1 treino em dupla ($\text{treinos\_em\_dupla} \ge 1$) versus praticantes exclusivamente individuais ($\text{treinos\_em\_dupla} == 0$).
- **5. Critério de Refutação Pré-estabelecido:**
  > **Cai se:** A taxa de churn de praticantes com treinos em dupla não for pelo menos **20% menor** do que a de corredores exclusivamente solitários ($p < 0,01$).
- **6. O que a variável NÃO mede:** Não captura treinos com amigos que usam outros apps (ex.: Strava, Garmin Connect) e não estão cadastrados na Vitaliza.
- **7. Riscos e Governança:**
  - *Tratamento de Inconsistência:* Conforme Decisão 004 em `decisoes.md`, treinos solo possuem `treino_com == ""` (string vazia), exigindo filtro estrito.

---

## 5. EDA Parte 2 — Subida do Churn e Marcos de 2026

A análise reproduzível completa está em [`saidas/eda_etapa3_marcos_2026.md`](eda_etapa3_marcos_2026.md), gerada por `src/analisar_eda_marcos.py`.

### 5.1 Série mensal

![Churn mensal](churn_mensal_2025_2026.png)

1. **O dado diz:** a reconstrução observa churn médio de **5,68% em 2025** e **6,68% em jan–set/2026**, com pico de **8,13% e 1.158 perdas em abril**.
2. **O dado não diz:** a diferença de quatro perdas frente à referência executiva de 1.154 não autoriza correção manual; preço, sazonalidade e composição de coortes continuam confundidos.
3. **Próxima pergunta:** quais segmentos comportamentais concentram a elevação sem usar churn para formar os clusters?

### 5.2 Três marcos

![Três marcos de 2026](marcos_2026.png)

- **Reajuste de 01/03:** o plano mensal passou de média de **10,22%** em jan–fev para **12,97%** em mar–abr. É associação antes/depois, não elasticidade causal.
- **Pesquisa desde 01/06:** foram observadas **3.389 expirações** entre jun–set (**2.271 lojas; 1.118 Web**) e **641 respondentes únicos**, todos Web; **288 respondentes únicos** ainda estavam ativos no corte (**289 respostas**).
- **Campanha de 10/08:** no ITT de 30 dias, controle teve **5,48%**, desafio **5,18%**, cupom **4,64%** e conteúdo **6,13%**. Cupom ficou **−0,84 p.p.** frente ao controle, mas **p=0,108**; nenhum braço atingiu significância de 5%.

### 5.3 Controles estatísticos

![Outliers por modalidade](outliers_por_modalidade.png)

![Correlação controlada](correlacao_controlada.png)

- A regra global de Tukey marca **81.775** treinos acima de 17,08 km, mas **73.120 são pedal**; distância alta não equivale automaticamente a erro.
- Entre contas com treino, `r(sessoes_app, minutos)=0,88`; após controlar o número de atividades, a correlação parcial cai para **0,02**.
- Esses resultados sustentam o uso de variáveis comportamentais controladas por exposição e modalidade na futura segmentação.

---

## 6. Segmentação dos 14.753 pagantes ativos

A clusterização não supervisionada foi executada sem churn, informação de saída, pesquisa ou campanha. Entre `k=3` e `k=4`, a solução de três segmentos apresentou o melhor silhouette elegível (**0,164**) e estabilidade quase perfeita por reamostragem (**ARI=0,998**), mantendo o menor grupo com **13,4%** da base.

- **Ativos ao ar livre:** 7.457 clientes (50,55%), recência mediana de 2 dias e 82,3% das atividades ao ar livre.
- **Ativos guiados por vídeo:** 5.317 (36,04%), recência de 2 dias e 92,2% das atividades em vídeo.
- **Adormecidos sem hábito:** 1.979 (13,41%), zero treino mediano em 30 dias e recência de 68 dias.

![Perfis dos segmentos](segmentacao_heatmap_perfis.png)

A separação entre os dois grupos ativos é moderada/baixa e aparece principalmente no modo de treino. A segmentação é descritiva e acionável, mas não deve ser interpretada como modelo de churn ou prova de causalidade.

## 7. Diretrizes de Governança, Ética e Conformidade com a LGPD

O pipeline de retenção preditiva manipula dados pessoais e comportamentais sensíveis (frequência de exercícios, localização geográfica por GPS e interações sociais). A modelagem deve atender aos seguintes mandamentos:

1. **Princípio da Não Discriminação (Art. 6º, IX da LGPD):**
   - É estritamente vedado utilizar modelos preditivos para negar serviços, aplicar reajustes punitivos ou degradar funcionalidades com base em dados demográficos sensíveis ou idade avançada.
   - Constatamos na EDA que **a idade possui poder preditivo univariado praticamente nulo (AUC 0,5088 após higienização)**, assim como o sexo e o modelo do smartwatch (AUC ~0,5009). Tais variáveis demográficas devem ser excluídas dos modelos finais para evitar viés algorítmico espúrio.
2. **Direito à Explicação e Revisão Humana (Art. 20 da LGPD):**
   - Todo assinante pontuado pelo modelo preditivo com alto risco de churn tem direito a compreender os critérios gerais da sua pontuação (ex.: explicabilidade via valores SHAP no nível individual).
   - Nenhuma decisão extrema (como rescisão contratual unilateral) pode ser tomada de forma 100% automatizada.
3. **Prevenção de Decisões Danosas em CRM (Evitar "Despertar Cães Adormecidos"):**
   - A modelagem de retenção deve ser acoplada a um modelo de **Uplift / Prescrição**. Clientes com baixa utilização que continuam pagando sem atrito não devem receber notificações agressivas de cancelamento, prevenindo churn induzido pela própria intervenção.
4. **Isolamento de Dados de Saúde e GPS:**
   - As imagens de mapas em `heatmaps/` e as coordenadas de rotas só podem ser processadas com anonimização espacial (expurgo do ponto de partida/chegada residencial) para evitar inferência de endereço doméstico do usuário.

---

## 8. Próximos Passos Recomendados para a Squad

1. **Validação do Pipeline de Modelagem Preditiva:**
- Submeter a base Ouro `dados/processados/ouro/features_eda_corte_set2026.parquet` ao benchmark de algoritmos (LightGBM vs. XGBoost vs. Regressão Logística com regularização).
   - Utilizar validação cruzada temporal (Time-Series Split) para blindagem total contra vazamento de dados.
2. **Implantação da Régua de Recuperação de Ponto Cego (CRM & Meios de Pagamento):**
   - Desenhar régua de contato emergencial para os 1.321 casos de cancelamento involuntário por falha de cartão/pix antes de entrarem em churn definitivo.
   - Estruturar notificações in-app para usuários em risco antes que desliguem a renovação automática nas lojas de aplicativos.
