# Registro de Decisões do Projeto - Vitaliza (Módulo 2)

Este documento registra as decisões metodológicas, de negócios e de engenharia de dados adotadas pela equipe ao longo do projeto.

---

### Decisão 001: Política de Imutabilidade dos Dados Brutos
- **Data:** 22/10/2026
- **Contexto:** Garantir reprodutibilidade científica e integridade do *data room*.
- **Decisão:** Os arquivos da pasta `dados/brutos/` são estritamente de leitura (*read-only*). Qualquer transformação, limpeza ou enriquecimento de variáveis gerará novos artefatos persistidos em `dados/processados/`.

---

### Decisão 002: Governança e Segurança do Repositório
- **Data:** 22/10/2026
- **Contexto:** Prevenção de vazamento de credenciais e controle de versionamento de grandes volumes de dados.
- **Decisão:** A pasta `dados/` e arquivos de variáveis de ambiente (`.env`) foram incluídos no `.gitignore`, mantendo o repositório leve e focado em código, documentação e relatórios.

---

### Decisão 003: Metodologia de Faturamento de Setembro de 2026
- **Data:** 22/10/2026
- **Contexto:** O faturamento reportado variava conforme o tratamento de fuso horário, status de transação, duplicidades e taxas de intermediação.
- **Decisão Adotada:**
  1. **Filtro de Status:** Considerar apenas cobranças com `status = 'aprovado'`.
  2. **Harmonização de Fuso:** Converter timestamps das lojas (UTC terminados em `Z`) para Horário de Brasília (UTC-3), alinhando ao corte oficial de 30/09/2026 às 23h59.
  3. **Expurgo de Duplicidades:** Desconsiderar cobranças duplicadas geradas por retentativas no mesmo dia/ciclo (93 casos somando R$ 6.830,40 indevidos), resultando no faturamento bruto real de **R$ 492.571,70** (~**R$ 492.572,00**).
  4. **Aplicação de Taxas Líquidas:** Abater 15% para App Store/Google Play, 3,5% para cartão e 0,99% para Pix Automático, consolidando o faturamento líquido de **R$ 436.442,35** (~**R$ 436.442,00**).

---

### Decisão 004: Auditoria de Dados Brutos e Tratamento de Inconsistências
- **Data:** 22/10/2026
- **Contexto:** Perfilamento integral dos dados brutos e confronto com o `Vitaliza: dicionário de dados` para fundamentar as etapas subsequentes de feature store e modelagem.
- **Decisões e Diretrizes Adotadas:**
  1. **Heatmaps de Rotas:** O arquivo `heatmaps_2026-07-31.zip` possui 12.431 imagens (todas com `user_id`s únicos), divergindo em +5 imagens das 12.426 documentadas no PDF. A contagem física real de 12.431 deve ser considerada na base de imagens de treino/validação.
  2. **Padronização de Valores Monetários (`pagamentos.csv`):** A coluna `valor` possui 19.750 linhas formatadas como texto com padrão brasileiro (`R$ 34,90`, `R$ 299,90`) nas vendas web (`cartao` e `pix_automatico`), contra notação decimal pura (`34.90`) nas lojas. O pipeline de ingestão deve obrigatoriamente higienizar a string (`str.replace('R$', '').str.replace(',', '.').astype(float)`).
  3. **Tratamento de Treinos Solo (`atividades.parquet`):** A ausência de parceiro em `treino_com` é expressa por string vazia `""` (1.240.338 registros, 98,87%), e não por `NaN`/`null`. Funções de agregação social devem considerar `treino_com != ""` para identificar treinos em dupla/grupo.
  4. **Preservação de Formato de CEP (`usuarios.csv`):** O campo `cep_prefixo` foi exportado numericamente com perda de zeros à esquerda em decorrência de valores nulos (1.894 casos). A ingestão deve converter para string com preenchimento à esquerda (`zfill(3)`).
  5. **Normalização de Entrada Livre (`onboarding.csv`):** O campo `dias_por_semana` contém termos livres (`3x`, `3 vezes`, etc.). Para modelagem, utilizar expressão regular para extrair o valor inteiro.

