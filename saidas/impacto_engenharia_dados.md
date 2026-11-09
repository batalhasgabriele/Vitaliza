# Impacto das melhorias de engenharia de dados

**Data local:** 08/11/2026. **Branch:** dev. **Execução aprovada:** `20261109T001700Z_df73ad48` (identificador em UTC).

## Resultado
A migração da EDA para Prata não alterou o conteúdo analítico publicado, com tolerância numérica absoluta/relativa de 1e-10. A população permaneceu em 32.583 usuários, com 101 colunas. Duas execuções independentes da EDA em staging reproduziram esse conteúdo. Não houve bloqueadores de chave/referência, e a candidata foi publicada.

| Controle | Resultado |
|---|---|
| População da EDA versus baseline | Igual nas duas execuções |
| Colunas alteradas versus baseline | Nenhuma |
| Comparação entre as duas execuções | Nenhuma alteração |
| Demais arquivos oficiais Ouro e tabelas existentes | Hashes iguais à baseline antes da publicação |
| Testes automatizados | 16 passaram |
| Tabelas Bronze | 12 hashes conferidos contra manifesto |

Primeira tentativa: a coluna legada `cep_prefixo` passou de numérica para textual ao consumir Prata. O gate detectou a mudança e não publicou. A compatibilidade numérica foi restaurada na Ouro, mantendo o identificador textual na Prata e em `cep_prefixo_str`. A execução seguinte passou. Nenhuma regra financeira ou população foi ajustada para forçar o resultado.

## Melhorias entregues
Leituras da EDA uniformizadas na Prata; controles de chaves, referências e granularidade; comparação por atributo; baseline preservada; staging com logs; hashes das entradas; escrita temporária seguida de substituição do arquivo EDA; seis documentos de engenharia em notebooks e ADR 017. Pastas privadas de baseline/execuções estão ignoradas pelo Git.

## Auditoria temporal e financeira
Foram observados 119 cadastros após o corte, 34.390 atividades anteriores à assinatura vinculadas a 9.471 usuários e 2.994 ativos com menos de 90 dias de assinatura. As atividades podem ser uso freemium legítimo. Foram identificados 1.941 grupos de cobranças pela regra atual de usuário/valor/dia, sem comprovação independente do ciclo econômico. Esses achados foram registrados sem exclusões automáticas.

## Limites do que foi validado
O teste de idempotência cobre a EDA, não a regeneração integral de Bronze até todos os relatórios. A conservação dos segmentos foi conferida por hashes, sem novo treinamento do clustering. A publicação atômica protege um arquivo, não toda a cadeia. Contratos detalhados de todos os campos, publicação por versão da cadeia completa, alteração da deduplicação financeira e reconstrução histórica de coortes continuam evoluções separadas. A inexistência de mudança numérica não resolve limitações metodológicas já documentadas.

Evidências: [QA completo](tabelas/qa_engenharia_dados.json), [auditoria temporal](tabelas/auditoria_temporal_engenharia.json), [mapa do pipeline](../notebooks/00_pipeline_etl_data_quality.md), [ADR 017](../decisoes/017-engenharia-prata-e-comparacao-resultados.md).
