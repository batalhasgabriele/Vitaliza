# Reconciliação e avaliação de impacto

> **Escopo após 12/11/2026:** Para a carteira consolidada, usar [12_consolidacao_semana5.md](12_consolidacao_semana5.md): mesmos 14.753 ativos, novas contagens por segmento e 2.255 renovações desligadas por eventos versus 2.250 no snapshot. As reconciliações abaixo conservam seu escopo/data original.

## Referência preservada
Antes da alteração, a Ouro e os agregados foram copiados para `dados/validacao_engenharia_baseline/`, fora do Git. Não compartilhar essa pasta: contém dados individuais. A EDA anterior também foi preservada para consulta.

## Comparação

**Resultado de 08/11/2026:** após tratar a compatibilidade da coluna legada de CEP, as duas execuções preservaram 32.583 usuários e o conteúdo das 101 colunas. Idempotência confirmada, sem bloqueadores e com publicação aprovada. Detalhes no [relatório de impacto](../saidas/impacto_engenharia_dados.md).
`src/validar_engenharia_dados.py` alinha as bases por user_id, confere população e compara todas as colunas. Valores numéricos aceitam tolerância absoluta/relativa de 1e-10; ausências são comparadas como ausências. Mudanças de tipo sem mudança de conteúdo são toleradas, mas o schema real fica registrado. A segunda execução compara a candidata com a primeira, para verificar idempotência do conteúdo da EDA.

Hashes de arquivos oficiais de Ouro e tabelas são comparados à baseline antes da publicação. Isso demonstra conservação dos demais resultados, não nova execução dos seus algoritmos. O resultado consolidado fica em [QA de engenharia](../saidas/tabelas/qa_engenharia_dados.json).

## Reconciliações de negócio ainda abertas
Abril apresenta 1.158 perdas reconstruídas versus 1.154 no enunciado. A migração para Prata não explica automaticamente a diferença. Pagamentos duplicados usam usuário + valor + dia como aproximação; pagamento_id identifica a tentativa, não necessariamente o ciclo econômico. Não mudar essa regra sem evidência que permita distinguir uma cobrança repetida de outra legítima.

Receita mensal equivalente de segmentos e faturamento de setembro são grandezas distintas. Nunca forçar igualdade entre elas. A precisão monetária em float é uma limitação; eventual migração para centavos/Decimal precisa declarar arredondamento das taxas e comparar os totais.

Na auditoria executada em 08/11/2026, foram encontrados 1.941 grupos de pagamentos aprovados com mesmo usuário, valor e dia, e 1.941 flags de duplicidade na Prata. Não foi inferido um identificador de ciclo inexistente. O diagnóstico não mudou a regra financeira.
