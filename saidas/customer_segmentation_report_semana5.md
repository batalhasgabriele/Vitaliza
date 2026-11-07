# Customer Segmentation Report — Semana 5

> **Status:** base empírica atualizada após a Etapa 4. Os três segmentos estão definidos; cartões de persona, hipóteses estruturadas e priorização serão finalizados na Etapa 5.

## 1. Evidências de contexto para a segmentação

### Subida do churn

A reconstrução por eventos harmonizados para Brasília observa churn médio de **5,68% ao mês em 2025** e **6,68% em jan–set/2026**, com pico de **8,13% e 1.158 perdas em abril**. A referência executiva informa 5,6%, 6,6% e 1.154; a diferença de quatro perdas em abril foi preservada como divergência de definição, sem ajuste artificial.

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

| Segmento | Clientes | Base | Receita líquida mensal | Evidência dominante |
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
4. **Acessível:** todos são ativos e alcançáveis por canais próprios; canal de cobrança foi perfilado.
5. **Acionável:** recência, formação de hábito e preferência por ar livre ou vídeo permitem intervenções distintas, que serão formalizadas na Etapa 5.

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

## 6. Seções a concluir na Etapa 5

- cartões de persona baseados nos três segmentos;
- hipóteses de drivers de churn por segmento;
- priorização preliminar: intervenção imediata, monitoramento ou não perturbe;
- alocação preliminar de canais e limites operacionais.
