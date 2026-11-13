# ADR 022: Resolução mestre em leitura consolidada

- **Data:** 12/11/2026
- **Autor(a) / Responsável:** Igor (solicitação) / Codex (redação)
- **Branch / Worktree:** dev
- **Status:** Implementada

## 1. Contexto e Motivação
O documento mestre havia se tornado um índice. O usuário solicitou uma leitura completa da resolução, compreensível sem alternar entre diversos arquivos.

## 2. Decisão Adotada
Ampliar `saidas/resolucao_case_vitaliza_semana5.md` com narrativa integral de negócios e tecnologia, usando somente resultados vigentes. Manter sua fonte editorial em `docs/resolucao_mestre_semana5.template.md`, consumida pelo gerador, e incluí-la no pacote para que reprocessamentos não substituam o texto por um índice.

## 3. Consequências e Impacto no Case
O texto reúne contexto, populações, ETL, qualidade, EDA, método, personas, avaliação histórica, campanha, prioridades, cenários e limitações. Não altera dados ou resultados. Mudanças futuras de números exigem revisão editorial do mestre, conforme a regra de consistência cruzada. Os 28 testes e a reprodução anterior continuam sendo evidências da consolidação; esta alteração é documental.
