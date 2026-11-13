# Validação suplementar da Semana 5

> **Escopo após 12/11/2026:** Validação histórica anterior à ADR 020. Para resultados e verificações vigentes, usar [qa_entrega_semana5.md](qa_entrega_semana5.md).

A segmentação publicada permanece como referência descritiva. Experimentos abaixo não foram selecionados pelo churn.

| variante               |   k |    inercia |   silhouette |   menor_grupo_pct |   ari_vs_publicado |   bootstrap_ari_media |   bootstrap_ari_min |
|:-----------------------|----:|-----------:|-------------:|------------------:|-------------------:|----------------------:|--------------------:|
| original_16            |   2 | 190996.383 |        0.297 |            14.994 |              0.323 |               nan     |             nan     |
| original_16            |   3 | 168615.130 |        0.164 |            13.414 |              1.000 |                 0.997 |               0.995 |
| original_16            |   4 | 153874.765 |        0.160 |            12.947 |              0.684 |                 0.971 |               0.934 |
| original_16            |   5 | 141596.227 |        0.170 |             3.803 |              0.607 |               nan     |             nan     |
| original_16            |   6 | 132553.094 |        0.174 |             3.803 |              0.473 |               nan     |             nan     |
| original_16            |   7 | 127954.744 |        0.160 |             3.803 |              0.413 |               nan     |             nan     |
| original_16            |   8 | 120178.161 |        0.162 |             3.803 |              0.395 |               nan     |             nan     |
| sem_contrato_14        |   2 | 163181.064 |        0.333 |            14.573 |              0.327 |               nan     |             nan     |
| sem_contrato_14        |   3 | 140643.777 |        0.193 |            13.014 |              0.988 |                 0.998 |               0.996 |
| sem_contrato_14        |   4 | 126010.847 |        0.190 |            12.479 |              0.657 |                 0.925 |               0.827 |
| sem_contrato_14        |   5 | 116431.407 |        0.201 |             8.805 |              0.545 |               nan     |             nan     |
| sem_contrato_14        |   6 | 105137.837 |        0.210 |             3.809 |              0.526 |               nan     |             nan     |
| sem_contrato_14        |   7 |  97724.024 |        0.206 |             3.809 |              0.449 |               nan     |             nan     |
| sem_contrato_14        |   8 |  93319.058 |        0.187 |             3.809 |              0.358 |               nan     |             nan     |
| comportamental_4_proxy |   2 |  39800.112 |        0.397 |            17.400 |              0.296 |               nan     |             nan     |
| comportamental_4_proxy |   3 |  29078.814 |        0.336 |            14.404 |              0.931 |                 0.996 |               0.994 |
| comportamental_4_proxy |   4 |  23215.799 |        0.328 |            14.228 |              0.599 |                 0.976 |               0.972 |
| comportamental_4_proxy |   5 |  19610.488 |        0.340 |             9.734 |              0.520 |               nan     |             nan     |
| comportamental_4_proxy |   6 |  16503.212 |        0.334 |             8.846 |              0.475 |               nan     |             nan     |
| comportamental_4_proxy |   7 |  14883.599 |        0.312 |             8.412 |              0.401 |               nan     |             nan     |
| comportamental_4_proxy |   8 |  13584.258 |        0.308 |             8.412 |              0.354 |               nan     |             nan     |

Silhuetas usam a mesma amostra determinística de 2.500 pessoas. Não comparar diretamente com a amostra de 5.000 da primeira versão. ARI entre variantes mede sensibilidade à especificação, não qualidade absoluta. Bootstrap: cinco reamostras com reposição, com StandardScaler reajustado; imputação, teto e log permanecem fixados na base completa, portanto não avalia toda a incerteza do pré-processamento. A variante de quatro atributos é uma aproximação de 90 dias, não uma reprodução literal da aula.

## Incerteza do experimento

| grupo    |   sorteados |   perdas_30d |   diferenca_vs_controle_pp |   ic95_inferior_pp |   ic95_superior_pp |   p_bonferroni_3 |
|:---------|------------:|-------------:|---------------------------:|-------------------:|-------------------:|-----------------:|
| conteudo |        3554 |          218 |                      0.658 |             -0.428 |              1.743 |            0.705 |
| controle |        3579 |          196 |                      0.000 |            nan     |            nan     |          nan     |
| cupom    |        3472 |          161 |                     -0.839 |             -1.862 |              0.183 |            0.324 |
| desafio  |        3515 |          182 |                     -0.299 |             -1.344 |              0.747 |            1.000 |

ICs normais de 95% para diferença de proporções independentes, não simultâneos. P-valores corrigidos para três comparações por Bonferroni. Intervalo cruzando zero não comprova equivalência ou ausência de efeito. Não há atribuição individual de uplift.
