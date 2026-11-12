"""Investiga diferenças de fonte sem alterar dados; publica somente agregados."""
from pathlib import Path
import json
import pandas as pd
from metricas_semana5 import estado_no_corte

ROOT = Path(__file__).resolve().parents[1]


def auditar(root=ROOT):
    prata = root / 'dados/processados/prata'
    a = pd.read_parquet(prata / 'assinaturas_limpas.parquet')
    e = pd.read_parquet(prata / 'eventos_assinatura_limpos.parquet')
    e['data_hora_br'] = pd.to_datetime(e.data_hora_br)
    estado = estado_no_corte(a, e, pd.Timestamp('2026-09-30 23:59:59'))
    snap = a.set_index('user_id').renovacao_automatica.eq('sim')
    ids = estado.index[estado.ativa & estado.renovacao_ligada.ne(snap)]
    ult = e[e.user_id.isin(ids)].sort_values('data_hora_br').groupby('user_id').tail(1)
    toggles = e[e.user_id.isin(ids) & e.evento.str.contains('renovacao_automatica')]
    ultimo_toggle=toggles.groupby('user_id').data_hora_br.max()
    renovou_apos_toggle=e[e.user_id.isin(ids) & e.evento.eq('renovacao') &
        e.data_hora_br.gt(e.user_id.map(ultimo_toggle))].user_id.nunique()
    exp = e[e.evento.eq('assinatura_expirada')]
    abril = exp[exp.data_hora_br.ge('2026-04-01') & exp.data_hora_br.lt('2026-05-01')]
    fim = pd.to_datetime(a.data_fim)
    raw = pd.read_csv(root / 'dados/brutos/eventos_assinatura.csv')
    raw_abril = raw[raw.evento.eq('assinatura_expirada') & raw.data_hora.str.startswith('2026-04')]
    res = dict(
        renovacao=dict(divergentes=len(ids),
            snapshot_ligada=int(snap.reindex(ids).sum()),
            eventos_ligada=int(estado.loc[ids,'renovacao_ligada'].sum()),
            renovaram_apos_ultimo_toggle=int(renovou_apos_toggle),
            ultimo_evento=ult.evento.value_counts().to_dict(),
            toggles_por_tipo=toggles.evento.value_counts().to_dict()),
        abril=dict(enunciado=1154,expiracoes_br=len(abril),usuarios_distintos=abril.user_id.nunique(),
            snapshot_data_fim_abril=int((fim.ge('2026-04-01') & fim.lt('2026-05-01')).sum()),
            eventos_brutos_mes_textual=len(raw_abril),
            internos_nos_brutos=int((~raw_abril.user_id.isin(a.user_id)).sum()),
            planos=abril.plano.value_counts().to_dict(),
            motivos=abril.detalhe.fillna('sem detalhe').value_counts().to_dict()))
    out = root / 'saidas/semana5_consolidada/tabelas/auditoria_divergencias.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(res,ensure_ascii=False,indent=2,default=int),encoding='utf-8')
    return res


if __name__ == '__main__':
    print(json.dumps(auditar(),ensure_ascii=False,indent=2,default=int))
