# ADR 011: Segmentação Não Supervisionada dos Pagantes Ativos

- **Data:** 05/11/2026
- **Autor(a) / Responsável:** Igor / Codex
- **Branch / Worktree:** `codex/plano-mestre-vitaliza`
- **Status:** Implementada

---

## 1. Contexto e Motivação

O Customer Segmentation Report da Semana 5 exige de três a quatro segmentos empiricamente sustentados, construídos sobre os 14.753 pagantes ativos em 30/09/2026 sem utilizar a informação de quem saiu. A segmentação precisa ser reproduzível, acionável e coerente com a arquitetura medalhão e com a governança da LGPD.

## 2. Decisão Adotada

Construir uma feature store exclusiva dos pagantes ativos a partir da camada Prata e aplicar K-Means sobre 16 atributos padronizados de comportamento, modo de treino, social, suporte, onboarding e contrato.

Foram excluídos da formação dos clusters: churn, status/data/motivo de saída, pesquisa de saída, campanha, abertura/clique, renovação automática e variáveis demográficas. Assimetrias foram tratadas com transformação `log1p`, extremos foram limitados no percentil 99 e ausências foram imputadas somente segundo regra explícita.

As soluções `k=3` e `k=4` foram comparadas por silhouette, Calinski–Harabasz, Davies–Bouldin, estabilidade ARI em oito reamostragens e tamanho mínimo de 5%. `k=5` foi mantido apenas como diagnóstico. Foi selecionado `k=3`, com silhouette amostral de 0,164, Davies–Bouldin de 2,007, ARI médio de 0,998 e menor cluster com 13,4% da base.

Os segmentos foram nomeados a partir dos centroides:

1. **Ativos ao ar livre:** 7.457 clientes (50,55%);
2. **Ativos guiados por vídeo:** 5.317 clientes (36,04%);
3. **Adormecidos sem hábito:** 1.979 clientes (13,41%).

## 3. Consequências e Impacto no Case

A segmentação fornece a base comum para os cartões de persona, hipóteses de drivers e priorização preliminar da Etapa 5, além de sustentar empiricamente o mini deck de tecnologia.

A estabilidade é elevada, mas a separação é baixa/moderada e há sobreposição visível entre os dois grupos ativos. Portanto, os nomes descrevem médias agregadas, não categorias humanas rígidas. Os clusters não substituem o modelo preditivo de churn nem a análise causal de uplift da Semana 10.

Os artefatos individuais são persistidos na camada Ouro; somente perfis agregados e gráficos sem identificadores são publicados em `saidas/`.
