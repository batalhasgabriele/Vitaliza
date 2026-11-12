"""Runner local auditável: Bronze → Prata → análises → entrega. Não publica externamente."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]

def hashes(p):
    return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest()
            for x in sorted(p.rglob('*')) if x.is_file() and x.name not in {'qa_pipeline.json','qa_visual.json','qa_testes.txt'}}

def main():
    run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    logs=ROOT/'dados/execucoes_engenharia'/('semana5_'+run);logs.mkdir(parents=True)
    bronze=hashes(ROOT/'dados/brutos'); prata=hashes(ROOT/'dados/processados/prata')
    old=hashes(ROOT/'saidas/semana5_consolidada')
    etapas=[]
    env=os.environ.copy();env['PYTHONIOENCODING']='utf-8';env['OMP_NUM_THREADS']='2';env['OPENBLAS_NUM_THREADS']='2'
    scripts=['auditar_bronze','limpeza_qualidade_dados','processar_eda','analisar_eda_marcos',
             'gerar_graficos_eda','consolidar_semana5','auditar_divergencias_semana5',
             'atualizar_documentacao_semana5','fechar_qa_semana5']
    for script in scripts:
        print(f'Executando {script}',flush=True)
        with (logs/f'{script}.log').open('w',encoding='utf-8') as log:
            r=subprocess.run([sys.executable,str(ROOT/'src'/f'{script}.py')],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        etapas.append(dict(script=script,codigo=r.returncode))
        if r.returncode:raise RuntimeError(f'Falha em {script}; veja {logs}')
    with (logs/'pytest.log').open('w',encoding='utf-8') as log:
        r=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
    assert r.returncode==0,f'Testes falharam: {logs}'
    (ROOT/'saidas/semana5_consolidada/tabelas/qa_testes.txt').write_text((logs/'pytest.log').read_text(encoding='utf-8'),encoding='utf-8')
    assert bronze==hashes(ROOT/'dados/brutos'),'Bronze alterada'
    novo=hashes(ROOT/'saidas/semana5_consolidada')
    qa=dict(run_id=run,etapas=etapas,bronze_inalterada=True,arquivos_bronze=len(bronze),
            prata_hashes_iguais=prata==hashes(ROOT/'dados/processados/prata'),
            testes=(logs/'pytest.log').read_text(encoding='utf-8').strip(),
            saidas_alteradas=[x for x in novo if novo[x]!=old.get(x)],hashes_saidas=novo)
    (ROOT/'saidas/semana5_consolidada/tabelas/qa_pipeline.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in qa.items() if k!='hashes_saidas'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
