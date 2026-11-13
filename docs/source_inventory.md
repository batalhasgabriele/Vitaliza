# Inventário das Fontes — Camada Bronze

- **Gerado em:** `2026-11-12T19:54:44-03:00`
- **Status:** **ATENCAO**
- **Política:** auditoria somente leitura; nenhum conteúdo de linha ou dado pessoal é publicado.
- **Data de corte do case:** `30/09/2026`.

## Fontes tabulares

| Arquivo | Linhas observadas | Referência | Confere | Tamanho (MiB) | Duplicidades na chave candidata |
|:---|---:|---:|:---:|---:|---:|
| `usuarios.csv` | 64,948 | 64,948 | ✅ | 7.49 | 0 |
| `assinaturas.csv` | 32,643 | 32,643 | ✅ | 2.41 | 0 |
| `amizades.csv` | 113,480 | 113,480 | ✅ | 3.57 | 0 |
| `campanha_ago26.csv` | 14,120 | 14,120 | ✅ | 1.27 | 0 |
| `eventos_assinatura.csv` | 275,565 | 275,565 | ✅ | 16.86 | 0 |
| `pagamentos.csv` | 165,548 | 165,548 | ✅ | 11.05 | 0 |
| `uso_mensal.csv` | 591,662 | 591,662 | ✅ | 18.25 | 0 |
| `atividades.parquet` | 1,254,475 | 1,254,475 | ✅ | 18.26 | 0 |
| `onboarding.csv` | 63,929 | 63,929 | ✅ | 5.46 | 0 |
| `pesquisa_saida.csv` | 643 | 643 | ✅ | 0.04 | 0 |
| `feed_posts.csv` | 119,309 | 119,309 | ✅ | 8.48 | 0 |
| `tickets_suporte.csv` | 4,422 | 4,422 | ✅ | 0.47 | 0 |

## Pacotes de heatmaps

| Arquivo | Imagens observadas | Referência | Confere | Compactado (MiB) | Descompactado (MiB) |
|:---|---:|---:|:---:|---:|---:|
| `heatmaps_2026-07-31.zip` | 12,431 | 12,426 | ⚠️ | 49.29 | 46.89 |
| `heatmaps_2026-09-30.zip` | 13,047 | 13,047 | ✅ | 51.75 | 49.23 |

## Alertas e bloqueios

- Contagem divergente em heatmaps_2026-07-31.zip: 12431 arquivos vs. 12426 esperados.

## Schemas e cobertura temporal

### `usuarios.csv`

- **Schema inferido:** `user_id` (VARCHAR), `email` (VARCHAR), `data_cadastro` (TIMESTAMP), `data_nascimento` (DATE), `sexo` (VARCHAR), `cidade` (VARCHAR), `uf` (VARCHAR), `cep_prefixo` (VARCHAR), `canal_aquisicao` (VARCHAR), `sistema` (VARCHAR), `versao_app` (VARCHAR), `relogio_conectado` (VARCHAR)
- **Nulos observados:** `data_nascimento`=3,301, `sexo`=3,142, `cep_prefixo`=1,894
- **data_cadastro:** `2020-09-01 12:00:00` a `2027-04-04 10:44:09`; não convertíveis: 0.
- **data_nascimento:** `1900-01-01` a `2031-05-12`; não convertíveis: 0.

### `assinaturas.csv`

- **Schema inferido:** `assinatura_id` (VARCHAR), `user_id` (VARCHAR), `plano_atual` (VARCHAR), `canal_cobranca` (VARCHAR), `inicio` (DATE), `status_atual` (VARCHAR), `renovacao_automatica` (VARCHAR), `data_fim` (DATE), `motivo_fim` (VARCHAR)
- **Nulos observados:** `data_fim`=14,813, `motivo_fim`=14,813
- **inicio:** `2020-09-08` a `2026-09-30`; não convertíveis: 0.
- **data_fim:** `2024-07-07` a `2026-09-30`; não convertíveis: 0.

### `amizades.csv`

- **Schema inferido:** `seguidor_id` (VARCHAR), `seguido_id` (VARCHAR), `desde` (DATE)
- **Nulos observados:** nenhum.
- **desde:** `2020-09-05` a `2026-10-09`; não convertíveis: 0.

### `campanha_ago26.csv`

- **Schema inferido:** `user_id` (VARCHAR), `grupo` (VARCHAR), `enviado_em` (TIMESTAMP), `canal` (VARCHAR), `titulo_mensagem` (VARCHAR), `oferta` (VARCHAR), `abriu_push` (BOOLEAN), `abriu_email` (BOOLEAN), `clicou` (BOOLEAN)
- **Nulos observados:** `enviado_em`=3,579, `canal`=3,579, `titulo_mensagem`=3,579, `oferta`=10,648
- **enviado_em:** `2026-08-10 10:00:00` a `2026-08-10 10:00:00`; não convertíveis: 0.

### `eventos_assinatura.csv`

- **Schema inferido:** `user_id` (VARCHAR), `data_hora` (TIMESTAMP WITH TIME ZONE), `evento` (VARCHAR), `plano` (VARCHAR), `canal_cobranca` (VARCHAR), `detalhe` (VARCHAR)
- **Nulos observados:** `plano`=72,873, `detalhe`=269,494
- **data_hora:** `2024-07-01 06:11:50-03` a `2026-09-30 22:59:33-03`; não convertíveis: 0.

### `pagamentos.csv`

- **Schema inferido:** `pagamento_id` (VARCHAR), `user_id` (VARCHAR), `data_hora` (TIMESTAMP WITH TIME ZONE), `valor` (VARCHAR), `metodo` (VARCHAR), `status` (VARCHAR), `tentativa` (BIGINT)
- **Nulos observados:** nenhum.
- **data_hora:** `2024-07-02 06:14:11-03` a `2026-09-30 22:54:51-03`; não convertíveis: 0.

### `uso_mensal.csv`

- **Schema inferido:** `user_id` (VARCHAR), `mes` (VARCHAR), `atividades` (BIGINT), `atividades_ar_livre` (BIGINT), `atividades_video` (BIGINT), `minutos` (BIGINT), `dias_ativos` (BIGINT), `sessoes_app` (BIGINT)
- **Nulos observados:** nenhum.
- **mes:** `2025-01` a `2026-09`; não convertíveis: 0.

### `atividades.parquet`

- **Schema inferido:** `atividade_id` (VARCHAR), `user_id` (VARCHAR), `inicio` (VARCHAR), `tipo` (VARCHAR), `duracao_min` (DOUBLE), `distancia_km` (DOUBLE), `ritmo_min_km` (DOUBLE), `fc_media` (DOUBLE), `origem` (VARCHAR), `gps_ok` (BOOLEAN), `treino_com` (VARCHAR)
- **Nulos observados:** `distancia_km`=574,835, `ritmo_min_km`=582,290, `fc_media`=764,987
- **inicio:** `2026-01-01 05:00:00` a `2026-10-01 00:59:00`; não convertíveis: 0.

### `onboarding.csv`

- **Schema inferido:** `onboarding_id` (VARCHAR), `user_id` (VARCHAR), `respondido_em` (DATE), `objetivo_texto` (VARCHAR), `como_conheceu` (VARCHAR), `nivel` (VARCHAR), `dias_por_semana` (VARCHAR)
- **Nulos observados:** `objetivo_texto`=5,467, `como_conheceu`=4,586, `nivel`=4,513, `dias_por_semana`=6,368
- **respondido_em:** `2020-09-01` a `2026-09-30`; não convertíveis: 0.

### `pesquisa_saida.csv`

- **Schema inferido:** `resposta_id` (VARCHAR), `user_id` (VARCHAR), `respondido_em` (DATE), `motivo_principal` (VARCHAR), `comentario` (VARCHAR)
- **Nulos observados:** `comentario`=183
- **respondido_em:** `2026-06-01` a `2026-09-30`; não convertíveis: 0.

### `feed_posts.csv`

- **Schema inferido:** `post_id` (VARCHAR), `user_id` (VARCHAR), `data_hora` (TIMESTAMP), `texto` (VARCHAR), `curtidas` (BIGINT)
- **Nulos observados:** nenhum.
- **data_hora:** `2025-07-01 06:07:55` a `2026-10-07 18:52:16`; não convertíveis: 0.

### `tickets_suporte.csv`

- **Schema inferido:** `ticket_id` (VARCHAR), `user_id` (VARCHAR), `aberto_em` (TIMESTAMP), `canal` (VARCHAR), `texto_cliente` (VARCHAR), `categoria_atendente` (VARCHAR), `status` (VARCHAR), `resolvido_em` (DATE)
- **Nulos observados:** `resolvido_em`=1,505
- **aberto_em:** `2025-07-01 08:15:00` a `2026-09-30 21:46:00`; não convertíveis: 0.
- **resolvido_em:** `2025-07-03` a `2026-10-07`; não convertíveis: 0.

## Interpretação

Este inventário valida presença, integridade de arquivo, contagens, schemas inferidos, nulos, chaves candidatas e intervalos temporais. Ele não substitui as validações semânticas e de negócio da camada Prata, que tratarão fusos, estados históricos, cobranças duplicadas e regras de elegibilidade.
