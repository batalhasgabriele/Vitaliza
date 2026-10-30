# ADR 005: Diretrizes Metodológicas de Modelagem Preditiva e Formulação de Hipóteses

- **Data:** 25/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Equipe Vitaliza
- **Branch / Worktree:** `dev`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
A retenção preditiva orientada a negócios exige um alinhamento estrito com os materiais didáticos do Módulo 2 do MBA Inteli, evitando armadilhas clássicas como vazamento temporal (*data leakage*), inferência causal ingênua e infração de princípios éticos da LGPD.

## 2. Decisão Adotada
Consolidar as diretrizes metodológicas obrigatórias para o time de modelagem (referência detalhada em `docs/aprendizados_aulas.md`):
1. **Estrutura Obrigatória de Hipóteses em 3 Partes:**
   - *Afirmação Causal:* Relação de causa e efeito clara ("X faz Y acontecer").
   - *Métrica Objetiva:* Medida específica extraída dos dados ("Medido por...").
   - *Critério de Refutação Pré-estabelecido:* Corte que invalida a hipótese se não comprovado ("Cai se...").
   - Organização estrita nos 4 galhos da Árvore MECE (Entrada, Uso, Contrato e Social).
2. **A Tríade do Case:**
   - *Prever:* Risco individual de saída até 29/11/2026 (probabilidade contínua de 0.0 a 1.0).
   - *Decidir:* Prescrição de intervenção priorizando quem só fica se for contatado, poupando os "cães adormecidos".
   - *Valorar:* Avaliação do retorno financeiro líquido respeitando limites de capacidade operacional (1.500 contatos/mês).
3. **Blindagem contra Vazamento Temporal (*Data Leakage*):**
   - Nenhuma variável pode incorporar informações geradas após a data de corte oficial (`30/09/2026`).
   - Proibido usar métricas induzidas pelo próprio cancelamento (ex: frequência zero no mês de cancelamento).
4. **Governança Ética e Conformidade com a LGPD:**
   - Embora idade apresente poder discriminatório univariado, regras automatizadas de preço ou exclusão de benefícios baseadas em idade violam o Princípio da Não Discriminação (Art. 6º, IX da LGPD).
   - Variáveis irrelevantes ou de risco ético com AUC próximo de 0,50 (gênero e telefone) devem ser descartadas.

## 3. Consequências e Impacto no Case
- Garante que os modelos preditivos sejam defensáveis perante o conselho executivo e auditáveis segundo as normas regulatórias brasileiras.
