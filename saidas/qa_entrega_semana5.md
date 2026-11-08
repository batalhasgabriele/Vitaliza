# Verificação da entrega — 08/11/2026

| Verificação | Resultado observado | Limite |
|---|---|---|
| Testes automatizados | 13 passaram | Testes unitários não garantem validade causal |
| Notebooks 01, 02 e 03 | Executados em kernels isolados sem erro | Leem bases e agregados existentes; não refazem toda a cadeia |
| Imutabilidade Bronze | 14 hashes SHA-256 iguais ao manifesto | 12 tabelas e 2 ZIPs |
| População segmentada | 14.753 usuários únicos | Corte de setembro |
| Sensibilidade | 21 combinações, três especificações e k=2…8 | Mudanças de espaço impedem comparação ingênua da silhueta |
| Experimento | ICs de três comparações incluem zero | Não comprova ausência de efeito |
| Personas e mini deck | Números referenciados aos agregados publicados | Hipóteses de motivação ainda precisam de teste |
| Orçamento proposto | 200 × R$ 0,01 = R$ 2,00 | Piloto não executado; custos habituais não estimados |

A execução de notebooks preservou os arquivos originais e descartou outputs em memória para evitar publicar amostras pessoais. O registro com hash de cada fonte está em `tabelas/qa_notebooks_semana5.json`. Houve avisos de compatibilidade do loop de eventos Windows e de células antigas sem ID, sem impedir execução.

## Como entregar e continuar

1. Ler `customer_segmentation_report_semana5.md` como artefato de negócios.
2. Apresentar `mini_deck_eda_semana5.md` com os PNGs ao lado; são oito slides em Markdown, não um PPTX.
3. Disponibilizar código, dependências, decisões e racional de reprodução do repositório. A base original precisa ser obtida pelo acesso autorizado do grupo, pois não integra o Git.
4. Para uma pasta pública, selecionar somente documentos, código e gráficos agregados. Não copiar `dados/`, outputs individuais ou textos pessoais.
5. Exportação para PDF/PPTX e publicação/submissão no Drive/Adalove ainda não realizadas.

## Limitações abertas que afetam a ambição de excelência

Auditar exposição desde cadastro/assinatura e aplicar as 12 semanas exatas na candidata compacta. Reconstruir coorte histórica com atributos disponíveis antes da saída e janela completa, sem usar o futuro na seleção. Reconciliar quatro perdas de abril. Não há estimativa prospectiva de churn nem uplift individual para as personas. Esses pontos estão documentados; não foram resolvidos por simplesmente executar os notebooks.
