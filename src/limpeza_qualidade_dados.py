"""
Pipeline Oficial de Limpeza e Auditoria das 5 Dimensões da Qualidade de Dados
Projeto Vitaliza — Módulo 2 MBA IA e Dados (Inteli)
Referência: Aula 2 de Tecnologia (Prof. Cesar Almiñana) + Dicionário de Dados
"""

import os
import re
import sys
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAW_DIR = "dados/brutos"
PROC_DIR = "dados/processados"
os.makedirs(PROC_DIR, exist_ok=True)

DATA_CORTE = pd.Timestamp("2026-09-30 23:59:59")

# Mapeamento canônico das 7 modalidades (Consistência: 11 rótulos -> 7 modalidades)
MAPA_MODALIDADES = {
    "corrida": "corrida",
    "run": "corrida",
    "caminhada": "caminhada",
    "walk": "caminhada",
    "forca": "forca",
    "strength": "forca",
    "pedal": "pedal",
    "ride": "pedal",
    "yoga": "yoga",
    "hiit": "hiit",
    "funcional": "funcional",
}

ROTULOS_INGLES = {"run", "walk", "strength", "ride"}

TAXAS_CANAL = {
    "app_store": 0.15,
    "google_play": 0.15,
    "cartao": 0.035,
    "pix_automatico": 0.0099,
}


def harmonizar_data_utc_para_br(dt_series: pd.Series) -> pd.Series:
    """Converte strings ISO terminadas em 'Z' (UTC) para Horário de Brasília (UTC-3, sem tz)."""
    s_str = dt_series.astype(str)
    is_utc = s_str.str.endswith("Z", na=False)
    res = pd.Series(index=dt_series.index, dtype="datetime64[ns]")
    if is_utc.any():
        res.loc[is_utc] = (
            pd.to_datetime(s_str[is_utc], utc=True)
            .dt.tz_convert("America/Sao_Paulo")
            .dt.tz_localize(None)
        )
    if (~is_utc).any():
        res.loc[~is_utc] = pd.to_datetime(s_str[~is_utc], errors="coerce")
    return res


def limpar_valor_monetario(s: pd.Series) -> pd.Series:
    """Converte strings monetárias ('R$ 39,90' ou '39.90') para float."""
    return (
        s.astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )


def auditar_populacao_e_contas_internas():
    print("=" * 75)
    print("0. POPULAÇÃO OFICIAL NO CORTE (30/09/2026) E CONTAS INTERNAS")
    print("=" * 75)
    df_usr = pd.read_csv(os.path.join(RAW_DIR, "usuarios.csv"))
    df_ass = pd.read_csv(os.path.join(RAW_DIR, "assinaturas.csv"))

    contas_internas = set(
        df_usr[df_usr["email"].str.endswith("@vitaliza.com.br", na=False)]["user_id"]
    )
    ativas_brutas = df_ass[df_ass["status_atual"] == "ativa"]
    ativas_pagantes = ativas_brutas[
        (~ativas_brutas["user_id"].isin(contas_internas))
        & (ativas_brutas["plano_atual"] != "cortesia")
    ]
    ativas_renov_ligada = ativas_pagantes[
        ativas_pagantes["renovacao_automatica"] == "sim"
    ]

    print(f"Total contas em usuarios.csv              : {len(df_usr):,}")
    print(f"Contas internas (@vitaliza.com.br)        : {len(contas_internas):,}")
    print(f"Assinaturas ativas brutas (assinaturas)   : {len(ativas_brutas):,}")
    print(f"Assinantes pagantes ativos (oficial)      : {len(ativas_pagantes):,}")
    print(f"Pagantes ativos c/ renovação ligada       : {len(ativas_renov_ligada):,}")

    # Higienizar usuarios.csv e salvar usuarios_limpo.csv e assinaturas_limpas.csv
    df_usr_clean = df_usr.copy()
    df_usr_clean["flag_conta_interna"] = df_usr_clean["user_id"].isin(contas_internas).astype(int)
    df_usr_clean["data_cadastro_dt"] = pd.to_datetime(df_usr_clean["data_cadastro"], errors="coerce")
    df_usr_clean["data_nascimento_dt"] = pd.to_datetime(df_usr_clean["data_nascimento"], errors="coerce")
    mask_nasc_inv = (df_usr_clean["data_nascimento_dt"].dt.year <= 1900) | (df_usr_clean["data_nascimento_dt"].dt.year >= 2026)
    df_usr_clean.loc[mask_nasc_inv, "data_nascimento_dt"] = pd.NaT
    df_usr_clean["idade"] = ((DATA_CORTE - df_usr_clean["data_nascimento_dt"]).dt.total_seconds() / (365.25 * 86400)).round(1)
    df_usr_clean["sexo"] = df_usr_clean["sexo"].astype(str).str.lower().map({"f": "F", "fem": "F", "feminino": "F", "m": "M", "masc": "M", "masculino": "M"}).fillna(df_usr_clean["sexo"])
    df_usr_clean["sistema"] = df_usr_clean["sistema"].astype(str).str.lower()
    df_usr_clean["cep_prefixo"] = df_usr_clean["cep_prefixo"].fillna(0).astype(int).astype(str).str.zfill(3)
    df_usr_clean.loc[df_usr["cep_prefixo"].isna(), "cep_prefixo"] = np.nan
    df_usr_clean.to_csv(os.path.join(PROC_DIR, "usuarios_limpo.csv"), index=False, encoding="utf-8")

    df_ass_clean = df_ass[(~df_ass["user_id"].isin(contas_internas)) & (df_ass["plano_atual"] != "cortesia")].copy()
    df_ass_clean.to_csv(os.path.join(PROC_DIR, "assinaturas_limpas.csv"), index=False, encoding="utf-8")
    print(f"  - Bases salvas: 'dados/processados/usuarios_limpo.csv' e 'dados/processados/assinaturas_limpas.csv'")
    return df_usr, df_ass, contas_internas


def auditar_dimensao_1_completude():
    print("\n" + "=" * 75)
    print("DIMENSÃO 1 — COMPLETUDE (onboarding.csv & usuarios.csv)")
    print("=" * 75)
    df_onb = pd.read_csv(os.path.join(RAW_DIR, "onboarding.csv"))
    n_total = len(df_onb)
    for col, status_doc in [
        ("objetivo_texto", "Opcional no dicionário"),
        ("nivel", "NÃO declarado opcional"),
        ("dias_por_semana", "NÃO declarado opcional"),
        ("como_conheceu", "Obrigatório"),
    ]:
        n_vazio = int(df_onb[col].isna().sum() + (df_onb[col].fillna("").astype(str).str.strip() == "").sum() - df_onb[col].isna().sum())
        pct = n_vazio / n_total * 100
        print(f"  - {col:<18}: {n_vazio:>6,} vazios ({pct:>5.1f}%) | [{status_doc}]")

    # Extrair valor numérico inteiro de dias_por_semana e criar flags de completude
    def extrair_dias(val):
        if pd.isna(val):
            return np.nan
        m = re.search(r"(\d+)", str(val).lower())
        return float(m.group(1)) if m else np.nan

    df_onb["dias_semana_pretendidos"] = df_onb["dias_por_semana"].apply(extrair_dias)
    df_onb["flag_onb_objetivo_preenchido"] = (
        df_onb["objetivo_texto"].fillna("").astype(str).str.strip() != ""
    ).astype(int)
    df_onb["flag_onb_nivel_preenchido"] = df_onb["nivel"].notna().astype(int)
    df_onb["flag_onb_dias_preenchido"] = df_onb["dias_por_semana"].notna().astype(int)
    df_onb["flag_onb_como_conheceu_preenchido"] = df_onb["como_conheceu"].notna().astype(int)

    out_onb = os.path.join(PROC_DIR, "onboarding_limpo.csv")
    df_onb.to_csv(out_onb, index=False, encoding="utf-8")
    print(f"  - Base limpa salva em '{out_onb}': {len(df_onb):,} linhas e {df_onb.shape[1]} colunas.")
    return df_onb


def auditar_e_limpar_atividades():
    print("\n" + "=" * 75)
    print("DIMENSÕES 2, 3 E 4 — VALIDADE, CONSISTÊNCIA E UNICIDADE (atividades.parquet)")
    print("=" * 75)
    df_atv = pd.read_parquet(os.path.join(RAW_DIR, "atividades.parquet"))
    n_bruto = len(df_atv)

    # 1. Validade (antes de deduplicar)
    sem_dist = int(df_atv["distancia_km"].isna().sum())
    com_dist = int(df_atv["distancia_km"].notna().sum())
    dist_maior_200 = int((df_atv["distancia_km"] > 200).sum())
    max_dist = float(df_atv["distancia_km"].max())
    dur_zero = int((df_atv["duracao_min"] <= 0).sum())

    print(f"[Validade - Bruto ({n_bruto:,} treinos)]")
    print(f"  - Sem distancia_km (indoor legítimo) : {sem_dist:,}")
    print(f"  - Com distancia_km (GPS)             : {com_dist:,}")
    print(f"  - Distância > 200 km (erro GPS)      : {dist_maior_200:,} (máx = {max_dist:,.2f} km)")
    print(f"  - Duração <= 0 min (inválido)        : {dur_zero:,}")

    # 2. Consistência (11 rótulos -> 7 modalidades canônicas)
    mask_ingles = df_atv["tipo"].isin(ROTULOS_INGLES)
    n_ingles = int(mask_ingles.sum())
    origens_ingles = df_atv.loc[mask_ingles, "origem"].value_counts().to_dict()
    n_run = int((df_atv["tipo"] == "run").sum())

    df_atv["tipo_canonico"] = df_atv["tipo"].map(MAPA_MODALIDADES)
    print(f"\n[Consistência - Modalidades]")
    print(f"  - Rótulos originais ({df_atv['tipo'].nunique()}): {sorted(df_atv['tipo'].unique())}")
    print(f"  - Rótulos canônicos ({df_atv['tipo_canonico'].nunique()}): {sorted(df_atv['tipo_canonico'].unique())}")
    print(f"  - Treinos em inglês: {n_ingles:,} ({n_ingles/n_bruto*100:.1f}%) | Origens: {origens_ingles}")
    print(f"  - Corridas 'run' que seriam perdidas sem mapeamento: {n_run:,}")

    # Sensibilidade da correlação r de Pearson nas corridas (duração x distância)
    corridas_todas = df_atv[
        (df_atv["tipo_canonico"] == "corrida") & (df_atv["distancia_km"].notna())
    ]
    r_bruto = corridas_todas["duracao_min"].corr(corridas_todas["distancia_km"])
    corridas_sem_erro = corridas_todas[
        (corridas_todas["distancia_km"] <= 200) & (corridas_todas["duracao_min"] > 0)
    ]
    n_corridas_erro = int((corridas_todas["distancia_km"] > 200).sum())
    r_limpo = corridas_sem_erro["duracao_min"].corr(corridas_sem_erro["distancia_km"])
    print(f"\n[Efeito no r de Pearson (Corridas: duracao_min x distancia_km)]")
    print(f"  - Com os {n_corridas_erro:,} treinos > 200 km : r = {r_bruto:.4f}")
    print(f"  - Sem os {n_corridas_erro:,} treinos > 200 km : r = {r_limpo:.4f}")

    # 3. Unicidade e Fuso do Garmin (UTC -> UTC-3)
    df_atv["inicio_dt_original"] = pd.to_datetime(df_atv["inicio"])
    # Garmin grava 3 horas à frente (UTC)
    df_atv["inicio_dt_br"] = df_atv["inicio_dt_original"]
    mask_garmin = df_atv["origem"] == "garmin"
    df_atv.loc[mask_garmin, "inicio_dt_br"] = df_atv.loc[
        mask_garmin, "inicio_dt_original"
    ] - pd.Timedelta(hours=3)

    # Identificar pares duplicados (mesmo user_id, tipo_canonico, duracao_min, distancia_km e início em até 5 min entre app e relógio)
    df_sorted = df_atv.sort_values(
        ["user_id", "tipo_canonico", "duracao_min", "inicio_dt_br"]
    ).copy()
    # Priorizar manter o registro ou identificar par (app + relógio)
    prev_user = df_sorted["user_id"].shift(1)
    prev_tipo = df_sorted["tipo_canonico"].shift(1)
    prev_dur = df_sorted["duracao_min"].shift(1)
    prev_dist = df_sorted["distancia_km"].fillna(-1).shift(1)
    curr_dist = df_sorted["distancia_km"].fillna(-1)
    prev_orig = df_sorted["origem"].shift(1)
    diff_min = (
        df_sorted["inicio_dt_br"] - df_sorted["inicio_dt_br"].shift(1)
    ).dt.total_seconds().abs() / 60.0

    is_dup_pair = (
        (df_sorted["user_id"] == prev_user)
        & (df_sorted["tipo_canonico"] == prev_tipo)
        & (df_sorted["duracao_min"] == prev_dur)
        & (np.isclose(curr_dist, prev_dist, equal_nan=True))
        & (diff_min <= 5.0)
        & (df_sorted["origem"] != prev_orig)
    )

    # Qual relógio gerou o par duplicado com o app?
    relogio_par = np.where(
        df_sorted["origem"] == "app", prev_orig, df_sorted["origem"]
    )
    dups_por_relogio = pd.Series(relogio_par[is_dup_pair]).value_counts().to_dict()
    n_dups = int(is_dup_pair.sum())

    print(f"\n[Unicidade - Pares Duplicados App + Relógio (após ajuste UTC-3 do Garmin)]")
    print(f"  - Total de pares duplicados encontrados : {n_dups:,}")
    print(f"  - Detalhamento por relógio              : {dups_por_relogio}")

    # Marcar flags de qualidade e salvar base limpa
    df_sorted["flag_duplicata_relogio"] = is_dup_pair
    df_sorted["flag_duracao_zero"] = df_sorted["duracao_min"] <= 0
    df_sorted["flag_distancia_acima_200km"] = df_sorted["distancia_km"] > 200
    df_sorted["flag_apos_corte"] = df_sorted["inicio_dt_br"] > DATA_CORTE

    # Para análises válidas: remover duplicatas, remover duração <= 0, remover pós-corte, e anular (NaN) distância > 200km
    df_limpo = df_sorted[
        (~df_sorted["flag_duplicata_relogio"])
        & (~df_sorted["flag_duracao_zero"])
        & (~df_sorted["flag_apos_corte"])
    ].copy()
    df_limpo.loc[df_limpo["flag_distancia_acima_200km"], "distancia_km"] = np.nan
    df_limpo.loc[df_limpo["flag_distancia_acima_200km"], "ritmo_min_km"] = np.nan

    out_path = os.path.join(PROC_DIR, "atividades_limpas.parquet")
    df_limpo.to_parquet(out_path, index=False)
    print(f"  - Base limpa salva em '{out_path}': {len(df_limpo):,} treinos válidos.")
    return df_limpo


def auditar_dimensao_5_temporalidade_e_vazamento():
    print("\n" + "=" * 75)
    print("DIMENSÃO 5 — TEMPORALIDADE (uso_mensal.csv) E VAZAMENTO (eventos_assinatura.csv)")
    print("=" * 75)
    df_uso = pd.read_csv(os.path.join(RAW_DIR, "uso_mensal.csv"))
    dez25 = df_uso[df_uso["mes"] == "2025-12"]
    jan26 = df_uso[df_uso["mes"] == "2026-01"]
    set26 = df_uso[df_uso["mes"] == "2026-09"]

    print("[Mudança de Regra de Gravação em uso_mensal.csv: Dez/2025 vs Jan/2026]")
    print(
        f"  - 2025-12: {len(dez25):>6,} linhas | zeros = {(dez25['minutos']==0).sum():>6,} "
        f"| média bruta = {dez25['minutos'].mean():>6.1f} min | média ativos (>0) = {dez25[dez25['minutos']>0]['minutos'].mean():>6.1f} min"
    )
    print(
        f"  - 2026-01: {len(jan26):>6,} linhas | zeros = {(jan26['minutos']==0).sum():>6,} "
        f"| média bruta = {jan26['minutos'].mean():>6.1f} min | média ativos (>0) = {jan26[jan26['minutos']>0]['minutos'].mean():>6.1f} min"
    )
    print(
        f"  - 2026-09: {len(set26):>6,} linhas | zeros = {(set26['minutos']==0).sum():>6,} ({(set26['minutos']==0).mean()*100:.1f}%) "
        f"| mediana = {set26['minutos'].median():.1f} | média = {set26['minutos'].mean():.1f} | s = {set26['minutos'].std():.1f} | CV = {set26['minutos'].std()/set26['minutos'].mean()*100:.0f}%"
    )

    # Correlação espúria sessoes_app x minutos em set/2026 controlada por atividades
    set26_ativos = set26[set26["minutos"] > 0]
    r_geral_ativos = set26_ativos["sessoes_app"].corr(set26_ativos["minutos"])
    r_geral_todos = set26["sessoes_app"].corr(set26["minutos"])
    # Correlação parcial / média ponderada dentro de cada valor exato de atividades
    corrs_por_k = []
    pesos = []
    for k, grp in set26_ativos.groupby("atividades"):
        if len(grp) >= 30 and grp["sessoes_app"].std() > 0 and grp["minutos"].std() > 0:
            corrs_por_k.append(grp["sessoes_app"].corr(grp["minutos"]))
            pesos.append(len(grp))
    r_controlado = float(np.average(corrs_por_k, weights=pesos))
    print(f"\n[Correlação Espúria e Variável de Controle em Set/2026]")
    print(f"  - r(sessoes_app, minutos) em todas as contas (56.565) : {r_geral_todos:.2f}")
    print(f"  - r(sessoes_app, minutos) nas contas ativas (15.685)  : {r_geral_ativos:.2f}")
    print(f"  - r(sessoes_app, minutos) controlado por 'atividades' : {r_controlado:.2f}")

    # Vazamento temporal: Retrato 30/09 (assinaturas.csv) vs Histórico 31/07 (eventos_assinatura.csv)
    df_ass = pd.read_csv(os.path.join(RAW_DIR, "assinaturas.csv"))
    df_usr = pd.read_csv(os.path.join(RAW_DIR, "usuarios.csv"))
    internas = set(df_usr[df_usr["email"].str.endswith("@vitaliza.com.br", na=False)]["user_id"])
    df_ass_pag = df_ass[(~df_ass["user_id"].isin(internas)) & (df_ass["plano_atual"] != "cortesia")].copy()

    df_ev = pd.read_csv(os.path.join(RAW_DIR, "eventos_assinatura.csv"))
    df_ev["data_hora_br"] = harmonizar_data_utc_para_br(df_ev["data_hora"])

    # Dos 2.250 ativos em 30/09 com renovacao_automatica == 'nao' no retrato
    ativos_renov_nao_retrato = df_ass_pag[
        (df_ass_pag["status_atual"] == "ativa") & (df_ass_pag["renovacao_automatica"] == "nao")
    ].copy()
    corte_jul = pd.Timestamp("2026-07-31 23:59:59")
    ativos_renov_nao_retrato["inicio_dt"] = pd.to_datetime(ativos_renov_nao_retrato["inicio"])

    ev_ate_jul = df_ev[
        (df_ev["user_id"].isin(ativos_renov_nao_retrato["user_id"]))
        & (df_ev["data_hora_br"] <= corte_jul)
        & (df_ev["evento"].isin(["assinatura_iniciada", "renovacao", "renovacao_automatica_desligada", "renovacao_automatica_religada"]))
    ].sort_values(["user_id", "data_hora_br"])

    ult_ev_jul = ev_ate_jul.groupby("user_id")["evento"].last()

    n_nao_assinava = int((ativos_renov_nao_retrato["inicio_dt"] > corte_jul).sum())
    ja_assinava = ativos_renov_nao_retrato[ativos_renov_nao_retrato["inicio_dt"] <= corte_jul]
    ult_status = ja_assinava["user_id"].map(ult_ev_jul)
    n_ja_desligada = int((ult_status == "renovacao_automatica_desligada").sum())
    n_ainda_ligada = len(ja_assinava) - n_ja_desligada

    print(f"\n[Prevenção de Vazamento Temporal: Retrato (30/09) vs Histórico em 31/07/2026]")
    print(f"  - Assinantes ativos c/ renovacao='nao' no retrato 30/09 : {len(ativos_renov_nao_retrato):,}")
    print(f"  - Já estavam c/ renovação desligada em 31/07            : {n_ja_desligada:,}")
    print(f"  - Ainda estavam c/ renovação LIGADA em 31/07            : {n_ainda_ligada:,}")
    print(f"  - Ainda nem assinavam em 31/07                          : {n_nao_assinava:,}")
    print(f"  - Total com erro (vazamento do futuro) se usar retrato  : {n_ainda_ligada + n_nao_assinava:,} ({(n_ainda_ligada + n_nao_assinava)/len(ativos_renov_nao_retrato)*100:.0f}%)")


def auditar_funil_faturamento_setembro2026():
    print("\n" + "=" * 75)
    print("RECONCILIAÇÃO CONTÁBIL — FATURAMENTO DE SETEMBRO/2026 (pagamentos.csv)")
    print("=" * 75)
    df_pag = pd.read_csv(os.path.join(RAW_DIR, "pagamentos.csv"), low_memory=False)
    df_pag["valor_num"] = limpar_valor_monetario(df_pag["valor"])

    # Passo 0: setembro pelo texto bruto da data (sem harmonizar fuso)
    mask_set_str = df_pag["data_hora"].astype(str).str.startswith("2026-09")
    soma_0_tudo_set = df_pag.loc[mask_set_str, "valor_num"].sum()

    # Passo 1: apenas status aprovado (sem recusado/estorno/chargeback) no texto bruto
    aprov_str = df_pag[mask_set_str & (df_pag["status"] == "aprovado")]
    soma_1_aprov_utc = aprov_str["valor_num"].sum()

    # Passo 2: harmonizar fuso horário (UTC 'Z' -> Brasília UTC-3)
    df_pag["data_hora_br"] = harmonizar_data_utc_para_br(df_pag["data_hora"])
    aprov_br_set = df_pag[
        (df_pag["status"] == "aprovado")
        & (df_pag["data_hora_br"] >= "2026-09-01 00:00:00")
        & (df_pag["data_hora_br"] <= "2026-09-30 23:59:59")
    ].copy()
    soma_2_aprov_br = aprov_br_set["valor_num"].sum()

    # Passo 3: remover cobranças aprovadas em duplicidade no mesmo ciclo/dia
    aprov_br_set["dia_br"] = aprov_br_set["data_hora_br"].dt.date
    aprov_br_set = aprov_br_set.sort_values(["user_id", "data_hora_br", "tentativa"])
    aprov_sem_dup = aprov_br_set.drop_duplicates(
        subset=["user_id", "valor_num", "dia_br"], keep="first"
    ).copy()
    soma_3_bruto = aprov_sem_dup["valor_num"].sum()

    # Passo 4: descontar taxas de intermediação por canal
    aprov_sem_dup["taxa"] = aprov_sem_dup["metodo"].map(TAXAS_CANAL).fillna(0.0)
    aprov_sem_dup["valor_liq"] = aprov_sem_dup["valor_num"] * (1.0 - aprov_sem_dup["taxa"])
    soma_4_liquido = aprov_sem_dup["valor_liq"].sum()

    print(f"  0. Soma bruta das linhas de set/2026 (s/ filtro status) : R$ {soma_0_tudo_set:>10,.0f}")
    print(f"  1. Apenas status == 'aprovado' (fuso original)          : R$ {soma_1_aprov_utc:>10,.0f}")
    print(f"  2. Harmonizado para Horário de Brasília (UTC-3)         : R$ {soma_2_aprov_br:>10,.0f}")
    print(f"  3. Sem duplicatas de cobrança no mesmo dia (BRUTO)      : R$ {soma_3_bruto:>10,.0f}")
    print(f"  4. Descontadas taxas de canal (LÍQUIDO OFICIAL)         : R$ {soma_4_liquido:>10,.0f}")

    # Salvar pagamentos_limpos.csv (com valor_num, data_hora_br, flag_duplicata_dia e valor_liq)
    df_pag_clean = df_pag[df_pag["data_hora_br"] <= DATA_CORTE].copy()
    df_pag_clean["dia_br"] = df_pag_clean["data_hora_br"].dt.date
    df_pag_clean = df_pag_clean.sort_values(["user_id", "data_hora_br", "tentativa"])
    mask_aprov = df_pag_clean["status"] == "aprovado"
    dup_aprov = df_pag_clean[mask_aprov].duplicated(subset=["user_id", "valor_num", "dia_br"], keep="first")
    df_pag_clean["flag_duplicata_aprovada_dia"] = False
    df_pag_clean.loc[mask_aprov, "flag_duplicata_aprovada_dia"] = dup_aprov.values
    df_pag_clean["taxa_canal"] = df_pag_clean["metodo"].map(TAXAS_CANAL).fillna(0.0)
    df_pag_clean["valor_liquido"] = np.where(
        (df_pag_clean["status"] == "aprovado") & (~df_pag_clean["flag_duplicata_aprovada_dia"]),
        (df_pag_clean["valor_num"] * (1.0 - df_pag_clean["taxa_canal"])).round(2),
        0.0,
    )
    df_pag_clean.to_csv(os.path.join(PROC_DIR, "pagamentos_limpos.csv"), index=False, encoding="utf-8")
    print(f"  - Base limpa salva em 'dados/processados/pagamentos_limpos.csv': {len(df_pag_clean):,} linhas.")


if __name__ == "__main__":
    auditar_populacao_e_contas_internas()
    auditar_dimensao_1_completude()
    auditar_e_limpar_atividades()
    auditar_dimensao_5_temporalidade_e_vazamento()
    auditar_funil_faturamento_setembro2026()

