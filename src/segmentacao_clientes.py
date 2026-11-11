"""Feature store e clusterização não supervisionada dos pagantes ativos.

Etapa 4 da Semana 5 — Projeto Vitaliza.
Entrada: exclusivamente tabelas Prata.
Saída: tabelas Ouro, agregados seguros e gráficos executivos.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
PRATA = ROOT / "dados" / "processados" / "prata"
OURO = ROOT / "dados" / "processados" / "ouro"
SAIDAS = ROOT / "saidas"
TABELAS = SAIDAS / "tabelas"
DATA_CORTE = pd.Timestamp("2026-09-30 23:59:59")
INICIO_90D = DATA_CORTE.normalize() - pd.Timedelta(days=89)
INICIO_30D = DATA_CORTE.normalize() - pd.Timedelta(days=29)
INICIO_60D = DATA_CORTE.normalize() - pd.Timedelta(days=59)
RANDOM_STATE = 42
POPULACAO_OFICIAL = 14_753

FEATURES_CLUSTER = [
    "recencia_treino_dias",
    "treinos_30d",
    "delta_treinos_30_60",
    "regularidade_3m",
    "n_modalidades_90d",
    "prop_ar_livre_3m",
    "prop_video_3m",
    "posts_90d",
    "curtidas_90d",
    "conexoes_sociais",
    "tickets_90d",
    "tenure_meses",
    "dias_semana_pretendidos",
    "flag_onb_dias_preenchido",
    "plano_anual",
    "canal_loja",
]

FEATURES_LOG = {
    "treinos_30d",
    "n_modalidades_90d",
    "posts_90d",
    "curtidas_90d",
    "conexoes_sociais",
    "tickets_90d",
    "tenure_meses",
}

PERFIS_LABELS = {
    "recencia_treino_dias": "Recência (dias)",
    "treinos_30d": "Treinos D-30",
    "delta_treinos_30_60": "Tendência D-30 vs D-60",
    "regularidade_3m": "Regularidade 3m",
    "n_modalidades_90d": "Diversidade 90d",
    "prop_ar_livre_3m": "Proporção ao ar livre",
    "prop_video_3m": "Proporção vídeo",
    "posts_90d": "Posts 90d",
    "curtidas_90d": "Curtidas 90d",
    "conexoes_sociais": "Conexões sociais",
    "tickets_90d": "Tickets 90d",
    "tenure_meses": "Tempo de casa",
    "dias_semana_pretendidos": "Intenção semanal",
    "flag_onb_dias_preenchido": "Onboarding preenchido",
    "plano_anual": "Plano anual",
    "canal_loja": "Canal loja",
}


def divisao_segura(numerador: pd.Series, denominador: pd.Series) -> pd.Series:
    """Divide séries, devolvendo zero quando o denominador é zero."""
    den = denominador.replace(0, np.nan)
    return numerador.div(den).replace([np.inf, -np.inf], np.nan).fillna(0.0)


def _agregar_atividades(ativos: pd.Index) -> tuple[pd.DataFrame, pd.Series]:
    atividades = pd.read_parquet(PRATA / "atividades_limpas.parquet")
    atividades = atividades.loc[atividades["user_id"].isin(ativos)].copy()
    atividades["inicio_dt_br"] = pd.to_datetime(atividades["inicio_dt_br"])
    atividades = atividades.loc[atividades["inicio_dt_br"] <= DATA_CORTE]

    ultima = atividades.groupby("user_id")["inicio_dt_br"].max()
    ultimos_90 = atividades.loc[atividades["inicio_dt_br"] >= INICIO_90D].copy()
    ultimos_30 = ultimos_90.loc[ultimos_90["inicio_dt_br"] >= INICIO_30D]
    faixa_31_60 = ultimos_90.loc[
        (ultimos_90["inicio_dt_br"] >= INICIO_60D)
        & (ultimos_90["inicio_dt_br"] < INICIO_30D)
    ]

    out = pd.DataFrame(index=ativos)
    out["treinos_30d"] = ultimos_30.groupby("user_id").size()
    out["treinos_31_60d"] = faixa_31_60.groupby("user_id").size()
    out["minutos_30d"] = ultimos_30.groupby("user_id")["duracao_min"].sum()
    out["treinos_90d"] = ultimos_90.groupby("user_id").size()
    out["n_modalidades_90d"] = ultimos_90.groupby("user_id")["tipo_canonico"].nunique()
    out["treinos_dupla_90d"] = (
        ultimos_90.assign(
            em_dupla=ultimos_90["treino_com"].fillna("").astype(str).str.strip().ne("")
        )
        .groupby("user_id")["em_dupla"]
        .sum()
    )
    out = out.fillna(0.0)
    out["delta_treinos_30_60"] = divisao_segura(
        out["treinos_30d"] - out["treinos_31_60d"],
        out["treinos_30d"] + out["treinos_31_60d"] + 1.0,
    ).clip(-1.0, 1.0)
    out["prop_treinos_dupla_90d"] = divisao_segura(
        out["treinos_dupla_90d"], out["treinos_90d"]
    )
    out["recencia_treino_dias"] = (
        (DATA_CORTE.normalize() - ultima.dt.normalize()).dt.days.reindex(ativos).fillna(181)
    ).clip(0, 181)

    modalidade = (
        ultimos_90.groupby(["user_id", "tipo_canonico"])
        .size()
        .rename("n")
        .reset_index()
        .sort_values(["user_id", "n", "tipo_canonico"], ascending=[True, False, True])
        .drop_duplicates("user_id")
        .set_index("user_id")["tipo_canonico"]
        .reindex(ativos)
        .fillna("sem_treino_90d")
    )
    return out, modalidade


def _agregar_uso(ativos: pd.Index, inicio_assinatura: pd.Series) -> pd.DataFrame:
    uso = pd.read_parquet(PRATA / "uso_mensal_limpo.parquet")
    uso = uso.loc[
        uso["user_id"].isin(ativos) & uso["mes"].between("2026-07", "2026-09")
    ].copy()

    soma = uso.groupby("user_id").agg(
        atividades_3m=("atividades", "sum"),
        ar_livre_3m=("atividades_ar_livre", "sum"),
        video_3m=("atividades_video", "sum"),
        minutos_3m=("minutos", "sum"),
        dias_ativos_3m=("dias_ativos", "sum"),
        sessoes_app_3m=("sessoes_app", "sum"),
        meses_com_uso_3m=("minutos", lambda s: int((s > 0).sum())),
    ).reindex(ativos).fillna(0.0)

    inicio_periodo = inicio_assinatura.dt.to_period("M")
    meses_expostos = inicio_periodo.map(
        lambda p: max(1, min(3, (pd.Period("2026-09", freq="M") - max(p, pd.Period("2026-07", freq="M"))).n + 1))
    )
    soma["meses_expostos_3m"] = meses_expostos.reindex(ativos).astype(float)
    soma["regularidade_3m"] = divisao_segura(
        soma["meses_com_uso_3m"], soma["meses_expostos_3m"]
    ).clip(0.0, 1.0)
    soma["media_atividades_3m"] = divisao_segura(
        soma["atividades_3m"], soma["meses_expostos_3m"]
    )
    soma["media_minutos_3m"] = divisao_segura(
        soma["minutos_3m"], soma["meses_expostos_3m"]
    )
    soma["prop_ar_livre_3m"] = divisao_segura(
        soma["ar_livre_3m"], soma["atividades_3m"]
    ).clip(0.0, 1.0)
    soma["prop_video_3m"] = divisao_segura(
        soma["video_3m"], soma["atividades_3m"]
    ).clip(0.0, 1.0)
    return soma


def _agregar_social_suporte(ativos: pd.Index) -> pd.DataFrame:
    amizades = pd.read_parquet(PRATA / "amizades_limpas.parquet")
    feed = pd.read_parquet(PRATA / "feed_posts_limpos.parquet")
    tickets = pd.read_parquet(PRATA / "tickets_suporte_limpos.parquet")

    out = pd.DataFrame(index=ativos)
    out["seguidores"] = amizades.groupby("seguido_id").size()
    out["seguindo"] = amizades.groupby("seguidor_id").size()

    feed["data_hora_dt"] = pd.to_datetime(feed["data_hora_dt"])
    feed90 = feed.loc[
        feed["user_id"].isin(ativos) & (feed["data_hora_dt"] >= INICIO_90D)
    ]
    out["posts_90d"] = feed90.groupby("user_id").size()
    out["curtidas_90d"] = feed90.groupby("user_id")["curtidas"].sum()

    tickets["aberto_em_dt"] = pd.to_datetime(tickets["aberto_em_dt"])
    tickets90 = tickets.loc[
        tickets["user_id"].isin(ativos) & (tickets["aberto_em_dt"] >= INICIO_90D)
    ]
    out["tickets_90d"] = tickets90.groupby("user_id").size()
    out["tickets_cobranca_90d"] = (
        tickets90.assign(
            cobranca=tickets90["categoria_atendente"].eq("cobranca").astype(int)
        )
        .groupby("user_id")["cobranca"]
        .sum()
    )
    out = out.fillna(0.0)
    out["conexoes_sociais"] = out["seguidores"] + out["seguindo"]
    return out


def _agregar_receita(ativos: pd.Index, base: pd.DataFrame) -> pd.DataFrame:
    pagamentos = pd.read_parquet(PRATA / "pagamentos_limpos.parquet")
    pagamentos = pagamentos.loc[
        pagamentos["user_id"].isin(ativos)
        & pagamentos["status"].eq("aprovado")
        & ~pagamentos["flag_duplicata_aprovada_dia"]
        & (pd.to_datetime(pagamentos["data_hora_br"]) <= DATA_CORTE)
    ].copy()
    ultimo = (
        pagamentos.sort_values(["user_id", "data_hora_br"])
        .drop_duplicates("user_id", keep="last")
        .set_index("user_id")[["valor_num", "valor_liquido"]]
        .reindex(ativos)
    )
    plano_anual = base.set_index("user_id")["plano_atual"].eq("anual")
    canal = base.set_index("user_id")["canal_cobranca"]
    taxa = canal.map(
        {"app_store": 0.15, "google_play": 0.15, "cartao": 0.035, "pix_automatico": 0.0099}
    ).fillna(0.0)
    fallback_bruto = pd.Series(np.where(plano_anual, 299.90, 39.90), index=ativos)
    bruto = ultimo["valor_num"].fillna(fallback_bruto)
    liquido = ultimo["valor_liquido"].fillna(bruto * (1.0 - taxa))
    return pd.DataFrame(
        {
            "receita_bruta_mensal_equiv": np.where(plano_anual, bruto / 12.0, bruto),
            "receita_liquida_mensal_equiv": np.where(plano_anual, liquido / 12.0, liquido),
            "flag_pagamento_ausente": ultimo["valor_num"].isna().astype(int),
        },
        index=ativos,
    )


def construir_feature_store() -> pd.DataFrame:
    """Cria uma linha por pagante ativo, sem target ou informação de saída."""
    assinaturas = pd.read_parquet(PRATA / "assinaturas_limpas.parquet")
    base = assinaturas.loc[assinaturas["status_atual"].eq("ativa")].copy()
    if len(base) != POPULACAO_OFICIAL or not base["user_id"].is_unique:
        raise ValueError(
            f"População inválida: {len(base):,} linhas; esperado {POPULACAO_OFICIAL:,} usuários únicos."
        )
    base["inicio_dt"] = pd.to_datetime(base["inicio"])
    base["tenure_meses"] = (
        (DATA_CORTE - base["inicio_dt"]).dt.total_seconds() / (30.4375 * 86_400)
    ).clip(lower=0.0)
    base["plano_anual"] = base["plano_atual"].eq("anual").astype(int)
    base["canal_loja"] = base["canal_cobranca"].isin(["app_store", "google_play"]).astype(int)
    base["renovacao_desligada"] = base["renovacao_automatica"].eq("nao").astype(int)
    ativos = pd.Index(base["user_id"], name="user_id")

    usuarios = pd.read_parquet(PRATA / "usuarios_limpo.parquet").set_index("user_id")
    onboarding = pd.read_parquet(PRATA / "onboarding_limpo.parquet")
    onboarding["respondido_em"] = pd.to_datetime(onboarding["respondido_em"])
    onboarding = (
        onboarding.sort_values(["user_id", "respondido_em"])
        .drop_duplicates("user_id", keep="last")
        .set_index("user_id")
    )

    features = base.set_index("user_id")
    features = features.join(
        usuarios[["canal_aquisicao", "sistema", "relogio_conectado", "idade", "sexo", "uf"]],
        how="left",
    )
    features = features.join(
        onboarding[
            [
                "nivel",
                "dias_semana_pretendidos",
                "flag_onb_objetivo_preenchido",
                "flag_onb_nivel_preenchido",
                "flag_onb_dias_preenchido",
            ]
        ],
        how="left",
    )

    atividades, modalidade = _agregar_atividades(ativos)
    uso = _agregar_uso(ativos, features["inicio_dt"])
    social = _agregar_social_suporte(ativos)
    receita = _agregar_receita(ativos, base)
    features = features.join([atividades, uso, social, receita])
    features["modalidade_principal_90d"] = modalidade

    features["dias_semana_pretendidos"] = pd.to_numeric(
        features["dias_semana_pretendidos"], errors="coerce"
    )
    for col in [
        "flag_onb_objetivo_preenchido",
        "flag_onb_nivel_preenchido",
        "flag_onb_dias_preenchido",
    ]:
        features[col] = features[col].fillna(0).astype(int)

    proibidas = {
        "churn",
        "status_atual",
        "data_fim",
        "motivo_fim",
        "motivo_pesquisa_saida",
        "grupo",
        "abriu_push",
        "abriu_email",
        "clicou",
    }
    usadas_proibidas = proibidas.intersection(FEATURES_CLUSTER)
    if usadas_proibidas:
        raise ValueError(f"Features proibidas na clusterização: {sorted(usadas_proibidas)}")
    if len(features) != POPULACAO_OFICIAL or not features.index.is_unique:
        raise ValueError("JOIN multiplicou ou removeu assinantes da feature store.")
    features = features.drop(
        columns=["status_atual", "data_fim", "motivo_fim", "renovacao_automatica"],
        errors="ignore",
    )
    return features.reset_index()


def preparar_matriz(features: pd.DataFrame) -> tuple[np.ndarray, pd.DataFrame, StandardScaler]:
    """Imputa, limita extremos, transforma assimetrias e padroniza as features."""
    matriz = features[FEATURES_CLUSTER].copy()
    mediana_dias = float(matriz["dias_semana_pretendidos"].median())
    matriz["dias_semana_pretendidos"] = matriz["dias_semana_pretendidos"].fillna(mediana_dias)
    matriz = matriz.fillna(0.0).astype(float)

    for col in matriz.columns:
        if col not in {"delta_treinos_30_60", "regularidade_3m", "prop_ar_livre_3m", "prop_video_3m", "flag_onb_dias_preenchido", "plano_anual", "canal_loja"}:
            matriz[col] = matriz[col].clip(upper=matriz[col].quantile(0.99))
        if col in FEATURES_LOG:
            matriz[col] = np.log1p(matriz[col].clip(lower=0.0))

    scaler = StandardScaler()
    x = scaler.fit_transform(matriz)
    return x, matriz, scaler


def _estabilidade_kmeans(x: np.ndarray, labels_referencia: np.ndarray, k: int) -> float:
    rng = np.random.default_rng(RANDOM_STATE)
    scores: list[float] = []
    for repeticao in range(8):
        amostra = rng.choice(len(x), size=int(len(x) * 0.8), replace=False)
        modelo = KMeans(n_clusters=k, n_init=20, random_state=RANDOM_STATE + repeticao + 1)
        modelo.fit(x[amostra])
        scores.append(adjusted_rand_score(labels_referencia, modelo.predict(x)))
    return float(np.mean(scores))


def avaliar_solucoes(x: np.ndarray) -> tuple[pd.DataFrame, dict[int, KMeans]]:
    """Compara k=3 e k=4; k=5 é mantido apenas como diagnóstico."""
    linhas: list[dict[str, float | int | str]] = []
    modelos: dict[int, KMeans] = {}
    for k in (3, 4, 5):
        modelo = KMeans(n_clusters=k, n_init=50, random_state=RANDOM_STATE)
        labels = modelo.fit_predict(x)
        tamanhos = pd.Series(labels).value_counts(normalize=True)
        linhas.append(
            {
                "k": k,
                "elegivel_entrega": "sim" if k in (3, 4) else "diagnostico",
                "silhouette_amostra": silhouette_score(
                    x, labels, sample_size=min(5_000, len(x)), random_state=RANDOM_STATE
                ),
                "calinski_harabasz": calinski_harabasz_score(x, labels),
                "davies_bouldin": davies_bouldin_score(x, labels),
                "estabilidade_ari": _estabilidade_kmeans(x, labels, k),
                "menor_cluster_pct": tamanhos.min() * 100.0,
                "inercia": modelo.inertia_,
            }
        )
        modelos[k] = modelo
    return pd.DataFrame(linhas), modelos


def escolher_k(metricas: pd.DataFrame) -> int:
    """Escolhe entre 3 e 4 clusters, priorizando separação com tamanho mínimo de 5%."""
    elegiveis = metricas.loc[
        metricas["k"].isin([3, 4]) & metricas["menor_cluster_pct"].ge(5.0)
    ].copy()
    if elegiveis.empty:
        raise ValueError("Nenhuma solução com 3 ou 4 clusters possui tamanho mínimo de 5%.")
    return int(elegiveis.sort_values(["silhouette_amostra", "estabilidade_ari"], ascending=False).iloc[0]["k"])


def criar_perfil(features: pd.DataFrame) -> pd.DataFrame:
    agrupado = features.groupby("cluster_id", sort=True)
    perfil = agrupado.agg(
        n=("user_id", "size"),
        receita_liquida_mensal=("receita_liquida_mensal_equiv", "sum"),
        recencia_mediana_dias=("recencia_treino_dias", "median"),
        treinos_30d_mediana=("treinos_30d", "median"),
        treinos_90d_mediana=("treinos_90d", "median"),
        minutos_3m_mediana=("minutos_3m", "median"),
        regularidade_3m_media=("regularidade_3m", "mean"),
        diversidade_90d_mediana=("n_modalidades_90d", "median"),
        prop_ar_livre_3m_media=("prop_ar_livre_3m", "mean"),
        prop_video_3m_media=("prop_video_3m", "mean"),
        prop_treinos_dupla_90d_media=("prop_treinos_dupla_90d", "mean"),
        posts_90d_media=("posts_90d", "mean"),
        conexoes_sociais_mediana=("conexoes_sociais", "median"),
        tickets_90d_media=("tickets_90d", "mean"),
        tenure_mediana_meses=("tenure_meses", "median"),
        plano_anual_pct=("plano_anual", "mean"),
        canal_loja_pct=("canal_loja", "mean"),
        renovacao_desligada_pct=("renovacao_desligada", "mean"),
    ).reset_index()
    perfil["pct_base"] = perfil["n"] / len(features) * 100.0
    perfil["receita_liquida_media_cliente"] = (
        perfil["receita_liquida_mensal"] / perfil["n"]
    )
    for col in ["plano_anual_pct", "canal_loja_pct", "renovacao_desligada_pct"]:
        perfil[col] *= 100.0
    perfil["modalidade_principal"] = perfil["cluster_id"].map(
        features.groupby("cluster_id")["modalidade_principal_90d"].agg(
            lambda s: s.value_counts().index[0]
        )
    )
    return perfil


def atribuir_nomes(perfil: pd.DataFrame) -> dict[int, str]:
    """Nomes determinísticos baseados no comportamento dominante de cada cluster."""
    p = perfil.set_index("cluster_id")
    nomes: dict[int, str] = {}
    mais_inativo = int(p["recencia_mediana_dias"].idxmax())
    nomes[mais_inativo] = "Adormecidos sem hábito"
    restantes = [int(i) for i in p.index if int(i) not in nomes]
    if len(restantes) == 1:
        nomes[restantes[0]] = "Ativos consistentes"
    elif len(restantes) == 2:
        ar_livre = max(restantes, key=lambda i: p.loc[i, "prop_ar_livre_3m_media"])
        nomes[ar_livre] = "Ativos ao ar livre"
        video = next(i for i in restantes if i != ar_livre)
        nomes[video] = "Ativos guiados por vídeo"
    elif len(restantes) == 3:
        ar_livre = max(restantes, key=lambda i: p.loc[i, "prop_ar_livre_3m_media"])
        nomes[ar_livre] = "Ativos ao ar livre"
        restantes_sem_ar = [i for i in restantes if i != ar_livre]
        video = max(restantes_sem_ar, key=lambda i: p.loc[i, "prop_video_3m_media"])
        nomes[video] = "Ativos guiados por vídeo"
        outro = next(i for i in restantes_sem_ar if i != video)
        nomes[outro] = "Praticantes em formação"
    return nomes


def _plot_metricas(metricas: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    specs = [
        ("silhouette_amostra", "Silhouette", True),
        ("davies_bouldin", "Davies–Bouldin", False),
        ("estabilidade_ari", "Estabilidade (ARI)", True),
    ]
    for ax, (col, titulo, maior_melhor) in zip(axes, specs):
        cores = ["#146C94" if k in (3, 4) else "#AAB7B8" for k in metricas["k"]]
        ax.bar(metricas["k"].astype(str), metricas[col], color=cores)
        ax.set(title=titulo, xlabel="Número de clusters (k)")
        ax.spines[["top", "right"]].set_visible(False)
        elegiveis = metricas.loc[metricas["k"].isin([3, 4])]
        melhor = elegiveis.loc[
            elegiveis[col].idxmax() if maior_melhor else elegiveis[col].idxmin(), "k"
        ]
        ax.text(0.02, 0.94, f"melhor elegível: k={int(melhor)}", transform=ax.transAxes, va="top")
    fig.suptitle("Validação estatística das soluções de segmentação", fontweight="bold")
    fig.text(0.5, 0.01, "k=5 é exibido em cinza apenas como diagnóstico; a entrega exige 3 a 4 segmentos.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(SAIDAS / "segmentacao_validacao_k.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def _plot_heatmap(features: pd.DataFrame, x: np.ndarray) -> pd.DataFrame:
    z = pd.DataFrame(x, columns=FEATURES_CLUSTER)
    z["segmento"] = features["segmento"].to_numpy()
    centroides = z.groupby("segmento").mean().sort_index()
    fig, ax = plt.subplots(figsize=(14, 4.8))
    limite = max(1.5, float(np.nanmax(np.abs(centroides.to_numpy()))))
    im = ax.imshow(centroides.to_numpy(), cmap="RdBu_r", vmin=-limite, vmax=limite, aspect="auto")
    ax.set_xticks(range(len(FEATURES_CLUSTER)), [PERFIS_LABELS[c] for c in FEATURES_CLUSTER], rotation=55, ha="right")
    ax.set_yticks(range(len(centroides)), centroides.index)
    ax.set_title("Perfil relativo dos segmentos (z-score das features)", fontweight="bold")
    fig.colorbar(im, ax=ax, label="Abaixo ← média da base → Acima")
    fig.tight_layout()
    fig.savefig(SAIDAS / "segmentacao_heatmap_perfis.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return centroides.reset_index()


def _plot_tamanho_receita(perfil: pd.DataFrame) -> None:
    data = perfil.sort_values("n", ascending=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    axes[0].barh(data["segmento"], data["n"], color="#146C94")
    axes[0].set(title="Clientes por segmento", xlabel="Assinantes ativos")
    axes[1].barh(data["segmento"], data["receita_liquida_mensal"] / 1_000, color="#F39C12")
    axes[1].set(title="Receita líquida mensal equivalente estimada", xlabel="R$ mil/mês")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(SAIDAS / "segmentacao_tamanho_receita.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def _plot_pca(features: pd.DataFrame, x: np.ndarray) -> pd.DataFrame:
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    coords = pca.fit_transform(x)
    rng = np.random.default_rng(RANDOM_STATE)
    idx = rng.choice(len(features), size=min(5_000, len(features)), replace=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    for segmento in sorted(features["segmento"].unique()):
        mask = features.iloc[idx]["segmento"].eq(segmento).to_numpy()
        ax.scatter(coords[idx][mask, 0], coords[idx][mask, 1], s=9, alpha=0.35, label=segmento)
    ax.set(
        title="Projeção bidimensional dos segmentos (amostra)",
        xlabel=f"PC1 ({pca.explained_variance_ratio_[0]:.1%})",
        ylabel=f"PC2 ({pca.explained_variance_ratio_[1]:.1%})",
    )
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(SAIDAS / "segmentacao_pca.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return pd.DataFrame(
        {
            "componente": ["PC1", "PC2"],
            "variancia_explicada": pca.explained_variance_ratio_,
        }
    )


def gerar_relatorio(
    metricas: pd.DataFrame,
    k_escolhido: int,
    perfil: pd.DataFrame,
    criterios: pd.DataFrame,
) -> None:
    m = metricas.loc[metricas["k"].eq(k_escolhido)].iloc[0]
    linhas = [
        "# Segmentação dos Pagantes Ativos — Etapa 4",
        "> Receita mensal equivalente estimada, não faturamento ou receita em risco. Acessibilidade depende de elegibilidade de contato. Consulte [a validação suplementar](validacao_semana5.md) para sensibilidade em k=2…8 e limitações.",
        "",
        "**Data de corte:** 30/09/2026",
        f"**População:** {POPULACAO_OFICIAL:,} pagantes ativos".replace(",", "."),
        "**Método:** K-Means sobre atributos comportamentais, sociais, contratuais e de necessidade; sem churn ou informação de saída.",
        "",
        "## 1. Escolha do número de segmentos",
        "",
        metricas.to_markdown(index=False, floatfmt=".3f"),
        "",
        "![Validação de k](segmentacao_validacao_k.png)",
        "",
        f"A solução selecionada possui **k={k_escolhido}**, silhouette amostral de **{m['silhouette_amostra']:.3f}**, "
        f"Davies–Bouldin de **{m['davies_bouldin']:.3f}**, estabilidade média ARI de **{m['estabilidade_ari']:.3f}** "
        f"e menor segmento com **{m['menor_cluster_pct']:.1f}%** da base.",
        "",
        "## 2. Perfil dos segmentos",
        "",
        perfil.to_markdown(index=False, floatfmt=".2f"),
        "",
        "![Perfis relativos](segmentacao_heatmap_perfis.png)",
        "",
        "![Tamanho e receita](segmentacao_tamanho_receita.png)",
        "",
        "![Projeção PCA](segmentacao_pca.png)",
        "",
        "## 3. Validação nos cinco critérios de negócio",
        "",
        criterios.to_markdown(index=False),
        "",
        "## 4. Regras de governança",
        "",
        "- A clusterização não usa churn, status de saída, pesquisa de saída, campanha, abertura, clique ou fatos posteriores ao corte.",
        "- Idade, sexo, UF e outras variáveis demográficas são mantidas apenas para auditoria de representação; não determinam os grupos.",
        "- `renovacao_automatica` é exibida somente após a formação dos clusters e não entra na distância do algoritmo.",
        "- Os nomes são interpretações executivas de centroides e não estereótipos individuais.",
        "- Segmentos descrevem semelhança; não demonstram causalidade nem substituem o modelo de risco da Semana 10.",
    ]
    (SAIDAS / "segmentacao_etapa4.md").write_text("\n".join(linhas), encoding="utf-8")


def main() -> None:
    OURO.mkdir(parents=True, exist_ok=True)
    SAIDAS.mkdir(parents=True, exist_ok=True)
    TABELAS.mkdir(parents=True, exist_ok=True)

    features = construir_feature_store()
    x, matriz_tratada, _ = preparar_matriz(features)
    metricas, modelos = avaliar_solucoes(x)
    k_escolhido = escolher_k(metricas)
    features["cluster_id"] = modelos[k_escolhido].labels_

    perfil_inicial = criar_perfil(features)
    nomes = atribuir_nomes(perfil_inicial)
    features["segmento"] = features["cluster_id"].map(nomes)
    perfil = criar_perfil(features)
    perfil["segmento"] = perfil["cluster_id"].map(nomes)
    perfil = perfil[
        ["cluster_id", "segmento"] + [c for c in perfil.columns if c not in {"cluster_id", "segmento"}]
    ]

    criterios = pd.DataFrame(
        [
            {"criterio": "Mensurável", "avaliacao": "Atende", "evidencia": "Tamanho, participação e receita calculados para os 14.753 ativos."},
            {"criterio": "Substancial", "avaliacao": "Atende", "evidencia": f"Menor grupo representa {perfil['pct_base'].min():.1f}% da base."},
            {"criterio": "Diferenciável", "avaliacao": "Atende com ressalva", "evidencia": f"Silhouette={metricas.loc[metricas.k.eq(k_escolhido), 'silhouette_amostra'].iloc[0]:.3f}; interpretar junto aos centroides."},
            {"criterio": "Acessível", "avaliacao": "Condicional", "evidencia": "Canal de cobrança não comprova elegibilidade ou permissão de contato; verificar antes do piloto."},
            {"criterio": "Acionável", "avaliacao": "Atende preliminarmente", "evidencia": "Hipóteses e piloto documentados no relatório executivo; eficácia ainda não demonstrada."},
        ]
    )

    features.to_parquet(OURO / "features_segmentacao_ativos_set2026.parquet", index=False)
    features[["user_id", "cluster_id", "segmento"]].to_parquet(
        OURO / "segmentos_ativos_set2026.parquet", index=False
    )
    metricas.to_csv(TABELAS / "metricas_clusterizacao.csv", index=False)
    perfil.to_csv(TABELAS / "perfil_segmentos.csv", index=False)
    criterios.to_csv(TABELAS / "criterios_segmentacao.csv", index=False)

    _plot_metricas(metricas)
    centroides = _plot_heatmap(features, x)
    centroides.to_csv(TABELAS / "centroides_segmentos.csv", index=False)
    _plot_tamanho_receita(perfil)
    pca_info = _plot_pca(features, x)
    pca_info.to_csv(TABELAS / "pca_segmentacao.csv", index=False)
    gerar_relatorio(metricas, k_escolhido, perfil, criterios)

    metadados = {
        "data_corte": str(DATA_CORTE),
        "populacao": len(features),
        "k_escolhido": k_escolhido,
        "features_cluster": FEATURES_CLUSTER,
        "features_excluidas_governanca": [
            "churn",
            "status_atual",
            "data_fim",
            "motivo_fim",
            "pesquisa_saida",
            "campanha",
            "idade",
            "sexo",
            "uf",
            "renovacao_automatica",
        ],
        "nomes_segmentos": {str(k): v for k, v in nomes.items()},
    }
    (TABELAS / "metadados_segmentacao.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Feature store: {len(features):,} usuários; k={k_escolhido}.")
    print(perfil.to_string(index=False))


if __name__ == "__main__":
    main()
