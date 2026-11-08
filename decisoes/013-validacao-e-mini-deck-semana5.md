# ADR 013: Sensibilidade, incerteza e fechamento local da Semana 5

- **Data:** 08/11/2026
- **Autor(a) / Responsável:** Igor / Codex
- **Branch / Worktree:** dev
- **Status:** Implementada

## 1. Contexto e Motivação
A primeira solução tem alta estabilidade e baixa separação. Era necessário avaliar a influência dos contratos, ampliar k=2…8 e evitar conclusões fortes de p-valores experimentais não significativos.

## 2. Decisão Adotada
Criar validação suplementar reproduzível em `src/validar_entrega_semana5.py`, com três especificações, k=2…8, cinco bootstraps para k=3/4 e IC normal não agrupado das diferenças ITT, com Bonferroni para três testes. Manter a segmentação publicada como referência descritiva: remover contratos dá ARI 0,988; quatro atributos dão ARI 0,931 e silhueta 0,336 no novo espaço. A versão compacta é candidata, não foi promovida.

Mini deck em Markdown, no próprio repositório, com oito slides e fontes explícitas, seguindo o destino previsto no plano. Não há PowerPoint/PDF exportado nesta versão. Relatório e documento mestre registram a natureza retrospectiva das AUCs antigas e a ausência de avaliação prospectiva.

## 3. Consequências e Impacto no Case
Reprodução suplementar não substitui reexecução de todos os notebooks, nem resolve a comparação temporal por exposição. Bootstrap mantém tetos/imputação fixos. Mantemos esses limites visíveis. Publicação no Drive e submissão seguem pendentes. Saídas agregadas não contêm identificadores individuais.
