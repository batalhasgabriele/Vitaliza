# Diretrizes para Agentes de IA - Projeto Vitaliza (Módulo 2 MBA Inteli)

## 1. Contexto do Projeto
- **Empresa:** Vitaliza (app freemium brasileiro de bem-estar, treinos ao ar livre com GPS, vídeos guiados e rede social).
- **Desafio:** Arquitetura da Retenção Preditiva (VP de Crescimento e Retenção).
- **Data de corte oficial:** 30/09/2026.

## 2. Regras de Estrutura e Governança de Arquivos
> **Regra Fundamental:** O desenho da pasta já é uma regra: **o dado bruto nunca é editado** (`dados/brutos/` é estritamente somente leitura).

- `docs/`: Enunciado oficial do case, dicionário de dados, síntese geral (`aprendizados_aulas.md`) e **guias de referência das aulas de negócios ([`docs/resumo_aulas_negocios.md`](docs/resumo_aulas_negocios.md)) e de tecnologia ([`docs/resumo_aulas_tecnologia.md`](docs/resumo_aulas_tecnologia.md))** — que devem ser consultados sempre que necessário como base conceitual, técnica e metodológica para o projeto, sem restringir análises adicionais. **Regra obrigatória:** ambos os arquivos de resumo devem ser atualizados **SEMPRE** que um novo arquivo de aula for adicionado na pasta `materiais-aulas/`.
- `instrucoes-case/`: Guia oficial do aluno para entrega de artefatos (Semanas 5 e 10) e enunciado completo do case Vitaliza.
- `materiais-aulas/`: Apostilas e apresentações das aulas de Negócios e Tecnologia do Módulo 2. Sempre que um novo arquivo de aula entrar nesta pasta, o respectivo resumo em `docs/resumo_aulas_negocios.md` ou `docs/resumo_aulas_tecnologia.md` deve ser imediatamente atualizado.
- `dados/brutos/`: Arquivos originais exportados dos sistemas (12 tabelas/logs e pasta `heatmaps/`). Nunca devem ser modificados ou sobrescritos.
- `dados/processados/`: Tabelas intermediárias tratadas e feature stores geradas pelo grupo.
- `notebooks/`: Notebooks de análise exploratória, modelagem e validação.
- `src/`: Scripts Python reutilizáveis (funções de limpeza, engenharia de atributos, modelagem).
- `saidas/`: Relatórios gerados, predições ordenadas para CRM, gráficos e artefatos de entrega.
- `decisoes/`: Arquivos individuais de decisões no padrão ADR (`NNN-titulo.md`), garantindo isolamento entre branches e rastreabilidade de autoria.
- `decisoes.md`: Sumário executivo e índice consolidado com tabela de todas as decisões tomadas.

## 3. Premissas de Negócio e Métricas
- **Retrato Oficial na Data de Corte (`30/09/2026`):**
  - **64.948 contas cadastradas** (maioria no plano gratuito).
  - **14.753 assinantes pagantes ativos** (57% no plano anual e 43% no plano mensal).
  - **Mix de Canais de Pagamento:** App Store (36,6%), Google Play (33,6%), Web - Cartão (20,3%) e Web - Pix Automático (9,5%). Sete em cada dez assinantes pagam via loja de aplicativos.
  - **Histórico de Churn Mensal:** Média de 5,6%/mês em 2025 e 6,6%/mês de jan a set/2026 (pico de 8,1% em abril/2026; 5,9% em agosto e 5,0% em setembro).
- **Preço e Receita Líquida:**
  - **Preço Mensal:** R$ 39,90 (desde 01/03/2026; era R$ 34,90 até 28/02/2026).
  - **Preço Anual:** R$ 299,90 (equivale a R$ 24,99/mês) ou R$ 239,90 no primeiro ano com cupom de influenciador (renovando pelo preço cheio).
  - **Taxas de Intermediação de Canais:**
    - App Store / Google Play: 15,0% (Vitaliza retém 85,0% → R$ 33,92 no mensal de R$ 39,90; R$ 254,92 no anual de R$ 299,90).
    - Web - Cartão: 3,5% (Vitaliza retém 96,5% → R$ 38,50 no mensal de R$ 39,90).
    - Web - Pix Automático: 0,99% (Vitaliza retém 99,01% → R$ 39,50 no mensal de R$ 39,90).
- **Custo de Servir e Custo de Aquisição (CAC):**
  - **Custo de Servir:** R$ 4,20/mês por assinante ativo (infraestrutura, conteúdo e suporte, usando ou não o app).
  - **CAC (2026):** R$ 118,00 em média por novo assinante adquirido (~3,5 mensalidades líquidas de loja).
- **Canais de Contato do CRM (Custos e Capacidades para Nov e Dez/2026):**
  - **Push:** Custo desprezível (R$ 0,00) | Limite: máximo de 1 envio por semana por assinante.
  - **E-mail:** R$ 0,01 por envio | Sem limite prático de capacidade.
  - **WhatsApp:** R$ 0,40 por mensagem | Teto operacional: **1.500 mensagens/mês** (R$ 600,00/mês com teto cheio; alcança ~1 em cada 10 pagantes).
  - **Time de CS (ligação ou chat ativo):** R$ 18,00 por atendimento | Teto operacional: **300 atendimentos/mês** (R$ 5.400,00/mês com teto cheio; alcança ~1 em cada 50 pagantes).
- **Ofertas Permitidas pelo CRM:**
  - **Plano Mensal — 30% de desconto por 3 meses:** Custo de R$ 11,97/mês sobre R$ 39,90 (total de R$ 35,91 nos 3 meses).
  - **Plano Anual — 1 mês grátis no fim do ciclo:** Custo de R$ 25,00 de receita abatida.
  - **Qualquer Plano — Pausa da assinatura por até 60 dias:** Receita do período fica adiada (sem custo direto).
  - **Qualquer Plano — Plano de treino ou conteúdo personalizado:** Sem custo direto.
- **Orçamento Global de CRM e IA Generativa:**
  - **R$ 40.000,00 por mês**, englobando custos de canais, descontos concedidos **e todos os custos de API de IA Generativa** (extração de texto/imagem e redação de mensagens personalizadas), que devem ser calculados pela tabela oficial do provedor escolhido e descontados do mesmo orçamento.
- **Tratamento de Fusos Horários:**
  - Lojas (Apple e Google) gravam em UTC (terminado em `Z`).
  - Meios próprios web (Cartão e Pix) gravam em Horário de Brasília (UTC-3).
  - Toda consolidação contábil ou de cohort deve harmonizar para o Horário de Brasília.
- **Tratamento de Cobranças Duplicadas:**
  - Retentativas de cobrança aprovadas em dobro no mesmo ciclo/dia devem ser expurgadas da receita líquida.

## 4. Cronograma, Entregáveis e Critérios de Avaliação (Guia de Projeto)
- **Padrão e Local de Entrega:** Submissão individual na plataforma Adalove (`https://adalove.inteli.edu.br/`) enviando apenas o link de uma pasta no Google Drive com compartilhamento público.
- **Foco Atual — Entregáveis da Semana 5 (Prazo: `15/11/2026 até 23:59` | Avaliação Formativa / Feedback):**
  - **Artefato de Negócios (`Customer Segmentation Report`):** Relatório executivo descritivo contendo:
    1. 3 a 4 segmentos descritos com **cartões de persona** (clusterização construída sem usar a informação de quem saiu);
    2. Hipóteses de *drivers* de churn por segmento;
    3. Priorização preliminar (intervenção imediata vs. monitoramento);
    4. Visualizações dos dados vindas da EDA;
    5. Seção de limitações da análise.
  - **Artefato de Tecnologia (`Análise Exploratória de Dados - EDA`):** Código + visualizações + **mini deck** que:
    1. Carrega, limpa e visualiza o dataset Vitaliza;
    2. Identifica padrões e correlações com churn (investigando a subida de 2026 e os marcos de reajuste em 01/03/2026, pesquisa de saída em 01/06/2026 e campanha A/B de 10/08/2026);
    3. Gera os gráficos que entram no relatório;
    4. Sustenta empiricamente a segmentação;
    5. Conta a história analítica em um **mini deck**.
- **Horizonte Futuro — Entregáveis da Semana 10 (Prazo: `20/12/2026 até 23:59` | Avaliação Somativa — Meta: Excepcional 9–10):**
  - **Artefato de Negócios (`Plano de Intervenção de Risco / Churn`):**
    - *Segmentação e Estratégia de Intervenção (40%):* Estratégia altamente personalizada por segmento cruzando risco preditivo e *uplift* incremental (separando persuadíveis, garantidos, perdidos e "não perturbe" via experimento de 10/08/2026), com hipóteses claras de driver de churn e mecanismos de teste/aprendizado embutidos.
    - *Racional Financeiro / ROI da Retenção (40%):* Modelo financeiro realista considerando LTV líquido, custo de servir, CAC, custos de contato/ofertas, **custos de IA (tokens e infraestrutura)** e KPIs claros (taxa de retenção, uplift, payback) respeitando os tetos de canais e os R$ 40.000/mês.
    - *Alinhamento Ambidestro (20%):* Sinergia profunda onde os segmentos de negócio retroalimentam o briefing de personalização da GenAI e a interpretação do modelo preditivo.
  - **Artefato de Tecnologia (`Aplicativo Web Preditivo-Generativo`):**
    - *Modelo Preditivo de Churn (40%):* Classificação supervisionada para prever saída nos 60 dias pós-corte (`até 29/11/2026`), progredindo de Regressão Logística para Árvores de Decisão e Bagging/Boosting, avaliando o ganho marginal e o custo/acurácia da extração de variáveis de texto e imagem via IA Generativa (frente a amostra rotulada à mão e contagem de pixels), com interpretação crítica (importância de features, análise de erros) e justificativa de *trade-offs* entre precisão e recall no contexto de retenção.
    - *Integração Preditivo-Generativo (40%):* Aplicação web (stack sugerida: **Python + Marimo + API GenAI**) cujo prompt incorpora dinamicamente o segmento, o score de risco e variáveis relevantes do cliente para personalização em escala.
    - *Adequação ao Problema (20%):* Código organizado, documentado e interface navegável por usuário não técnico com viabilidade corporativa (UX, performance, manutenibilidade).

## 5. Política de Branches e Fluxo Git
- **Branch `main`:** É a branch de entrega oficial, estável e de produção. **Nunca comitar ou desenvolver diretamente na `main`**.
- **Branch `dev`:** É a branch de trabalho ativo. Todas as alterações locais, códigos, notebooks e análises devem ser desenvolvidos e comitados na `dev`.
- **Merge para `main`:** O avanço ou merge de alterações da `dev` para a `main` só ocorre mediante solicitação e aprovação explícita do usuário.

## 6. Comandos

### Ativação do Ambiente Virtual (`.venv`)
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(Caso haja restrição de execução de scripts no PowerShell: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*
- **Windows (Prompt de Comando / CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **macOS / Linux (Bash/Zsh):**
  ```bash
  source .venv/bin/activate
  ```

### Inicialização do JupyterLab
- **Com o ambiente ativado:**
  ```bash
  jupyter lab
  ```
- **Diretamente via interpretador do ambiente (sem ativar manualmente):**
  - **Windows (PowerShell):**
    ```powershell
    .\.venv\Scripts\jupyter-lab.exe
    ```
  - **macOS / Linux:**
    ```bash
    ./.venv/bin/jupyter-lab
    ```

## 7. Como trabalhar
- antes de uma tarefa com mais passos, apresente um plano e espere aprovação
- **controle de etapas da Semana 5:** consultar e atualizar obrigatoriamente o arquivo [`docs/plano_entrega_semana5.md`](docs/plano_entrega_semana5.md) **SEMPRE** que finalizarmos uma etapa e/ou quando iniciarmos uma nova etapa da construção dos artefatos da Semana 5, mantendo o status de cada passo atualizado para nunca perdermos o rumo
- **propagação de mudanças e consistência cruzada:** se houver mudança em algum arquivo, base processada ou critério técnico/negócio que impacte outros documentos do projeto (notebooks, gráficos, relatórios em `saidas/`, ADRs em `decisoes/` ou guias em `docs/`), **todos os documentos impactados devem ser obrigatoriamente atualizados** para evitar números divergentes
- consultar sempre que necessário os resumos consolidados das aulas de negócios ([`docs/resumo_aulas_negocios.md`](docs/resumo_aulas_negocios.md)) e de tecnologia ([`docs/resumo_aulas_tecnologia.md`](docs/resumo_aulas_tecnologia.md)) como base conceitual, técnica e metodológica (sem se restringir a eles)
- **atualização contínua dos resumos de aulas:** ambos os arquivos de resumo ([`docs/resumo_aulas_negocios.md`](docs/resumo_aulas_negocios.md) e [`docs/resumo_aulas_tecnologia.md`](docs/resumo_aulas_tecnologia.md)) devem ser atualizados **SEMPRE** que um novo arquivo de aula for adicionado na pasta `materiais-aulas/`, incluindo o resumo completo da nova aula
- após executar uma análise, salvar o racional na pasta notebooks/ para utilizar em cenários de replicação/recálculo
- estrutura recomendada para o prompt de análises: pergunta, arquivos, regras, formato de saída e definition of done. se alguma dessas informações não tiver clara, pergunte.
- aspectos de negócios, correções feitas e regras estabelecidas devem ser registradas em um novo arquivo em `decisoes/NNN-titulo.md` (seguindo `decisoes/TEMPLATE.md` com autor e branch) e referenciadas na tabela índice de `decisoes.md`.
