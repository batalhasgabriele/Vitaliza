# Linhagem de métricas e features

> **Escopo após 12/11/2026:** A linhagem abaixo documenta a versão anterior da segmentação. A EDA de 32.583 históricos permanece descritiva; os cinco atributos e cortes da segmentação vigente estão em [12_consolidacao_semana5.md](12_consolidacao_semana5.md).

| Saída | Origem e transformação | Consumo |
|---|---|---|
| População ativa | Assinaturas Prata, status ativo e regras de elegibilidade | Segmentação, personas, tamanho dos grupos |
| Churn mensal | Eventos e população reconstruída; perdas / ativos no início do mês | EDA dos marcos, relatório e deck |
| Receita líquida | Pagamentos, valor numérico, taxa do canal e regra de duplicidade | EDA financeira |
| Receita mensal equivalente | Pagamento aprovado recente; anual dividido por 12, taxas e fallback | Perfil dos segmentos; não é receita contábil do mês |
| Recência | Último treino conhecido até o corte; dias desde a atividade | Distância do K-Means |
| Frequência 30/90 dias | Contagem de atividades limpas nas respectivas janelas | K-Means e perfil |
| Preferência ar livre/vídeo | Proporções individuais em uso mensal julho–setembro | K-Means e média das proporções por segmento |
| Renovação desligada | Estado contratual observado após agrupar | Perfil descritivo; não entra no clustering |
| Diferença experimental | Saídas em 30 dias / sorteados de cada braço menos controle | EDA e intervalos de incerteza |

As definições executáveis estão em `src/processar_eda.py`, `src/analisar_eda_marcos.py` e `src/segmentacao_clientes.py`. Os nomes, unidades e transformações de clustering também constam em `saidas/tabelas/metadados_segmentacao.json`.

## Impacto de mudanças
Mudança em Prata exige revalidar EDA e segmentação. Mudança nos atributos, regras ou amostra exige regenerar agregados, gráficos, personas, mini deck e documento mestre. Comparar com a versão anterior antes de publicar. Registrar decisão em ADR, inclusive quando a correção alterar legitimamente os números.

Não usar o nome de uma feature para concluir sua disponibilidade histórica: consultar [auditoria temporal](07_auditoria_temporal_coortes.md).
