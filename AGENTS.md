# Diretrizes para Agentes de IA - Projeto Vitaliza (Módulo 2 MBA Inteli)

## 1. Contexto do Projeto
- **Empresa:** Vitaliza (app freemium brasileiro de bem-estar, treinos ao ar livre com GPS, vídeos guiados e rede social).
- **Desafio:** Arquitetura da Retenção Preditiva (VP de Crescimento e Retenção).
- **Data de corte oficial:** 30/09/2026.

## 2. Regras de Estrutura e Governança de Arquivos
> **Regra Fundamental:** O desenho da pasta já é uma regra: **o dado bruto nunca é editado** (`dados/brutos/` é estritamente somente leitura).

- `docs/`: Enunciado oficial do case e dicionário de dados.
- `dados/brutos/`: Arquivos originais exportados dos sistemas (12 tabelas/logs e pasta `heatmaps/`). Nunca devem ser modificados ou sobrescritos.
- `dados/processados/`: Tabelas intermediárias tratadas e feature stores geradas pelo grupo.
- `notebooks/`: Notebooks de análise exploratória, modelagem e validação.
- `src/`: Scripts Python reutilizáveis (funções de limpeza, engenharia de atributos, modelagem).
- `saidas/`: Relatórios gerados, predições ordenadas para CRM, gráficos e artefatos de entrega.
- `decisoes.md`: Log de decisões de negócios e de modelagem adotadas pela equipe.

## 3. Premissas de Negócio e Métricas
- **Preço Mensal:** R$ 39,90 (desde 01/03/2026; era R$ 34,90 antes).
- **Preço Anual:** R$ 299,90 (ou R$ 239,90 no primeiro ano com cupom de influenciador).
- **Taxas de Intermediação de Canais:**
  - App Store / Google Play: 15,0% (Vitaliza retém 85,0%).
  - Web - Cartão: 3,5% (Vitaliza retém 96,5%).
  - Web - Pix Automático: 0,99% (Vitaliza retém 99,01%).
- **Tratamento de Fusos Horários:**
  - Lojas (Apple e Google) gravam em UTC (terminado em `Z`).
  - Meios próprios web (Cartão e Pix) gravam em Horário de Brasília (UTC-3).
  - Toda consolidação contábil ou de cohort deve harmonizar para o Horário de Brasília.
- **Tratamento de Cobranças Duplicadas:**
  - Retentativas de cobrança aprovadas em dobro no mesmo ciclo/dia devem ser expurgadas da receita líquida.

## 4. Política de Branches e Fluxo Git
- **Branch `main`:** É a branch de entrega oficial, estável e de produção. **Nunca comitar ou desenvolver diretamente na `main`**.
- **Branch `dev`:** É a branch de trabalho ativo. Todas as alterações locais, códigos, notebooks e análises devem ser desenvolvidos e comitados na `dev`.
- **Merge para `main`:** O avanço ou merge de alterações da `dev` para a `main` só ocorre mediante solicitação e aprovação explícita do usuário.

## 5. Comandos

### Ativação do Ambiente Virtual (`.venv`)
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(Caso haja restrição de execução de scripts no PowerShell: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*
- **Windows (Prompt de Comando / CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **macOS / Linux (Bash/Zsh):**
  ```bash
  source .venv/bin/activate
  ```

### Inicialização do JupyterLab
- **Com o ambiente ativado:**
  ```bash
  jupyter lab
  ```
- **Diretamente via interpretador do ambiente (sem ativar manualmente):**
  - **Windows (PowerShell):**
    ```powershell
    .\.venv\Scripts\jupyter-lab.exe
    ```
  - **macOS / Linux:**
    ```bash
    ./.venv/bin/jupyter-lab
    ```

## 6. Como trabalhar
- antes de uma tarefa com mais passos, apresente um plano e espere aprovação
- após executar uma análise, salvar o racional na pasta notebooks/ para utilizar em cenários de replicação/recálculo
- estrutura recomendada para o prompt de análises: pergunta, arquivos, regras, formato de saída e definition of done. se alguma dessas informações não tiver clara, pergunte.
- aspectos de negócios, correções feitas e regras estabelecidas devem ser registradas no arquivo decisoes.md

