# ADR 007: Diretrizes Técnicas da Auditoria de Qualidade de Dados (12 Tabelas)

- **Data:** 29/10/2026
- **Autor(a) / Responsável:** Gabriele Batalha / Agente 2 (Worktree Cluster)
- **Branch / Worktree:** `cluster-v1`
- **Status:** Aprovada / Implementada

---

## 1. Contexto e Motivação
Execução da auditoria formal multidimensional nas 12 tabelas brutas via skill `data-quality-audit` (mais de 2,49 milhões de registros auditados) para garantir consistência estrutural, integridade referencial e blindagem temporal antes dos modelos de clusterização e classificação.

## 2. Decisão Adotada
Padronizar as seguintes rotinas de engenharia de dados nos scripts de pré-processamento:
1. **Blindagem contra Vazamento Temporal (Data Leakage):**
   - Todas as tabelas transacionais e comportamentais (`usuarios`, `atividades`, `feed_posts`, `amizades`) devem aplicar o filtro estrito `timestamp <= '2026-09-30 23:59:59'`.
   - Expurgar os 119 cadastros futuros (estendendo-se anômala e artificialmente até 2027), 273 amizades, 122 posts e 34 treinos ocorridos após o corte oficial.
2. **Harmonização de Fuso Horário Obrigatória:**
   - Em `pagamentos.csv` e `eventos_assinatura.csv`, eventos registrados pelas lojas em UTC com sufixo `Z` devem ser convertidos para Horário de Brasília (`America/Sao_Paulo`).
   - Alinha as transações de 01/10 até 02h59 UTC de volta ao dia 30/09/2026, eliminando falsos vazamentos e conferindo 100% de conformidade com o corte oficial.
3. **Sanitização de Valores Monetários:**
   - Tratar os 19.750 valores textuais em `pagamentos.valor` com `.str.replace('R$', '').str.replace(' ', '').str.replace(',', '.').astype(float)`.
   - Preservar valores negativos como estornos e chargebacks válidos (368 casos).
4. **Higienização de Variáveis Demográficas e Casing:**
   - Converter em `NaN` datas de nascimento anômalas (`<= 1900` e `>= 2026`, totalizando 606 casos em `usuarios.csv`).
   - Normalizar `sistema` para minúsculas (`.str.lower()`) e mapear `sexo` para categorias canônicas: `{'fem': 'F', 'feminino': 'F', 'masc': 'M', 'masculino': 'M'}`.
5. **Integridade Referencial Reconhecida:**
   - Fica registrado que o grafo de integridade relacional entre as tabelas possui 0 órfãos (100% de conformidade referencial entre entidades filhas e a tabela-mãe `usuarios.csv`).
6. **Expurgo de Atividades sem Duração:**
   - Filtrar `duracao_min > 0` ao computar métricas de uso e hábitos esportivos (expurgando 3.649 registros anômalos de `atividades.parquet`).

## 3. Consequências e Impacto no Case
- Bases de dados processadas completamente auditadas, purgadas de anomalias sintéticas e prontas para alimentação de modelos de clustering e previsão de churn.
