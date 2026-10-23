# Inventário dos Dados Brutos e Auditoria do Dicionário - Projeto Vitaliza

**Data de Execução:** 22/10/2026  
**Ambiente:** `dev`  
**Data de Corte Oficial:** 30/09/2026  
**Referência Oficial:** `docs/Vitaliza - Dicionário de dados.pdf`  

> **Governança:** Todos os arquivos de `dados/brutos/` foram inspecionados estritamente em modo somente leitura (*read-only*), preservando integralmente o estado original dos dados brutos.

---

## 1. Visão Geral e Comparativo com o Dicionário de Dados

| Seção | Arquivo | Entidade / Linha | Linhas Reais | Linhas Dicionário | Diff Linhas | Colunas Reais | Colunas Dicionário | Status Linhas | Status Colunas |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02 | `usuarios.csv` | conta | 64.948 | 64.948 | 0 | 12 | 12 | ✅ Conforme | ✅ Conforme |
| 03 | `assinaturas.csv` | assinatura | 32.643 | 32.643 | 0 | 9 | 9 | ✅ Conforme | ✅ Conforme |
| 04 | `amizades.csv` | relação de seguir | 113.480 | 113.480 | 0 | 3 | 3 | ✅ Conforme | ✅ Conforme |
| 05 | `campanha_ago26.csv` | assinante sorteado | 14.120 | 14.120 | 0 | 9 | 9 | ✅ Conforme | ✅ Conforme |
| 06 | `eventos_assinatura.csv` | evento | 275.565 | 275.565 | 0 | 6 | 6 | ✅ Conforme | ✅ Conforme |
| 07 | `pagamentos.csv` | cobrança | 165.548 | 165.548 | 0 | 7 | 7 | ✅ Conforme | ✅ Conforme |
| 08 | `uso_mensal.csv` | usuário e mês | 591.662 | 591.662 | 0 | 8 | 8 | ✅ Conforme | ✅ Conforme |
| 09 | `atividades.parquet` | treino | 1.254.475 | 1.254.475 | 0 | 11 | 11 | ✅ Conforme | ✅ Conforme |
| 10 | `onboarding.csv` | conta | 63.929 | 63.929 | 0 | 7 | 7 | ✅ Conforme | ✅ Conforme |
| 11 | `pesquisa_saida.csv` | resposta | 643 | 643 | 0 | 5 | 5 | ✅ Conforme | ✅ Conforme |
| 12 | `feed_posts.csv` | post | 119.309 | 119.309 | 0 | 5 | 5 | ✅ Conforme | ✅ Conforme |
| 13 | `tickets_suporte.csv` | chamado | 4.422 | 4.422 | 0 | 8 | 8 | ✅ Conforme | ✅ Conforme |

### Mapas de Calor (`heatmaps`)
| Corte Temporal | Arquivo Compactado | Imagens Reais (.png) | Imagens Dicionário | Diferença | Amostra de Exemplo | Status |
|:---:|:---|:---:|:---:|:---:|:---|:---:|
| 2026-07-31 | `heatmaps_2026-07-31.zip` | 12.431 | 12.426 | +5 | `2026-07-31/u_0aa0410a.png` | ⚠️ Divergente (+5) |
| 2026-09-30 | `heatmaps_2026-09-30.zip` | 13.047 | 13.047 | 0 | `2026-09-30/u_0aa0410a.png` | ✅ Conforme |

---

## 2. Inventário Detalhado por Arquivo

### 2.2 `usuarios.csv` (Seção 02)
- **Conceito:** 1 linha por **conta**.
- **Volume:** 64.948 linhas x 12 colunas (Dicionário: 64.948 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_997536a0` | - |
| `email` | `str` | string / email | 0 | 0 | 0 | 0.00% | `leticiamendes15@hotmail.com` | - |
| `data_cadastro` | `str` | datetime | 0 | 0 | 0 | 0.00% | `2026-03-29 10:36:50` | - |
| `data_nascimento` | `str` | date | 3.301 | 0 | 3.301 | 5.08% | `1992-07-21` | - |
| `sexo` | `str` | string (categórico: M/F) | 3.142 | 0 | 3.142 | 4.84% | `F` | - |
| `cidade` | `str` | string | 0 | 0 | 0 | 0.00% | `Santos` | - |
| `uf` | `str` | string (UF) | 0 | 0 | 0 | 0.00% | `SP` | - |
| `cep_prefixo` | `float64` | numeric / integer (3 dígitos) | 1.894 | 0 | 1.894 | 2.92% | `110.0` | Armazenado como float64 devido a NaNs; perdeu formatação de 3 dígitos (ex: 110.0) |
| `canal_aquisicao` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `meta_ads` | - |
| `sistema` | `str` | string (ios/android) | 0 | 0 | 0 | 0.00% | `android` | - |
| `versao_app` | `str` | string (versão semver) | 0 | 0 | 0 | 0.00% | `5.1.0` | - |
| `relogio_conectado` | `str` | string (garmin/apple_watch/nenhum) | 0 | 0 | 0 | 0.00% | `nenhum` | - |


### 2.3 `assinaturas.csv` (Seção 03)
- **Conceito:** 1 linha por **assinatura**.
- **Volume:** 32.643 linhas x 9 colunas (Dicionário: 32.643 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `assinatura_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `s_000000` | - |
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_f4d898b7` | - |
| `plano_atual` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `anual` | - |
| `canal_cobranca` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `app_store` | - |
| `inicio` | `str` | date | 0 | 0 | 0 | 0.00% | `2023-10-25` | - |
| `status_atual` | `str` | string (ativa/cancelada) | 0 | 0 | 0 | 0.00% | `ativa` | - |
| `renovacao_automatica` | `str` | string / boolean (sim/nao) | 0 | 0 | 0 | 0.00% | `nao` | - |
| `data_fim` | `str` | date | 14.813 | 0 | 14.813 | 45.38% | `2025-08-12` | - |
| `motivo_fim` | `str` | string (categórico) | 14.813 | 0 | 14.813 | 45.38% | `renovacao_desligada` | - |


### 2.4 `amizades.csv` (Seção 04)
- **Conceito:** 1 linha por **relação de seguir**.
- **Volume:** 113.480 linhas x 3 colunas (Dicionário: 113.480 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `seguidor_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_24a5509e` | - |
| `seguido_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_d24b134d` | - |
| `desde` | `str` | date | 0 | 0 | 0 | 0.00% | `2020-10-26` | - |


### 2.5 `campanha_ago26.csv` (Seção 05)
- **Conceito:** 1 linha por **assinante sorteado**.
- **Volume:** 14.120 linhas x 9 colunas (Dicionário: 14.120 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_f4d898b7` | - |
| `grupo` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `conteudo` | - |
| `enviado_em` | `str` | datetime | 3.579 | 0 | 3.579 | 25.35% | `2026-08-10 10:00:00` | - |
| `canal` | `str` | string | 3.579 | 0 | 3.579 | 25.35% | `push+email` | - |
| `titulo_mensagem` | `str` | string | 3.579 | 0 | 3.579 | 25.35% | `Seu plano de treino personalizado está pronto` | - |
| `oferta` | `str` | string | 10.648 | 0 | 10.648 | 75.41% | `1_mes_gratis` | - |
| `abriu_push` | `bool` | boolean | 0 | 0 | 0 | 0.00% | `True` | - |
| `abriu_email` | `bool` | boolean | 0 | 0 | 0 | 0.00% | `False` | - |
| `clicou` | `bool` | boolean | 0 | 0 | 0 | 0.00% | `False` | - |


### 2.6 `eventos_assinatura.csv` (Seção 06)
- **Conceito:** 1 linha por **evento**.
- **Volume:** 275.565 linhas x 6 colunas (Dicionário: 275.565 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_520b225e` | - |
| `data_hora` | `str` | datetime (misto com fuso) | 0 | 0 | 0 | 0.00% | `2024-07-01T22:22:27Z` | Fusos mistos: UTC terminado em 'Z' (lojas) e sem fuso / UTC-3 (meios próprios) |
| `evento` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `trial_iniciado` | - |
| `plano` | `str` | string (categórico) | 72.873 | 0 | 72.873 | 26.44% | `mensal` | - |
| `canal_cobranca` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `google_play` | - |
| `detalhe` | `str` | string | 269.494 | 0 | 269.494 | 97.80% | `falha_pagamento` | - |


### 2.7 `pagamentos.csv` (Seção 07)
- **Conceito:** 1 linha por **cobrança**.
- **Volume:** 165.548 linhas x 7 colunas (Dicionário: 165.548 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `pagamento_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `p_0000000` | - |
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_6c7fd4bc` | - |
| `data_hora` | `str` | datetime (misto com fuso) | 0 | 0 | 0 | 0.00% | `2024-07-02T13:27:50Z` | Fusos mistos: UTC terminado em 'Z' (lojas) e sem fuso / UTC-3 (meios próprios) |
| `valor` | `str` | float / numeric | 0 | 0 | 0 | 0.00% | `34.90` | Valores mistos: strings com 'R$ X,XX' (19.750 casos) e números decimais 'X.XX' |
| `metodo` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `app_store` | - |
| `status` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `aprovado` | - |
| `tentativa` | `int64` | integer | 0 | 0 | 0 | 0.00% | `1` | - |


### 2.8 `uso_mensal.csv` (Seção 08)
- **Conceito:** 1 linha por **usuário e mês**.
- **Volume:** 591.662 linhas x 8 colunas (Dicionário: 591.662 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_f4d898b7` | - |
| `mes` | `str` | date / period | 0 | 0 | 0 | 0.00% | `2025-01` | - |
| `atividades` | `int64` | integer | 0 | 0 | 0 | 0.00% | `1` | - |
| `atividades_ar_livre` | `int64` | integer | 0 | 0 | 0 | 0.00% | `0` | - |
| `atividades_video` | `int64` | integer | 0 | 0 | 0 | 0.00% | `1` | - |
| `minutos` | `int64` | integer | 0 | 0 | 0 | 0.00% | `28` | - |
| `dias_ativos` | `int64` | integer | 0 | 0 | 0 | 0.00% | `1` | - |
| `sessoes_app` | `int64` | integer | 0 | 0 | 0 | 0.00% | `2` | - |


### 2.9 `atividades.parquet` (Seção 09)
- **Conceito:** 1 linha por **treino**.
- **Volume:** 1.254.475 linhas x 11 colunas (Dicionário: 1.254.475 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `atividade_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `a_0201284` | - |
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_5bea0f50` | - |
| `inicio` | `str` | datetime | 0 | 0 | 0 | 0.00% | `2026-01-01 05:00:00` | - |
| `tipo` | `str` | string (corrida/caminhada/pedal/funcional/yoga/etc.) | 0 | 0 | 0 | 0.00% | `corrida` | - |
| `duracao_min` | `float64` | float | 0 | 0 | 0 | 0.00% | `46.0` | - |
| `distancia_km` | `float64` | float | 574.835 | 0 | 574.835 | 45.82% | `7.67` | - |
| `ritmo_min_km` | `float64` | float | 582.290 | 0 | 582.290 | 46.42% | `6.0` | - |
| `fc_media` | `float64` | float / integer | 764.987 | 0 | 764.987 | 60.98% | `162.0` | - |
| `origem` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `apple_health` | - |
| `gps_ok` | `bool` | boolean | 0 | 0 | 0 | 0.00% | `True` | - |
| `treino_com` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_c1ba241b` | - |


### 2.10 `onboarding.csv` (Seção 10)
- **Conceito:** 1 linha por **conta**.
- **Volume:** 63.929 linhas x 7 colunas (Dicionário: 63.929 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `onboarding_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `o_000000` | - |
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_f4d898b7` | - |
| `respondido_em` | `str` | date | 0 | 0 | 0 | 0.00% | `2023-10-18` | - |
| `objetivo_texto` | `str` | string (texto livre) | 5.467 | 0 | 5.467 | 8.55% | `ok` | - |
| `como_conheceu` | `str` | string (texto livre) | 4.586 | 0 | 4.586 | 7.17% | `ok` | - |
| `nivel` | `str` | string (categórico) | 4.513 | 0 | 4.513 | 7.06% | `iniciante` | - |
| `dias_por_semana` | `str` | string / integer | 6.368 | 0 | 6.368 | 9.96% | `3` | - |


### 2.11 `pesquisa_saida.csv` (Seção 11)
- **Conceito:** 1 linha por **resposta**.
- **Volume:** 643 linhas x 5 colunas (Dicionário: 643 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `resposta_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `q_00000` | - |
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_e2e082a4` | - |
| `respondido_em` | `str` | date | 0 | 0 | 0 | 0.00% | `2026-06-01` | - |
| `motivo_principal` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `preco` | - |
| `comentario` | `str` | string (texto livre) | 183 | 0 | 183 | 28.46% | `era só até a formatura` | - |


### 2.12 `feed_posts.csv` (Seção 12)
- **Conceito:** 1 linha por **post**.
- **Volume:** 119.309 linhas x 5 colunas (Dicionário: 119.309 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `post_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `f_0069439` | - |
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_825e8b99` | - |
| `data_hora` | `str` | datetime | 0 | 0 | 0 | 0.00% | `2025-07-01 06:07:55` | - |
| `texto` | `str` | string (texto livre com emojis) | 0 | 0 | 0 | 0.00% | `perna destruída 😂` | - |
| `curtidas` | `int64` | integer | 0 | 0 | 0 | 0.00% | `3` | - |


### 2.13 `tickets_suporte.csv` (Seção 13)
- **Conceito:** 1 linha por **chamado**.
- **Volume:** 4.422 linhas x 8 colunas (Dicionário: 4.422 linhas).

| Coluna | Tipo Real (Pandas) | Tipo Dicionário | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Exemplo de Dado | Observações |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| `ticket_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `t_000368` | - |
| `user_id` | `str` | string / id | 0 | 0 | 0 | 0.00% | `u_2e176106` | - |
| `aberto_em` | `str` | datetime | 0 | 0 | 0 | 0.00% | `2025-07-01 19:56:00` | - |
| `canal` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `email` | - |
| `texto_cliente` | `str` | string (texto livre) | 0 | 0 | 0 | 0.00% | `cobraram duas vezes?? quero entender` | - |
| `categoria_atendente` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `cobranca` | - |
| `status` | `str` | string (categórico) | 0 | 0 | 0 | 0.00% | `aberto` | - |
| `resolvido_em` | `str` | datetime | 1.505 | 0 | 1.505 | 34.03% | `2025-07-03` | - |


---

## 3. Matriz Consolidada de Divergências, Anomalias e Pontos de Atenção

A comparação rigorosa entre o que está documentado no `Vitaliza: dicionário de dados` e a realidade física dos arquivos brutos revelou as seguintes inconsistências e particularidades técnicas:

### 3.1 Divergência na Contagem de Imagens dos Mapas de Calor (`heatmaps`)
- **Corte 31/07/2026 (`heatmaps_2026-07-31.zip`):**
  - O dicionário documenta **12.426 imagens**.
  - O arquivo bruto contém **12.431 imagens `.png`** (todas correspondentes a `user_id`s únicos, ex: `2026-07-31/u_0aa0410a.png`).
  - **Diferença:** **+5 imagens a mais** no arquivo real do que o reportado no dicionário.
- **Corte 30/09/2026 (`heatmaps_2026-09-30.zip`):**
  - O dicionário documenta **13.047 imagens**.
  - O arquivo bruto contém exatamente **13.047 imagens `.png`** (conforme a 100%).

### 3.2 Formatação Mista em `pagamentos.csv` (`valor`)
- **Problema:** A coluna `valor` foi carregada como `object` (string) em vez de numérica (`float64`).
- **Causa Raiz:** Foram detectadas **19.750 linhas** formatadas no padrão brasileiro com cifrão e vírgula (`'R$ 34,90'`, `'R$ 299,90'`), enquanto as demais **145.798 linhas** vêm como texto decimal com ponto (`'34.90'`).
- **Distribuição por Canal:**
  - Todas as 19.750 ocorrências com `R$` vêm dos canais próprios web: **13.044 de `cartao`** e **6.706 de `pix_automatico`**.
  - As lojas (`app_store` e `google_play`) utilizam exclusivamente notação decimal pura (`34.90`).
- **Impacto:** Qualquer cálculo direto de receita que execute `sum()` sem prévia higienização (`str.replace`, limpeza de `R$` e conversão de vírgula para ponto) gerará erro ou resultados incorretos.

### 3.3 Disparidade de Fusos Horários em `pagamentos.csv` e `eventos_assinatura.csv` (`data_hora`)
- **Problema:** A mesma coluna contém timestamps expressos em fusos horários distintos sem indicação explícita nos canais locais.
- **Evidência:**
  - Eventos de lojas (`app_store`, `google_play`): gravados em formato ISO 8601 UTC terminado em `Z` (ex: `2024-07-01T22:22:27Z`).
  - Eventos próprios da web (`cartao`, `pix_automatico`): gravados sem sufixo de fuso (ex: `2024-07-01 08:42:40`), representando o Horário de Brasília (UTC-3).
- **Impacto:** Conforme a Decisão 003 de governança do projeto, consolidações contábeis e cortes mensais (como o fechamento de 30/09/2026 às 23h59) exigem a conversão explícita dos registros em UTC para UTC-3 antes de aplicar filtros temporais.

### 3.4 Representação Sentinela de Ausência em `atividades.parquet` (`treino_com`)
- **Problema:** O campo `treino_com` não possui valores nulos (`NaN` = 0), mas contém **1.240.338 strings vazias (`""`)** (98,87% do arquivo).
- **Interpretação:** Apenas 14.137 treinos (1,13%) foram realizados com companhia marcada (contendo o `user_id` do parceiro).
- **Impacto:** Funções como `.isna()` ou `.dropna()` não identificam os treinos individuais; é mandatório tratar strings vazias como ausência de parceiro.

### 3.5 Perda de Formatação em `usuarios.csv` (`cep_prefixo`)
- **Problema:** O dicionário descreve o campo como '3 primeiros dígitos do CEP', mas a coluna foi inferida como `float64` devido à presença de **1.894 valores nulos (2,92%)**.
- **Impacto:** Prefixos de CEP iniciados por zero perderam o zero à esquerda (ex: `046` virou `46.0`). Deve ser tratado como string com preenchimento de zeros (`zfill(3)`).

### 3.6 Texto Livre em `onboarding.csv` (`dias_por_semana`)
- **Problema:** O dicionário explicita que o campo é texto livre. A coluna possui formatos heterogêneos misturando dígitos (`'3'`, `'4'`), expressões compostas (`'3 vezes'`, `'3x'`, `'4 vezes'`) e **6.368 valores nulos (9,96%)**.
- **Impacto:** Para utilização em modelagem preditiva ou segmentação, será necessária extração por expressão regular (regex) para extrair o valor inteiro pretendido.

### 3.7 Categoria Sentinela em `usuarios.csv` (`relogio_conectado`)
- **Problema:** O campo possui 0 nulos, pois usuários sem relógio são registrados com a string literal `'nenhum'` (**40.159 usuários**, 61,83% da base).
- **Distribuição:** `'nenhum'` (40.159), `'garmin'` (13.403) e `'apple_watch'` (11.386).

### 3.8 Ausências Estruturais Válidas por Regra de Negócio
- **`campanha_ago26.csv`:**
  - `enviado_em`, `canal`, `titulo_mensagem`: exatamente **3.579 nulos (25,35%)**, correspondendo aos usuários do grupo de `controle`, que não receberam nenhuma mensagem.
  - `oferta`: **10.648 nulos (75,41%)**, pois apenas o grupo `cupom` (3.472 usuários) recebeu oferta com código/benefício.
- **`assinaturas.csv`:**
  - `data_fim` e `motivo_fim`: exatamente **14.813 nulos (45,38%)**, correspondendo a todas as assinaturas que seguiam ativas na data da exportação (01/10/2026).
- **`tickets_suporte.csv`:**
  - `resolvido_em`: **1.505 nulos (34,03%)**, correspondendo aos chamados que ainda não foram concluídos (status `aberto` ou `sem_resposta`).
- **`pesquisa_saida.csv`:**
  - `comentario`: **183 nulos (28,46%)**, por ser um campo opcional na pesquisa de cancelamento web.
- **`atividades.parquet`:**
  - `distancia_km` (45,82% nulos) e `ritmo_min_km` (46,42% nulos): ausentes em atividades sem GPS (como treinos em vídeo/funcional/yoga).
  - `fc_media` (60,98% nulos): ausente em treinos registrados sem sincronização de relógio cardíaco.
