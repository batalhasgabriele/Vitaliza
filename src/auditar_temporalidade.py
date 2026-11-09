"""Diagnóstico agregado de exposição e regras ambíguas; não altera populações."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    prata = ROOT / 'dados/processados/prata'
    usr = pd.read_parquet(prata/'usuarios_limpo.parquet')
    ass = pd.read_parquet(prata/'assinaturas_limpas.parquet')
    atv = pd.read_parquet(prata/'atividades_limpas.parquet')
    pag = pd.read_parquet(prata/'pagamentos_limpos.parquet')
    corte = pd.Timestamp('2026-09-30 23:59:59')
    vinculadas = atv[['user_id','inicio_dt_br']].merge(ass[['user_id','inicio']], on='user_id', validate='many_to_one')
    antes = pd.to_datetime(vinculadas.inicio_dt_br) < pd.to_datetime(vinculadas.inicio)
    ativos = ass.loc[ass.status_atual.eq('ativa')]
    pares = pag.loc[pag.status.eq('aprovado')].groupby(['user_id','valor_num','dia_br']).size()
    out = {
        'corte': str(corte),
        'cadastros_apos_corte': int(usr.flag_cadastro_apos_corte.sum()),
        'atividades_vinculadas_anteriores_assinatura': int(antes.sum()),
        'usuarios_com_atividade_antes_assinatura': int(vinculadas.loc[antes,'user_id'].nunique()),
        'ativos_com_menos_90_dias_assinatura': int(((corte-pd.to_datetime(ativos.inicio)).dt.total_seconds()/86400 < 90).sum()),
        'grupos_pagamento_aprovado_mesmo_usuario_valor_dia': int((pares>1).sum()),
        'flags_pagamento_duplicado': int(pag.flag_duplicata_aprovada_dia.sum()),
        'observacao': 'Atividade antes da assinatura pode ser freemium legítimo; não excluída. Grupos de pagamento são candidatos segundo a regra atual, não ciclos comprovados. Nenhum dado foi alterado.'
    }
    (ROOT/'saidas/tabelas/auditoria_temporal_engenharia.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    main()
