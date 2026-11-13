"""Gráficos da segmentação da base inteira e dos pontos de atenção (saidas/base_inteira/*.png)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "saidas" / "base_inteira"; T = S / "tabelas"
ORD = ["Ativo ao Ar Livre", "Treino Indoor Guiado", "Hábito Fraco", "Treina em Companhia"]
COR = dict(zip(ORD, ["#1baf7a", "#2a78d6", "#eb6834", "#eda100"]))
INK, MUTED, GRID = "#1c1b19", "#6b6a65", "#e4e3de"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#b9b8b2", "xtick.color": MUTED, "ytick.color": INK,
                     "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK, "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white"})
br = lambda v, d=1: f"{v:.{d}f}".replace(".", ",")
fmt = mt.FuncFormatter(lambda x, _: f"{x:g}".replace(".", ","))
ROT = {"pct_acompanhado": "% treinos acompanhados", "pct_ar_livre": "% treinos ao ar livre", "regularidade": "Regularidade (semanas com treino)", "treinos_mes": "Treinos/mês",
       "n_modalidades": "Modalidades distintas", "posts_mes": "Posts/mês", "min_por_treino": "Minutos por treino", "dias_semana_pretendidos": "Dias/semana declarados", "conexoes": "Conexões sociais"}

# 1. Centróides
z = pd.read_csv(T / "centroides_z.csv", index_col=0); imp = pd.read_csv(T / "importancia_variaveis.csv", index_col=0)["eta2"]
m = z.loc[ORD, imp.index].T
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.imshow(m.values, cmap=LinearSegmentedColormap.from_list("d", ["#2a78d6", "#f1f0ec", "#eb6834"]), vmin=-2, vmax=2, aspect="auto")
ax.set_xticks(range(4), [p.replace(" ao ", "\nao ").replace(" Guiado", "\nGuiado").replace(" em ", "\nem ") for p in ORD]); ax.xaxis.tick_top(); ax.tick_params(length=0)
ax.set_yticks(range(len(m)), [f"{ROT[v]}  (η² {br(imp[v], 2)})" for v in m.index])
for i in range(m.shape[0]):
    for j in range(4):
        v = m.values[i, j]; ax.text(j, i, ("+" if v > 0 else "") + br(v, 2), ha="center", va="center", fontsize=9, color="white" if abs(v) > 1.2 else INK)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks(np.arange(-.5, 4), minor=True); ax.set_yticks(np.arange(-.5, len(m)), minor=True); ax.grid(which="minor", color="white", lw=2); ax.tick_params(which="minor", length=0)
fig.savefig(S / "01_centroides.png"); plt.close(fig)

# 2. Tamanho, receita e churn
R = pd.read_csv(T / "resumo_personas.csv", index_col=0)
fig, axs = plt.subplots(1, 4, figsize=(12, 2.9), sharey=True)
for ax, (col, tit, ref) in zip(axs, [("pct_base", "% dos clientes", None), ("pct_receita", "% da receita líquida", None), ("churn_mensal_pct", "Churn mensal (%)", "Base"), ("churn_mensal_mensalistas_pct", "Churn mensal do plano mensal (%)", "Base")]):
    v = R.loc[ORD[::-1], col]
    ax.barh(range(4), v, color=[COR[p] for p in ORD[::-1]], height=.6)
    for y, x in enumerate(v): ax.text(x + v.max() * .03, y, br(x), va="center", fontsize=9, color=INK)
    if ref: ax.axvline(R.loc[ref, col], color=INK, lw=1, ls="--"); ax.text(R.loc[ref, col], -0.85, f"média da base {br(R.loc[ref, col])}", fontsize=8, color=MUTED, ha="center"); ax.set_ylim(-1.1, 3.5)
    ax.set_title(tit, fontsize=10); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.set_xlim(0, v.max() * 1.3)
axs[0].set_yticks(range(4), ORD[::-1])
fig.tight_layout(); fig.savefig(S / "02_tamanho_receita_churn.png"); plt.close(fig)

# 3. Churn por fase do objetivo com prazo
cf = pd.read_csv(T / "churn_por_fase_evento.csv")
fases = ["sem prazo", "evento à frente", "evento recente (±60 dias)", "evento passou há 60+ dias"]
cores = {"sem prazo": "#b9b8b2", "evento à frente": "#9ec5f0", "evento recente (±60 dias)": "#eb6834", "evento passou há 60+ dias": "#2a78d6"}
fig, ax = plt.subplots(figsize=(9, 3.6)); w = .2
for i, f in enumerate(fases):
    v = cf[cf.fase_evento.eq(f)].set_index("persona").reindex(ORD)
    ax.bar(np.arange(4) + (i - 1.5) * w, v.saiu_pct, width=w - .02, color=cores[f], label=f)
    for x, (y, n) in enumerate(zip(v.saiu_pct, v.n)):
        if n >= 30: ax.text(x + (i - 1.5) * w, y + 1.2, f"{y:.0f}", ha="center", fontsize=7.5, color=INK)
ax.set_xticks(range(4), ORD); ax.set_ylabel("% que saiu na janela", color=MUTED); ax.grid(axis="y", color=GRID, lw=.7); ax.set_ylim(0, 85)
ax.legend(frameon=False, ncols=4, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 1.12)); ax.yaxis.set_major_formatter(fmt)
fig.savefig(S / "03_churn_objetivo_prazo.png"); plt.close(fig)

# 4. Personas x segmentos do time (só ativos)
c = pd.read_csv(T / "estatisticas_categoricas.csv"); c = c[c.variavel.eq("Segmento do time (só ativos)")].set_index("categoria")[ORD]
fig, ax = plt.subplots(figsize=(7.5, 2.8))
ax.imshow(c.values, cmap=LinearSegmentedColormap.from_list("s", ["#f6f6f3", "#2a78d6"]), vmin=0, vmax=100, aspect="auto")
ax.set_xticks(range(4), [p.replace(" ao ", "\nao ").replace(" Guiado", "\nGuiado").replace(" em ", "\nem ") for p in ORD]); ax.xaxis.tick_top(); ax.tick_params(length=0)
ax.set_yticks(range(len(c)), c.index)
for i in range(c.shape[0]):
    for j in range(4): ax.text(j, i, br(c.values[i, j]) + "%", ha="center", va="center", fontsize=9, color="white" if c.values[i, j] > 60 else INK)
for s in ax.spines.values(): s.set_visible(False)
fig.savefig(S / "04_personas_vs_segmentos_time.png"); plt.close(fig)

# 5. Distribuições
b = pd.read_pickle(S / "_fit.pkl")
V = [("treinos_mes", "Treinos/mês", 1), ("regularidade", "% semanas com treino", 100), ("pct_ar_livre", "% treinos ao ar livre", 100), ("pct_acompanhado", "% treinos acompanhados", 100), ("n_modalidades", "Modalidades distintas", 1), ("sessoes_app_mes", "Sessões de app/mês (não entrou)", 1)]
fig, axs = plt.subplots(2, 3, figsize=(11, 5), sharey=True)
for ax, (col, t, k) in zip(axs.flat, V):
    bp = ax.boxplot([b.loc[b.persona.eq(p), col].dropna() * k for p in ORD[::-1]], orientation="horizontal", widths=.55, patch_artist=True, showfliers=False,
                    medianprops=dict(color=INK, lw=2), whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED))
    for pa, p in zip(bp["boxes"], ORD[::-1]): pa.set(facecolor=COR[p], edgecolor="white")
    ax.set_yticks(range(1, 5), ORD[::-1]); ax.set_title(t); ax.grid(axis="x", color=GRID, lw=.7); ax.xaxis.set_major_formatter(fmt)
fig.tight_layout(); fig.savefig(S / "05_distribuicoes.png"); plt.close(fig)

# 6. Campanha: efeito do cupom muda com a janela
cp = pd.read_csv(T / "campanha_janelas.csv")
cp = cp[cp.grupo.eq("cupom")].reset_index(drop=True)
fig, ax = plt.subplots(figsize=(8, 2.6))
for y, r in cp.iloc[::-1].reset_index(drop=True).iterrows():
    sig = r.ic95_sup < 0
    ax.plot([r.ic95_inf, r.ic95_sup], [y, y], color="#2a78d6" if sig else "#b9b8b2", lw=3, solid_capstyle="round")
    ax.scatter([r.dif_pp], [y], s=60, color="#2a78d6" if sig else "#8d8c86", zorder=3, edgecolor="white", linewidth=1.5)
    ax.text(r.ic95_sup + .15, y, f"{br(r.dif_pp, 1)} p.p.", va="center", fontsize=9, color=INK)
ax.axvline(0, color=INK, lw=1); ax.set_yticks(range(3), cp.janela[::-1].str.replace(", ", "\n")); ax.set_xlabel("Cupom menos controle, em pontos percentuais de churn (IC 95%)", color=MUTED)
ax.xaxis.set_major_formatter(fmt); ax.grid(axis="x", color=GRID, lw=.7); ax.set_xlim(-7.5, 1.8)
fig.savefig(S / "06_campanha_janelas.png"); plt.close(fig)
print("ok")
