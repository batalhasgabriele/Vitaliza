> HISTORICO SUPERADO PELA ADR 020. Contém resultados/interpretações não vigentes. Não usar na entrega.

# Customer Segmentation Report — Semana 5

> **Versão executiva — 08/11/2026.** Corte em 30/09/2026. Personas descritivas e piloto proposto, ainda não executado. Complemento técnico: [validação e sensibilidade](validacao_semana5.md).

## 1. Evidências de contexto para a segmentação

### Subida do churn

A reconstrução por eventos harmonizados para Brasília observa churn médio de **5,68% ao mês em 2025** e **6,68% em jan–set/2026**, com pico de **8,13% e 1.158 perdas em abril**. A referência executiva informa 5,6%, 6,6% e 1.154; a causa da diferença de quatro perdas em abril permanece não reconciliada, sem ajuste artificial.

### Reajuste de março

No plano mensal, a média observada passou de **10,22% em jan–fev** para **12,97% em mar–abr**. Isso sustenta uma hipótese de sensibilidade a preço para teste por coorte e tempo de casa, mas não demonstra causalidade: sazonalidade, composição de clientes e vencimentos mudam simultaneamente.

### Ponto cego da pesquisa de saída

Entre junho e setembro foram observadas **3.389 expirações**, sendo **2.271 nas lojas** e **1.118 na Web**. Os **641 respondentes únicos** da pesquisa são 100% Web; **288 respondentes únicos** ainda estavam ativos no corte, correspondendo a **289 respostas**. Motivos declarados não podem ser generalizados para os aproximadamente 70% que pagam pelas lojas.

### Campanha randomizada de agosto

No horizonte ITT completo de 30 dias, o churn foi:

| Braço | Sorteados | Churn 30d | Diferença vs. controle | p-valor |
|:---|---:|---:|---:|---:|
| Controle | 3.579 | 5,48% | 0,00 p.p. | — |
| Desafio | 3.515 | 5,18% | −0,30 p.p. | 0,576 |
| Cupom | 3.472 | 4,64% | −0,84 p.p. | 0,108 |
| Conteúdo | 3.554 | 6,13% | +0,66 p.p. | 0,235 |

Nenhuma comparação atingiu significância estatística de 5%. Portanto, ainda não é válido classificar indivíduos como “persuadíveis” ou “não perturbe” com base apenas nesses resultados agregados. Abertura e clique são variáveis pós-tratamento e não foram usados para selecionar participantes na análise causal.

## 2. Método de segmentação

Os clusters foram construídos exclusivamente sobre os **14.753 pagantes ativos no corte**, sem churn, status de saída, pesquisa de saída, campanha ou informação posterior como entrada. Idade, sexo, UF e renovação automática também não determinaram os grupos.

Foram combinadas 16 variáveis de recência, frequência, tendência, regularidade, diversidade, modo de treino, social, suporte, tempo de casa, onboarding e contrato. Valores assimétricos receberam transformação logarítmica e limite no percentil 99; todas as variáveis foram padronizadas antes do K-Means.

Entre as soluções elegíveis, `k=3` apresentou silhouette amostral de **0,164**, Davies–Bouldin de **2,007**, estabilidade média **ARI=0,998** e menor grupo com **13,4%** da base. A separação é moderada/baixa, mas muito estável: os segmentos são úteis como estrutura descritiva e acionável, não como fronteiras naturais rígidas.

## 3. Segmentos empíricos

| Segmento | Clientes | Base | Receita líquida mensal equivalente estimada | Evidência dominante |
|:---|---:|---:|---:|:---|
| **Ativos ao ar livre** | 7.457 | 50,55% | R$ 209.995,60 | Mediana de 10 treinos em 30 dias, recência de 2 dias e 82,3% das atividades ao ar livre. |
| **Ativos guiados por vídeo** | 5.317 | 36,04% | R$ 152.203,80 | Mediana de 10 treinos em 30 dias, recência de 2 dias e 92,2% das atividades em vídeo. |
| **Adormecidos sem hábito** | 1.979 | 13,41% | R$ 43.351,69 | Mediana de zero treino em 30 dias, recência de 68 dias e regularidade de apenas 12,3% nos três meses. |

![Perfis relativos dos segmentos](segmentacao_heatmap_perfis.png)

![Tamanho e receita dos segmentos](segmentacao_tamanho_receita.png)

O grupo adormecido concentra **98,2% de planos anuais** e **59,6% com renovação desligada** no corte, contra 9,5% nos ativos ao ar livre e 6,8% nos ativos por vídeo. A renovação desligada foi observada apenas depois da formação dos clusters; ela não participou da distância do algoritmo.

## 4. Validação preliminar nos cinco critérios

1. **Mensurável:** tamanho, participação e receita estão calculados para toda a população ativa.
2. **Substancial:** o menor segmento ainda reúne 1.979 clientes e 13,4% da base.
3. **Diferenciável:** o grupo adormecido é claramente distinto; os dois grupos ativos se sobrepõem em intensidade e se diferenciam principalmente pelo modo de treino.
4. **Acessível, sob condição:** canal de cobrança foi perfilado, mas não comprova permissão de contato, telefone válido ou push habilitado. A elegibilidade precisa ser verificada antes de qualquer campanha.
5. **Acionável:** recência, formação de hábito e preferência por ar livre ou vídeo permitem os testes distintos descritos abaixo. Eficácia permanece uma hipótese.

## 5. Limitações e governança

1. **Correlação não é causa:** o aumento após o reajuste é observacional e não estima elasticidade isolada.
2. **Viés de canal:** a pesquisa de saída cobre Web e exclui estruturalmente as lojas.
3. **Viés de seleção:** responder à pesquisa é uma escolha; respondentes podem diferir dos não respondentes.
4. **Janela experimental:** o data room oferece 30 dias completos após 10/08, mas não 60 dias completos.
5. **Pós-tratamento:** abertura e clique não podem definir a comparação ITT principal.
6. **LGPD e minimização:** textos, GPS e imagens não devem ser expostos nos cartões; personas devem usar agregados e evitar discriminação demográfica.
7. **Não perturbe:** a alternativa de não contato permanece legítima, mas a identificação individual desse grupo exige evidência incremental mais robusta na Semana 10.
8. **Separação dos clusters:** silhouette de 0,164 e a PCA mostram sobreposição relevante entre os dois grupos ativos; nomes resumem centroides, não tipos humanos absolutos.
9. **Segmentação não é risco:** o grupo adormecido possui mais renovação desligada, mas cluster não substitui probabilidade de churn nem estima uplift causal.

## 6. Cartões de persona ancorados em dados

Os cartões representam grupos estatísticos, não pessoas reais. Não inferimos profissão, renda, idade, saúde ou motivações individuais. Percentuais de modalidade são médias das proporções individuais, não participação agregada de todos os treinos.

### Ativos ao ar livre — manter a rotina externa

- **Evidência:** 7.457 pessoas (50,55%), mediana de 10 treinos em 30 dias e recência de 2 dias. Média individual de 82,3% ao ar livre. Plano anual em 52,5% e lojas em 70,8%.
- **Valor representado:** R$ 209.995,60 de receita líquida mensal equivalente estimada.
- **Necessidade hipotética:** manter continuidade e variedade da rotina. A base não comprova insatisfação ou desejo de competir.
- **Driver a investigar:** interrupção do hábito, fricção no registro do treino e perda de relevância do conteúdo.
- **Ação proposta:** monitorar queda de atividade e testar convite opcional a treino ao ar livre. Sucesso: recuperação de atividade e retenção incremental contra controle.

### Ativos guiados por vídeo — preservar a conveniência

- **Evidência:** 5.317 pessoas (36,04%), mediana de 10 treinos em 30 dias e recência de 2 dias. Média individual de 92,2% em vídeo. Plano anual em 49,3% e lojas em 70,3%.
- **Valor representado:** R$ 152.203,80 de receita líquida mensal equivalente estimada.
- **Necessidade hipotética:** encontrar sessões úteis e manter regularidade. Não inferimos falta de tempo a partir da modalidade.
- **Driver a investigar:** fadiga de catálogo ou dificuldade para encontrar uma sessão adequada.
- **Ação proposta:** monitorar e testar seleção editorial de vídeos. Sucesso: atividade incremental em 30 dias, sem aumento de descadastro ou churn.

### Adormecidos sem hábito — investigar antes de ampliar contato

- **Evidência:** 1.979 pessoas (13,41%), mediana de zero treino em 30 dias e 68 dias desde o último treino. Plano anual em 98,2%. Renovação desligada em 59,6%, observada apenas após agrupar.
- **Valor representado:** R$ 43.351,69 de receita líquida mensal equivalente estimada.
- **Necessidade hipotética:** retomar com menor esforço ou ajustar a assinatura a uma pausa. Ausência de registro não comprova abandono de atividade física.
- **Driver a investigar:** hábito não formado e descompasso entre contrato e uso. Não é possível distinguir individualmente persuadíveis de pessoas prejudicadas pelo contato.
- **Ação proposta:** intervenção imediata significa preparar um piloto controlado e verificar elegibilidade, não disparar para todo o grupo. Sucesso: retenção incremental com custo sustentável e sem dano aos participantes.

## 7. Hipóteses por segmento e mecanismos de aprendizado

| Galho da árvore | Público | Ação a testar | Resultado esperado e como verificar |
|---|---|---|---|
| Características de entrada | Adormecidos com onboarding antigo | Reconfirmar preferências voluntariamente | Mais sessões em 30 dias versus controle; resposta não define a população ITT |
| Comportamento de uso | Adormecidos | Oferecer rotina curta com conteúdo existente | Retomada de treino e menor saída em 60 dias versus controle |
| Comportamento de uso | Ativos por vídeo com queda de uso | Seleção editorial alinhada à modalidade | Recuperação de atividade, sem presumir causa da queda |
| Ciclo de vida e contrato | Mensais de ambos os grupos ativos | Testar comunicação de valor antes de testar desconto | Menor saída com margem incremental positiva; estratificar por plano |
| Comunidade e social | Ativos ao ar livre | Convite opcional a atividade compartilhada | Maior regularidade versus controle; não interpretar associação social como causalidade |
| Experiência e suporte | Qualquer grupo com problema documentado | Resolver a fricção identificada | Redução da reincidência e melhora da retenção; atendimento necessário nunca é negado ao controle |

Hipóteses são mecanismos concorrentes e podem coexistir na mesma pessoa. A árvore organiza investigação, sem provar causas mutuamente exclusivas.

## 8. Priorização e orçamento preliminar

**Proposta de piloto, não lista de envio:** selecionar até 400 adormecidos elegíveis, estratificar por plano e canal de cobrança e sortear 200 para uma única mensagem por e-mail com conteúdo existente e 200 para controle sem campanha adicional. Manter atendimento solicitado em ambos. Se houver menos elegíveis, reduzir simetricamente. A seleção não usa abertura/clique posterior. O piloto pequeno verifica viabilidade e possíveis danos; não foi dimensionado para comprovar uma redução pequena de churn.

| Prioridade | Público | Conduta |
|---|---|---|
| Imediata | Adormecidos elegíveis | Piloto limitado e diagnóstico, com revisão humana |
| Monitoramento | Ambos os grupos ativos | Acompanhar recência e frequência. Desenhar testes específicos sem desconto automático |
| Sem campanha adicional | Controle, recusas de contato e pessoas sem elegibilidade comprovada | Preservar atendimento habitual. Esta é uma regra operacional, não uma classificação causal de “sleeping dog” |

| Recurso do piloto mensal | Quantidade máxima | Custo | Teto do case |
|---|---:|---:|---:|
| E-mail | 200 envios | R$ 2,00 | Sem limite prático |
| Push | 0 | R$ 0,00 | 1 por semana por assinante |
| WhatsApp | 0 | R$ 0,00 | 1.500 mensagens/mês |
| CS proativo adicional | 0 | R$ 0,00 | 300 atendimentos/mês |
| Descontos e API GenAI | 0 | R$ 0,00 | Integram o orçamento global |
| **Total incremental planejado** | | **R$ 2,00** | **R$ 40.000/mês** |

Saldo de R$ 39.998,00 não é autorização de gasto. Usamos texto editorial existente, sem API de produção. Custos habituais de atendimento não foram estimados e devem ser reconciliados pelo operador antes da execução. Não é necessário consumir os tetos para demonstrar viabilidade.

**Protocolo antes do envio:** registrar população elegível, semente e atribuição, conteúdo, datas, consentimento aplicável e supressões. Definir churn em 60 dias como desfecho primário, retomada em 30 dias como secundário e descadastro/reclamações como guardrails. Acompanhar ambos os braços por janela completa e analisar por intenção de tratar. Dimensionar a amostra para uma expansão com baseline e efeito mínimo relevante acordados. Suspender novos envios diante de reclamação grave e revisar diferenças com incerteza, sem declarar vitória por inspeções repetidas de p-valor.

## 9. Limites adicionais para uma interpretação responsável

- Receita equivalente divide pagamentos anuais por 12 e aplica taxas, com fallback quando falta pagamento. Não é faturamento contábil de setembro, margem, LTV, nem receita em risco. Risco financeiro requer probabilidade de saída e horizonte compatíveis, ainda não estimados.
- Os 16 atributos incluem plano e canal. A [sensibilidade](validacao_semana5.md) compara sua remoção e uma especificação comportamental compacta. Estabilidade alta não elimina a separação baixa nem valida causalidade.
- A base ativa de setembro não contém a janela completa de 60 dias até 29/11. Não inventamos churn futuro por persona. Os exemplos da aula em julho são outra população e não devem ser copiados como resultados próprios.
- A EDA antiga alinha janelas ao cancelamento de quem saiu e ao corte de quem ficou. Suas AUCs são associações retrospectivas, não desempenho de previsão prospectiva. A curva antiga por duração não substitui Kaplan–Meier com censura.
- Medidas agregadas de uso incluem períodos com regras de registro diferentes. Novos assinantes têm exposições distintas, e janelas de atividades e uso mensal não são idênticas. Validar esse efeito antes de promover uma nova segmentação.
- O piloto proposto exige revisão das preferências de contato e minimização dos dados. O pacote público deve conter agregados, nunca GPS, textos pessoais ou linhas identificáveis.

## 10. Rastreabilidade

Perfis: `tabelas/perfil_segmentos.csv`; método: `../src/segmentacao_clientes.py`; experimentos de robustez e ICs: `../src/validar_entrega_semana5.py`; contexto: `eda_etapa3_marcos_2026.md`; decisões: ADRs 011, 012 e 013. Cada regeneração da segmentação exige revisão conjunta deste relatório, do documento mestre e do mini deck.
