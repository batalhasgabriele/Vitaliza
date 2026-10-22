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
