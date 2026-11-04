# ADR 008: Consolidação do Guia de Artefatos (Semanas 5 e 10) e Premissas Oficiais do Case

- **Data:** 01/11/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Gemininha (Copilota IA)
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
A partir da leitura integral dos documentos oficiais na pasta `instrucoes-case/` (`[Inteli MBA] Guia de Projeto - Entrega de Artefatos - Módulo 2 (2026.2B).pdf` e `Vitaliza - Enunciado do case.pdf`), identificou-se a necessidade de atualizar as diretrizes mestras do projeto (`AGENTS.md`) para refletir:
1. O escopo exato dos artefatos de Negócios e Tecnologia das **Semanas 5 e 10** e as rubricas de avaliação (conceito Excepcional 9–10);
2. Os parâmetros operacionais e financeiros completos da **Seção 03 do Enunciado Oficial** (base ativa de 14.753 pagantes no corte, custo de servir, CAC, tetos e custos de canais de CRM, cardápio de ofertas e orçamento mensal unificado de R$ 40.000,00 incluindo custos de API de IA Generativa).

## 2. Decisão Adotada
Registrar no `AGENTS.md` e adotar como referência obrigatória em todas as análises, segmentações, simulações financeiras e aplicações os seguintes parâmetros e entregáveis:

### 2.1. Parâmetros Oficiais do Enunciado (Seção 03)
- **Base no corte (`30/09/2026`):** 64.948 contas cadastradas e **14.753 assinantes pagantes ativos** (57% anual, 43% mensal; 36,6% App Store, 33,6% Google Play, 20,3% Web Cartão, 9,5% Web Pix).
- **Custo de Servir:** `R$ 4,20/mês` por assinante ativo (independentemente do uso).
- **CAC Médio (2026):** `R$ 118,00` por novo assinante.
- **Canais de Contato (Novembro e Dezembro de 2026):**
  - *Push:* R$ 0,00 | Limite de 1 envio/semana por assinante.
  - *E-mail:* R$ 0,01/envio | Sem limite prático.
  - *WhatsApp:* R$ 0,40/mensagem | Teto de **1.500 mensagens/mês** (R$ 600,00/mês no teto).
  - *Time de CS (ligação/chat ativo):* R$ 18,00/atendimento | Teto de **300 atendimentos/mês** (R$ 5.400,00/mês no teto).
- **Ofertas de Retenção Permitidas:**
  - *Plano Mensal:* 30% de desconto por 3 meses (custo de R$ 11,97/mês ou R$ 35,91 no trimestre).
  - *Plano Anual:* 1 mês grátis no fim do ciclo (custo de R$ 25,00 de receita abatida).
  - *Qualquer Plano:* Pausa da assinatura por até 60 dias (receita adiada, sem custo direto) ou Plano de treino/conteúdo personalizado (sem custo direto).
- **Orçamento Mensal Unificado (CRM + IA Generativa):**
  - **R$ 40.000,00/mês**, cobrindo disparos, descontos concedidos e todos os custos de chamadas de API de IA Generativa (extração de variáveis de texto/imagem e geração de mensagens personalizadas).

### 2.2. Roteiro de Entregáveis
1. **Semana 5 (Entrega até `15/11/2026 às 23:59` — Avaliação Formativa):**
   - **Negócios (`Customer Segmentation Report`):** Relatório executivo descritivo contendo 3–4 segmentos com cartões de persona (clusterização sem usar a variável *target* de saída), hipóteses de *drivers* de churn por segmento, priorização preliminar (imediata vs. monitoramento), visualizações da EDA e seção de limitações da análise.
   - **Tecnologia (`Análise Exploratória de Dados - EDA`):** Código + visualizações + **mini deck** que carrega, limpa e visualiza o dataset Vitaliza, identifica padrões e correlações com churn, gera os gráficos do relatório, sustenta empiricamente a segmentação e conta a história analítica.
2. **Semana 10 (Entrega até `20/12/2026 às 23:59` — Avaliação Somativa):**
   - **Negócios (`Plano de Intervenção de Risco / Churn`):** Estratégia de intervenção por segmento combinando score preditivo e *uplift* (persuadíveis vs. garantidos, perdidos e "não perturbe" via experimento de 10/08/2026), modelo financeiro de ROI completo (incluindo custos de tokens/infra de IA e KPIs de retenção, uplift e payback) e alinhamento ambidestro com a aplicação generativa.
   - **Tecnologia (`Aplicativo Web Preditivo-Generativo`):** Modelo de classificação supervisionada para saída em 60 dias pós-corte (`até 29/11/2026`), avaliação do ganho marginal de features de texto e imagem extraídas via IA Generativa e protótipo web (Python + Marimo + API GenAI) que consome o risco e o segmento para redigir mensagens hiperpersonalizadas.

## 3. Consequências e Impacto no Case
- Alinha 100% do trabalho aos critérios de avaliação das trilhas de Negócios e Tecnologia do MBA Inteli.
- Garante que a preparação imediata para a **Semana 5** já construa as bases (EDA, personas sem vazamento do target e gráficos executivos) que alimentarão o modelo preditivo, a análise de *uplift* e o aplicativo web da **Semana 10**.

