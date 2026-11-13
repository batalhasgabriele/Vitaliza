# ADR 024: Auditoria e correções do deck executivo

- **Data:** 12/11/2026
- **Autor(a) / Responsável:** Lorena
- **Branch / Worktree:** dev
- **Status:** Proposta, aguardando discussão com o time

---

## 1. Contexto e Motivação

O deck executivo de 7 slides foi alinhado à consolidação da ADR 020, mas um feedback e a auditoria seguinte encontraram números que distorciam a leitura: receita anual por setembro × 12, piloto sem poder estatístico para os cenários apresentados, orçamento com ofertas fora da estratégia, sinal de vínculo social com vazamento de desfecho e métricas de receita e churn sem rótulo.

## 2. Decisão Adotada

1. **Fonte dos números:** consolidação da ADR 020; números complementares em `src/numeros_deck_executivo.py`, gravados em `saidas/deck_executivo/auditoria/` (só agregados).
2. **Receita anual:** receita líquida de caixa dos últimos 12 meses (R$ 4,7 mi), não setembro × 12.
3. **Fatores de churn:** coeficiente de incerteza (informação mútua ÷ entropia) em cortes fixos, com atributos medidos só até o corte.
4. **Vínculo social:** conexões contadas só até o corte; sem evidência de associação (H6).
5. **Piloto:** dimensionar pelo menor efeito detectável; randomizar os 2.255 elegíveis com renovação desligada (≥ 2,9 p.p.) em vez de 200 por braço (≥ 6,9 p.p.).
6. **Orçamento:** em fases condicionadas à evidência (pilotos, canais, ofertas), com IA a calcular.
7. **Glossário:** receita de caixa, receita equivalente, margem e três medidas de churn.

## 3. Consequências e Impacto no Case

- **Novos arquivos:** `src/numeros_deck_executivo.py`, `saidas/deck_executivo/auditoria/` e `notebooks/14_auditoria_deck_executivo.md`.
- **Deck:** slides corrigidos conforme o notebook 14.
- **Diverge da ADR 020 em:** tamanho do piloto (400 → 2.255 randomizados) e proposta de ampliar a prioridade 2 para 1.783 mensalistas novos. Adotar exige atualizar a consolidação.
- **Limites:** datas de evento sem validação humana; taxas de coorte não são risco individual; associações, não causas.
