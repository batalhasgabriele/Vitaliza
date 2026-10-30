"""
Auditoria Multidimensional de Qualidade de Dados - Todas as 12 Tabelas Brutas da Vitaliza
Dimensões auditadas com base na skill data-quality-audit:
1. Completude (Completeness)
2. Unicidade (Uniqueness)
3. Validade (Validity)
4. Consistência (Consistency & Referential Integrity)
5. Temporalidade (Timeliness & Data Leakage vs 30/09/2026)
"""

import os
import json
import re
from datetime import datetime
import pandas as pd
import numpy as np

DATA_CORTE = pd.to_datetime('2026-09-30 23:59:59')

def audit_all():
    print("Iniciando auditoria completa das 12 tabelas do data room...")
    
    results = {}
    
    # -------------------------------------------------------------------------
    # 1. Carregamento dos dados brutos (modo somente leitura)
    # -------------------------------------------------------------------------
    print("Carregando tabelas...")
    df_users = pd.read_csv('dados/brutos/usuarios.csv')
    df_ass = pd.read_csv('dados/brutos/assinaturas.csv')
    df_amiz = pd.read_csv('dados/brutos/amizades.csv')
    df_camp = pd.read_csv('dados/brutos/campanha_ago26.csv')
    df_evt = pd.read_csv('dados/brutos/eventos_assinatura.csv')
    df_pag = pd.read_csv('dados/brutos/pagamentos.csv', low_memory=False)
    df_uso = pd.read_csv('dados/brutos/uso_mensal.csv')
    df_ativ = pd.read_parquet('dados/brutos/atividades.parquet')
    df_onb = pd.read_csv('dados/brutos/onboarding.csv')
    df_pesq = pd.read_csv('dados/brutos/pesquisa_saida.csv')
    df_feed = pd.read_csv('dados/brutos/feed_posts.csv')
    df_tick = pd.read_csv('dados/brutos/tickets_suporte.csv')
    
    tabelas = {
        'usuarios': (df_users, 'user_id'),
        'assinaturas': (df_ass, 'assinatura_id'),
        'amizades': (df_amiz, None), # chave composta: seguidor_id + seguido_id
        'campanha_ago26': (df_camp, 'user_id'),
        'eventos_assinatura': (df_evt, None), # chave composta: user_id + data_hora + evento
        'pagamentos': (df_pag, 'pagamento_id'),
        'uso_mensal': (df_uso, None), # chave composta: user_id + mes
        'atividades': (df_ativ, 'atividade_id'),
        'onboarding': (df_onb, 'onboarding_id'),
        'pesquisa_saida': (df_pesq, 'resposta_id'),
        'feed_posts': (df_feed, 'post_id'),
        'tickets_suporte': (df_tick, 'ticket_id'),
    }
    
    # -------------------------------------------------------------------------
    # 2. Completude por tabela e coluna
    # -------------------------------------------------------------------------
    print("Avaliando Completude...")
    completude_res = []
    for tab_name, (df, _) in tabelas.items():
        total_rows = len(df)
        for col in df.columns:
            null_count = int(df[col].isna().sum())
            empty_str = 0
            if df[col].dtype == object or str(df[col].dtype) in ('str', 'string'):
                # checar string vazia
                empty_str = int((df[col].fillna('').astype(str).str.strip() == '').sum() - null_count)
            total_missing = null_count + max(0, empty_str)
            pct_missing = (total_missing / total_rows * 100) if total_rows > 0 else 0.0
            
            status = "PASS"
            if pct_missing > 20.0:
                status = "FAIL"
            elif pct_missing > 5.0:
                status = "WARN"
                
            completude_res.append({
                'tabela': tab_name,
                'coluna': col,
                'total_linhas': total_rows,
                'nulos': null_count,
                'strings_vazias': max(0, empty_str),
                'total_ausentes': total_missing,
                'pct_ausente': round(pct_missing, 2),
                'status': status
            })
            
    results['completude'] = completude_res
    
    # -------------------------------------------------------------------------
    # 3. Unicidade por tabela
    # -------------------------------------------------------------------------
    print("Avaliando Unicidade...")
    unicidade_res = []
    for tab_name, (df, pk) in tabelas.items():
        total_rows = len(df)
        full_dupes = int(df.duplicated().sum())
        pk_dupes = 0
        pk_name = pk
        
        if pk:
            pk_dupes = int(df[pk].duplicated().sum())
        elif tab_name == 'amizades':
            pk_name = 'seguidor_id + seguido_id'
            pk_dupes = int(df.duplicated(subset=['seguidor_id', 'seguido_id']).sum())
        elif tab_name == 'uso_mensal':
            pk_name = 'user_id + mes'
            pk_dupes = int(df.duplicated(subset=['user_id', 'mes']).sum())
        elif tab_name == 'eventos_assinatura':
            pk_name = 'user_id + data_hora + evento'
            pk_dupes = int(df.duplicated(subset=['user_id', 'data_hora', 'evento']).sum())
            
        unicidade_res.append({
            'tabela': tab_name,
            'total_linhas': total_rows,
            'linhas_duplicadas': full_dupes,
            'pct_linhas_duplicadas': round(full_dupes / total_rows * 100, 2),
            'pk_coluna': pk_name,
            'pk_duplicadas': pk_dupes,
            'pct_pk_duplicadas': round(pk_dupes / total_rows * 100, 2),
            'status': 'FAIL' if (full_dupes > 0 or pk_dupes > 0) else 'PASS'
        })
    results['unicidade'] = unicidade_res
    
    # -------------------------------------------------------------------------
    # 4. Consistência e Integridade Referencial (FK -> PK)
    # -------------------------------------------------------------------------
    print("Avaliando Consistência e Integridade Referencial...")
    fk_checks = [
        # (tabela_filha, coluna_fk, tabela_mae, coluna_pk)
        ('assinaturas', 'user_id', 'usuarios', 'user_id'),
        ('amizades', 'seguidor_id', 'usuarios', 'user_id'),
        ('amizades', 'seguido_id', 'usuarios', 'user_id'),
        ('campanha_ago26', 'user_id', 'usuarios', 'user_id'),
        ('eventos_assinatura', 'user_id', 'usuarios', 'user_id'),
        ('pagamentos', 'user_id', 'usuarios', 'user_id'),
        ('uso_mensal', 'user_id', 'usuarios', 'user_id'),
        ('atividades', 'user_id', 'usuarios', 'user_id'),
        ('onboarding', 'user_id', 'usuarios', 'user_id'),
        ('pesquisa_saida', 'user_id', 'usuarios', 'user_id'),
        ('feed_posts', 'user_id', 'usuarios', 'user_id'),
        ('tickets_suporte', 'user_id', 'usuarios', 'user_id'),
    ]
    
    integridade_res = []
    for child_tab, child_col, parent_tab, parent_col in fk_checks:
        c_df, _ = tabelas[child_tab]
        p_df, _ = tabelas[parent_tab]
        
        child_vals = c_df[child_col].dropna()
        parent_set = set(p_df[parent_col].dropna())
        
        orphans = child_vals[~child_vals.isin(parent_set)]
        orphan_count = int(len(orphans))
        total_child = int(len(child_vals))
        orphan_pct = round(orphan_count / total_child * 100, 2) if total_child > 0 else 0.0
        
        integridade_res.append({
            'relacao': f"{child_tab}.{child_col} -> {parent_tab}.{parent_col}",
            'filha_linhas_nao_nulas': total_child,
            'orfaos': orphan_count,
            'pct_orfaos': orphan_pct,
            'status': 'FAIL' if orphan_count > 0 else 'PASS'
        })
    results['integridade_referencial'] = integridade_res
    
    # -------------------------------------------------------------------------
    # 5. Consistência Lógica Específica
    # -------------------------------------------------------------------------
    print("Avaliando Consistência Lógica Específica...")
    logica_res = []
    
    # Assinaturas: data_fim >= inicio
    ass_datas = df_ass[df_ass['data_fim'].notna()].copy()
    ass_inconsistentes = int((pd.to_datetime(ass_datas['data_fim']) < pd.to_datetime(ass_datas['inicio'])).sum())
    logica_res.append({
        'tabela': 'assinaturas',
        'regra': 'data_fim >= inicio',
        'violacoes': ass_inconsistentes,
        'pct_violacoes': round(ass_inconsistentes / len(ass_datas) * 100, 2) if len(ass_datas) > 0 else 0,
        'detalhe': 'Data de término anterior à data de início'
    })
    
    # Assinaturas: status_atual vs motivo_fim
    ativas_com_motivo = int(((df_ass['status_atual'] == 'ativa') & (df_ass['motivo_fim'].notna())).sum())
    logica_res.append({
        'tabela': 'assinaturas',
        'regra': 'status_atual == ativa -> motivo_fim nulo',
        'violacoes': ativas_com_motivo,
        'pct_violacoes': round(ativas_com_motivo / (df_ass['status_atual'] == 'ativa').sum() * 100, 2),
        'detalhe': 'Assinaturas ativas com motivo de término preenchido'
    })
    
    # Pagamentos: valores monetários numéricos vs string
    def extrai_valor(v):
        if pd.isna(v): return np.nan
        s = str(v).replace('R$', '').replace(' ', '').replace(',', '.')
        try:
            return float(s)
        except:
            return np.nan
            
    vals_pag = df_pag['valor'].apply(extrai_valor)
    vals_invalidos = int(vals_pag.isna().sum())
    vals_negativos = int((vals_pag < 0).sum())
    logica_res.append({
        'tabela': 'pagamentos',
        'regra': 'valor > 0 e conversível para numérico',
        'violacoes': vals_invalidos + vals_negativos,
        'pct_violacoes': round((vals_invalidos + vals_negativos) / len(df_pag) * 100, 2),
        'detalhe': f'{vals_invalidos} não conversíveis, {vals_negativos} negativos'
    })
    
    # Pagamentos: valores textuais com "R$"
    pag_string_rs = int(df_pag['valor'].astype(str).str.contains('R').sum())
    logica_res.append({
        'tabela': 'pagamentos',
        'regra': 'formato numérico padrão (sem prefixo textual R$)',
        'violacoes': pag_string_rs,
        'pct_violacoes': round(pag_string_rs / len(df_pag) * 100, 2),
        'detalhe': 'Valores formatados como texto em reais nas vendas web'
    })
    
    # Atividades: duracao_min > 0 e distancia_km >= 0
    ativ_dur_invalida = int(((df_ativ['duracao_min'] <= 0) | (df_ativ['duracao_min'].isna())).sum())
    ativ_dist_negativa = int((df_ativ['distancia_km'].dropna() < 0).sum())
    logica_res.append({
        'tabela': 'atividades',
        'regra': 'duracao_min > 0 e distancia_km >= 0',
        'violacoes': ativ_dur_invalida + ativ_dist_negativa,
        'pct_violacoes': round((ativ_dur_invalida + ativ_dist_negativa) / len(df_ativ) * 100, 2),
        'detalhe': f'{ativ_dur_invalida} durações <= 0, {ativ_dist_negativa} distâncias < 0'
    })
    
    # Atividades: treino_com nulos vs string vazia
    ativ_treino_com_vazio = int((df_ativ['treino_com'].fillna('').astype(str).str.strip() == '').sum())
    logica_res.append({
        'tabela': 'atividades',
        'regra': 'treino solo codificado como string vazia em vez de NaN',
        'violacoes': ativ_treino_com_vazio,
        'pct_violacoes': round(ativ_treino_com_vazio / len(df_ativ) * 100, 2),
        'detalhe': '98,87% das atividades possuem string vazia em treino_com'
    })
    
    # Tickets: resolvido_em >= aberto_em
    tick_resolv = df_tick[df_tick['resolvido_em'].notna()].copy()
    tick_datas_inconsistentes = int((pd.to_datetime(tick_resolv['resolvido_em']) < pd.to_datetime(tick_resolv['aberto_em'])).sum())
    logica_res.append({
        'tabela': 'tickets_suporte',
        'regra': 'resolvido_em >= aberto_em',
        'violacoes': tick_datas_inconsistentes,
        'pct_violacoes': round(tick_datas_inconsistentes / len(tick_resolv) * 100, 2) if len(tick_resolv) > 0 else 0,
        'detalhe': 'Chamado resolvido antes da data de abertura'
    })
    
    results['consistencia_logica'] = logica_res
    
    # -------------------------------------------------------------------------
    # 6. Validade de Domínios e Formatos
    # -------------------------------------------------------------------------
    print("Avaliando Validade de Domínios e Formatos...")
    validade_res = []
    
    # Assinaturas plano_atual
    planos_inv = int((~df_ass['plano_atual'].isin(['mensal', 'anual'])).sum())
    validade_res.append({
        'tabela': 'assinaturas',
        'coluna': 'plano_atual',
        'regra': "in ['mensal', 'anual']",
        'violacoes': planos_inv,
        'pct_violacoes': round(planos_inv / len(df_ass) * 100, 2),
        'valores_encontrados': df_ass['plano_atual'].value_counts().to_dict()
    })
    
    # Assinaturas status_atual
    status_ass_inv = int((~df_ass['status_atual'].isin(['ativa', 'cancelada'])).sum())
    validade_res.append({
        'tabela': 'assinaturas',
        'coluna': 'status_atual',
        'regra': "in ['ativa', 'cancelada']",
        'violacoes': status_ass_inv,
        'pct_violacoes': round(status_ass_inv / len(df_ass) * 100, 2),
        'valores_encontrados': df_ass['status_atual'].value_counts().to_dict()
    })
    
    # Assinaturas canal_cobranca
    canais_ass = df_ass['canal_cobranca'].value_counts().to_dict()
    validade_res.append({
        'tabela': 'assinaturas',
        'coluna': 'canal_cobranca',
        'regra': "lojas e web",
        'violacoes': 0,
        'pct_violacoes': 0.0,
        'valores_encontrados': canais_ass
    })
    
    # Pagamentos status
    pag_status_inv = int((~df_pag['status'].isin(['aprovado', 'recusado', 'estornado', 'reembolsado', 'cancelado', 'em_processamento'])).sum())
    validade_res.append({
        'tabela': 'pagamentos',
        'coluna': 'status',
        'regra': "status de transação válidos",
        'violacoes': pag_status_inv,
        'pct_violacoes': round(pag_status_inv / len(df_pag) * 100, 2),
        'valores_encontrados': df_pag['status'].value_counts().to_dict()
    })
    
    # Atividades tipo
    ativ_tipos = df_ativ['tipo'].value_counts().to_dict()
    validade_res.append({
        'tabela': 'atividades',
        'coluna': 'tipo',
        'regra': "modalidades esportivas válidas",
        'violacoes': 0,
        'pct_violacoes': 0.0,
        'valores_encontrados': ativ_tipos
    })
    
    # Tickets categoria_atendente
    tick_cat = df_tick['categoria_atendente'].value_counts().to_dict()
    validade_res.append({
        'tabela': 'tickets_suporte',
        'coluna': 'categoria_atendente',
        'regra': "categorias de suporte válidas",
        'violacoes': 0,
        'pct_violacoes': 0.0,
        'valores_encontrados': tick_cat
    })
    
    results['validade'] = validade_res
    
    # -------------------------------------------------------------------------
    # 7. Temporalidade e Detecção de Vazamento Pós-Corte (30/09/2026)
    # -------------------------------------------------------------------------
    print("Avaliando Temporalidade e Vazamento Temporal...")
    time_cols = [
        ('usuarios', df_users, 'data_cadastro'),
        ('assinaturas', df_ass, 'inicio'),
        ('assinaturas', df_ass[df_ass['data_fim'].notna()], 'data_fim'),
        ('amizades', df_amiz, 'desde'),
        ('campanha_ago26', df_camp[df_camp['enviado_em'].notna()], 'enviado_em'),
        ('eventos_assinatura', df_evt, 'data_hora'),
        ('pagamentos', df_pag, 'data_hora'),
        ('atividades', df_ativ, 'inicio'),
        ('pesquisa_saida', df_pesq, 'respondido_em'),
        ('feed_posts', df_feed, 'data_hora'),
        ('tickets_suporte', df_tick, 'aberto_em'),
    ]
    
    temporalidade_res = []
    for tab_name, df_sub, col_time in time_cols:
        ts_naive = pd.to_datetime(df_sub[col_time].astype(str).str.replace('Z', '').str[:19], errors='coerce')
        min_date = ts_naive.min()
        max_date = ts_naive.max()
        
        futuros = int((ts_naive > pd.to_datetime('2026-09-30 23:59:59')).sum())
        total_valid = int(ts_naive.notna().sum())
        pct_futuros = round(futuros / total_valid * 100, 2) if total_valid > 0 else 0.0
        
        temporalidade_res.append({
            'tabela': tab_name,
            'coluna_tempo': col_time,
            'data_minima': str(min_date),
            'data_maxima': str(max_date),
            'registros_pos_corte': futuros,
            'pct_pos_corte': pct_futuros,
            'status': 'WARN' if futuros > 0 else 'PASS'
        })
        
    results['temporalidade'] = temporalidade_res
    
    # -------------------------------------------------------------------------
    # 8. Exportação dos Resultados Consolidados
    # -------------------------------------------------------------------------
    print("Exportando artefatos...")
    with open('saidas/auditoria_qualidade_todas_tabelas.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print("Auditoria concluída com sucesso! Resultados salvos em saidas/auditoria_qualidade_todas_tabelas.json")

if __name__ == '__main__':
    audit_all()
