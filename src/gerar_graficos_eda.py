import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from matplotlib.patches import Patch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300

df = pd.read_parquet("dados/processados/ouro/features_eda_corte_set2026.parquet")

# Imprimir tabela completa de perfilamento (Média, DP, Mediana, IQR) sem vazamento pós-cancelamento e normalizada por vigência
metricas_tabela = [
    ("atividades_ultimos_30d", "Treinos nos Últimos 30d Antes do Cancelamento/Corte (D-30)"),
    ("atividades_31_a_60d", "Treinos entre 31d e 60d Antes do Cancelamento/Corte (D-60)"),
    ("media_atividades_mes", "Média de Atividades/Mês (Na Vigência)"),
    ("media_atividades_mes_ativo", "Média de Atividades/Mês (Meses Ativos >0)"),
    ("media_minutos_mes", "Minutos de Treino/Mês (Na Vigência)"),
    ("media_minutos_mes_ativo", "Minutos de Treino/Mês (Meses Ativos >0)"),
    ("media_dias_ativos_mes", "Dias Ativos/Mês (Na Vigência)"),
    ("media_sessoes_mes", "Sessões no App/Mês (Na Vigência)"),
    ("prop_meses_ativos_vigencia", "Proporção de Meses Ativos na Vigência"),
    ("n_modalidades_distintas", "Modalidades Canônicas Distintas (7 máx)"),
    ("receita_bruta_mensal", "Valor Médio Pago/Mês na Vigência (R$)"),
    ("media_posts_mes", "Média de Posts no Feed/Mês (Na Vigência)"),
    ("media_curtidas_mes", "Média de Curtidas Recebidas/Mês (Na Vigência)"),
    ("media_treinos_dupla_mes", "Média de Treinos em Dupla/Mês (Na Vigência)"),
    ("num_seguidores", "Número de Seguidores na Comunidade"),
    ("duracao_mediana", "Duração do Treino (min - Base Limpa)"),
    ("distancia_mediana", "Distância do Treino (km - Base Limpa)"),
    ("idade", "Idade (Higienizada)"),
]

print("=== TABELA 2.1 ATUALIZADA (SEM VAZAMENTO PÓS-CANCELAMENTO) ===")
for col, label in metricas_tabela:
    s_atv = df[df["churn"] == 0][col].dropna()
    s_cnc = df[df["churn"] == 1][col].dropna()
    m_atv, sd_atv, med_atv, iqr_atv = (
        s_atv.mean(),
        s_atv.std(),
        s_atv.median(),
        s_atv.quantile(0.75) - s_atv.quantile(0.25),
    )
    m_cnc, sd_cnc, med_cnc, iqr_cnc = (
        s_cnc.mean(),
        s_cnc.std(),
        s_cnc.median(),
        s_cnc.quantile(0.75) - s_cnc.quantile(0.25),
    )
    var_pct = ((med_cnc - med_atv) / med_atv * 100) if med_atv != 0 else 0.0
    print(
        f"| **{label}** | {m_atv:.2f} (±{sd_atv:.2f}) | **{med_atv:.2f} ({iqr_atv:.2f})** | {m_cnc:.2f} (±{sd_cnc:.2f}) | **{med_cnc:.2f} ({iqr_cnc:.2f})** | **{var_pct:+.1f}%** |"
    )

# 1. Boxplots de Assimetria de Uso (Na Vigência)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
df["status_label"] = df["churn"].map({0: "Ativo (Base Set/26)", 1: "Cancelado"})
palette = {"Ativo (Base Set/26)": "#2ECC71", "Cancelado": "#E74C3C"}

sns.boxplot(
    data=df,
    x="status_label",
    y="media_atividades_mes",
    ax=axes[0, 0],
    palette=palette,
    hue="status_label",
    legend=False,
    showfliers=False,
)
axes[0, 0].set_title(
    "Média de Atividades/Mês na Vigência (Sem Outliers)", fontsize=13, fontweight="bold"
)
axes[0, 0].set_xlabel("")
axes[0, 0].set_ylabel("Atividades / Mês")

sns.boxplot(
    data=df,
    x="status_label",
    y="atividades_ultimos_30d",
    ax=axes[0, 1],
    palette=palette,
    hue="status_label",
    legend=False,
    showfliers=False,
)
axes[0, 1].set_title(
    "Treinos nos Últimos 30d Antes do Cancelamento (D-30)", fontsize=13, fontweight="bold"
)
axes[0, 1].set_xlabel("")
axes[0, 1].set_ylabel("Treinos em D-30")

sns.boxplot(
    data=df,
    x="status_label",
    y="media_sessoes_mes",
    ax=axes[1, 0],
    palette=palette,
    hue="status_label",
    legend=False,
    showfliers=False,
)
axes[1, 0].set_title(
    "Média de Sessões no App/Mês na Vigência (Sem Outliers)",
    fontsize=13,
    fontweight="bold",
)
axes[1, 0].set_xlabel("")
axes[1, 0].set_ylabel("Sessões / Mês")

sns.boxplot(
    data=df,
    x="status_label",
    y="media_curtidas_mes",
    ax=axes[1, 1],
    palette=palette,
    hue="status_label",
    legend=False,
    showfliers=False,
)
axes[1, 1].set_title(
    "Média de Curtidas Recebidas/Mês na Vigência (Sem Outliers)", fontsize=13, fontweight="bold"
)
axes[1, 1].set_xlabel("")
axes[1, 1].set_ylabel("Curtidas / Mês")

plt.suptitle(
    "Perfilamento Estatístico Robusto: Comparação Ativos vs. Cancelados (Durante a Vigência)",
    fontsize=16,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig("saidas/boxplot_assimetria_uso.png", bbox_inches="tight")
plt.close()
print("\nGráfico 1 salvo: saidas/boxplot_assimetria_uso.png")

# 2. Curva de Sobrevivência / Lifetime por Plano
order_life = [
    "0 meses (<30d)",
    "1 mes (30-59d)",
    "2 meses (60-89d)",
    "3 meses (90-119d)",
    "4-5 meses",
    "6+ meses",
]
df_life = df.groupby(["faixa_lifetime", "plano_atual"])["churn"].mean().reset_index()
df_life["churn_pct"] = df_life["churn"] * 100

plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_life,
    x="faixa_lifetime",
    y="churn_pct",
    hue="plano_atual",
    order=order_life,
    palette={"anual": "#3498DB", "mensal": "#E67E22"},
)
plt.title(
    "Curva de Churn por Tempo de Casa (Lifetime) e Tipo de Contrato",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Tempo de Casa (Lifetime)", fontsize=12, fontweight="bold")
plt.ylabel("Taxa de Churn (%)", fontsize=12, fontweight="bold")
plt.ylim(0, 100)
for p in plt.gca().patches:
    h = p.get_height()
    if h > 0:
        plt.gca().annotate(
            f"{h:.1f}%",
            (p.get_x() + p.get_width() / 2.0, h + 1.5),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
plt.legend(title="Plano", title_fontsize="11", fontsize="10")
plt.tight_layout()
plt.savefig("saidas/curva_sobrevivencia_lifetime.png", bbox_inches="tight")
plt.close()
print("Gráfico 2 salvo: saidas/curva_sobrevivencia_lifetime.png")

# 3. Diagnóstico do Ponto Cego
cancelados = df[df["churn"] == 1]
tot = len(cancelados)
pesq_web = cancelados["motivo_pesquisa_saida"].notna().sum()
lojas_sem = cancelados["canal_cobranca"].isin(["app_store", "google_play"]).sum()
involuntario = cancelados["motivo_fim"].isin(["falha_pagamento", "chargeback"]).sum()
web_sem_pesq = tot - pesq_web - lojas_sem

labels = [
    f"Cancelamento Lojas (Stores)\nSem Tela do App\n{lojas_sem} ({lojas_sem/tot*100:.1f}%)",
    f"Cancelamento Involuntário\n(Falha/Chargeback)\n{involuntario} ({involuntario/tot*100:.1f}%)",
    f"Web Sem Pesquisa\n(Voluntário s/ Resposta)\n{web_sem_pesq} ({web_sem_pesq/tot*100:.1f}%)",
    f"Pesquisa de Saída\nPreenchida (Web)\n{pesq_web} ({pesq_web/tot*100:.1f}%)",
]
sizes = [lojas_sem, involuntario, web_sem_pesq, pesq_web]
colors = ["#E74C3C", "#F39C12", "#95A5A6", "#27AE60"]

plt.figure(figsize=(10, 8))
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    textprops=dict(color="black", fontsize=11),
    pctdistance=0.75,
    explode=(0.03, 0.03, 0.03, 0.08),
)
plt.title(
    "Diagnóstico do Ponto Cego: 98,0% dos Cancelamentos Ocorrem sem Pesquisa de Saída",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
plt.tight_layout()
plt.savefig("saidas/ponto_cego_cancelamentos.png", bbox_inches="tight")
plt.close()
print("Gráfico 3 salvo: saidas/ponto_cego_cancelamentos.png")

# 4. Gráfico de AUC-ROC Univariado (100% Sem Vazamento Pós-Cancelamento e Normalizado por Vigência!)
variaveis_auc = [
    ("atividades_ultimos_30d", "Treinos nos Últimos 30d Antes do Cancelamento (D-30)", "Uso"),
    ("razao_uso_ultimo_mes", "Razão de Uso Recente (D-30 vs Média Vigência)", "Uso"),
    ("atividades_31_a_60d", "Treinos entre 31d e 60d Antes do Cancelamento (D-60)", "Uso"),
    ("n_modalidades_distintas", "Diversidade de Modalidades (7 Canônicas)", "Uso"),
    ("prop_meses_ativos_vigencia", "Proporção de Meses Ativos na Vigência", "Uso"),
    ("media_dias_ativos_mes", "Média de Dias Ativos/Mês (Na Vigência)", "Uso"),
    ("media_atividades_mes", "Média de Atividades/Mês (Na Vigência)", "Uso"),
    ("media_minutos_mes", "Média de Minutos/Mês (Na Vigência)", "Uso"),
    ("media_sessoes_mes", "Média de Sessões no App/Mês (Na Vigência)", "Uso"),
    ("media_video_mes", "Média de Treinos Vídeo Guiado/Mês (Na Vigência)", "Uso"),
    ("media_ar_livre_mes", "Média de Treinos Ar Livre/Mês (Na Vigência)", "Uso"),
    ("media_posts_mes", "Média de Posts no Feed/Mês (Na Vigência)", "Social"),
    ("media_curtidas_mes", "Média de Curtidas no Feed/Mês (Na Vigência)", "Social"),
    ("num_seguidores", "Número de Seguidores na Comunidade", "Social"),
    ("media_treinos_dupla_mes", "Média de Treinos em Dupla/Mês (Na Vigência)", "Social"),
    ("eh_plano_anual", "Tipo de Plano (Anual vs. Mensal)", "Contrato"),
    ("receita_bruta_mensal", "Valor Médio Pago/Mês (R$ na Vigência)", "Contrato"),
    ("teve_carencia", "Entrou em Período de Carência", "Contrato"),
    ("pagamentos_recusados", "Cobranças Recusadas", "Contrato"),
    ("eh_canal_loja", "Canal de Cobrança (Lojas vs. Web)", "Contrato"),
    ("idade", "Idade do Usuário (Higienizada)", "Entrada"),
    ("dias_semana_pretendidos", "Dias Pretendidos (Onboarding)", "Entrada"),
    ("tem_relogio", "Smartwatch Conectado", "Entrada"),
]

y = df["churn"].values
auc_rows = []
print("\n=== TABELA 2.4 AUC-ROC ATUALIZADA (SEM VAZAMENTO PÓS-CANCELAMENTO) ===")
for col, label, galho in variaveis_auc:
    s = df[col].fillna(df[col].median()).values
    auc = roc_auc_score(y, s)
    auc_ef = max(auc, 1.0 - auc)
    direcao = "Aumenta Churn" if auc >= 0.5 else "Reduz Churn (Protetor)"
    auc_rows.append(
        {
            "Variavel": label,
            "Col": col,
            "AUC": auc_ef,
            "Galho": galho,
            "Direcao": direcao,
        }
    )

df_auc_plot = pd.DataFrame(auc_rows).sort_values("AUC", ascending=False)
for _, r in df_auc_plot.iterrows():
    print(
        f"| **{r['Galho']}** | `{r['Col']}` | {r['Variavel']} | **{r['AUC']:.4f}** | {r['Direcao']} |"
    )

color_map = {
    "Uso": "#3498DB",
    "Contrato": "#9B59B6",
    "Social": "#2ECC71",
    "Entrada": "#E67E22",
}

plt.figure(figsize=(12, 8.5))
bars = plt.barh(
    df_auc_plot["Variavel"][::-1],
    df_auc_plot["AUC"][::-1],
    color=[color_map[g] for g in df_auc_plot["Galho"][::-1]],
)
plt.axvline(
    0.5, color="red", linestyle="--", linewidth=1.5, label="AUC Neutro / Aleatório (0.50)"
)
plt.axvline(
    0.7,
    color="green",
    linestyle=":",
    linewidth=1.5,
    label="Forte Poder Discriminatório (>= 0.70)",
)
plt.title(
    "Poder Discriminatório Univariado (AUC-ROC) dos Preditores de Churn (Sem Vazamento Pós-Cancelamento)",
    fontsize=13.5,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Área Sob a Curva ROC (AUC-ROC)", fontsize=12, fontweight="bold")
plt.xlim(0.45, 1.0)

for bar in bars:
    w = bar.get_width()
    plt.text(
        w + 0.008,
        bar.get_y() + bar.get_height() / 2,
        f"{w:.3f}",
        va="center",
        fontsize=9,
        fontweight="bold",
    )

legend_elements = [Patch(facecolor=color_map[k], label=k) for k in color_map]
legend_elements.append(
    plt.Line2D([0], [0], color="red", linestyle="--", label="Aleatório (0.50)")
)
legend_elements.append(
    plt.Line2D([0], [0], color="green", linestyle=":", label="Forte Poder (0.70)")
)
plt.legend(
    handles=legend_elements,
    loc="lower right",
    title="Galho MECE / Referência",
    title_fontsize="10",
    fontsize="9",
)
plt.tight_layout()
plt.savefig("saidas/auc_roc_ranking.png", bbox_inches="tight")
plt.close()
print("\nGráfico 4 salvo: saidas/auc_roc_ranking.png")
