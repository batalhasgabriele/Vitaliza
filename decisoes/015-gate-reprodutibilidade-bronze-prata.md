# ADR 015: Gate de Reprodutibilidade Bronze → Prata

- **Data:** 04/11/2026
- **Autor(a) / Responsável:** Igor / Codex
- **Branch / Worktree:** `codex/plano-mestre-vitaliza`
- **Status:** Implementada

---

## 1. Contexto e Motivação

As etapas 1 e 2 da Semana 5 estavam registradas como concluídas, porém os dados processados não são versionados e a camada Bronze foi disponibilizada novamente em 04/11/2026. Antes de iniciar a EDA Parte 2, tornou-se necessário demonstrar que o pipeline reproduz os resultados oficiais sem depender de arquivos derivados anteriores.

## 2. Decisão Adotada

Instituir um gate obrigatório de reprodutibilidade composto por:

1. auditoria somente leitura das 12 fontes tabulares e dos dois pacotes de heatmaps;
2. manifesto com SHA-256, contagens, schemas, nulos, chaves candidatas e cobertura temporal;
3. execução do pipeline de qualidade diretamente sobre a Bronze;
4. persistência exclusiva em Parquet na camada `dados/processados/prata/`;
5. verificação dos hashes da Bronze após a execução;
6. bloqueio da EDA Parte 2 caso haja fonte ausente, chave esperada ausente ou falha de reprodução material.

O inventário foi implementado em `src/auditar_bronze.py`, com saídas em `docs/source_inventory.md` e `saidas/auditoria_bronze/manifesto_bronze.json`.

## 3. Consequências e Impacto no Case

Todas as contagens tabulares oficiais foram confirmadas, assim como 64.948 contas, 14.753 pagantes ativos, 9.383 pares duplicados de atividades, 823 casos de vazamento potencial e R$ 436.442 de receita líquida de setembro. A Bronze permaneceu inalterada. Cinco Parquets foram materializados no gate inicial; eventos, uso, campanha e pesquisa foram adicionados à Prata pela Etapa 3. Na Etapa 4, amizades, posts e tickets também foram materializados na Prata, fechando a linhagem das fontes usadas pela feature store de segmentação.

Foi encontrada uma divergência não bloqueante: o pacote de 31/07 contém 12.431 PNGs únicos, enquanto o dicionário informa 12.426. Os cinco arquivos excedentes foram preservados e a causa permanece em aberto; nenhuma contagem foi ajustada artificialmente. O alerta não impede a EDA tabular, mas deverá ser considerado antes de qualquer uso de imagens.
