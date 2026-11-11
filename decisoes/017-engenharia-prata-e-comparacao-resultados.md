# ADR 017: EDA sobre Prata e publicação condicionada à comparação

- **Data:** 08/11/2026
- **Autor(a) / Responsável:** Igor / Codex
- **Branch / Worktree:** dev
- **Status:** Implementada; evidência de execução em `saidas/tabelas/qa_engenharia_dados.json`

## 1. Contexto e Motivação
A EDA combinava fontes Bronze e Prata. A mudança precisava preservar resultados ou identificar precisamente suas diferenças, conforme solicitação do usuário. O guia de engenharia recomenda contratos, granularidade, rastreabilidade, idempotência e validação antes de publicar.

## 2. Decisão Adotada
Consumir Prata na EDA; validar chaves de usuário/assinatura e conservação da população; escrever a Ouro por arquivo temporário e substituição. Preservar baseline privada e executar duas vezes em staging. Comparar todas as colunas por usuário com tolerância numérica 1e-10. O runner bloqueia promoção quando encontra diferenças ou falhas críticas, conserva logs e publica somente agregados de auditoria.

Documentar contratos, linhagem, temporalidade, reconciliação e execução em seis Markdown em notebooks. O contrato observado não é apresentado como contrato completo de todos os campos. Preservar política financeira, população e semântica temporal até que alterações sejam justificadas por evidência.

## 3. Consequências e Impacto no Case
A auditoria temporal revelou exposição desigual e atividades anteriores à assinatura, que podem ser freemium. Não excluir sem distinguir a pergunta de negócio. A regra de deduplicação monetária continua uma aproximação por usuário/valor/dia. Controle atômico cobre a EDA individual; publicação transacional de toda a cadeia é uma evolução ainda não implementada. A migração de fonte não equivale à reconstrução histórica para prever churn.
