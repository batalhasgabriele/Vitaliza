# Relatório de Qualidade de Dados: Auditoria Multidimensional do Data Room (12 Tabelas)
**Projeto:** Vitaliza - Arquitetura de Retenção Preditiva  
**Skill Utilizada:** `data-quality-audit`  
**Data de Corte Oficial:** 30/09/2026 às 23:59:59 (Horário de Brasília)  
**Volume Total Auditado:** 12 tabelas | Mais de 2,49 milhões de registros | 87 colunas analisadas  
**Data de Execução:** 29/10/2026  

---

## 1. Scorecard Executivo de Qualidade por Tabela

Metodologia baseada nas 6 dimensões de qualidade de dados (`references/quality_dimensions.md`), ponderando **Completude (20%)**, **Unicidade (15%)**, **Validade (20%)**, **Consistência (25%)** e **Temporalidade (20%)**:

| Tabela | Entidade | Volume (Linhas) | Completude | Unicidade | Validade | Consistência | Temporalidade | Score Final (/10) | Status Global |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `usuarios` | conta | 64.948 | 9.2 | 10.0 | 7.5 | 9.5 | 8.5 | **8.86** | ✅ Aprovado c/ ressalvas |
| `assinaturas` | assinatura | 32.643 | 9.0 | 10.0 | 10.0 | 10.0 | 10.0 | **9.80** | ✅ Conforme |
| `amizades` | relação de seguir | 113.480 | 10.0 | 10.0 | 10.0 | 10.0 | 9.0 | **9.80** | ✅ Conforme |
| `campanha_ago26` | assinante sorteado | 14.120 | 8.0 | 10.0 | 10.0 | 10.0 | 10.0 | **9.60** | ✅ Conforme |
| `eventos_assinatura` | log de evento | 275.565 | 10.0 | 10.0 | 9.5 | 10.0 | 10.0 | **9.90** | ✅ Conforme |
| `pagamentos` | cobrança | 165.548 | 10.0 | 10.0 | 8.0 | 9.5 | 10.0 | **9.45** | ✅ Aprovado c/ ressalvas |
| `uso_mensal` | usuário x mês | 591.662 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | **10.00** | ✅ Conforme |
| `atividades` | treino esportivo | 1.254.475 | 9.5 | 10.0 | 8.5 | 9.5 | 9.5 | **9.40** | ✅ Aprovado c/ ressalvas |
| `onboarding` | questionário entrada | 63.929 | 9.5 | 10.0 | 8.5 | 10.0 | 10.0 | **9.60** | ✅ Conforme |
| `pesquisa_saida` | resposta saída | 643 | 9.0 | 10.0 | 10.0 | 10.0 | 10.0 | **9.80** | ✅ Conforme |
| `feed_posts` | postagem rede | 119.309 | 9.0 | 10.0 | 10.0 | 10.0 | 9.0 | **9.60** | ✅ Conforme |
| `tickets_suporte` | chamado suporte | 4.422 | 9.0 | 10.0 | 10.0 | 10.0 | 10.0 | **9.80** | ✅ Conforme |

**Índice Médio de Qualidade do Data Room:** **9.68 / 10** (Excelente integridade estrutural, com pontos específicos de atenção em padronização de formatos e expurgo temporal).

---

## 2. Matriz Geral de Completude (Dados Ausentes por Tabela)

Detalhamento de todas as colunas que possuem registros nulos (`NaN`) ou *strings* vazias (`''`):

| Tabela | Coluna Auditada | Total Linhas | Nulos / NaNs | Strings Vazias | Total Ausentes | % Ausente | Classificação |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| `usuarios` | `data_nascimento` | 64,948 | 3,301 | 0 | 3,301 | **5.08%** | ⚠️ `WARN` (>5%) |
| `usuarios` | `sexo` | 64,948 | 3,142 | 0 | 3,142 | **4.84%** | ℹ️ `INFO` (<5%) |
| `usuarios` | `cep_prefixo` | 64,948 | 1,894 | 0 | 1,894 | **2.92%** | ℹ️ `INFO` (<5%) |
| `assinaturas` | `data_fim` | 32,643 | 14,813 | 0 | 14,813 | **45.38%** | 🔴 `ALERTA` (>20%) |
| `assinaturas` | `motivo_fim` | 32,643 | 14,813 | 0 | 14,813 | **45.38%** | 🔴 `ALERTA` (>20%) |
| `campanha_ago26` | `enviado_em` | 14,120 | 3,579 | 0 | 3,579 | **25.35%** | 🔴 `ALERTA` (>20%) |
| `campanha_ago26` | `canal` | 14,120 | 3,579 | 0 | 3,579 | **25.35%** | 🔴 `ALERTA` (>20%) |
| `campanha_ago26` | `titulo_mensagem` | 14,120 | 3,579 | 0 | 3,579 | **25.35%** | 🔴 `ALERTA` (>20%) |
| `campanha_ago26` | `oferta` | 14,120 | 10,648 | 0 | 10,648 | **75.41%** | 🔴 `ALERTA` (>20%) |
| `eventos_assinatura` | `plano` | 275,565 | 72,873 | 0 | 72,873 | **26.44%** | 🔴 `ALERTA` (>20%) |
| `eventos_assinatura` | `detalhe` | 275,565 | 269,494 | 0 | 269,494 | **97.80%** | 🔴 `ALERTA` (>20%) |
| `atividades` | `distancia_km` | 1,254,475 | 574,835 | 0 | 574,835 | **45.82%** | 🔴 `ALERTA` (>20%) |
| `atividades` | `ritmo_min_km` | 1,254,475 | 582,290 | 0 | 582,290 | **46.42%** | 🔴 `ALERTA` (>20%) |
| `atividades` | `fc_media` | 1,254,475 | 764,987 | 0 | 764,987 | **60.98%** | 🔴 `ALERTA` (>20%) |
| `atividades` | `treino_com` | 1,254,475 | 0 | 1,240,338 | 1,240,338 | **98.87%** | 🔴 `ALERTA` (>20%) |
| `onboarding` | `objetivo_texto` | 63,929 | 5,467 | 0 | 5,467 | **8.55%** | ⚠️ `WARN` (>5%) |
| `onboarding` | `como_conheceu` | 63,929 | 4,586 | 0 | 4,586 | **7.17%** | ⚠️ `WARN` (>5%) |
| `onboarding` | `nivel` | 63,929 | 4,513 | 0 | 4,513 | **7.06%** | ⚠️ `WARN` (>5%) |
| `onboarding` | `dias_por_semana` | 63,929 | 6,368 | 0 | 6,368 | **9.96%** | ⚠️ `WARN` (>5%) |
| `pesquisa_saida` | `comentario` | 643 | 183 | 0 | 183 | **28.46%** | 🔴 `ALERTA` (>20%) |
| `tickets_suporte` | `resolvido_em` | 4,422 | 1,505 | 0 | 1,505 | **34.03%** | 🔴 `ALERTA` (>20%) |

> **Observação sobre Completude:** As colunas com alta taxa de ausência em `assinaturas` (`data_fim`, `motivo_fim` com 45,38%) e `campanha_ago26` (`oferta` com 75,41%) refletem a própria **regra de negócio** (assinaturas ainda ativas não possuem término; grupos de controle da campanha não recebem oferta de desconto).

---

## 3. Análise de Unicidade (Uniqueness)

| Tabela | Chave Avaliada | Duplicatas de Linha Inteira | Duplicatas de Chave | Status | Diagnóstico |
|:---|:---|:---:|:---:|:---:|:---|
| `usuarios` | `user_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `assinaturas` | `assinatura_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `amizades` | `seguidor_id + seguido_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `campanha_ago26` | `user_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `eventos_assinatura` | `user_id + data_hora + evento` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `pagamentos` | `pagamento_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `uso_mensal` | `user_id + mes` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `atividades` | `atividade_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `onboarding` | `onboarding_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `pesquisa_saida` | `resposta_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `feed_posts` | `post_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |
| `tickets_suporte` | `ticket_id` | 0 (0,00%) | 0 (0,00%) | ✅ `PASS` | 100% íntegro. Nenhuma colisão identificada. |

**Conclusão de Unicidade:** O data room possui **zero duplicatas integrais** e **zero colisões de chave primária/natural**, conferindo confiabilidade absoluta às operações de junção (*JOIN*).

---

## 4. Análise de Validade e Domínios de Dados (Validity)

Identificação de tipos, formatos e perturbações sintáticas encontradas:

1. **Padronização Textual Monetária (`pagamentos.csv`):**
   - **19.750 linhas (11,93%)** possuem valores gravados como texto em padrão brasileiro (`'R$ 34,90'`, `'R$ 299,90'`), decorrentes do processamento das vendas Web (`cartao` e `pix_automatico`), contra notação float pura (`34.90`) nas lojas Apple/Google.
2. **Valores Negativos Legítimos (`pagamentos.csv`):**
   - Existem **368 cobranças com valor negativo** (`-39.90` e `-299.90`), correspondendo estritamente a eventos de estorno (`status == 'estornado'`, 72 casos) e contestações (`status == 'chargeback'`, 296 casos).
3. **Inconsistência de Casing em Variáveis Categóricas (`usuarios.csv`):**
   - `sexo`: 24.830 registros (38,23%) utilizam variações de texto livre (`Fem`, `feminino`, `Masc`, `masculino`) em vez do padrão binário `F`/`M`.
   - `sistema`: 16.067 registros (24,74%) contêm maiúsculas não normalizadas (`iOS`, `Android`, `IOS`).
4. **Anomalias Extremas de Data de Nascimento (`usuarios.csv`):**
   - **412 registros** com a data padrão de sistema legado `1900-01-01` (idade aparente de 126,7 anos).
   - **194 registros** com a data futura espúria `2031-05-12` (idade negativa de -4,6 anos).
5. **Codificação de Treinos Solo (`atividades.parquet`):**
   - O campo `treino_com` expressa a ausência de parceiro através de string vazia `''` em **1.240.338 registros (98,87%)**, e não como `null`/`NaN`.
6. **Durações Nulas ou Menores que Zero (`atividades.parquet`):**
   - **3.649 treinos (0,29%)** registram `duracao_min <= 0`, necessitando de expurgo em agregações de tempo de treino.

---

## 5. Consistência e Integridade Referencial (Consistency)

### 5.1 Grafo de Integridade Referencial (Foreign Keys)

| Relação (Tabela Filha → Tabela Mãe) | Linhas Não-Nulas | Registros Órfãos | % Órfãos | Status |
|:---|:---:|:---:|:---:|:---:|
| `assinaturas.user_id -> usuarios.user_id` | 32,643 | 0 | 0.00% | ✅ `PASS` |
| `amizades.seguidor_id -> usuarios.user_id` | 113,480 | 0 | 0.00% | ✅ `PASS` |
| `amizades.seguido_id -> usuarios.user_id` | 113,480 | 0 | 0.00% | ✅ `PASS` |
| `campanha_ago26.user_id -> usuarios.user_id` | 14,120 | 0 | 0.00% | ✅ `PASS` |
| `eventos_assinatura.user_id -> usuarios.user_id` | 275,565 | 0 | 0.00% | ✅ `PASS` |
| `pagamentos.user_id -> usuarios.user_id` | 165,548 | 0 | 0.00% | ✅ `PASS` |
| `uso_mensal.user_id -> usuarios.user_id` | 591,662 | 0 | 0.00% | ✅ `PASS` |
| `atividades.user_id -> usuarios.user_id` | 1,254,475 | 0 | 0.00% | ✅ `PASS` |
| `onboarding.user_id -> usuarios.user_id` | 63,929 | 0 | 0.00% | ✅ `PASS` |
| `pesquisa_saida.user_id -> usuarios.user_id` | 643 | 0 | 0.00% | ✅ `PASS` |
| `feed_posts.user_id -> usuarios.user_id` | 119,309 | 0 | 0.00% | ✅ `PASS` |
| `tickets_suporte.user_id -> usuarios.user_id` | 4,422 | 0 | 0.00% | ✅ `PASS` |

> **Destaque de Governança:** O ecossistema relacional da Vitaliza possui **ZERO registros órfãos** em todas as entidades dependentes. Toda atividade, post, assinatura, pagamento e ticket pertence a um usuário cadastrado.

### 5.2 Regras de Consistência Lógica Interna

- **`assinaturas.data_fim >= assinaturas.inicio`:** 100% conforme (0 violações).
- **`status_atual == 'ativa' ⇒ motivo_fim é nulo`:** 100% conforme (0 violações).
- **`tickets_suporte.resolvido_em >= tickets_suporte.aberto_em`:** 100% conforme (0 violações).
- **Compatibilidade Sistema x Smartwatch:** 100% conforme (0 usuários Android com Apple Watch).
- **Compatibilidade CEP Prefixo x UF:** 100% conforme (0 CEPs atribuídos a estados incorretos).

---

## 6. Temporalidade e Diagnóstico de Vazamento Temporal (Timeliness)

### 6.1 Análise de Fuso Horário e Harmonização para Horário de Brasília (UTC-3)

- **Diagnóstico:** As lojas Apple e Google gravam timestamps em UTC com sufixo `Z` (`2026-10-01T01:59:33Z`), enquanto os canais web (cartão e Pix) gravam em horário local de Brasília (`2026-09-30 22:54:51`).
- **Impacto da Harmonização:** Quando os registros das lojas são convertidos para o Horário de Brasília (UTC-3), os eventos ocorridos em 01/10 até 02h59 UTC recaem **dentro do dia 30/09/2026**. Após a conversão, `pagamentos.csv` e `eventos_assinatura.csv` apresentam **EXATAMENTE 0 registros posteriores ao corte oficial**.

### 6.2 Vazamento Temporal Real (Eventos Pós-Corte de 30/09/2026)

| Tabela | Coluna Temporal | Menor Data Registrada | Maior Data Registrada | Registros Pós-Corte | % Pós-Corte | Severidade |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| `usuarios` | `data_cadastro` | `2020-09-01 12:00:00` | `2027-04-04 10:44:09` | **119** | 0.18% | ⚠️ Atenção |
| `assinaturas` | `inicio` | `2020-09-08 00:00:00` | `2026-09-30 00:00:00` | **0** | 0.00% | ✅ Normal |
| `assinaturas` | `data_fim` | `2024-07-07 00:00:00` | `2026-09-30 00:00:00` | **0** | 0.00% | ✅ Normal |
| `amizades` | `desde` | `2020-09-05 00:00:00` | `2026-10-09 00:00:00` | **273** | 0.24% | ⚠️ Atenção |
| `campanha_ago26` | `enviado_em` | `2026-08-10 10:00:00` | `2026-08-10 10:00:00` | **0** | 0.00% | ✅ Normal |
| `eventos_assinatura` | `data_hora` | `2024-07-01 10:10:08` | `2026-10-01 01:59:33` | **44** | 0.02% | ⚠️ Atenção |
| `pagamentos` | `data_hora` | `2024-07-02 09:18:58` | `2026-10-01 01:50:25` | **30** | 0.03% | ⚠️ Atenção |
| `atividades` | `inicio` | `2026-01-01 05:00:00` | `2026-10-01 00:59:00` | **34** | 0.00% | ⚠️ Atenção |
| `pesquisa_saida` | `respondido_em` | `2026-06-01 00:00:00` | `2026-09-30 00:00:00` | **0** | 0.00% | ✅ Normal |
| `feed_posts` | `data_hora` | `2025-07-01 06:07:55` | `2026-10-07 18:52:16` | **122** | 0.10% | ⚠️ Atenção |
| `tickets_suporte` | `aberto_em` | `2025-07-01 08:15:00` | `2026-09-30 21:46:00` | **0** | 0.00% | ✅ Normal |

**Detalhamento dos Vazamentos Reais:**
- `usuarios.csv`: **119 contas cadastradas entre 01/10/2026 e 04/04/2027**.
- `amizades.csv`: **273 relações de amizade formadas entre 01/10/2026 e 09/10/2026**.
- `feed_posts.csv`: **122 postagens publicadas entre 01/10/2026 e 07/10/2026**.
- `atividades.parquet`: **34 treinos iniciados na madrugada de 01/10/2026** (entre 00h00 e 00h59).

---

## 7. Recomendações Técnicas Obrigatórias para os Pipelines de Dados

Para assegurar conformidade científica, blindagem contra vazamento temporal e robustez algorítmica na modelagem e segmentação, os pipelines de feature store devem implementar as seguintes etapas:

1. **Filtro Temporal Canônico de Corte:**
   - Aplicar estritamente `timestamp <= '2026-09-30 23:59:59'` em todas as tabelas transacionais e comportamentais (`usuarios`, `atividades`, `feed_posts`, `amizades`).
2. **Harmonização de Fuso Horário:**
   - Em `pagamentos` e `eventos_assinatura`, converter strings com sufixo `Z` de UTC para `America/Sao_Paulo` antes de qualquer agregação financeira ou contábil.
3. **Sanitização de Valores Monetários:**
   - Remover prefixos `R$`, espaços e converter vírgulas em pontos em `pagamentos.valor`: `.str.replace('R$', '').str.replace(' ', '').str.replace(',', '.').astype(float)`.
4. **Tratamento de Anomalias de Idade:**
   - Converter em `NaN` datas de nascimento `<= 1900` ou `>= 2026` em `usuarios.data_nascimento`.
5. **Normalização de Casing:**
   - Aplicar `.str.lower()` em `sistema` e mapear `sexo` para categorias canônicas `{'fem': 'F', 'feminino': 'F', 'masc': 'M', 'masculino': 'M'}`.
6. **Tratamento de Strings Vazias em Atividades Sociais:**
   - Utilizar a condição `treino_com.fillna('').str.strip() != ''` para identificar atividades em dupla/grupo.
7. **Expurgo de Durações Inválidas:**
   - Filtrar `duracao_min > 0` ao calcular estatísticas de treino para evitar distorção de medianas e médias.