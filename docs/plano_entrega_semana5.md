# Plano e controle da entrega — Semana 5

Atualizado em **12/11/2026**, branch **dev**. Consolidação implementada na [ADR 020](../decisoes/020-consolidacao-temporal-semana5.md), autorizada por Igor. Este é o painel vigente; o histórico anterior está no Git e em `saidas/historico_antes_adr020/`.

Prazo do guia: **15/11/2026, até 23:59**. Cada aluno envia na Adalove o link de uma pasta pública no Drive. Aulas também mencionam datas de atividades parciais; não substituem o prazo do guia.

## Entregas e situação atual

**Revisão do mestre — ADR 023:** requisitos do guia mapeados na abertura; definição de churn, matriz de hipóteses por segmento, prioridades e vínculo com EDA/código/mini deck explícitos. Mudança documental, sem recálculo dos resultados.

**Leitura consolidada — ADR 022:** documento mestre ampliado com contexto, engenharia, EDA, personas, avaliação histórica, campanha, prioridade, economia, limitações e continuidade. Fonte editorial em `docs/resolucao_mestre_semana5.template.md`; versão de leitura em `saidas/resolucao_case_vitaliza_semana5.md`. Alteração documental, sem recálculo de métricas.

**Fechamento autorizado em 12/11 — ADR 021 concluído:** validação independente aprovada, sem Git e sem Prata/Ouro iniciais. Sete tabelas, atribuições e receita preservadas; 28 testes aprovados. Pasta e ZIP de entrega montados com manifesto de integridade. Publicação externa não foi realizada.

| Etapa | Área | Requisito | Situação | Onde encontrar |
|---|---|---|---|---|
| 1 | Tecnologia | Carregar, limpar e auditar dados | Concluída. Bronze preservada, Prata reproduzida sem alteração de conteúdo | `src/limpeza_qualidade_dados.py`; `notebooks/00_pipeline_etl_data_quality.md` |
| 2 | Tecnologia | EDA, distribuições e cobertura | Concluída com correções. Coorte de 90 dias substitui interpretação incorreta de sobrevivência; pesquisa sem dupla contagem | `saidas/eda_e_hipoteses_vitaliza.md`; `notebooks/02_eda_e_hipoteses.ipynb` |
| 3 | Tecnologia e negócios | Churn de 2026, reajuste, pesquisa e campanha | Concluída com ressalvas de reconciliação e causalidade. Campanha ITT de 30 dias e sensibilidades separadas | `saidas/eda_etapa3_marcos_2026.md`; `saidas/semana5_consolidada/tabelas/campanha.csv` |
| 4 | Tecnologia | 3–4 segmentos sem usar churn no agrupamento | Concluída. Três perfis, cinco atributos, janela de 84 dias; k=3/4 comparados; bootstrap completo; coortes históricas anteriores ao desfecho | `src/consolidar_semana5.py`; `notebooks/03_segmentacao_clusters.ipynb`; `notebooks/12_consolidacao_semana5.md` |
| 5 | Negócios | Cartões, hipóteses, prioridade, gráficos e limitações | Concluída localmente. Três personas, regras sem sobreposição e piloto proposto, não executado | [Relatório HTML](../saidas/semana5_consolidada/relatorio_executivo.html); [fonte MD](../saidas/customer_segmentation_report_semana5.md) |
| 6 | Tecnologia | Mini deck com história analítica | Concluída localmente. Cinco slides com tabela, gráfico e mensagens centrais | [Mini deck HTML](../saidas/semana5_consolidada/mini_deck.html); [fonte MD](../saidas/mini_deck_eda_semana5.md) |
| 7 | Ambas | Consistência, reprodução e comparação com versões anteriores | Concluída. 28 testes; três notebooks; reprodução independente desde Bronze; mesmos 14.753 ativos, atribuições e receita da ADR 020 | [QA](../saidas/qa_entrega_semana5.md); `saidas/semana5_consolidada/tabelas/qa_fechamento.json` |
| 8 | Ambas | Pacote final, código, matriz de requisitos e integridade | Concluída localmente; pasta e ZIP gerados e conferidos | `saidas/entrega_semana5/00_LEIA-ME.md`; `saidas/entrega_semana5.zip` |
| 9 | Aluno | Drive público e submissão individual | Pendente externamente. Nenhum envio foi realizado | Instruções no `00_LEIA-ME.md` do pacote |

## Números vigentes e interpretação
Formatos finais: [relatório PDF, seis páginas](../saidas/semana5_consolidada/relatorio_executivo.pdf) e [mini deck PDF, cinco slides](../saidas/semana5_consolidada/mini_deck.pdf), além dos HTML e Markdown. Todas as páginas dos PDFs foram renderizadas e inspecionadas; o registro está em `saidas/semana5_consolidada/tabelas/qa_pdf.json`.


- Carteira em 30/09/2026: **14.753 ativos**; nenhum foi excluído na consolidação.
- Segmentos atuais: **6.797 Atleta ao Ar Livre**, **5.109 Treino em Casa Guiado** e **2.847 Hábito Fraco**. Os nomes são rótulos comportamentais, não biografias.
- **1.119** clientes com menos de 30 dias têm classificação provisória; permanecem nas contagens e nos desfechos, mas não ajustam centroides.
- A janela atual é comum: 84 dias, limitada ao início da assinatura. A proposta anterior de base inteira usava outra população e janela. Os números não devem ser misturados.
- Avaliação histórica: modelo de maio aplicado a julho antes dos 60 dias seguintes. Não representa previsão individual para setembro.
- Renovação desligada: **2.255 por eventos** versus **2.250 no snapshot**, divergência de cinco registros mantida como ressalva.
- Receita equivalente não é margem, receita em risco nem benefício causal de uma campanha.

## Limitações ainda abertas

| Ponto | Tratamento atual | Próximo passo |
|---|---|---|
| Abril: quatro perdas a mais que no enunciado | Auditoria: 1.158 usuários distintos, também presentes no cadastro; UTC textual dá 1.160, sem contas internas | Confirmar origem/regra do número 1.154 com responsável pelo case |
| Cinco divergências de renovação | Auditoria: renovação após último desligamento sem toggle explícito de religamento; sem empate de timestamp | Confirmar regra do sistema de origem; manter ressalva temporal |
| Deduplicação financeira por usuário/valor/dia | Regra auditável, aproximação do ciclo | Obter identificador de ciclo, se disponível |
| Objetivos extraídos de texto | Fora da decisão operacional até validação | Amostra rotulada por humanos e avaliação de erro |
| Efeito das ações propostas | Hipóteses e piloto de viabilidade, sem ROI observado | Dimensionar e executar experimento autorizado |
| Classificação de provisórios | Flag explícita; não excluir saídas precoces | Reavaliar quando houver mais observação |

Essas limitações não são corrigidas inventando dados. São parte da interpretação da entrega.

## Continuidade do grupo

Tecnologia mantém pipeline, métricas, notebooks e gráficos. Negócios mantém hipóteses e narrativa; números vêm dos agregados gerados. Alterações de método exigem nova decisão e regeneração conjunta de relatório/deck. A ADR 020 substitui as versões anteriores de segmentação e suas interpretações, preservadas para comparação.

Para reproduzir, seguir [o método](../notebooks/12_consolidacao_semana5.md). Para localizar todos os artefatos, começar pelo [documento mestre](../saidas/resolucao_case_vitaliza_semana5.md). Nunca editar Bronze; trabalhar na dev; merge para main apenas mediante solicitação explícita.

## Semana 10

Continuam fora da Semana 5: modelo supervisionado, avaliação incremental de texto/imagem, risco individual de 60 dias, política de intervenção e ROI, integração GenAI e aplicativo. O piloto editorial desta entrega é uma proposta, não uma campanha executada.

