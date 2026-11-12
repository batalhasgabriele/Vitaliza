import subprocess
import sys
if __name__ == '__main__':
    raise SystemExit('Gerador histórico desativado pela ADR 020. Execute src/atualizar_documentacao_semana5.py.')
import nbformat as nbf

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

nb = nbf.v4.new_notebook()

# Célula 1: Título e Contexto
c1 = nbf.v4.new_markdown_cell("""# Vitaliza - Análise Exploratória de Dados (EDA) e Portfólio de Hipóteses MECE (Etapa 2)
**Módulo 2 MBA Inteli | Liderança de Ciência de Dados**  
**Data de Corte Oficial:** 30/09/2026 às 23:59:59 (Horário de Brasília)  
**Última Execução (Base Limpa e Sem Vazamento Pós-Saída):** 01/11/2026  
**Objetivo de Negócio:** Investigar a escalada do churn mensal (5,6% -> 6,6% geral; pico de 8,1% em abr/2026) e estruturar hipóteses causais testáveis para o pipeline de retenção preditiva.

---

### Diretrizes de Governança e Regras de Qualidade Aplicadas (Etapa 1 -> Etapa 2):
1. **Dados Brutos Imutáveis:** A pasta `dados/brutos/` é estritamente somente leitura.
2. **População Oficial Sem Contas Internas:** Expurgadas as `60` contas `@vitaliza.com.br` (`cortesia`), consolidando `32.583` assinaturas pagas históricas (`14.753` pagantes ativos e `17.830` encerradas no corte de `30/09/2026`).
3. **As 5 Dimensões da Qualidade Aplicadas (`ADR 009`):**
   - *Completude:* Flags de preenchimento do onboarding preservadas (`flag_onb_*_preenchido`) e idades inválidas (`<= 1900` ou `>= 2026`, `606` casos) convertidas em `NaN`.
   - *Validade:* Expurgados `3.649` treinos com duração zero e anuladas `951` distâncias GPS `> 200 km` em `atividades_limpas.parquet`.
   - *Consistência:* Mapeados os `11` rótulos de treino para `7` modalidades canônicas (`376.930` registros em inglês integrados).
   - *Unicidade e Fuso:* Convertido o fuso `UTC` do Garmin para `UTC-3` e removidos os `9.383` pares de treinos duplicados (`5.199` Garmin + `4.184` Apple Health), além das cobranças aprovadas em duplicidade no mesmo ciclo/dia.
   - *Temporalidade e Blindagem Contra Vazamento Pós-Cancelamento:* Todas as métricas mensais (`media_atividades_mes`, `media_minutos_mes`, `media_dias_ativos_mes`, `media_sessoes_mes`) são calculadas **estritamente dentro da janela de vigência de cada assinatura (`inicio` até a data de cancelamento — ou até `30/09/2026` para quem segue ativo)** dividida pelos meses de vigência, e a desaceleração recente é medida nas janelas relativas **`D-30` (`atividades_ultimos_30d`)** e **`D-60` (`atividades_31_a_60d`)** anteriores ao cancelamento (eliminando o vazamento pós-cancelamento de olhar para meses fixos do calendário como agosto/setembro de 2026 para quem já havia cancelado antes!).
""")

# Célula 2: Imports e Configuração
c2 = nbf.v4.new_code_cell("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_auc_score

# Configuração visual
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['figure.dpi'] = 120
pd.set_option('display.max_columns', 100)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

print("Ambiente configurado com sucesso!")
""")

# Célula 3: Carga da Feature Store Processada
c3 = nbf.v4.new_markdown_cell("""## 1. Carga da Feature Store Consolidada e Higienizada (Corte 30/09/2026)
Carregamos a base analítica em `dados/processados/ouro/features_eda_corte_set2026.parquet`, gerada após a execução do pipeline das 5 Dimensões da Qualidade e blindagem pós-desfecho (`src/limpeza_qualidade_dados.py` e `src/processar_eda.py`).""")

c4 = nbf.v4.new_code_cell("""df = pd.read_parquet('../dados/processados/ouro/features_eda_corte_set2026.parquet')
print(f"Total de assinaturas pagas analisadas: {len(df):,}")
print(f"Status atual da base: {df['status_atual'].value_counts().to_dict()}")
print(f"Pagantes ativos em 30/09/2026: {(df['churn'] == 0).sum():,} (sendo {((df['churn'] == 0) & (df['renovacao_automatica'] == 'sim')).sum():,} com renovação automática ligada)")
print(f"Taxa de churn acumulada histórica no corte: {df['churn'].mean():.2%}")
df.head(3)
""")

# Célula 5: Perfilamento Estatístico Robusto
c5 = nbf.v4.new_markdown_cell("""## 2. Perfilamento Estatístico Robusto: Média, DP, Mediana e IQR (Durante a Vigência)
Comparamos Ativos vs. Cancelados reportando **Média e Desvio Padrão ($s$)** junto com **Mediana e Intervalo Interquartil (IQR)**, calculados estritamente durante os meses de vigência de cada assinatura e nas janelas relativas de 30 e 60 dias antes do cancelamento (`D-30` e `D-60`), evitando qualquer viés de inatividade pós-cancelamento.""")

c6 = nbf.v4.new_code_cell("""metricas_robustas = [
    'atividades_ultimos_30d', 'atividades_31_a_60d',
    'media_atividades_mes', 'media_atividades_mes_ativo',
    'media_minutos_mes', 'media_minutos_mes_ativo',
    'media_dias_ativos_mes', 'media_sessoes_mes',
    'prop_meses_ativos_vigencia', 'n_modalidades_distintas',
    'receita_bruta_mensal', 'num_seguidores', 'media_posts_mes', 'media_curtidas_mes',
    'media_treinos_dupla_mes', 'duracao_mediana', 'distancia_mediana', 'idade'
]

perfil_rows = []
for m in metricas_robustas:
    s_atv = df[df['churn'] == 0][m].dropna()
    s_cnc = df[df['churn'] == 1][m].dropna()
    med_atv = s_atv.median()
    med_cnc = s_cnc.median()
    var_mediana_pct = ((med_cnc - med_atv) / med_atv * 100.0) if med_atv != 0 else np.nan
    perfil_rows.append({
        'Métrica': m,
        'Ativo_Média': s_atv.mean(),
        'Ativo_DP': s_atv.std(),
        'Ativo_Mediana': med_atv,
        'Ativo_IQR': s_atv.quantile(0.75) - s_atv.quantile(0.25),
        'Cancelado_Média': s_cnc.mean(),
        'Cancelado_DP': s_cnc.std(),
        'Cancelado_Mediana': med_cnc,
        'Cancelado_IQR': s_cnc.quantile(0.75) - s_cnc.quantile(0.25),
        'Variação_Mediana_%': var_mediana_pct
    })

df_perfil = pd.DataFrame(perfil_rows)
display(df_perfil)
""")

# Célula 7: Visualização Boxplots
c7 = nbf.v4.new_code_cell("""fig, axes = plt.subplots(2, 2, figsize=(14, 10))
df['status_label'] = df['churn'].map({0: 'Ativo (Base Set/26)', 1: 'Cancelado'})
palette = {'Ativo (Base Set/26)': '#2ECC71', 'Cancelado': '#E74C3C'}

sns.boxplot(data=df, x='status_label', y='media_atividades_mes', ax=axes[0, 0], palette=palette, hue='status_label', legend=False, showfliers=False)
axes[0, 0].set_title('Média de Atividades/Mês na Vigência (Sem Outliers)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Atividades / Mês')

sns.boxplot(data=df, x='status_label', y='atividades_ultimos_30d', ax=axes[0, 1], palette=palette, hue='status_label', legend=False, showfliers=False)
axes[0, 1].set_title('Treinos nos Últimos 30d Antes do Cancelamento (D-30)', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Treinos em D-30')

sns.boxplot(data=df, x='status_label', y='media_sessoes_mes', ax=axes[1, 0], palette=palette, hue='status_label', legend=False, showfliers=False)
axes[1, 0].set_title('Média de Sessões no App/Mês na Vigência (Sem Outliers)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Sessões / Mês')

sns.boxplot(data=df, x='status_label', y='media_curtidas_mes', ax=axes[1, 1], palette=palette, hue='status_label', legend=False, showfliers=False)
axes[1, 1].set_title('Média de Curtidas Recebidas/Mês na Vigência (Sem Outliers)', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Curtidas / Mês')

plt.suptitle('Perfilamento Estatístico Robusto: Comparação Ativos vs. Cancelados (Durante a Vigência)', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
""")

# Célula 8: Sobrevivência e Cohorts de Lifetime
c8 = nbf.v4.new_markdown_cell("""## 3. Análise de Sobrevivência e Cohorts de Lifetime (O "Vale da Morte" M2/M3)
Analisamos a curva de sobrevivência e taxa de churn estratificada por:
1. **Faixas de Tempo de Casa (Lifetime):** 0 meses (<30d), 1 mês (30-59d), 2 meses (60-89d), 3 meses (90-119d), 4-5 meses e 6+ meses.
2. **Tipo de Contrato:** Mensal vs. Anual.
3. **Canal de Cobrança:** Lojas (App Store e Google Play) vs. Meios Próprios Web (Cartão e Pix).""")

c9 = nbf.v4.new_code_cell("""order_life = ['0 meses (<30d)', '1 mes (30-59d)', '2 meses (60-89d)', '3 meses (90-119d)', '4-5 meses', '6+ meses']

print("=== Churn por Faixa de Lifetime e Plano ===")
ct_life_plano = df.groupby(['plano_atual', 'faixa_lifetime'])['churn'].agg(
    Total='count',
    Cancelados='sum',
    Taxa_Churn=lambda s: s.mean() * 100
).reindex(order_life, level=1).reset_index()
display(ct_life_plano)

# Gráfico de barras da curva de churn
plt.figure(figsize=(12, 6))
sns.barplot(data=ct_life_plano, x='faixa_lifetime', y='Taxa_Churn', hue='plano_atual', order=order_life, palette={'anual': '#3498DB', 'mensal': '#E67E22'})
plt.title('Curva de Churn por Tempo de Casa (Lifetime) e Tipo de Contrato', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Tempo de Casa (Lifetime)', fontsize=12, fontweight='bold')
plt.ylabel('Taxa de Churn (%)', fontsize=12, fontweight='bold')
plt.ylim(0, 100)
for p in plt.gca().patches:
    h = p.get_height()
    if h > 0:
        plt.gca().annotate(f'{h:.1f}%', (p.get_x() + p.get_width() / 2., h + 1.5),
                           ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.legend(title='Plano Contratado')
plt.tight_layout()
plt.show()
""")

# Célula 10: Diagnóstico do Ponto Cego
c10 = nbf.v4.new_markdown_cell("""## 4. Diagnóstico do "Ponto Cego" de Cancelamento
Mapeamos a proporção de cancelamentos que ocorreram sem registro na pesquisa de saída do app Vitaliza:
- **Cancelamentos via Stores (Apple App Store e Google Play):** Efetuados externamente nos ajustes do sistema operacional do smartphone sem nunca abrir tela de pesquisa no app Vitaliza (`100%` de ponto cego).
- **Cancelamentos Involuntários:** Falhas definitivas de cobrança (`1.321` casos / `7,41%`) e chargebacks (`292` casos / `1,64%`).
- **Pesquisa de Saída (`pesquisa_saida.csv`):** Iniciada apenas em `01/06/2026` e restrita aos canais Web (`Cartão` e `Pix`), cobrindo apenas `353` dos `17.830` encerramentos históricos (`1,98%`).""")

c11 = nbf.v4.new_code_cell("""cancelados_df = df[df['churn'] == 1]
tot_canc = len(cancelados_df)

com_pesquisa = cancelados_df['motivo_pesquisa_saida'].notna().sum()
sem_pesquisa = tot_canc - com_pesquisa

print(f"Total de Cancelamentos Históricos: {tot_canc:,}")
print(f"Cancelamentos COM Pesquisa de Saída: {com_pesquisa} ({com_pesquisa/tot_canc:.2%})")
print(f"Cancelamentos no PONTO CEGO (Sem Pesquisa): {sem_pesquisa:,} ({sem_pesquisa/tot_canc:.2%})")

ponto_cego_canal = cancelados_df.groupby('canal_cobranca').agg(
    Total_Cancelados=('user_id', 'count'),
    Com_Pesquisa=('motivo_pesquisa_saida', lambda s: s.notna().sum()),
    Prop_Pesquisa_Pct=('motivo_pesquisa_saida', lambda s: s.notna().mean() * 100),
    Falhas_Pagamento=('motivo_fim', lambda s: (s == 'falha_pagamento').sum()),
    Chargebacks=('motivo_fim', lambda s: (s == 'chargeback').sum())
).reset_index()
display(ponto_cego_canal)
""")

# Célula 12: Poder Discriminatório Univariado (AUC-ROC)
c12 = nbf.v4.new_markdown_cell("""## 5. Poder Discriminatório Univariado (AUC-ROC) Sem Vazamento Pós-Cancelamento
Avaliamos a capacidade discriminatória univariada de cada preditor em relação ao cancelamento histórico.
- **Blindagem Metodológica:** Excluímos variáveis fixas no calendário de fim de período (`atividades_set26`, `atividades_ago26`) — que geravam falso sinal porque quem cancelou meses antes naturalmente tem zero treinos em setembro — e excluímos o próprio evento de saída (`desligou_renovacao`). Em seu lugar, avaliamos **janelas móveis relativas ao cancelamento (`D-30` e `D-60` antes do cancelamento, ou antes do corte `30/09/2026` para ativos)** e **médias restritas aos meses de vigência ativa da assinatura**.""")

c13 = nbf.v4.new_code_cell("""variaveis_preditoras = [
    ('atividades_ultimos_30d', 'Treinos nos Últimos 30d Antes do Cancelamento (D-30)', 'Uso'),
    ('razao_uso_ultimo_mes', 'Razão de Uso Recente (D-30 vs Média Vigência)', 'Uso'),
    ('atividades_31_a_60d', 'Treinos entre 31d e 60d Antes do Cancelamento (D-60)', 'Uso'),
    ('n_modalidades_distintas', 'Diversidade de Modalidades (7 Canônicas)', 'Uso'),
    ('prop_meses_ativos_vigencia', 'Proporção de Meses Ativos na Vigência', 'Uso'),
    ('media_dias_ativos_mes', 'Média de Dias Ativos/Mês (Na Vigência)', 'Uso'),
    ('media_atividades_mes', 'Média de Atividades/Mês (Na Vigência)', 'Uso'),
    ('media_minutos_mes', 'Média de Minutos de Treino/Mês (Na Vigência)', 'Uso'),
    ('media_sessoes_mes', 'Média de Sessões no App/Mês (Na Vigência)', 'Uso'),
    ('media_ar_livre_mes', 'Média de Treinos Ar Livre/Mês (Na Vigência)', 'Uso'),
    ('media_video_mes', 'Média de Treinos Vídeo Guiado/Mês (Na Vigência)', 'Uso'),
    ('prop_gps_ok', 'Proporção Treinos com GPS Válido', 'Uso'),
    ('eh_plano_anual', 'Tipo de Plano (Anual vs. Mensal)', 'Contrato'),
    ('receita_bruta_mensal', 'Valor Médio Pago/Mês (R$ na Vigência)', 'Contrato'),
    ('teve_carencia', 'Entrou em Período de Carência', 'Contrato'),
    ('pagamentos_recusados', 'Cobranças Recusadas', 'Contrato'),
    ('eh_canal_loja', 'Canal de Cobrança (Lojas vs. Web)', 'Contrato'),
    ('total_tickets', 'Total de Tickets de Suporte', 'Contrato'),
    ('media_treinos_dupla_mes', 'Média de Treinos em Dupla/Mês (Na Vigência)', 'Social'),
    ('prop_treinos_dupla', 'Proporção Treinos em Dupla', 'Social'),
    ('num_seguidores', 'Número de Seguidores na Comunidade', 'Social'),
    ('num_seguindo', 'Número de Usuários que Segue', 'Social'),
    ('media_posts_mes', 'Média de Posts no Feed/Mês (Na Vigência)', 'Social'),
    ('media_curtidas_mes', 'Média de Curtidas no Feed/Mês (Na Vigência)', 'Social'),
    ('idade', 'Idade do Usuário (Higienizada)', 'Entrada'),
    ('tem_relogio', 'Possui Smartwatch Conectado', 'Entrada'),
    ('dias_semana_pretendidos', 'Dias/Semana Pretendidos (Onboarding)', 'Entrada'),
]

auc_results = []
y = df['churn'].values

for col, nome, galho in variaveis_preditoras:
    s = df[col].fillna(df[col].median()).values
    auc = roc_auc_score(y, s)
    direcao = 'Aumenta Churn' if auc >= 0.5 else 'Reduz Churn (Protetor)'
    auc_efetivo = max(auc, 1.0 - auc)
    auc_results.append({
        'Galho MECE': galho,
        'Variável': col,
        'Nome Legível': nome,
        'AUC Discriminatório': auc_efetivo,
        'Efeito': direcao
    })

df_auc = pd.DataFrame(auc_results).sort_values('AUC Discriminatório', ascending=False)
display(df_auc)
""")

# Célula 14: Síntese e Hipóteses MECE
c14 = nbf.v4.new_markdown_cell("""## 6. Portfólio de Hipóteses MECE para Mitigação do Churn

As análises estatísticas subsidiam o portfólio de hipóteses causais testáveis estruturadas nos galhos MECE:

### Galho 1: Características de Entrada e Expectativa (Quem entrou?)
- **H1.1: Gap de Expectativa no Onboarding:** Usuários que declaram meta de alta frequência (>= 4 dias/semana) e praticam < 2 dias no M1 sofrem frustração psicológica e churnam precocemente.
- **H1.2: Oportunismo de Cupom e Sensibilidade ao Preço Cheio:** Assinantes atraídos por cupom de influenciador no 1º ano (R$ 239,90) têm maior propensão a cancelar na renovação para o preço cheio (R$ 299,90).

### Galho 2: Comportamento de Uso e Produto (O que faz no app?)
- **H2.1: Queda Antecipada de Atividade nas Janelas Relativas (D-30 e D-60 antes do Desfecho):** O churn é precedido por uma desaceleração real de treinos nos 30 a 60 dias que antecedem o término da assinatura, bem como por menor regularidade mensal durante a vigência.
- **H2.2: Diversidade Esportiva vs. Monotonia de Modalidade:** Praticantes que exploram múltiplas modalidades canônicas (`n_modalidades_distintas`) apresentam retenção muito superior aos restritos a uma única modalidade ou apenas vídeo guiado.

### Galho 3: Ciclo de Vida, Financeiro e Suporte (Há quanto tempo e qual vínculo?)
- **H3.1: Vale da Morte do Plano Mensal no M2/M3:** O plano mensal apresenta churn de `76,55%` no 2º mês e `79,29%` no 3º mês devido à ausência de barreira contratual de saída.
- **H3.2: Cancelamento Involuntário por Fricção de Cobrança:** `7,41%` dos cancelamentos (`1.321` casos) são falhas de cobrança não recuperadas e `1,64%` (`292` casos) são chargebacks.

### Galho 4: Comunidade e Ancoragem Social (Está conectado a outros?)
- **H4.1: Blindagem por Laços Sociais no Feed:** Usuários ativos no feed social (`total_posts` e `total_curtidas`) apresentam forte efeito protetor contra o churn.
- **H4.2: Treino em Parceria (Efeito Rede Operacional):** A prática de treinos em dupla (`treino_com != ""`) reduz o risco de cancelamento ao criar compromisso interpessoal.
""")

nb.cells = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14]

NB_PATH = "notebooks/02_eda_e_hipoteses.ipynb"
with open(NB_PATH, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Notebook notebooks/02_eda_e_hipoteses.ipynb atualizado! Executando células via jupyter nbconvert...")
subprocess.run(
    [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        NB_PATH,
    ],
    check=True,
)
print("Execução de notebooks/02_eda_e_hipoteses.ipynb concluída com sucesso!")
