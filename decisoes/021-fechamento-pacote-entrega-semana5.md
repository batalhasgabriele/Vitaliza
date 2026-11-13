# ADR 021: Fechamento e pacote de entrega da Semana 5

- **Data:** 12/11/2026
- **Autor(a) / Responsável:** Igor (autorização) / Codex (implementação)
- **Branch / Worktree:** dev
- **Status:** Implementada; validação independente aprovada

## 1. Contexto e Motivação
A ADR 020 consolidou o método e as apresentações. Falta tornar a entrega transportável, conferir as ressalvas de fonte e garantir que a reprodução não dependa das bases históricas individuais ou de um checkout Git antigo.

## 2. Decisão Adotada
Revisar divergências por eventos; preservar ressalvas sem regra verificável. Montar pacote local por lista explícita de arquivos: apresentações, código, documentação vigente, testes e tabelas agregadas. Dados individuais e documentos das aulas não integram o pacote público. Gerar manifesto de integridade e matriz de requisitos. Validar em diretório independente a reprodução com as entradas autorizadas.

## 3. Consequências e Impacto no Case
O pacote facilita avaliação e continuidade por colegas/IA. Não muda automaticamente centroides, população ou campanha. Comparações históricas tornam-se opcionais; ausência de uma base antiga não deve impedir uma execução nova. Submissão individual na Adalove e publicação no Drive são atos separados do fechamento local.

## 4. Resultado da validação
Execução independente `20261112T232847Z`, sem `.git`, Prata/Ouro inicial ou base histórica individual: **28 testes aprovados**, três notebooks executados, 14 arquivos Bronze preservados, Prata idêntica, sete tabelas analíticas equivalentes, 14.753 ativos com mesmas atribuições e receita. O fallback dos canais financeiros foi corrigido e coberto por teste, sem mudar os valores observados.

O enunciado e os dados continuam divergindo em quatro perdas de abril. Nos cinco estados de renovação conflitantes, há renovação posterior ao último desligamento sem religamento explícito; manter ressalva. Ver [auditoria e racional](../notebooks/13_fechamento_entrega_semana5.md) e `saidas/semana5_consolidada/tabelas/qa_fechamento.json`.
