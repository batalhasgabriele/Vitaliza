"""Etapa 3 da EDA: churn mensal, marcos de 2026 e controles estatísticos.

Entradas são lidas exclusivamente da camada Bronze/Prata. As saídas agregadas
seguem para a camada Ouro e para ``saidas/``. Nenhum resultado é descrito como
causal, exceto a comparação ITT da campanha randomizada dentro da janela
observável de 30 dias.
"""

from __future__ import annotations

import json
import math
from statistics import NormalDist
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
BRONZE = ROOT / "dados" / "brutos"
PRATA = ROOT / "dados" / "processados" / "prata"
OURO = ROOT / "dados" / "processados" / "ouro"
SAIDAS = ROOT / "saidas"
TABELAS = SAIDAS / "tabelas"

COR_LOJA = "#4464AD"
COR_WEB = "#2A9D8F"
COR_ALERTA = "#E76F51"
COR_NEUTRA = "#6C757D"


def harmonizar_data_utc_para_br(series: pd.Series) -> pd.Series:
    """Converte valores terminados em Z de UTC para Brasília e preserva web local."""
    values = series.astype("string")
    is_utc = values.str.endswith("Z", na=False)
    result = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")
    if is_utc.any():
        result.loc[is_utc] = (
            pd.to_datetime(values.loc[is_utc], utc=True, errors="coerce")
            .dt.tz_convert("America/Sao_Paulo")
            .dt.tz_localize(None)
        )
    if (~is_utc).any():
        result.loc[~is_utc] = pd.to_datetime(values.loc[~is_utc], errors="coerce")
    return result


def two_proportion_p_value(success_a: int, total_a: int, success_b: int, total_b: int) -> float:
    """Teste z bilateral de duas proporções; retorna 1 quando não há variância."""
    pooled = (success_a + success_b) / (total_a + total_b)
    variance = pooled * (1 - pooled) * (1 / total_a + 1 / total_b)
    if variance <= 0:
        return 1.0
    z_score = (success_a / total_a - success_b / total_b) / math.sqrt(variance)
    return 2 * (1 - NormalDist().cdf(abs(z_score)))


def preparar_fontes() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    usuarios = pd.read_csv(BRONZE / "usuarios.csv", low_memory=False)
    assinaturas = pd.read_parquet(PRATA / "assinaturas_limpas.parquet")
    assinaturas["inicio_dt"] = pd.to_datetime(assinaturas["inicio"], errors="raise")
    eventos = pd.read_parquet(PRATA / "eventos_assinatura_limpos.parquet")
    if eventos["data_hora_br"].isna().any():
        raise ValueError("Existem timestamps de eventos não convertíveis.")

    expiracoes = (
        eventos.loc[eventos["evento"] == "assinatura_expirada"]
        .sort_values(["user_id", "data_hora_br"])
        .drop_duplicates("user_id", keep="last")
        [["user_id", "data_hora_br", "plano", "canal_cobranca", "detalhe"]]
        .rename(columns={"data_hora_br": "expiracao_br"})
    )
    assinaturas = assinaturas.merge(expiracoes, on="user_id", how="left", validate="one_to_one")
    return usuarios, assinaturas, eventos


def construir_churn_mensal(assinaturas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    months = pd.date_range("2025-01-01", "2026-09-01", freq="MS")
    records: list[dict[str, object]] = []
    plan_records: list[dict[str, object]] = []

    for month in months:
        next_month = month + pd.offsets.MonthBegin(1)
        active_mask = (assinaturas["inicio_dt"] < month) & (
            assinaturas["expiracao_br"].isna() | (assinaturas["expiracao_br"] >= month)
        )
        loss_mask = (assinaturas["expiracao_br"] >= month) & (assinaturas["expiracao_br"] < next_month)
        active_start = int(active_mask.sum())
        losses = int(loss_mask.sum())
        records.append(
            {
                "mes": month,
                "ativos_inicio": active_start,
                "perdas": losses,
                "churn": losses / active_start if active_start else np.nan,
            }
        )
        for plan in ("mensal", "anual"):
            plan_mask = assinaturas["plano_atual"] == plan
            plan_active = int((active_mask & plan_mask).sum())
            plan_losses = int((loss_mask & plan_mask).sum())
            plan_records.append(
                {
                    "mes": month,
                    "plano": plan,
                    "ativos_inicio": plan_active,
                    "perdas": plan_losses,
                    "churn": plan_losses / plan_active if plan_active else np.nan,
                }
            )

    churn = pd.DataFrame(records)
    churn_plano = pd.DataFrame(plan_records)
    churn["ano"] = churn["mes"].dt.year
    churn["churn_pct"] = churn["churn"] * 100
    churn_plano["churn_pct"] = churn_plano["churn"] * 100
    return churn, churn_plano


def analisar_pesquisa(assinaturas: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    start = pd.Timestamp("2026-06-01")
    end = pd.Timestamp("2026-10-01")
    losses = assinaturas.loc[
        (assinaturas["expiracao_br"] >= start) & (assinaturas["expiracao_br"] < end)
    ].copy()
    losses["grupo_canal"] = np.where(
        losses["canal_cobranca_y"].isin(["app_store", "google_play"]), "Lojas", "Web"
    )
    loss_summary = losses.groupby("grupo_canal", as_index=False).agg(perdas=("user_id", "nunique"))

    survey = pd.read_parquet(PRATA / "pesquisa_saida_limpa.parquet")
    unique_survey = survey.sort_values("respondido_em").drop_duplicates("user_id", keep="last")
    respondent = unique_survey.merge(
        assinaturas[["user_id", "canal_cobranca_x", "status_atual"]], on="user_id", how="left"
    )
    respondent["grupo_canal"] = np.where(
        respondent["canal_cobranca_x"].isin(["app_store", "google_play"]), "Lojas", "Web"
    )
    response_summary = respondent.groupby("grupo_canal", as_index=False).agg(
        respondentes=("user_id", "nunique")
    )
    summary = loss_summary.merge(response_summary, on="grupo_canal", how="outer").fillna(0)
    summary[["perdas", "respondentes"]] = summary[["perdas", "respondentes"]].astype(int)
    summary["cobertura_aparente_pct"] = np.where(
        summary["perdas"] > 0, summary["respondentes"] / summary["perdas"] * 100, np.nan
    )
    metrics = {
        "respostas": int(len(survey)),
        "respondentes_unicos": int(unique_survey["user_id"].nunique()),
        "respondentes_ativos_corte": int((respondent["status_atual"] == "ativa").sum()),
        "respostas_ativas_corte": int(
            survey.merge(
                assinaturas[["user_id", "status_atual"]], on="user_id", how="left"
            )["status_atual"].eq("ativa").sum()
        ),
        "perdas_jun_set": int(losses["user_id"].nunique()),
    }
    return summary, metrics


def analisar_campanha(eventos: pd.DataFrame) -> pd.DataFrame:
    campaign = pd.read_parquet(PRATA / "campanha_ago26_limpa.parquet")
    # O controle não recebeu mensagem e, portanto, não possui enviado_em. A
    # janela ITT começa na data comum de sorteio para todos os braços.
    campaign["data_atribuicao"] = pd.Timestamp("2026-08-10 00:00:00")
    expirations = (
        eventos.loc[eventos["evento"] == "assinatura_expirada", ["user_id", "data_hora_br"]]
        .sort_values(["user_id", "data_hora_br"])
        .drop_duplicates("user_id", keep="last")
        .rename(columns={"data_hora_br": "expiracao_br"})
    )
    campaign = campaign.merge(expirations, on="user_id", how="left", validate="one_to_one")
    campaign["churn_30d"] = (
        campaign["expiracao_br"].notna()
        & (campaign["expiracao_br"] >= campaign["data_atribuicao"])
        & (campaign["expiracao_br"] < campaign["data_atribuicao"] + pd.Timedelta(days=30))
    )
    summary = campaign.groupby("grupo", as_index=False).agg(
        sorteados=("user_id", "nunique"),
        perdas_30d=("churn_30d", "sum"),
        abriu_push_pct=("abriu_push", "mean"),
        abriu_email_pct=("abriu_email", "mean"),
        clicou_pct=("clicou", "mean"),
    )
    summary["churn_30d_pct"] = summary["perdas_30d"] / summary["sorteados"] * 100
    control = summary.loc[summary["grupo"] == "controle"].iloc[0]
    summary["diferenca_vs_controle_pp"] = summary["churn_30d_pct"] - control["churn_30d_pct"]
    summary["p_valor_vs_controle"] = summary.apply(
        lambda row: 1.0
        if row["grupo"] == "controle"
        else two_proportion_p_value(
            int(row["perdas_30d"]),
            int(row["sorteados"]),
            int(control["perdas_30d"]),
            int(control["sorteados"]),
        ),
        axis=1,
    )
    for column in ("abriu_push_pct", "abriu_email_pct", "clicou_pct"):
        summary[column] *= 100
    return summary.sort_values("grupo").reset_index(drop=True)


def analisar_outliers() -> tuple[pd.DataFrame, dict[str, float]]:
    activities = pd.read_parquet(BRONZE / "atividades.parquet", columns=["tipo", "distancia_km"])
    map_types = {"run": "corrida", "walk": "caminhada", "strength": "forca", "ride": "pedal"}
    activities["modalidade"] = activities["tipo"].replace(map_types)
    gps = activities.loc[activities["distancia_km"].notna()].copy()
    q1 = float(gps["distancia_km"].quantile(0.25))
    q3 = float(gps["distancia_km"].quantile(0.75))
    threshold = q3 + 1.5 * (q3 - q1)
    gps["outlier_global"] = gps["distancia_km"] > threshold
    summary = (
        gps.groupby("modalidade", as_index=False)
        .agg(
            treinos=("distancia_km", "size"),
            mediana_km=("distancia_km", "median"),
            outliers_regra_global=("outlier_global", "sum"),
        )
        .sort_values("outliers_regra_global", ascending=False)
    )
    summary["pct_marcado_global"] = summary["outliers_regra_global"] / summary["treinos"] * 100
    metrics = {
        "q1": q1,
        "q3": q3,
        "limiar_tukey": threshold,
        "outliers_global": int(gps["outlier_global"].sum()),
        "outliers_pedal": int(
            gps.loc[gps["modalidade"] == "pedal", "outlier_global"].sum()
        ),
    }
    return summary, metrics


def analisar_correlacao() -> pd.DataFrame:
    usage = pd.read_parquet(PRATA / "uso_mensal_limpo.parquet")
    september = usage.loc[usage["mes"] == "2026-09"].copy()
    active = september.loc[september["atividades"] > 0].copy()
    raw_all = float(september["sessoes_app"].corr(september["minutos"]))
    raw_active = float(active["sessoes_app"].corr(active["minutos"]))
    design = np.column_stack([np.ones(len(active)), active["atividades"].to_numpy(dtype=float)])
    beta_sessions = np.linalg.lstsq(design, active["sessoes_app"].to_numpy(dtype=float), rcond=None)[0]
    beta_minutes = np.linalg.lstsq(design, active["minutos"].to_numpy(dtype=float), rcond=None)[0]
    residual_sessions = active["sessoes_app"].to_numpy(dtype=float) - design @ beta_sessions
    residual_minutes = active["minutos"].to_numpy(dtype=float) - design @ beta_minutes
    partial = float(np.corrcoef(residual_sessions, residual_minutes)[0, 1])
    return pd.DataFrame(
        [
            {"metrica": "Correlação bruta — todas as contas", "n": len(september), "r": raw_all},
            {"metrica": "Correlação bruta — contas com treino", "n": len(active), "r": raw_active},
            {"metrica": "Correlação parcial — controlando atividades", "n": len(active), "r": partial},
        ]
    )


def configurar_grafico() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 180,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titleweight": "bold",
        }
    )


def plot_churn(churn: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 5.8))
    ax.plot(churn["mes"], churn["churn_pct"], marker="o", color=COR_LOJA, linewidth=2.2)
    for date, label, color in (
        (pd.Timestamp("2026-03-01"), "Reajuste", COR_ALERTA),
        (pd.Timestamp("2026-06-01"), "Pesquisa de saída", COR_WEB),
        (pd.Timestamp("2026-08-10"), "Campanha A/B", "#8F5DA2"),
    ):
        ax.axvline(date, linestyle="--", linewidth=1.3, color=color, alpha=0.85)
        ax.text(date, ax.get_ylim()[1] * 0.98, label, rotation=90, va="top", ha="right", color=color)
    ax.set(title="Churn mensal de assinantes pagantes", xlabel="Mês", ylabel="Perdas / ativos no início do mês (%)")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(SAIDAS / "churn_mensal_2025_2026.png", bbox_inches="tight")
    plt.close(fig)


def plot_marcos(
    churn_plan: pd.DataFrame,
    survey: pd.DataFrame,
    campaign: pd.DataFrame,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))
    monthly = churn_plan.loc[
        (churn_plan["plano"] == "mensal")
        & (churn_plan["mes"] >= "2026-01-01")
        & (churn_plan["mes"] <= "2026-07-01")
    ]
    axes[0].plot(monthly["mes"], monthly["churn_pct"], marker="o", color=COR_ALERTA)
    axes[0].axvline(pd.Timestamp("2026-03-01"), linestyle="--", color=COR_NEUTRA)
    axes[0].set(title="1. Reajuste: plano mensal", ylabel="Churn (%)", xlabel="Mês")
    axes[0].tick_params(axis="x", rotation=45)

    survey_plot = survey.set_index("grupo_canal")[["perdas", "respondentes"]]
    survey_plot.plot(kind="bar", ax=axes[1], color=[COR_LOJA, COR_WEB])
    axes[1].set(title="2. Pesquisa: alcance por canal", ylabel="Pessoas", xlabel="Canal")
    axes[1].tick_params(axis="x", rotation=0)
    axes[1].legend(["Perdas jun–set", "Respondentes"])

    camp = campaign.set_index("grupo")["churn_30d_pct"].reindex(
        ["controle", "desafio", "cupom", "conteudo"]
    )
    axes[2].bar(camp.index, camp.values, color="#8F5DA2")
    control = float(campaign.loc[campaign["grupo"] == "controle", "churn_30d_pct"].iloc[0])
    axes[2].axhline(control, linestyle="--", color=COR_NEUTRA, label="Controle")
    axes[2].set(title="3. Campanha: churn ITT em 30 dias", ylabel="Churn em 30 dias (%)", xlabel="Braço sorteado")
    axes[2].tick_params(axis="x", rotation=25)
    axes[2].legend()
    fig.suptitle("Três marcos de 2026: evidência observacional e experimental", fontsize=15, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SAIDAS / "marcos_2026.png", bbox_inches="tight")
    plt.close(fig)


def plot_outliers(summary: pd.DataFrame) -> None:
    plot_data = summary.sort_values("outliers_regra_global")
    colors = [COR_ALERTA if value == "pedal" else COR_LOJA for value in plot_data["modalidade"]]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(plot_data["modalidade"], plot_data["outliers_regra_global"], color=colors)
    ax.set(title="Regra global de Tukey marca sobretudo treinos de pedal", xlabel="Treinos acima do limiar global", ylabel="Modalidade")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(SAIDAS / "outliers_por_modalidade.png", bbox_inches="tight")
    plt.close(fig)


def plot_correlation(summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    colors = [COR_LOJA, COR_WEB, COR_ALERTA]
    bars = ax.barh(summary["metrica"], summary["r"], color=colors)
    ax.bar_label(bars, labels=[f"{value:.2f}" for value in summary["r"]], padding=4)
    ax.set(title="A associação sessões × minutos desaparece após o controle", xlabel="Correlação de Pearson (r)", ylabel="")
    ax.set_xlim(-0.05, 1.0)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(SAIDAS / "correlacao_controlada.png", bbox_inches="tight")
    plt.close(fig)


def render_report(
    churn: pd.DataFrame,
    churn_plan: pd.DataFrame,
    survey: pd.DataFrame,
    survey_metrics: dict[str, object],
    campaign: pd.DataFrame,
    outliers: pd.DataFrame,
    outlier_metrics: dict[str, float],
    correlation: pd.DataFrame,
) -> str:
    mean_2025 = churn.loc[churn["ano"] == 2025, "churn_pct"].mean()
    mean_2026 = churn.loc[churn["ano"] == 2026, "churn_pct"].mean()
    peak = churn.loc[churn["churn_pct"].idxmax()]
    jan_feb = churn_plan.loc[
        (churn_plan["plano"] == "mensal") & churn_plan["mes"].isin(pd.to_datetime(["2026-01-01", "2026-02-01"])),
        "churn_pct",
    ].mean()
    mar_apr = churn_plan.loc[
        (churn_plan["plano"] == "mensal") & churn_plan["mes"].isin(pd.to_datetime(["2026-03-01", "2026-04-01"])),
        "churn_pct",
    ].mean()
    best = campaign.loc[campaign["grupo"] != "controle"].sort_values("churn_30d_pct").iloc[0]
    corr_raw = float(correlation.iloc[1]["r"])
    corr_partial = float(correlation.iloc[2]["r"])
    lines = [
        "# EDA Parte 2 — Churn e Marcos de 2026",
        "",
        "**Data de corte:** 30/09/2026\n",
        "**Regra de comunicação:** 1 tabela + 1 gráfico + 3 frases por achado.",
        "",
        "## 1. Série mensal de churn",
        "",
        churn[["mes", "ativos_inicio", "perdas", "churn_pct"]].to_markdown(index=False, floatfmt=".2f"),
        "",
        "![Churn mensal](churn_mensal_2025_2026.png)",
        "",
        f"1. **O dado diz:** a média mensal foi {mean_2025:.2f}% em 2025 e {mean_2026:.2f}% entre jan–set/2026; o pico observado foi {peak['churn_pct']:.2f}% em {peak['mes']:%m/%Y}, com {int(peak['perdas']):,} perdas.",
        "   **Reconciliação:** a reconstrução por `assinatura_expirada` harmonizada para Brasília fica próxima das referências executivas de 5,6%, 6,6% e 1.154 perdas em abril, mas observa 5,68%, 6,68% e 1.158. A diferença de quatro casos em abril é preservada como divergência de definição, não ajustada artificialmente.",
        "2. **O dado não diz:** a coincidência temporal com preço, sazonalidade ou campanha não identifica causalidade isoladamente.",
        "3. **Próxima pergunta:** quais perfis comportamentais concentram a alta de 2026 sem usar churn para formar os segmentos?",
        "",
        "## 2. Três marcos de 2026",
        "",
        "### 2.1 Reajuste de 01/03",
        "",
        churn_plan.loc[(churn_plan["plano"] == "mensal") & (churn_plan["mes"].between("2026-01-01", "2026-07-01"))][["mes", "ativos_inicio", "perdas", "churn_pct"]].to_markdown(index=False, floatfmt=".2f"),
        "",
        f"1. **O dado diz:** no plano mensal, a média de churn passou de {jan_feb:.2f}% em jan–fev para {mar_apr:.2f}% em mar–abr.",
        "2. **O dado não diz:** o desenho antes/depois mistura reajuste, sazonalidade, composição de coortes e proximidade de renovação; não estima elasticidade causal.",
        "3. **Próxima pergunta:** o efeito aparente persiste ao comparar coortes e controlar tempo de casa, canal e vencimento?",
        "",
        "### 2.2 Pesquisa de saída a partir de 01/06",
        "",
        survey.to_markdown(index=False, floatfmt=".2f"),
        "",
        f"1. **O dado diz:** houve {survey_metrics['perdas_jun_set']:,} expirações entre junho e setembro e {survey_metrics['respondentes_unicos']:,} respondentes únicos; {survey_metrics['respondentes_ativos_corte']:,} respondentes únicos ({survey_metrics['respostas_ativas_corte']:,} respostas) ainda estavam ativos no corte.",
        "2. **O dado não diz:** motivos declarados por usuários Web que optaram por responder não representam automaticamente perdas nas lojas nem causas de churn.",
        "3. **Próxima pergunta:** como combinar motivos declarados com comportamento prévio sem criar vazamento ou generalização indevida?",
        "",
        "### 2.3 Campanha randomizada de 10/08",
        "",
        campaign.to_markdown(index=False, floatfmt=".3f"),
        "",
        f"1. **O dado diz:** no horizonte completo de 30 dias, o menor churn ITT foi do braço `{best['grupo']}` ({best['churn_30d_pct']:.2f}%), diferença de {best['diferenca_vs_controle_pp']:.2f} p.p. frente ao controle (p={best['p_valor_vs_controle']:.3f}); nenhuma comparação atingiu significância de 5%.",
        "2. **O dado não diz:** abertura e clique são pós-tratamento e não podem ser usados para definir causalmente quem foi persuadido; o data room não oferece 60 dias completos após 10/08.",
        "3. **Próxima pergunta:** os intervalos e o tamanho amostral sustentam heterogeneidade por segmento em um holdout adequado?",
        "",
        "![Três marcos](marcos_2026.png)",
        "",
        "## 3. Outliers por modalidade",
        "",
        outliers.to_markdown(index=False, floatfmt=".2f"),
        "",
        "![Outliers](outliers_por_modalidade.png)",
        "",
        f"1. **O dado diz:** a regra global de Tukey usa limiar de {outlier_metrics['limiar_tukey']:.2f} km e marca {int(outlier_metrics['outliers_global']):,} treinos; {int(outlier_metrics['outliers_pedal']):,} são pedal.",
        "2. **O dado não diz:** distância alta não é automaticamente erro; uma regra global confunde modalidades com escalas físicas distintas.",
        "3. **Próxima pergunta:** quais limites de validade e dispersão devem ser definidos dentro de cada modalidade antes da segmentação?",
        "",
        "## 4. Correlação controlada",
        "",
        correlation.to_markdown(index=False, floatfmt=".3f"),
        "",
        "![Correlação controlada](correlacao_controlada.png)",
        "",
        f"1. **O dado diz:** entre contas com treino, r(sessoes, minutos) é {corr_raw:.2f}; após controlar linearmente o número de atividades, cai para {corr_partial:.2f}.",
        "2. **O dado não diz:** abrir o aplicativo mais vezes causa aumento de minutos; ambas as métricas refletem principalmente quantos treinos foram feitos.",
        "3. **Próxima pergunta:** quais variáveis mantêm sinal próprio após controle por volume de atividade e tempo de exposição?",
        "",
        "## Limitações",
        "",
        "- A Prata de assinaturas é usada apenas para identidade, início e atributos contratuais do retrato; o evento terminal vem da Prata de eventos harmonizada para Brasília.",
        "- A série começa em 2025, período integralmente coberto pelo log iniciado em 01/07/2024.",
        "- O reajuste é análise observacional; somente a campanha randomizada permite interpretação causal ITT no horizonte observado.",
        "- A pesquisa de saída possui viés de canal e seleção; respostas de usuários ainda ativos não equivalem a perdas concluídas.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    for directory in (OURO, SAIDAS, TABELAS):
        directory.mkdir(parents=True, exist_ok=True)
    configurar_grafico()
    _, subscriptions, events = preparar_fontes()
    churn, churn_plan = construir_churn_mensal(subscriptions)
    survey, survey_metrics = analisar_pesquisa(subscriptions)
    campaign = analisar_campanha(events)
    outliers, outlier_metrics = analisar_outliers()
    correlation = analisar_correlacao()

    churn.to_parquet(OURO / "churn_mensal_2025_2026.parquet", index=False)
    churn_plan.to_parquet(OURO / "churn_mensal_por_plano_2025_2026.parquet", index=False)
    churn.to_csv(TABELAS / "churn_mensal_2025_2026.csv", index=False)
    churn_plan.to_csv(TABELAS / "churn_mensal_por_plano_2025_2026.csv", index=False)
    survey.to_csv(TABELAS / "pesquisa_saida_cobertura.csv", index=False)
    campaign.to_csv(TABELAS / "campanha_ago26_itt_30d.csv", index=False)
    outliers.to_csv(TABELAS / "outliers_por_modalidade.csv", index=False)
    correlation.to_csv(TABELAS / "correlacao_controlada.csv", index=False)

    plot_churn(churn)
    plot_marcos(churn_plan, survey, campaign)
    plot_outliers(outliers)
    plot_correlation(correlation)

    report = render_report(
        churn,
        churn_plan,
        survey,
        survey_metrics,
        campaign,
        outliers,
        outlier_metrics,
        correlation,
    )
    (SAIDAS / "eda_etapa3_marcos_2026.md").write_text(report, encoding="utf-8")
    metrics = {
        "media_churn_2025_pct": float(churn.loc[churn["ano"] == 2025, "churn_pct"].mean()),
        "media_churn_2026_pct": float(churn.loc[churn["ano"] == 2026, "churn_pct"].mean()),
        "pesquisa": survey_metrics,
        "outliers": outlier_metrics,
        "correlacao": correlation.to_dict(orient="records"),
    }
    (SAIDAS / "tabelas" / "metricas_etapa3.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(report)


if __name__ == "__main__":
    main()
