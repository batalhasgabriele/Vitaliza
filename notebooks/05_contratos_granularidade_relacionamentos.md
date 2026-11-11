# Contratos, granularidade e relacionamentos

## Escopo
Contrato operacional da migração da EDA, corte 30/09/2026. Responsabilidade funcional: frente de Tecnologia; a pessoa responsável por aprovar exceções deve ser definida pelo grupo. Schemas observados e contagens reais ficam em [qa_engenharia_dados.json](../saidas/tabelas/qa_engenharia_dados.json), sem amostras pessoais.

| Tabela Prata | Uma linha representa | Chave candidata testada |
|---|---|---|
| usuarios_limpo | Conta | user_id |
| assinaturas_limpas | Assinatura | assinatura_id |
| onboarding_limpo | Resposta de onboarding | onboarding_id |
| atividades_limpas | Atividade | atividade_id |
| pagamentos_limpos | Tentativa/transação | pagamento_id |
| uso_mensal_limpo | Usuário no mês | user_id + mes |
| campanha_ago26_limpa | Atribuição experimental | user_id |
| pesquisa_saida_limpa | Resposta de pesquisa | resposta_id |
| feed_posts_limpos | Post | post_id |
| tickets_suporte_limpos | Ticket | ticket_id |
| amizades_limpas | Vínculo dirigido | seguidor_id + seguido_id |
| eventos_assinatura_limpos | Evento de assinatura | Sem ID; definição composta ainda exige decisão |

## Relações e severidades
Chaves nulas ou duplicadas nas candidatas acima bloqueiam a publicação da migração. Usuários referenciados devem existir no cadastro. A EDA atual também exige user_id único em assinaturas: se surgirem múltiplas assinaturas por pessoa, interromper e redesenhar a granularidade antes de agregar.

Eventos e atividades são 1:N com usuários. Agregar antes de incorporar à tabela de uma linha por pessoa. A junção do uso com janelas declara `many_to_one`; a consolidação final verifica a conservação das linhas e a unicidade. Essas verificações não substituem contratos detalhados de todas as colunas.

O schema observado é um inventário, não um schema completo imutável: tipos, domínios e política de evolução exigem revisão se uma fonte mudar. Não presumir que a regra de 14.753 clientes vale para cortes futuros.
