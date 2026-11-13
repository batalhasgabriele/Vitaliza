# Vitaliza — Semana 5

## Entrega atual (ADR 020)
- [Resolução mestre — leitura consolidada do case](saidas/resolucao_case_vitaliza_semana5.md).
- Pacote final: `saidas/entrega_semana5/` e `saidas/entrega_semana5.zip` (gerados localmente, fora do Git).
- [Matriz dos requisitos](docs/matriz_requisitos_semana5.md) e [fechamento/reprodução independente](notebooks/13_fechamento_entrega_semana5.md).
- [Relatório executivo PDF — seis páginas](saidas/semana5_consolidada/relatorio_executivo.pdf)
- [Mini deck PDF — cinco slides](saidas/semana5_consolidada/mini_deck.pdf)
- [Relatório executivo HTML](saidas/semana5_consolidada/relatorio_executivo.html)
- [Mini deck HTML — cinco slides](saidas/semana5_consolidada/mini_deck.html)
- [Fonte Markdown do relatório](saidas/customer_segmentation_report_semana5.md)
- [Método e reprodução](notebooks/12_consolidacao_semana5.md)
- [QA e impacto](saidas/qa_entrega_semana5.md)

PDF permite pré-visualização no Drive; HTML é autossuficiente: baixar e abrir no navegador. Para entregar, colocar relatório, mini deck, código/decisões e índice em uma pasta pública do Drive. Cada aluno submete seu link na Adalove. Publicação não é feita pelos scripts.

## Executar
Python com `requirements-notebooks.txt` inclui `requirements-data.txt`. Executar da raiz:
```powershell
uv run --with-requirements requirements-notebooks.txt python src/executar_semana5.py
uv run --with-requirements requirements-notebooks.txt python src/revisar_notebooks_semana5.py
```
Se apenas Prata estiver disponível: `python src/consolidar_semana5.py` gera a consolidação. Não confundir com execução completa desde Bronze.

Para validar a portabilidade: `uv run --with-requirements requirements-notebooks.txt python src/validar_portabilidade_semana5.py`. Esse comando copia a Bronze para um diretório privado de validação e executa sem Prata/Ouro anteriores e sem histórico Git. Não muda as entradas originais. Para montar a distribuição após validação: `python src/montar_pacote_semana5.py`.

Para explorar o pacote sem os dados originais, instalar `requirements-notebooks.txt` e abrir os notebooks 02 e 03, que leem os agregados distribuídos. O notebook 01 e o recálculo completo precisam do data room autorizado. As bases antigas de segmentação são opcionais, usadas somente na comparação de impacto.

Depois de atualizar os HTML, regenerar e revisar os PDFs: `node src/verificar_html_semana5.cjs --pdf`. Esse comando adicional requer Node, Playwright e Microsoft Edge disponíveis no ambiente; não integra as dependências Python. Conferir seis páginas de relatório e cinco de deck. O pipeline Python não atualiza PDFs sozinho.

## Estrutura
Bronze é imutável. Prata contém limpeza; Ouro contém análises por cliente; `saidas/semana5_consolidada/tabelas/` contém agregados autoritativos. `src/` implementa, `notebooks/` explica e demonstra, `decisoes/` registra escolhas. Trabalhar na dev; main só mediante autorização de merge.

As versões anteriores em `saidas/historico_antes_adr020/` e as tabelas de propostas k=4/k=3 da base inteira são históricas e não entram no pacote de entrega atual. Não publicar dados individuais, GPS, textos ou logs privados por simples cópia da pasta do projeto. Os dados do case são fictícios, mas o projeto mantém a separação entre análise e pacote público.

## Próxima etapa
Semana 10: classificação supervisionada, ganho marginal de texto/imagem, política de retenção e ROI, aplicação com GenAI. A Semana 5 não comprova efeito individual nem retorno de campanhas ainda não executadas.
