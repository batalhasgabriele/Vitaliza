# ADR 003: Metodologia de Faturamento de Setembro de 2026

- **Data:** 22/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
O faturamento contábil reportado para o mês de setembro de 2026 divergia entre diferentes áreas da Vitaliza em função de fusos horários, transações pendentes/recusadas, duplicidades de cobrança e taxas retidas pelas lojas de aplicativos e intermediadores de pagamento.

## 2. Decisão Adotada
O cálculo oficial de faturamento do mês de setembro/2026 deve seguir rigorosamente as 4 regras:
1. **Filtro de Status:** Considerar estritamente cobranças com `status = 'aprovado'`.
2. **Harmonização de Fuso Horário:** Converter timestamps de lojas (Apple e Google gravados em UTC com sufixo `Z`) para Horário de Brasília (UTC-3), alinhando ao corte contábil oficial de 30/09/2026 às 23h59.
3. **Expurgo de Duplicidades:** Desconsiderar cobranças duplicadas decorrentes de retentativas no mesmo ciclo/dia (93 casos somando R$ 6.830,40 indevidos), fixando o faturamento bruto real em **R$ 492.571,70** (~R$ 492.572,00).
4. **Aplicação de Taxas Líquidas de Intermediação:**
   - App Store e Google Play: dedução de 15,0% (Vitaliza retém 85,0%).
   - Web - Cartão: dedução de 3,5% (Vitaliza retém 96,5%).
   - Web - Pix Automático: dedução de 0,99% (Vitaliza retém 99,01%).
   - Faturamento líquido apurado: **R$ 436.442,35** (~R$ 436.442,00).

## 3. Consequências e Impacto no Case
- Estabelece a linha de base contábil oficial de MRR e faturamento líquido para as análises de LTV/CAC e cálculo do retorno financeiro líquido das estratégias de retenção.
