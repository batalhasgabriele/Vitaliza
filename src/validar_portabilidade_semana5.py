"""Executa a entrega em diretório independente, com cópia privada da Bronze."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import pandas as pd
from montar_pacote_semana5 import fontes_codigo, sha

ROOT=Path(__file__).resolve().parents[1]
ANALITICAS=['perfil_personas','coortes_60d','campanha','selecao_k','prioridades','cenarios_financeiros','coorte_90d']


def main():
    run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stage=ROOT/'dados/execucoes_engenharia'/('fechamento_'+run)
    stage.mkdir(parents=True)
    raw=ROOT/'dados/brutos'
    bronze={p.relative_to(raw).as_posix():sha(p) for p in sorted(raw.rglob('*')) if p.is_file()}
    for rel in fontes_codigo():
        p=stage/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
    shutil.copytree(raw,stage/'dados/brutos')
    # Sem Prata, Ouro, relatórios históricos ou .git na inicialização.
    env=os.environ.copy();env.update(PYTHONIOENCODING='utf-8',OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2')
    for script in ['executar_semana5.py','revisar_notebooks_semana5.py']:
        print('Reprodução independente:',script,flush=True)
        with (stage/(script+'.log')).open('w',encoding='utf-8') as log:
            p=subprocess.run([sys.executable,str(stage/'src'/script)],cwd=stage,env=env,stdout=log,stderr=subprocess.STDOUT)
        if p.returncode:raise RuntimeError(f'Falha em {script}; log em {stage}')
    tab=Path('saidas/semana5_consolidada/tabelas')
    iguais=[]
    for name in ANALITICAS:
        pd.testing.assert_frame_equal(pd.read_csv(ROOT/tab/(name+'.csv')),pd.read_csv(stage/tab/(name+'.csv')),
                                      check_dtype=False,rtol=1e-10,atol=1e-10)
        iguais.append(name)
    gold=Path('dados/processados/ouro/segmentos_consolidados_set2026.parquet')
    before=pd.read_parquet(ROOT/gold).sort_values('user_id').reset_index(drop=True)
    after=pd.read_parquet(stage/gold).sort_values('user_id').reset_index(drop=True)
    pd.testing.assert_frame_equal(before,after,check_dtype=False,rtol=1e-10,atol=1e-10)
    prata=ROOT/'dados/processados/prata'
    prata_igual=all(sha(p)==sha(stage/'dados/processados/prata'/p.name) for p in prata.glob('*.parquet'))
    assert prata_igual
    assert bronze=={p.relative_to(raw).as_posix():sha(p) for p in sorted(raw.rglob('*')) if p.is_file()}
    assert bronze=={p.relative_to(stage/'dados/brutos').as_posix():sha(p) for p in (stage/'dados/brutos').rglob('*') if p.is_file()}
    notebook_qa=json.loads((stage/'saidas/tabelas/qa_notebooks_semana5.json').read_text())
    assert len(notebook_qa)==3
    assert all(sha(ROOT/'notebooks'/x['notebook'])==x['sha256_fonte'] for x in notebook_qa)
    testes=(stage/tab/'qa_testes.txt').read_text(encoding='utf-8')
    result=dict(aprovado=True,run_id=run,sem_git=True,sem_prata_inicial=True,sem_base_historica=True,
        arquivos_bronze_preservados=len(bronze),prata_identica=True,ativos=len(after),
        atribuicoes_e_receita_preservadas=True,tabelas_equivalentes=iguais,
        testes=testes.strip(),notebooks=notebook_qa,
        fontes={str(p):sha(ROOT/p) for p in fontes_codigo()},
        limitacoes=['Fonte abril 1.154 vs 1.158','Cinco estados de renovação divergentes',
                    'Texto sem validação humana fora das ações','Publicação e submissão não realizadas'])
    (ROOT/tab/'qa_fechamento.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copy2(stage/tab/'qa_testes.txt',ROOT/tab/'qa_testes.txt')
    shutil.copy2(stage/'saidas/tabelas/qa_notebooks_semana5.json',ROOT/'saidas/tabelas/qa_notebooks_semana5.json')
    print(json.dumps({k:v for k,v in result.items() if k not in {'fontes','notebooks'}},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
