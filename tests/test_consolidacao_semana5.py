from pathlib import Path
import sys
import pandas as pd
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from metricas_semana5 import estado_no_corte, exposicao_meses, fase_evento, proporcao_saida_90d, wilson
from consolidar_semana5 import atributos, ajustar, atribuir, transformar
from gerar_graficos_eda import cobertura_pesquisa


def test_receita_fallback_usa_canais_reais_do_case(monkeypatch):
    import consolidar_semana5 as c
    pagamentos=pd.DataFrame(dict(status=['aprovado'],flag_duplicata_aprovada_dia=[False],
        valor_num=[1.],data_hora_br=['2026-01-01'],user_id=['fora'],valor_liquido=[.85]))
    monkeypatch.setattr(c,'ler',lambda nome:pagamentos)
    base=pd.DataFrame(dict(canal_cobranca=['cartao','pix_automatico','app_store'],
        plano=['mensal','mensal','anual']),index=['a','b','c'])
    assert np.allclose(c.receita_atual(base),[39.90*.965,39.90*.9901,299.90*.85/12])


def fontes_minimas():
    a=pd.DataFrame(dict(user_id=["a","b"],inicio=pd.to_datetime(["2025-01-01","2026-07-25"]),
                        plano_atual=["mensal","anual"],canal_cobranca=["web_cartao","app_store"],
                        status_atual=["expirada","ativa"],data_fim=["2026-09-01",None]))
    ev=pd.DataFrame(dict(user_id=["a","a","a"],data_hora_br=pd.to_datetime(["2026-05-01","2026-08-01","2026-09-01"]),
                         evento=["renovacao","renovacao_automatica_desligada","assinatura_expirada"],
                         plano=["mensal"]*3,canal_cobranca=["web_cartao"]*3))
    return a,ev


def test_estado_nao_usa_snapshot_futuro_e_distingue_opt_out():
    a,ev=fontes_minimas()
    jul=estado_no_corte(a,ev,pd.Timestamp("2026-07-31"))
    ago=estado_no_corte(a,ev,pd.Timestamp("2026-08-20"))
    set_=estado_no_corte(a,ev,pd.Timestamp("2026-09-02"))
    assert jul.loc['a','ativa'] and jul.loc['a','renovacao_ligada']
    assert ago.loc['a','ativa'] and not ago.loc['a','renovacao_ligada']
    assert not set_.loc['a','ativa']


def test_atributos_nao_mudam_com_treino_ou_onboarding_futuro():
    a,ev=fontes_minimas()
    at=pd.DataFrame(dict(user_id=['a','a','b'],atividade_id=[1,2,3],
        inicio_dt_br=pd.to_datetime(['2026-07-20','2026-08-01','2026-07-26']),tipo_canonico=['corrida','yoga','yoga']))
    o=pd.DataFrame(dict(user_id=['a','b','a'],respondido_em=pd.to_datetime(['2025-01-01','2026-07-25','2026-08-01']),dias_semana_pretendidos=[3,2,7]))
    corte=pd.Timestamp('2026-07-31 23:59:59')
    um=atributos(a,ev,at,o,corte)
    dois=atributos(a,ev,at[at.inicio_dt_br<=corte],o[o.respondido_em<=corte],corte)
    pd.testing.assert_frame_equal(um,dois)
    assert um.loc['a','n_treinos']==1 and um.loc['a','dias_semana_pretendidos']==3
    assert um.loc['a','dias_observados']==84 and um.loc['b','provisorio']


def test_pessoa_tempo_nao_inventa_mes_completo():
    assert np.isclose(exposicao_meses([1]).iloc[0],1/30.4375)


def test_chargeback_isolado_nao_expira_acesso():
    a,ev=fontes_minimas()
    ev.loc[2,'evento']='chargeback'
    assert estado_no_corte(a,ev,pd.Timestamp('2026-09-02')).loc['a','ativa']


def test_faixa_evento_simetrica():
    result=fase_evento(pd.Series([-61,-60,30,60,61,np.nan]))
    assert result[1]==result[2]==result[3]=='evento ±60 dias'
    assert result[0]!=result[1] and result[4]!=result[3]


def test_coorte_90d_inclui_saida_precoce_e_exclui_seguimento_incompleto():
    a=pd.DataFrame(dict(inicio=['2026-01-01','2026-01-01','2026-09-01'],
        data_fim=['2026-01-02',None,'2026-09-02'],plano_atual=['mensal']*3))
    r=proporcao_saida_90d(a,pd.Timestamp('2026-09-30')).set_index('plano').loc['mensal']
    assert r['n']==2 and r['saidas_90d']==1 and r['taxa']==.5
    assert r.ic95_inf<.5<r.ic95_sup


def test_wilson_limites_com_zero_ou_todos_eventos():
    lo,hi=wilson(0,10); assert abs(lo)<1e-12 and 0<hi<1
    lo,hi=wilson(10,10); assert 0<lo<1 and abs(hi-1)<1e-12


def test_cobertura_pesquisa_nao_duplica_motivos_financeiros():
    a=pd.DataFrame(dict(user_id=['a','b','c'],canal_cobranca=['app_store','web_cartao','web_pix'],
        motivo_fim=['falha_pagamento','chargeback','renovacao_desligada']))
    e=pd.DataFrame(dict(user_id=['a','b','c'],evento=['assinatura_expirada']*3,data_hora_br=['2026-07-01']*3))
    q=pd.DataFrame(dict(user_id=['c']))
    r=cobertura_pesquisa(a,e,q)
    assert sum(r.values())==3 and r['Web com resposta']==1
