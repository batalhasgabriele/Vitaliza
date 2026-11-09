"""Valida Prata e migração da EDA em staging, sem publicar diferenças silenciosas."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
KEYS = {
    'usuarios_limpo': ['user_id'], 'assinaturas_limpas': ['assinatura_id'],
    'onboarding_limpo': ['onboarding_id'], 'atividades_limpas': ['atividade_id'],
    'pagamentos_limpos': ['pagamento_id'], 'uso_mensal_limpo': ['user_id', 'mes'],
    'campanha_ago26_limpa': ['user_id'], 'pesquisa_saida_limpa': ['resposta_id'],
    'feed_posts_limpos': ['post_id'], 'tickets_suporte_limpos': ['ticket_id'],
    'amizades_limpas': ['seguidor_id', 'seguido_id'],
    'eventos_assinatura_limpos': None,
}


def comparar(a, b):
    """Compara conteúdo por chave; tolerância numérica evita ruído de ponto flutuante."""
    if not a.user_id.is_unique or not b.user_id.is_unique:
        raise ValueError('user_id precisa ser único para comparar')
    a, b = a.set_index('user_id').sort_index(), b.set_index('user_id').sort_index()
    if not a.index.equals(b.index):
        return {'populacao_igual': False, 'colunas_alteradas': ['populacao']}
    alteradas = []
    for col in sorted(set(a.columns) | set(b.columns)):
        if col not in a or col not in b:
            alteradas.append(col)
            continue
        x, y = a[col], b[col]
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            igual = np.isclose(x.astype(float), y.astype(float), rtol=1e-10, atol=1e-10, equal_nan=True).all()
        else:
            igual = ((x.eq(y)) | (x.isna() & y.isna())).fillna(False).all()
        if not igual:
            alteradas.append(col)
    return {'populacao_igual': True, 'colunas_alteradas': alteradas}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publicar', action='store_true', help='Publica somente EDA sem diferenças e sem blockers')
    args = parser.parse_args()
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8]
    stage = ROOT / 'dados/execucoes_engenharia' / run_id
    stage.mkdir(parents=True)
    prata = ROOT / 'dados/processados/prata'
    shutil.copytree(prata, stage / 'dados/processados/prata')
    (stage / 'dados/processados/ouro').mkdir(parents=True)
    usuarios = pd.read_parquet(prata / 'usuarios_limpo.parquet')
    validos = set(usuarios.user_id)
    checks = []
    contratos = []
    for nome, keys in KEYS.items():
        df = pd.read_parquet(prata / (nome + '.parquet'))
        contratos.append({'tabela': nome, 'linhas': len(df), 'chave_candidata': keys,
                         'schema': {c: str(t) for c, t in df.dtypes.items()}})
        key_bad = keys and (df[keys].isna().any().any() or df.duplicated(keys).any())
        checks.append({'tabela': nome, 'teste': 'chave_candidata',
                       'status': 'BLOCKER' if key_bad else ('PASS' if keys else 'WARNING'),
                       'detalhe': 'Sem identificador de evento: chave composta requer decisão' if keys is None else ''})
        for col in ['user_id', 'seguidor_id', 'seguido_id']:
            if col in df:
                n = int((~df[col].isin(validos)).sum())
                checks.append({'tabela': nome, 'teste': 'referencia_' + col,
                               'status': 'BLOCKER' if n else 'PASS', 'quantidade': n})
    baseline = ROOT / 'dados/validacao_engenharia_baseline/ouro/features_eda_corte_set2026.parquet'
    atual = ROOT / 'dados/processados/ouro/features_eda_corte_set2026.parquet'
    if not baseline.exists():
        raise ValueError('Baseline ausente: salvar a versão anterior antes de validar')
    resultados = []
    primeira = None
    for tentativa in (1, 2):
        with (stage / f'eda_{tentativa}.log').open('w', encoding='utf-8') as log:
            subprocess.run([sys.executable, str(ROOT / 'src/processar_eda.py')], cwd=stage,
                           stdout=log, stderr=subprocess.STDOUT, check=True)
        df = pd.read_parquet(stage / 'dados/processados/ouro/features_eda_corte_set2026.parquet')
        resultados.append(comparar(pd.read_parquet(baseline), df))
        if primeira is None:
            primeira = df.copy()
        else:
            idempotencia = comparar(primeira, df)
    # Demais resultados oficiais não são regenerados por esta migração; verificar conservação.
    conservados = []
    for pasta, destino in [('ouro', ROOT / 'dados/processados/ouro'), ('tabelas', ROOT / 'saidas/tabelas')]:
        for p in (ROOT / 'dados/validacao_engenharia_baseline' / pasta).iterdir():
            outro = destino / p.name
            conservados.append({'arquivo': pasta + '/' + p.name,
                'hash_igual': outro.exists() and hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(outro.read_bytes()).digest()})
    aprovado = (not any(c['status'] == 'BLOCKER' for c in checks)
                and all(not r['colunas_alteradas'] for r in resultados)
                and not idempotencia['colunas_alteradas'])
    publicado = False
    if args.publicar and aprovado:
        temp = atual.with_suffix('.tmp.parquet')
        shutil.copy2(stage / 'dados/processados/ouro/features_eda_corte_set2026.parquet', temp)
        temp.replace(atual)
        publicado = True
    report = dict(run_id=run_id, codigo_sha256=hashlib.sha256((ROOT/'src/processar_eda.py').read_bytes()).hexdigest(),
                  entradas_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in prata.glob('*.parquet')},
                  checks=checks, contratos_observados=contratos, comparacao_baseline=resultados,
                  idempotencia=idempotencia, conservacao_antes_publicacao=conservados,
                  aprovado=aprovado, publicado=publicado)
    (stage / 'resultado.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    out = ROOT / 'saidas/tabelas/qa_engenharia_dados.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ['run_id','comparacao_baseline','idempotencia','aprovado','publicado']}, ensure_ascii=False))
    print('Blockers:', [c for c in checks if c['status']=='BLOCKER'])
    if args.publicar and not aprovado:
        raise SystemExit('Publicação bloqueada; resultados oficiais preservados')


if __name__ == '__main__':
    main()
