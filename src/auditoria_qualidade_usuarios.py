"""
Auditoria completa de Qualidade de Dados na Base de Usuários (usuarios.csv)
Dimensões avaliadas conforme a skill data-quality-audit:
1. Validade (Validity)
2. Consistência (Consistency)
3. Unicidade (Uniqueness)
4. Temporalidade (Timeliness / Freshness)
"""

import json
from datetime import datetime
import pandas as pd
import numpy as np

def run_audit():
    df_users = pd.read_csv('dados/brutos/usuarios.csv')
    total = len(df_users)
    print(f"=== AUDITORIA DE QUALIDADE DE DADOS: usuarios.csv (N={total}) ===\n")

    # ----------------------------------------------------
    # 1. UNICIDADE (UNIQUENESS)
    # ----------------------------------------------------
    dupe_rows = int(df_users.duplicated().sum())
    dupe_pk = int(df_users['user_id'].duplicated().sum())
    dupe_email = int(df_users['email'].duplicated().sum())

    print("--- 1. UNICIDADE ---")
    print(f"Linhas 100% duplicadas: {dupe_rows} ({dupe_rows/total*100:.2f}%)")
    print(f"Chave Primária (user_id) duplicada: {dupe_pk} ({dupe_pk/total*100:.2f}%)")
    print(f"Chave Natural (email) duplicada: {dupe_email} ({dupe_email/total*100:.2f}%)")

    # ----------------------------------------------------
    # 2. VALIDADE (VALIDITY)
    # ----------------------------------------------------
    print("\n--- 2. VALIDADE ---")
    # Padrão user_id (u_8hex)
    id_pattern = r'^u_[a-f0-9]{8}$'
    invalid_ids = int((~df_users['user_id'].astype(str).str.match(id_pattern)).sum())
    print(f"user_id fora da máscara regex (u_[a-f0-9]{{8}}): {invalid_ids} ({invalid_ids/total*100:.2f}%)")

    # Formato de e-mail
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    invalid_emails = int((~df_users['email'].astype(str).str.match(email_pattern)).sum())
    print(f"E-mails com formato/sintaxe inválida: {invalid_emails} ({invalid_emails/total*100:.2f}%)")

    # Categorias permitidas
    # Sexo: M, F (ou nulo)
    non_null_sexo = df_users['sexo'].dropna()
    invalid_sexo = int((~non_null_sexo.isin(['M', 'F'])).sum())
    print(f"Sexo fora de ['M', 'F']: {invalid_sexo} ({invalid_sexo/total*100:.2f}%)")

    # UF: 27 UFs brasileiras
    ufs_validas = {'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 
                   'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'}
    invalid_uf = int((~df_users['uf'].isin(ufs_validas)).sum())
    print(f"UF fora da lista oficial de 27 UFs: {invalid_uf} ({invalid_uf/total*100:.2f}%)")

    # Sistema: ios, android
    invalid_sistema = int((~df_users['sistema'].isin(['ios', 'android'])).sum())
    print(f"Sistema fora de ['ios', 'android']: {invalid_sistema} ({invalid_sistema/total*100:.2f}%)")

    # Canal de aquisição
    canais_permitidos = {'meta_ads', 'google_ads', 'organico', 'influenciador', 'indicacao_amigos', 'parcerias', 'tiktok_ads'}
    invalid_canal = int((~df_users['canal_aquisicao'].isin(canais_permitidos)).sum())
    print(f"Canal aquisição: {df_users['canal_aquisicao'].value_counts().to_dict()}")

    # Versão do App (SemVer)
    semver_pattern = r'^\d+\.\d+\.\d+$'
    invalid_versao = int((~df_users['versao_app'].astype(str).str.match(semver_pattern)).sum())
    print(f"Versão do app fora do formato SemVer (X.Y.Z): {invalid_versao} ({invalid_versao/total*100:.2f}%)")
    print(f"Versões presentes: {df_users['versao_app'].value_counts().to_dict()}")

    # Relógio conectado
    relogios_permitidos = {'nenhum', 'garmin', 'apple_watch'}
    invalid_relogio = int((~df_users['relogio_conectado'].isin(relogios_permitidos)).sum())
    print(f"Relógio conectado: {df_users['relogio_conectado'].value_counts().to_dict()}")

    # Faixa de CEP (prefixo de 3 dígitos: 10 a 999)
    non_null_cep = df_users['cep_prefixo'].dropna()
    invalid_cep = int(((non_null_cep < 10) | (non_null_cep > 999) | (non_null_cep % 1 != 0)).sum())
    print(f"CEP prefixo fora da faixa válida (010 a 999): {invalid_cep} ({invalid_cep/total*100:.2f}%)")

    # Idade / Nascimento (data válida e faixa razoável)
    dt_nasc = pd.to_datetime(df_users['data_nascimento'], errors='coerce')
    invalid_nasc_parse = int((df_users['data_nascimento'].notna() & dt_nasc.isna()).sum())
    print(f"data_nascimento com falha de parse: {invalid_nasc_parse}")
    
    data_corte = pd.to_datetime('2026-09-30 23:59:59')
    idade_no_corte = (data_corte - dt_nasc).dt.days / 365.25
    idade_valida = idade_no_corte.dropna()
    idade_outliers = int(((idade_valida < 10) | (idade_valida > 100)).sum())
    print(f"Idade no corte < 10 anos ou > 100 anos: {idade_outliers} ({idade_outliers/total*100:.2f}%)")
    print(f"Idade mínima: {idade_valida.min():.1f} anos, máxima: {idade_valida.max():.1f} anos, mediana: {idade_valida.median():.1f} anos")

    # ----------------------------------------------------
    # 3. CONSISTÊNCIA (CONSISTENCY)
    # ----------------------------------------------------
    print("\n--- 3. CONSISTÊNCIA ---")
    # A) Consistência entre campos internos (Cross-field consistency)
    dt_cadastro = pd.to_datetime(df_users['data_cadastro'], errors='coerce')
    cadastro_antes_nascimento = int(((dt_cadastro < dt_nasc) & dt_nasc.notna()).sum())
    print(f"Usuários com data_cadastro anterior a data_nascimento: {cadastro_antes_nascimento} ({cadastro_antes_nascimento/total*100:.2f}%)")

    # Idade na data de cadastro
    idade_no_cadastro = (dt_cadastro - dt_nasc).dt.days / 365.25
    cadastro_menor_12anos = int(((idade_no_cadastro < 12) & dt_nasc.notna()).sum())
    print(f"Usuários com idade inferior a 12 anos na data de cadastro: {cadastro_menor_12anos}")

    # Sistema vs Relógio Conectado (Apple Watch no Android?)
    android_applewatch = int(((df_users['sistema'] == 'android') & (df_users['relogio_conectado'] == 'apple_watch')).sum())
    print(f"Usuários Android com Apple Watch conectado: {android_applewatch} ({android_applewatch/total*100:.2f}%)")

    # B) Consistência Geográfica (Regra de CEP Prefixo vs UF no Brasil)
    # Faixas aproximadas de 1º dígito de CEP:
    # 0xxx, 1xxx: SP
    # 2xxx: RJ (20-28), ES (29)
    # 3xxx: MG
    # 4xxx: BA, SE
    # 5xxx: PE, AL, PB, RN
    # 6xxx: CE, PI, MA, PA, AP, AM, RR, AC
    # 7xxx: DF, GO, TO, MT, RO, MS
    # 8xxx: PR, SC
    # 9xxx: RS
    def cep_esperado_uf(cep_pref, uf):
        if pd.isna(cep_pref):
            return True
        p = int(cep_pref)
        # SP: 010-199
        if uf == 'SP' and 10 <= p <= 199: return True
        # RJ: 200-289
        if uf == 'RJ' and 200 <= p <= 289: return True
        # ES: 290-299
        if uf == 'ES' and 290 <= p <= 299: return True
        # MG: 300-399
        if uf == 'MG' and 300 <= p <= 399: return True
        # BA: 400-489
        if uf == 'BA' and 400 <= p <= 489: return True
        # SE: 490-499
        if uf == 'SE' and 490 <= p <= 499: return True
        # PE: 500-569
        if uf == 'PE' and 500 <= p <= 569: return True
        # AL: 570-579
        if uf == 'AL' and 570 <= p <= 579: return True
        # PB: 580-589
        if uf == 'PB' and 580 <= p <= 589: return True
        # RN: 590-599
        if uf == 'RN' and 590 <= p <= 599: return True
        # CE: 600-639
        if uf == 'CE' and 600 <= p <= 639: return True
        # PI: 640-649
        if uf == 'PI' and 640 <= p <= 649: return True
        # MA: 650-659
        if uf == 'MA' and 650 <= p <= 659: return True
        # PA: 660-688
        if uf == 'PA' and 660 <= p <= 688: return True
        # AP: 689
        if uf == 'AP' and p == 689: return True
        # AM: 690-692, 694-698
        if uf == 'AM' and (690 <= p <= 692 or 694 <= p <= 698): return True
        # RR: 693
        if uf == 'RR' and p == 693: return True
        # AC: 699
        if uf == 'AC' and p == 699: return True
        # DF: 700-727, 730-736
        if uf == 'DF' and (700 <= p <= 727 or 730 <= p <= 736): return True
        # GO: 728-729, 737-767
        if uf == 'GO' and (728 <= p <= 729 or 737 <= p <= 767): return True
        # TO: 770-779
        if uf == 'TO' and 770 <= p <= 779: return True
        # MT: 780-788
        if uf == 'MT' and 780 <= p <= 788: return True
        # RO: 789
        if uf == 'RO' and p == 789: return True
        # MS: 790-799
        if uf == 'MS' and 790 <= p <= 799: return True
        # PR: 800-879
        if uf == 'PR' and 800 <= p <= 879: return True
        # SC: 880-899
        if uf == 'SC' and 880 <= p <= 899: return True
        # RS: 900-999
        if uf == 'RS' and 900 <= p <= 999: return True
        return False

    cep_inconsistente = sum(not cep_esperado_uf(row['cep_prefixo'], row['uf']) for _, row in df_users[df_users['cep_prefixo'].notna()].iterrows())
    print(f"CEP prefixo incompatível com a UF declarada: {cep_inconsistente} ({cep_inconsistente/total*100:.2f}%)")

    # C) Integridade Referencial Cruzada (Referential Integrity com outras tabelas)
    parent_users = set(df_users['user_id'])
    
    # Assinaturas
    df_ass = pd.read_csv('dados/brutos/assinaturas.csv')
    orf_ass = int((~df_ass['user_id'].isin(parent_users)).sum())
    print(f"Órfãos em assinaturas.csv (user_id inexistente em usuarios.csv): {orf_ass}")

    # Onboarding
    df_onb = pd.read_csv('dados/brutos/onboarding.csv')
    orf_onb = int((~df_onb['user_id'].isin(parent_users)).sum())
    print(f"Órfãos em onboarding.csv: {orf_onb}")

    # Atividades
    df_ativ = pd.read_parquet('dados/brutos/atividades.parquet')
    orf_ativ = int((~df_ativ['user_id'].isin(parent_users)).sum())
    print(f"Órfãos em atividades.parquet: {orf_ativ}")

    # ----------------------------------------------------
    # 4. TEMPORALIDADE (TIMELINESS / FRESHNESS)
    # ----------------------------------------------------
    print("\n--- 4. TEMPORALIDADE ---")
    data_min_cad = dt_cadastro.min()
    data_max_cad = dt_cadastro.max()
    print(f"Data mínima de cadastro: {data_min_cad}")
    print(f"Data máxima de cadastro: {data_max_cad}")

    cadastros_futuros = int((dt_cadastro > data_corte).sum())
    print(f"Cadastros com data posterior ao corte (30/09/2026 23:59:59): {cadastros_futuros}")

    lag_corte = (data_corte - data_max_cad).total_seconds() / 3600
    print(f"Lag do último cadastro em relação ao corte oficial: {lag_corte:.2f} horas")

    # Distribuição anual de cadastros
    df_users['ano_cadastro'] = dt_cadastro.dt.year
    print(f"Cadastros por ano:\n{df_users['ano_cadastro'].value_counts().sort_index().to_dict()}")

if __name__ == '__main__':
    run_audit()
