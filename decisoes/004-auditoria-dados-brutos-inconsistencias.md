# ADR 004: Auditoria de Dados Brutos e Tratamento de Inconsistências

- **Data:** 22/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
A auditoria minuciosa das 12 tabelas brutas e o confronto direto com o documento oficial `Vitaliza: dicionário de dados` revelou divergências de contagem, formatações heterogêneas de texto e perdas de caracteres por conversões automáticas.

## 2. Decisão Adotada
Padronizar as seguintes rotinas de limpeza obrigatórias nos scripts de ingestão e pré-processamento:
1. **Heatmaps de Rotas GPS (`heatmaps_2026-07-31.zip`):** O arquivo contém fisicamente 12.431 imagens (com `user_id`s únicos), divergindo em +5 das 12.426 documentadas no PDF. A contagem física real de **12.431** é a referência oficial.
2. **Sanitização de Valores Monetários (`pagamentos.csv`):** A coluna `valor` possui 19.750 linhas formatadas como texto com padrão brasileiro (`R$ 34,90`, `R$ 299,90`) nos canais web (`cartao` e `pix_automatico`), contra notação decimal pura (`34.90`) nas lojas. Higienização obrigatória: `.str.replace('R$', '').str.replace(' ', '').str.replace(',', '.').astype(float)`.
3. **Treinos Individuais vs. em Grupo (`atividades.parquet`):** A ausência de parceiro em `treino_com` é preenchida por string vazia `""` (1.240.338 registros, 98,87%), e não por `NaN`/`null`. Qualquer filtro de treinos sociais deve checar `treino_com != ""`.
4. **Preservação de Formato de CEP (`usuarios.csv`):** O campo `cep_prefixo` foi exportado numericamente com perda de zeros à esquerda em decorrência de valores nulos (1.894 casos). A ingestão deve converter para string com preenchimento à esquerda (`zfill(3)`).
5. **Normalização de Entrada Livre (`onboarding.csv`):** O campo `dias_por_semana` contém termos livres (`3x`, `3 vezes`, etc.). Utilizar regex para extração do valor numérico inteiro.

## 3. Consequências e Impacto no Case
- Prevenção de quebras de tipagem e joins inconsistentes nas etapas de feature store.
- Eliminação de vieses de agregação em contagens geográficas e métricas de conexão social.
