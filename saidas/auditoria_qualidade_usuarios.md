# Relatório de Qualidade de Dados: Base de Usuários (`usuarios.csv`)
**Projeto:** Vitaliza - Arquitetura de Retenção Preditiva  
**Skill Utilizada:** `data-quality-audit`  
**Referência Metodológica:** `references/quality_dimensions.md` e scripts oficiais da skill  
**Volume Auditado:** 64.948 registros x 12 colunas  
**Data de Execução:** 29/10/2026  

---

## 1. Scorecard Executivo de Qualidade

| Dimensão de Qualidade | Peso | Score (0 a 10) | Status | Principais Evidências |
| :--- | :---: | :---: | :---: | :--- |
| **1. Unicidade (Uniqueness)** | 15% | **10.0 / 10** | ✅ Conforme | `user_id` e `email` 100% únicos (0 duplicatas completas ou parciais). |
| **2. Validade (Validity)** | 20% | **7.5 / 10** | ⚠️ Alerta | Inconsistência de encoding em `sexo` (38,2% fora de M/F) e `sistema` (24,7% fora de minúsculas); 606 datas de nascimento espúrias (0,93%). |
| **3. Consistência (Consistency)** | 25% | **9.5 / 10** | ✅ Conforme | Integridade referencial impecável (0 órfãos em assinaturas, onboarding e treinos); 0 Apple Watches em Android; 194 inconsistências de nascimento vs cadastro. |
| **4. Temporalidade (Timeliness)** | 20% | **8.5 / 10** | ⚠️ Atenção | Histórico contínuo de 2020 a 2026, porém presença de 119 registros pós-corte oficial (indo até abril/2027), exigindo filtro estrito de corte. |
| **5. Completude (Completeness)** | 20% | **9.2 / 10** | ✅ Conforme | 9 de 12 colunas 100% preenchidas. Faltantes concentrados em `data_nascimento` (5,08%), `sexo` (4,84%) e `cep_prefixo` (2,92%). |
| **Índice Global de Qualidade** | **100%** | **8.86 / 10** | ✅ Aprovado com Ressalvas | Base íntegra para modelagem, desde que aplicadas as etapas de sanitização de strings e filtro temporal de corte. |

---

## 2. Detalhamento por Dimensão

### 2.1 Unicidade (Uniqueness)
- **Chave Primária (`user_id`):** 64.948 valores únicos (0 duplicatas, 0.00%).
- **Chave Natural (`email`):** 64.948 valores únicos (0 duplicatas, 0.00%).
- **Linhas Duplicadas (Full-row duplicates):** 0 linhas (0.00%).
- **Diagnóstico:** A entidade conta/usuário preserva unicidade absoluta de ponta a ponta.

### 2.2 Validade (Validity)
- **Estrutura Sintática / Regex:**
  - `user_id`: 100% em conformidade com o padrão `^u_[a-f0-9]{8}$`.
  - `email`: 100% em conformidade com regex de e-mails válidos RFC.
  - `versao_app`: 100% em conformidade com SemVer (`^\d+\.\d+\.\d+$`), variando de `4.9.8` a `5.4.1`.
  - `cep_prefixo`: 100% dos preenchidos encontram-se no range válido de 3 dígitos (010 a 999).
  - `uf`: 100% pertencem às 27 UFs oficiais do Brasil.
- **Anomalias de Domínio e Valores:**
  - **`sexo` (38,23% não padronizado):** Presença de termos livres (`Fem`: 6.657, `feminino`: 6.520, `Masc`: 5.838, `masculino`: 5.815), além do formato binário padrão `F` (19.330) e `M` (17.646).
  - **`sistema` (24,74% não padronizado):** Mistura de maiúsculas e minúsculas (`iOS`: 7.463, `IOS`: 1.480, `Android`: 7.124).
  - **`data_nascimento` (0,93% inválido):**
    - 412 usuários com data padrão de sistema legado `1900-01-01` (idade aparente de 126,7 anos).
    - 194 usuários com data futura espúria `2031-05-12` (idade aparente de -4,6 anos).

### 2.3 Consistência (Consistency)
- **Integridade Referencial Inter-tabelas (FK Check):**
  - `assinaturas.csv`: **0 órfãos** (100% das 32.643 assinaturas referenciam um usuário existente).
  - `onboarding.csv`: **0 órfãos** (100% dos 63.929 questionários referenciam um usuário existente).
  - `atividades.parquet`: **0 órfãos** (100% dos 1.254.475 treinos referenciam um usuário existente).
- **Consistência Lógica Cruzada (Cross-field Rules):**
  - `sistema` vs `relogio_conectado`: **100% consistente** (nenhum usuário com Android possui Apple Watch conectado).
  - `cep_prefixo` vs `uf`: **100% consistente** (todos os 63.054 prefixos de CEP pertencem ao intervalo geográfico oficial da respectiva UF).
  - `data_cadastro` vs `data_nascimento`: 194 inconsistências (0,30%) em que a data de cadastro é anterior ao nascimento (geradas pelos nascimentos em 2031).

### 2.4 Temporalidade (Timeliness / Freshness)
- **Início do Histórico:** `01/09/2020 12:00:00`.
- **Evolução de Cadastros:**
  - 2020: 439
  - 2021: 1.383
  - 2022: 1.336
  - 2023: 1.441
  - 2024: 11.939 (início da expansão comercial)
  - 2025: 26.167 (maior volume de expansão)
  - 2026 (até 30/09): 22.083
- **Vazamento Temporal / Registros Futuros:**
  - Existem **119 registros de cadastro com timestamp posterior a 30/09/2026 23:59:59** (estendendo-se até `04/04/2027 10:44:09`).
  - Nenhum desses 119 usuários possui assinatura ou treino registrado no data room, mas devem ser obrigatoriamente filtrados para blindagem contra vazamento temporal (*data leakage*).
