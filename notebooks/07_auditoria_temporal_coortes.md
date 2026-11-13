# Auditoria temporal e coortes

> **Escopo após 12/11/2026:** Auditoria anterior preservada como evidência dos riscos identificados. As coortes de maio/julho e os alvos vigentes estão definidos em [12_consolidacao_semana5.md](12_consolidacao_semana5.md).

## Pergunta
Cada atributo descreve o que era conhecido na data da decisão? Pessoas com menos tempo de observação estão sendo comparadas de maneira adequada?

## Regras atuais
Corte oficial: 30/09/2026, Brasília. Eventos com Z são convertidos de UTC. A EDA histórica alinha janelas ao desfecho de cancelados e ao corte de ativos: isso produz associações retrospectivas, não uma avaliação preditiva prospectiva. A segmentação descreve ativos em setembro, sem usar churn como entrada.

## Pontos de atenção
- Cadastro após o corte tem flag na Prata. A flag não constitui automaticamente uma política de exclusão em todas as análises.
- Atividades anteriores à assinatura podem representar uso freemium legítimo. Antes de removê-las, decidir se o atributo descreve relação com o app ou experiência como pagante.
- Uso mensal não permite separar precisamente a parte do mês anterior/posterior à assinatura sem informação diária.
- Janela de 90 dias não equivale a 12 semanas (84 dias). Uma migração deve reconstruir os atributos, comparar a segmentação e atualizar as personas.
- Ausência de registro não comprova zero atividade real. Flags de cobertura devem acompanhar imputações quando não há garantia de observação.
- Timestamp do evento não comprova quando a informação ficou disponível; a base não oferece garantia universal de `available_at`.

## Coorte histórica proposta
Reconstruir elegíveis em 31/07 com eventos disponíveis naquele corte; calcular atributos somente até essa data; agrupar sem target; observar saída nos 60 dias seguintes. Nunca filtrar retrospectivamente pelos ativos em setembro. Somente depois comparar saída por grupo. Essa reconstrução continua como evolução metodológica, não está incluída na migração de fonte da EDA.

## Diagnóstico executado em 08/11/2026
`src/auditar_temporalidade.py` encontrou 119 cadastros após o corte, 34.390 atividades anteriores à assinatura vinculadas a 9.471 usuários e 2.994 ativos com menos de 90 dias de assinatura. Essas contagens descrevem a base; não alteram automaticamente elegibilidade ou imputação. O vínculo de atividades com assinaturas foi validado como muitos-para-um. Fonte: [agregados temporais](../saidas/tabelas/auditoria_temporal_engenharia.json).

## Aceite da migração e evolução
Para a migração atual: população e atributos publicados devem ser comparados à baseline. Para uma mudança temporal futura: registrar o denominador e quantificar os clientes afetados, inclusive casos sem observação completa. Não substituir silenciosamente uma definição para melhorar a métrica.
