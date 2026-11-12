# Execução, logs e reprocessamento

> **Escopo após 12/11/2026:** Entrada vigente: `python src/executar_semana5.py`, seguida de `python src/revisar_notebooks_semana5.py`, conforme [README](../README.md). Comandos antigos de segmentação reproduzem versões históricas e não devem substituir os artefatos atuais.

## Pré-requisitos
Executar da raiz do repositório, na branch dev, com Python/dependências de `requirements-data.txt`. Ter as bases Prata e a baseline privada disponíveis. Nunca editar a Bronze para corrigir resultados.

```powershell
$env:UV_CACHE_DIR='.uv-cache'
uv run --with-requirements requirements-data.txt python src/validar_engenharia_dados.py
uv run --with-requirements requirements-data.txt python src/auditar_temporalidade.py
uv run --with-requirements requirements-data.txt pytest -q
```

O validador cria uma pasta privada em `dados/execucoes_engenharia/<run_id>/`, copia a Prata, executa a EDA duas vezes, salva logs e contratos observados. O JSON agregado fica em `saidas/tabelas/qa_engenharia_dados.json`. Os logs locais não devem ser copiados automaticamente para publicação.

## Publicação controlada da EDA
Após análise do relatório:

```powershell
uv run --with-requirements requirements-data.txt python src/validar_engenharia_dados.py --publicar
```

O comando repete a validação e bloqueia publicação se houver chave inválida, referência órfã, mudança de população ou de atributos. A escrita temporária seguida de substituição protege um arquivo individual. Não há transação que publique simultaneamente todas as tabelas Prata/Ouro. O runner cobre a migração da EDA; não deve ser anunciado como orquestrador completo do projeto.

## Recuperação
Em falha, consultar a pasta da execução e manter o último resultado oficial. Corrigir a causa em dev, executar novamente e comparar. A baseline é preservada; restauração deve selecionar explicitamente o arquivo afetado e validar dependências. Não apagar diretórios inteiros para tentar corrigir uma execução.

## Evolução operacional
Para uma cadeia completa, adaptar cada produtor para receber diretórios de entrada/saída e publicar por versão aprovada. Definir responsável, política de retenção e alertas antes de agendar. O projeto usa snapshot fechado: frescor deve ser verificado contra o corte esperado, não exigindo dados recentes em relação à data atual.
