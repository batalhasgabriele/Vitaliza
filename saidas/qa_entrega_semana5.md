# QA e impacto — Semana 5 consolidada

## Resultado
Entrega local consolidada na dev (ADR 020). Relatório HTML de seis seções, mini deck HTML de cinco slides e fontes Markdown gerados dos mesmos agregados.

## O que mudou nos resultados
População atual: **14,753 ativos únicos**. População preservada frente à base antiga; ARI versus 16 atributos: **0.828**. Isso é concordância, não qualidade absoluta.

| persona               |   proposta_11nov |   consolidada_84d |   diferenca |
|:----------------------|-----------------:|------------------:|------------:|
| Atleta ao Ar Livre    |             7514 |              6797 |        -717 |
| Treino em Casa Guiado |             5419 |              5109 |        -310 |
| Hábito Fraco          |             1820 |              2847 |        1027 |

A mudança foi deliberada: janela comum de 84 dias, cinco atributos, regularidade pelos logs e exposição explícita. A proposta de 11/11 usava a vigência de janeiro até saída/corte. Não atribuir a diferença a perda de linhas por limpeza.

## Controles executados
- Runner completo Bronze → Prata → EDA → marcos → gráficos → consolidação → documentação, com logs em dados/execucoes_engenharia/. Resultado em `semana5_consolidada/tabelas/qa_pipeline.json`.
- Os 14 hashes Bronze foram preservados; Prata reproduzida byte a byte.
- A execução completa reproduziu as tabelas analíticas da primeira consolidação. Depois, a apresentação foi refinada e o IC do controle contra ele próprio foi fixado em zero; contagens, taxas e comparações dos tratamentos permaneceram iguais. Os modelos não foram reajustados nessas alterações finais. `qa_pipeline.json` preserva o retrato daquela execução; `qa_testes.txt`, `qa_visual.json` e `impacto.json` registram as verificações finais correspondentes.
- Testes semânticos de estados, futuro, exposição, coorte, intervalos e partição da pesquisa, além dos testes anteriores. Registro final em `semana5_consolidada/tabelas/qa_testes.txt`.
- Notebooks: registro em `tabelas/qa_notebooks_semana5.json`; consomem agregados e não substituem o runner.
- HTML: ver `semana5_consolidada/tabelas/qa_visual.json`; revisão de seções com screenshots locais, imagens carregadas e sem overflow horizontal.
- PDF: seis páginas de relatório e cinco slides exportados, todas as páginas renderizadas e inspecionadas. Registro da exportação em `semana5_consolidada/tabelas/qa_pdf.json`. PDFs requerem reexportação após alterações nos HTML, conforme README.

## Resultados estatísticos
Silhueta k=3 de 0,350 e cinco reamostragens bootstrap de todo pré-processamento com ARI médio 0.998. É uma verificação exploratória de estabilidade, não prova de generalização. Coortes em maio/julho: modelo de maio congelado ao avaliar julho; todos os provisórios elegíveis permanecem nos desfechos. Taxas e incerteza em `coortes_60d.csv`.

Campanha principal reproduz controle 5,48%, cupom 4,64%, desafio 5,18% e conteúdo 6,13% de expiração em 30 dias. Sensibilidades estão separadas por plano, desfecho e horizonte. Não identificam efeito individual.

## Limites não encerrados por software
Abril: eventos e cadastro concordam em 1.158 perdas, contra 1.154 do enunciado; não são duplicatas. Nos cinco estados de renovação divergentes, há renovação após o último desligamento sem religamento explícito. A causa do conflito exige confirmação da fonte. Auditoria em `semana5_consolidada/tabelas/auditoria_divergencias.json`. A regra financeira usuário/valor/dia ainda aproxima o ciclo; extração de objetivos textuais não tem amostra humana validada e permanece fora das decisões operacionais. Histórico observado sob intervenções reais não é risco natural sem tratamento. Plano/canal sem evento usam fallback cadastral. Não há target de setembro observado até novembro.

## Entrega externa
Publicação no Drive, verificação de permissões e submissão na Adalove não foram realizadas. Não copiar dados individuais nem a pasta histórica para o pacote público. Começar por `../README.md`.
