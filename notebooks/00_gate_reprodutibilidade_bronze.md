# Gate de Reprodutibilidade Bronze → Prata

**Data:** 04/11/2026
**Branch:** `codex/plano-mestre-vitaliza`
**Escopo:** Semana 5 — revalidação da Etapa 1 antes do início da EDA Parte 2.

## Pergunta

Os dados disponibilizados em `dados/brutos/` reproduzem as contagens, regras de qualidade e reconciliações já registradas no projeto sem alteração da camada Bronze?

## Fontes

- 11 arquivos CSV e `atividades.parquet` em `dados/brutos/`;
- dois pacotes ZIP em `dados/brutos/heatmaps/`;
- `docs/Vitaliza - Dicionário de dados.pdf`;
- `src/auditar_bronze.py`;
- `src/limpeza_qualidade_dados.py`;
- ADRs 001, 003, 004, 007, 009 e 014.

## Regras

1. A Bronze é estritamente somente leitura.
2. O inventário não publica amostras de linhas, dados pessoais ou textos livres.
3. Todos os arquivos são identificados por SHA-256.
4. Tabelas limpas são gravadas em Parquet na camada Prata.
5. Datas terminadas em `Z` são convertidas de UTC para `America/Sao_Paulo`; datas web sem `Z` são interpretadas como horário local.
6. Divergências com o dicionário são registradas, não corrigidas artificialmente.

## Reprodução

```powershell
$env:UV_CACHE_DIR='.uv-cache'
uv run --system-certs --with-requirements requirements-data.txt pytest -q
uv run --system-certs --with-requirements requirements-data.txt python src/auditar_bronze.py
uv run --system-certs --with-requirements requirements-data.txt python src/limpeza_qualidade_dados.py
```

## Resultados

- As 12 fontes tabulares estão presentes e suas contagens coincidem com o dicionário.
- As chaves candidatas auditadas não apresentaram duplicidades.
- `heatmaps_2026-09-30.zip` contém as 13.047 imagens esperadas.
- `heatmaps_2026-07-31.zip` contém 12.431 PNGs únicos, cinco acima da referência de 12.426. A causa não foi inferida; os arquivos foram preservados.
- A Bronze permaneceu inalterada após o pipeline, confirmado por SHA-256.
- Foram reproduzidos 64.948 usuários, 60 contas internas, 14.753 pagantes ativos e 12.503 pagantes com renovação ligada.
- Foram reproduzidos 9.383 pares de atividades duplicadas, resultando em 1.241.461 atividades válidas na Prata.
- Foram reproduzidos 823 casos de vazamento potencial ao usar retrospectivamente o snapshot de assinaturas de 30/09 em 31/07.
- A reconciliação de setembro reproduziu R$ 492.572 de receita bruta deduplicada e R$ 436.442 de receita líquida.

## Artefatos Prata gerados

| Arquivo | Linhas |
|:---|---:|
| `usuarios_limpo.parquet` | 64.948 |
| `assinaturas_limpas.parquet` | 32.583 |
| `onboarding_limpo.parquet` | 63.929 |
| `atividades_limpas.parquet` | 1.241.461 |
| `pagamentos_limpos.parquet` | 165.548 |
| `eventos_assinatura_limpos.parquet` | 275.565 |
| `uso_mensal_limpo.parquet` | 591.662 |
| `campanha_ago26_limpa.parquet` | 14.120 |
| `pesquisa_saida_limpa.parquet` | 643 |
| `amizades_limpas.parquet` | 113.207 |
| `feed_posts_limpos.parquet` | 119.187 |
| `tickets_suporte_limpos.parquet` | 4.422 |

`assinaturas_limpas.parquet` possui 60 linhas a menos que o snapshot bruto porque exclui contas internas/cortesia conforme a regra já aprovada. As três fontes sociais e de suporte foram adicionadas à Prata na Etapa 4 para fechar a linhagem da feature store de segmentação.

## Limitações

- A diferença de cinco heatmaps em julho exige investigação semântica futura, mas não bloqueia a EDA tabular.
- O inventário estrutural não substitui a reconstrução histórica de estados de assinatura.
- As demais fontes permanecem auditadas na Bronze até terem contrato de transformação explícito; eventos, uso, campanha e pesquisa foram adicionados à Prata quando a Etapa 3 definiu suas regras temporais.

## Definition of Done

O gate é considerado concluído porque as fontes foram inventariadas, a Bronze permaneceu intacta, os resultados anteriores foram reproduzidos, os artefatos Prata foram gerados nos caminhos medalhão e os alertas foram documentados. A próxima etapa autorizável é a EDA Parte 2, começando pela série histórica de churn e pelos três marcos de 2026.
# Relação com o pipeline completo

Este documento descreve o gate da Bronze. Para seguir até Prata/Ouro, consultar [pipeline ETL e Data Quality](00_pipeline_etl_data_quality.md). A validação de migração e idempotência da EDA é um controle adicional, registrado em [reconciliação](08_reconciliacao_dados_indicadores.md); não deve ser confundido com reexecução integral de todos os produtores.
