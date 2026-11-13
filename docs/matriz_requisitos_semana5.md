# Matriz de requisitos — entrega da Semana 5

A [resolução mestre](../saidas/resolucao_case_vitaliza_semana5.md) agora explicita todos os requisitos em sua abertura: definições de churn na seção 3, padrões na 5.4, hipóteses de drivers por segmento na 7.4, prioridade imediata versus monitoramento na 10 e relação com código e mini deck na 15. Evidências e hipóteses estão separadas; as limitações permanecem na seção 12.

Fonte: `[Inteli MBA] Guia de Projeto - Entrega de Artefatos - Módulo 2 (2026.2B).pdf`, seção de artefatos da trilha obrigatória. A Semana 5 é formativa; os critérios de nota e o aplicativo preditivo-generativo pertencem à Semana 10.

| Área | Pedido do guia | Evidência entregue | Localização |
|---|---|---|---|
| Negócios | 3–4 segmentos e cartões de persona | Três cartões baseados no comportamento, com evidência e limites | [Relatório](../saidas/semana5_consolidada/relatorio_executivo.pdf), páginas 2–4 |
| Negócios | Hipóteses de drivers de churn por segmento | Meta concluída, relevância do conteúdo e formação de hábito, formuladas como hipóteses | Relatório, páginas 2–4 |
| Negócios | Priorização imediata versus monitoramento | Quatro públicos operacionais sem sobreposição | Relatório, página 6; `saidas/semana5_consolidada/tabelas/prioridades.csv` |
| Negócios | Visualizações vindas da EDA | Tamanhos dos perfis e saída histórica com intervalo de confiança | Relatório, páginas 1 e 5 |
| Negócios | Limitações da análise | Temporalidade, cobertura, causalidade, provisórios e ressalvas de fonte | Relatório, páginas 5–6; [método](../notebooks/12_consolidacao_semana5.md); [QA](../saidas/qa_entrega_semana5.md) |
| Tecnologia | Código que carrega e limpa o dataset | Pipeline Bronze → Prata → Ouro, contratos e testes | `src/executar_semana5.py`, `src/limpeza_qualidade_dados.py`, notebook 01 |
| Tecnologia | Visualizações e padrões/correlações com churn | Série mensal, reajuste, cobertura da pesquisa e campanha; comparação histórica por segmento | [EDA dos marcos](../saidas/eda_etapa3_marcos_2026.md), notebook 02 e tabelas agregadas |
| Tecnologia | Gerar gráficos que entram no relatório | Apresentações geradas dos mesmos agregados | `src/consolidar_semana5.py` |
| Tecnologia | Sustentação empírica dos segmentos | Cinco atributos anteriores ao desfecho; k comparados; bootstrap e coortes | Notebook 03, `selecao_k.csv`, `coortes_60d.csv` e [método](../notebooks/12_consolidacao_semana5.md) |
| Tecnologia | História analítica em mini deck | Cinco slides com tabela, gráfico e mensagens centrais | [Mini deck](../saidas/semana5_consolidada/mini_deck.pdf) |
| Entrega | Formato livre em pasta pública do Drive; link individual na Adalove | Pasta e ZIP locais preparados; submissão depende do aluno | `saidas/entrega_semana5/00_LEIA-ME.md` |

Os resultados são descritivos. A avaliação histórica não é previsão individual para setembro, e os pilotos não foram executados. O pacote inclui as evidências suficientes para revisão sem exigir exposição dos dados individuais.
