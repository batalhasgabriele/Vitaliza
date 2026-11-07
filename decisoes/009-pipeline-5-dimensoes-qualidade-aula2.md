# ADR 009: Pipeline de Limpeza pelas 5 Dimensões da Qualidade de Dados e Reconciliação da Aula 2 de Tecnologia

- **Data:** 01/11/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Antigravity AI
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
A Aula 2 de Tecnologia (Prof. Cesar Almiñana) estabeleceu o protocolo oficial de inspeção e limpeza de dados fundamentado nas **5 Dimensões da Qualidade de Dados** (Wang & Strong, 1996: Completude, Validade, Consistência, Unicidade e Temporalidade), além das regras de reconciliação contábil de setembro/2026 e de prevenção de vazamento temporal (*data leakage*) entre retratos (`assinaturas.csv`) e logs históricos (`eventos_assinatura.csv`). Era necessário atualizar o pipeline de engenharia de dados (`src/limpeza_qualidade_dados.py`, `src/processar_eda.py` e `notebooks/01_inventario_dados.ipynb`) para incorporar integralmente essas regras e auditar todos os números de controle.

## 2. Decisão Adotada
Ficam instituídas e implementadas no código oficial do projeto as seguintes regras de limpeza e validação:

1. **População Oficial e Expurgo de Contas Internas:**
   - Das `64.948` contas em `usuarios.csv` e `14.813` assinaturas ativas brutas em `assinaturas.csv`, são expurgadas as **`60` contas internas (`@vitaliza.com.br` / plano `cortesia`)**, resultando nos **`14.753` assinantes pagantes ativos** no corte de `30/09/2026` (sendo **`12.503`** com `renovacao_automatica == 'sim'` e **`2.250`** com `renovacao_automatica == 'nao'`).
2. **Dimensão 1 — Completude (`onboarding.csv`):**
   - Diferenciar vazios opcionais declarados no dicionário (`objetivo_texto`: `5.467` vazios / `8,6%`) de vazios não declarados (`nivel`: `4.513` vazios / `7,1%`; `dias_por_semana`: `6.368` vazios / `10,0%`; `como_conheceu`: `4.586` vazios / `7,2%`).
   - Em vez de descartar linhas (`dropna`), criar variáveis indicadoras (`flag_onb_*_preenchido`) para preservar o sinal comportamental de não preenchimento.
3. **Dimensão 2 — Validade (`atividades.parquet`):**
   - Preservar os **`574.835` treinos sem `distancia_km`** como treinos *indoor* legítimos (sem GPS).
   - Nos **`679.640` treinos com GPS**, expurgar/anular (`NaN`) as distâncias dos **`951` treinos com `distancia_km > 200 km`** (erro de GPS, chegando a `10.012,75 km` no `apple_health`), o que restaura a correlação linear ($r$ de Pearson) entre duração e distância nas corridas de **`0,12` para `0,89`** (`555` corridas anômalas).
   - Remover das agregações de treino os **`3.649` registros com `duracao_min <= 0`**.
4. **Dimensão 3 — Consistência (`atividades.parquet`):**
   - Padronizar os **11 rótulos originais** para as **7 modalidades canônicas** (`run` $\rightarrow$ `corrida`, `walk` $\rightarrow$ `caminhada`, `strength` $\rightarrow$ `forca`, `ride` $\rightarrow$ `pedal`, além de `funcional`, `hiit` e `yoga`), integrando os **`376.930` treinos gravados em inglês (`30,0%` da base, 100% oriundos do `app`)** e evitando a perda de **`162.108` corridas (`run`)**.
5. **Dimensão 4 — Unicidade e Harmonização de Fuso do Garmin (`atividades.parquet`):**
   - Converter os timestamps da origem `garmin` de `UTC` (-3 horas) para Horário de Brasília (`UTC-3`) antes da deduplicação.
- Remover os **`9.383` pares de treinos duplicados** (mesmo `user_id`, modalidade canônica, duração, distância e início em até 5 minutos entre `app` e relógio), compostos exatamente por **`4.184` pares com `apple_health`** e **`5.199` pares com `garmin`**, gerando a base Prata `dados/processados/prata/atividades_limpas.parquet` (`1.241.461` treinos válidos até o corte).
6. **Dimensão 5 — Temporalidade (`uso_mensal.csv`) e Prevenção de Vazamento Temporal (`eventos_assinatura.csv`):**
   - Em `uso_mensal.csv`, separar o cálculo de médias de **meses efetivamente ativos (`minutos > 0`)** das médias de **2026**, neutralizando a mudança de regra de gravação ocorrida em `jan/2026` (em `dez/2025` havia `13.624` linhas e `0` zeros, com média de `264,6 min`; em `jan/2026` passaram a ser gravadas `25.697` linhas com zero num total de `41.130` linhas, derrubando a média bruta para `117,9 min` enquanto a média dos ativos subiu para `314,2 min`).
   - Para qualquer análise histórica em data de corte passada $t$ (ex.: `31/07/2026`), reconstruir o status de `renovacao_automatica` a partir de `eventos_assinatura.csv` (evitando o vazamento temporal de **`823` assinantes / `37%`** entre os `2.250` ativos com renovação desligada no retrato de `30/09/2026`, dos quais `754` ainda estavam com renovação ligada e `69` nem assinavam em `31/07/2026`).
7. **Reconciliação Oficial do Faturamento de Setembro/2026 (`pagamentos.csv`):**
   - Fica validado o funil contábil oficial de `set/2026`: Soma bruta sem filtro de status (`R$ 509.588`) $\rightarrow$ Apenas `status == 'aprovado'` (`R$ 499.503`) $\rightarrow$ Harmonizado para Horário de Brasília `UTC-3` (`R$ 499.402`) $\rightarrow$ Expurgadas cobranças aprovadas em duplicidade no mesmo dia (**`R$ 492.572` Faturamento Bruto**) $\rightarrow$ Descontadas taxas de canal de 15% lojas, 3,5% cartão e 0,99% Pix (**`R$ 436.442` Faturamento Líquido Oficial**).

## 3. Consequências e Impacto no Case
- Geração da base higienizada `dados/processados/prata/atividades_limpas.parquet` e atualização da feature store Ouro `dados/processados/ouro/features_eda_corte_set2026.parquet`.
- Documentação integral e auditável no notebook `notebooks/01_inventario_dados.ipynb`, garantindo reprodutibilidade total para os entregáveis das Semanas 5 e 10.

