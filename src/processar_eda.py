import sys
import os
import re
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("Iniciando processamento da EDA Vitaliza (Sem Vazamento Pós-Desfecho)...")

DATA_CORTE = pd.Timestamp("2026-09-30 23:59:59")

# 1. Carregar usuarios (com higienização demográfica e de casing)
df_usr = pd.read_csv("dados/brutos/usuarios.csv")
contas_internas = set(
    df_usr[df_usr["email"].str.endswith("@vitaliza.com.br", na=False)]["user_id"]
)
df_usr["data_cadastro_dt"] = pd.to_datetime(df_usr["data_cadastro"], errors="coerce")
df_usr["data_nascimento_dt"] = pd.to_datetime(df_usr["data_nascimento"], errors="coerce")
mask_nasc_invalido = (df_usr["data_nascimento_dt"].dt.year <= 1900) | (
    df_usr["data_nascimento_dt"].dt.year >= 2026
)
df_usr.loc[mask_nasc_invalido, "data_nascimento_dt"] = pd.NaT
df_usr["idade"] = (
    (DATA_CORTE - df_usr["data_nascimento_dt"]).dt.total_seconds() / (365.25 * 86400)
).astype(float)
df_usr["sexo"] = (
    df_usr["sexo"]
    .astype(str)
    .str.lower()
    .map({"f": "F", "fem": "F", "feminino": "F", "m": "M", "masc": "M", "masculino": "M"})
    .fillna(df_usr["sexo"])
)
df_usr["sistema"] = df_usr["sistema"].astype(str).str.lower()
df_usr["tem_relogio"] = (df_usr["relogio_conectado"] != "nenhum").astype(int)
df_usr["cep_prefixo_str"] = (
    df_usr["cep_prefixo"].fillna(0).astype(int).astype(str).str.zfill(3)
)

# 2. Carregar assinaturas (excluindo as 60 contas internas / cortesia)
df_ass = pd.read_csv("dados/brutos/assinaturas.csv")
df_ass = df_ass[
    (~df_ass["user_id"].isin(contas_internas)) & (df_ass["plano_atual"] != "cortesia")
].copy()

df_ass["inicio_dt"] = pd.to_datetime(df_ass["inicio"])
df_ass["data_fim_dt"] = pd.to_datetime(df_ass["data_fim"])

# Target histórico: Churn até 30/09/2026
df_ass["churn"] = df_ass["status_atual"].isin(["expirada", "reembolsada"]).astype(int)

# Data de desfecho de cada assinatura (data_fim para cancelados; 30/09/2026 para ativos)
df_ass["data_desfecho"] = df_ass["data_fim_dt"].fillna(DATA_CORTE)
df_ass[" data_desfecho"] = df_ass["data_desfecho"].clip(upper=DATA_CORTE)
df_ass["data_desfecho"] = df_ass["data_desfecho"].clip(upper=DATA_CORTE)
df_ass["mes_inicio"] = df_ass["inicio_dt"].dt.strftime("%Y-%m")
df_ass["mes_desfecho"] = df_ass["data_desfecho"].dt.strftime("%Y-%m")

df_ass["lifetime_dias"] = (
    (df_ass["data_desfecho"] - df_ass["inicio_dt"]).dt.total_seconds() / 86400.0
).clip(lower=1.0)
df_ass["lifetime_meses"] = np.floor(df_ass["lifetime_dias"] / 30.0).astype(int)
# Número de meses de vigência efetiva (mínimo 1 mês para cálculo de taxas mensais justas entre 2025 e 2026)
df_ass["meses_vigencia"] = np.maximum(1.0, np.ceil(df_ass["lifetime_dias"] / 30.4375))


def categorizar_lifetime(m):
    if m <= 0:
        return "0 meses (<30d)"
    elif m == 1:
        return "1 mes (30-59d)"
    elif m == 2:
        return "2 meses (60-89d)"
    elif m == 3:
        return "3 meses (90-119d)"
    elif m in [4, 5]:
        return "4-5 meses"
    else:
        return "6+ meses"


df_ass["faixa_lifetime"] = df_ass["lifetime_meses"].apply(categorizar_lifetime)
df_ass["grupo_canal"] = df_ass["canal_cobranca"].apply(
    lambda c: "Lojas (Apple/Google)"
    if c in ["app_store", "google_play"]
    else "Web (Cartao/Pix)"
)

print(f"Total assinaturas pagas: {len(df_ass):,} | Churn: {df_ass['churn'].mean():.2%}")

# Mapa rápido de janela de vigência por user_id
janela_user = df_ass[["user_id", "inicio_dt", "data_desfecho", "mes_inicio", "mes_desfecho", "meses_vigencia"]].copy()

# 3. Carregar Onboarding (Dimensão 1 — Completude)
df_onb = pd.read_csv("dados/brutos/onboarding.csv")


def extrair_dias(val):
    if pd.isna(val):
        return np.nan
    s = str(val).lower()
    m = re.search(r"(\d+)", s)
    if m:
        return float(m.group(1))
    return np.nan


df_onb["dias_semana_pretendidos"] = df_onb["dias_por_semana"].apply(extrair_dias)
df_onb["flag_onb_objetivo_preenchido"] = (
    df_onb["objetivo_texto"].fillna("").astype(str).str.strip() != ""
).astype(int)
df_onb["flag_onb_nivel_preenchido"] = df_onb["nivel"].notna().astype(int)
df_onb["flag_onb_dias_preenchido"] = df_onb["dias_por_semana"].notna().astype(int)
onb_user = df_onb.drop_duplicates(subset=["user_id"]).set_index("user_id")[
    [
        "nivel",
        "dias_semana_pretendidos",
        "como_conheceu",
        "flag_onb_objetivo_preenchido",
        "flag_onb_nivel_preenchido",
        "flag_onb_dias_preenchido",
    ]
]


# 4. Carregar eventos de assinatura
def harmonizar_data(dt_series):
    is_utc = dt_series.str.endswith("Z", na=False)
    s_utc = (
        pd.to_datetime(dt_series[is_utc], utc=True)
        .dt.tz_convert("America/Sao_Paulo")
        .dt.tz_localize(None)
    )
    s_br = pd.to_datetime(dt_series[~is_utc])
    res = pd.Series(index=dt_series.index, dtype="datetime64[ns]")
    res[is_utc] = s_utc
    res[~is_utc] = s_br
    return res


df_ev = pd.read_csv("dados/brutos/eventos_assinatura.csv")
df_ev["data_hora_dt"] = harmonizar_data(df_ev["data_hora"])
df_ev = df_ev[df_ev["data_hora_dt"] <= DATA_CORTE].copy()

ev_user = df_ev.groupby("user_id").agg(
    total_renovacoes=("evento", lambda s: (s == "renovacao").sum()),
    desligou_renovacao=(
        "evento",
        lambda s: (s == "renovacao_automatica_desligada").sum() > 0,
    ),
    religou_renovacao=(
        "evento",
        lambda s: (s == "renovacao_automatica_religada").sum() > 0,
    ),
    teve_carencia=("evento", lambda s: (s == "periodo_carencia").sum() > 0),
    cancelou_web=("evento", lambda s: (s == "cancelamento_web").sum() > 0),
    teve_chargeback=("evento", lambda s: (s == "chargeback").sum() > 0),
)

# 5. Carregar pagamentos
df_pag = pd.read_csv("dados/brutos/pagamentos.csv", low_memory=False)
df_pag["data_hora_dt"] = harmonizar_data(df_pag["data_hora"])
df_pag = df_pag[df_pag["data_hora_dt"] <= DATA_CORTE].copy()


def limpar_valor(v):
    if pd.isna(v):
        return 0.0
    s = str(v).replace("R$", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except:
        return 0.0


df_pag["valor_num"] = df_pag["valor"].apply(limpar_valor)

df_pag_aprov = df_pag[df_pag["status"] == "aprovado"].copy()
df_pag_aprov["data_dia"] = df_pag_aprov["data_hora_dt"].dt.date
df_pag_aprov = df_pag_aprov.sort_values(["user_id", "data_hora_dt"])
duplicadas_mask = df_pag_aprov.duplicated(
    subset=["user_id", "valor_num", "data_dia"], keep="first"
)
df_pag_aprov_limpo = df_pag_aprov[~duplicadas_mask].copy()

taxas = {
    "app_store": 0.15,
    "google_play": 0.15,
    "cartao": 0.035,
    "pix_automatico": 0.0099,
}
df_pag_aprov_limpo["taxa"] = df_pag_aprov_limpo["metodo"].map(taxas).fillna(0.0)
df_pag_aprov_limpo["valor_liq"] = df_pag_aprov_limpo["valor_num"] * (
    1 - df_pag_aprov_limpo["taxa"]
)

pag_user = df_pag_aprov_limpo.groupby("user_id").agg(
    total_pago_bruto=("valor_num", "sum"),
    total_pago_liq=("valor_liq", "sum"),
    qtd_pagamentos=("pagamento_id", "count"),
    ticket_medio_transacao=("valor_num", "mean"),
)

pag_falhas = (
    df_pag[df_pag["status"] == "recusado"]
    .groupby("user_id")
    .size()
    .rename("pagamentos_recusados")
)

# 6. Carregar uso mensal RESTRITO À VIGÊNCIA DE CADA ASSINATURA (Sem vazamento pós-saída!)
df_uso = pd.read_csv("dados/brutos/uso_mensal.csv")
df_uso = df_uso[df_uso["mes"] <= "2026-09"].copy()
df_uso_vig = df_uso.merge(janela_user, on="user_id", how="inner")
# Filtrar estritamente meses dentro da vigência da assinatura (mes_inicio <= mes <= mes_desfecho)
df_uso_vig = df_uso_vig[
    (df_uso_vig["mes"] >= df_uso_vig["mes_inicio"])
    & (df_uso_vig["mes"] <= df_uso_vig["mes_desfecho"])
].copy()

df_uso_ativo = df_uso_vig[df_uso_vig["minutos"] > 0]

uso_user = df_uso_vig.groupby("user_id").agg(
    meses_registrados=("mes", "count"),
    meses_com_uso=("minutos", lambda s: (s > 0).sum()),
    total_atividades_mensal=("atividades", "sum"),
    total_ar_livre_mensal=("atividades_ar_livre", "sum"),
    total_video_mensal=("atividades_video", "sum"),
    total_minutos_mensal=("minutos", "sum"),
    total_dias_ativos=("dias_ativos", "sum"),
    total_sessoes_app=("sessoes_app", "sum"),
)

uso_user_ativo = df_uso_ativo.groupby("user_id").agg(
    media_minutos_mes_ativo=("minutos", "mean"),
    media_atividades_mes_ativo=("atividades", "mean"),
)
uso_user = uso_user.join(uso_user_ativo, how="left")

# 7. Carregar atividades detalhadas limpas RESTRITAS ATÉ O DESFECHO DE CADA ASSINATURA
if os.path.exists("dados/processados/atividades_limpas.parquet"):
    df_atv = pd.read_parquet("dados/processados/atividades_limpas.parquet")
else:
    from limpeza_qualidade_dados import auditar_e_limpar_atividades
    df_atv = auditar_e_limpar_atividades()

df_atv = df_atv.merge(
    janela_user[["user_id", "inicio_dt", "data_desfecho"]], on="user_id", how="inner"
)
# Garantir apenas treinos até a data de desfecho da assinatura
df_atv = df_atv[df_atv["inicio_dt_br"] <= df_atv["data_desfecho"]].copy()
df_atv["em_dupla"] = (df_atv["treino_com"].fillna("").str.strip() != "").astype(int)

# Janelas relativas ao desfecho (D-30 e D-60 antes de sair ou antes do corte 30/09 para ativos):
# Sem vazamento pós-saída!
dias_ate_desfecho = (
    df_atv["data_desfecho"] - df_atv["inicio_dt_br"]
).dt.total_seconds() / 86400.0
df_atv["treino_ultimos_30d"] = ((dias_ate_desfecho >= 0) & (dias_ate_desfecho <= 30)).astype(int)
df_atv["treino_31_a_60d"] = ((dias_ate_desfecho > 30) & (dias_ate_desfecho <= 60)).astype(int)
df_atv["minutos_ultimos_30d"] = np.where(df_atv["treino_ultimos_30d"] == 1, df_atv["duracao_min"], 0.0)

atv_user = df_atv.groupby("user_id").agg(
    total_treinos_log=("atividade_id", "count"),
    atividades_ultimos_30d=("treino_ultimos_30d", "sum"),
    atividades_31_a_60d=("treino_31_a_60d", "sum"),
    minutos_ultimos_30d=("minutos_ultimos_30d", "sum"),
    n_modalidades_distintas=("tipo_canonico", "nunique"),
    duracao_mediana=("duracao_min", "median"),
    duracao_iqr=("duracao_min", lambda s: s.quantile(0.75) - s.quantile(0.25)),
    distancia_mediana=("distancia_km", "median"),
    distancia_iqr=("distancia_km", lambda s: s.quantile(0.75) - s.quantile(0.25)),
    treinos_em_dupla=("em_dupla", "sum"),
    prop_treinos_dupla=("em_dupla", "mean"),
    prop_gps_ok=("gps_ok", "mean"),
)

# 8. Carregar Amizades e Comunidade (até data_desfecho da assinatura)
df_amiz = pd.read_csv("dados/brutos/amizades.csv")
df_amiz["desde_dt"] = pd.to_datetime(df_amiz["desde"])
df_amiz = df_amiz[df_amiz["desde_dt"] <= DATA_CORTE].copy()

df_amiz_segd = df_amiz.merge(
    janela_user[["user_id", "data_desfecho"]], left_on="seguido_id", right_on="user_id", how="inner"
)
df_amiz_segd = df_amiz_segd[df_amiz_segd["desde_dt"] <= df_amiz_segd["data_desfecho"]]
seguidores = df_amiz_segd.groupby("seguido_id").size().rename("num_seguidores")

df_amiz_segr = df_amiz.merge(
    janela_user[["user_id", "data_desfecho"]], left_on="seguidor_id", right_on="user_id", how="inner"
)
df_amiz_segr = df_amiz_segr[df_amiz_segr["desde_dt"] <= df_amiz_segr["data_desfecho"]]
seguindo = df_amiz_segr.groupby("seguidor_id").size().rename("num_seguindo")

# 9. Feed posts (até data_desfecho da assinatura)
df_feed = pd.read_csv("dados/brutos/feed_posts.csv")
df_feed["data_hora_dt"] = pd.to_datetime(df_feed["data_hora"])
df_feed = df_feed[df_feed["data_hora_dt"] <= DATA_CORTE].copy()
df_feed = df_feed.merge(
    janela_user[["user_id", "data_desfecho"]], on="user_id", how="inner"
)
df_feed = df_feed[df_feed["data_hora_dt"] <= df_feed["data_desfecho"]].copy()

feed_user = df_feed.groupby("user_id").agg(
    total_posts=("post_id", "count"), total_curtidas=("curtidas", "sum")
)

# 10. Suporte (até data_desfecho da assinatura)
df_sup = pd.read_csv("dados/brutos/tickets_suporte.csv")
df_sup["aberto_em_dt"] = pd.to_datetime(df_sup["aberto_em"])
df_sup = df_sup[df_sup["aberto_em_dt"] <= DATA_CORTE].copy()
df_sup = df_sup.merge(
    janela_user[["user_id", "data_desfecho"]], on="user_id", how="inner"
)
df_sup = df_sup[df_sup["aberto_em_dt"] <= df_sup["data_desfecho"]].copy()

sup_user = df_sup.groupby("user_id").agg(
    total_tickets=("ticket_id", "count"),
    tickets_cobranca=("categoria_atendente", lambda s: (s == "cobranca").sum()),
    tickets_tecnicos=("categoria_atendente", lambda s: (s == "tecnico").sum()),
)

# 11. Campanha Agosto 2026
df_camp = pd.read_csv("dados/brutos/campanha_ago26.csv")
camp_user = df_camp.drop_duplicates(subset=["user_id"]).set_index("user_id")[
    ["abriu_push", "abriu_email", "clicou"]
]

# 12. Pesquisa de Saída
df_pesq = pd.read_csv("dados/brutos/pesquisa_saida.csv")
pesq_user = (
    df_pesq.drop_duplicates(subset=["user_id"])
    .set_index("user_id")["motivo_principal"]
    .rename("motivo_pesquisa_saida")
)

# CONSOLIDAÇÃO DA TABELA MASTER
print("Consolidando tabela analítica master...")
df_master = df_ass.merge(df_usr, on="user_id", how="left")
df_master = df_master.merge(onb_user, on="user_id", how="left")
df_master = df_master.merge(ev_user, on="user_id", how="left")
df_master = df_master.merge(pag_user, on="user_id", how="left")
df_master = df_master.merge(pag_falhas, on="user_id", how="left")
df_master = df_master.merge(uso_user, on="user_id", how="left")
df_master = df_master.merge(atv_user, on="user_id", how="left")
df_master = df_master.merge(seguidores, left_on="user_id", right_index=True, how="left")
df_master = df_master.merge(seguindo, left_on="user_id", right_index=True, how="left")
df_master = df_master.merge(feed_user, on="user_id", how="left")
df_master = df_master.merge(sup_user, on="user_id", how="left")
df_master = df_master.merge(camp_user, on="user_id", how="left")
df_master = df_master.merge(pesq_user, on="user_id", how="left")

# Preenchimento de nulos para contagens e métricas
fill_zero_cols = [
    "total_renovacoes",
    "desligou_renovacao",
    "religou_renovacao",
    "teve_carencia",
    "cancelou_web",
    "teve_chargeback",
    "total_pago_bruto",
    "total_pago_liq",
    "qtd_pagamentos",
    "pagamentos_recusados",
    "meses_registrados",
    "meses_com_uso",
    "total_atividades_mensal",
    "total_ar_livre_mensal",
    "total_video_mensal",
    "total_minutos_mensal",
    "total_dias_ativos",
    "total_sessoes_app",
    "media_minutos_mes_ativo",
    "media_atividades_mes_ativo",
    "total_treinos_log",
    "atividades_ultimos_30d",
    "atividades_31_a_60d",
    "minutos_ultimos_30d",
    "n_modalidades_distintas",
    "treinos_em_dupla",
    "num_seguidores",
    "num_seguindo",
    "total_posts",
    "total_curtidas",
    "total_tickets",
    "tickets_cobranca",
    "tickets_tecnicos",
    "flag_onb_objetivo_preenchido",
    "flag_onb_nivel_preenchido",
    "flag_onb_dias_preenchido",
]

for col in fill_zero_cols:
    if col in df_master.columns:
        df_master[col] = df_master[col].fillna(0)

# Calcular médias mensais na vigência da assinatura (harmonizando 2025 e 2026 sem vazamento pós-saída e sem viés de tempo acumulado!)
df_master["media_atividades_mes"] = (
    df_master["total_atividades_mensal"] / df_master["meses_vigencia"]
)
df_master["media_minutos_mes"] = (
    df_master["total_minutos_mensal"] / df_master["meses_vigencia"]
)
df_master["media_dias_ativos_mes"] = (
    df_master["total_dias_ativos"] / df_master["meses_vigencia"]
)
df_master["media_sessoes_mes"] = (
    df_master["total_sessoes_app"] / df_master["meses_vigencia"]
)
df_master["media_ar_livre_mes"] = (
    df_master["total_ar_livre_mensal"] / df_master["meses_vigencia"]
)
df_master["media_video_mes"] = (
    df_master["total_video_mensal"] / df_master["meses_vigencia"]
)
df_master["media_posts_mes"] = (
    df_master["total_posts"] / df_master["meses_vigencia"]
)
df_master["media_curtidas_mes"] = (
    df_master["total_curtidas"] / df_master["meses_vigencia"]
)
df_master["media_treinos_dupla_mes"] = (
    df_master["treinos_em_dupla"] / df_master["meses_vigencia"]
)
# Ticket mensal equivalente (R$/mês): divide por 12 para plano anual (R$ 24,99 ou R$ 19,99 c/ cupom) e mantém valor mensal (R$ 34,90 ou R$ 39,90) para plano mensal
df_master["receita_bruta_mensal"] = np.where(
    df_master["plano_atual"] == "anual",
    df_master["ticket_medio_transacao"].fillna(299.90) / 12.0,
    df_master["ticket_medio_transacao"].fillna(39.90),
)
df_master["eh_plano_anual"] = (df_master["plano_atual"] == "anual").astype(int)
df_master["eh_canal_loja"] = (
    df_master["canal_cobranca"].isin(["app_store", "google_play"]).astype(int)
)
df_master["prop_meses_ativos_vigencia"] = (
    df_master["meses_com_uso"] / df_master["meses_vigencia"]
).clip(upper=1.0)
# Razão de aceleração/desaceleração no último mês antes do cancelamento vs média da vigência
df_master["razao_uso_ultimo_mes"] = df_master["atividades_ultimos_30d"] / (
    df_master["media_atividades_mes"] + 1.0
)

# Salvar feature store processada
output_parquet = "dados/processados/features_eda_corte_set2026.parquet"
df_master.to_parquet(output_parquet, index=False)
print(
    f"Feature store salva com sucesso em: {output_parquet} com {len(df_master):,} registros e {df_master.shape[1]} colunas."
)
