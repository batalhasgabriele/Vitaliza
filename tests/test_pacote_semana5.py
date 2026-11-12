from pathlib import Path
import hashlib
import json
import sys
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from montar_pacote_semana5 import limpar_notebook, conferir_manifesto


def test_notebook_publico_preserva_codigo_sem_outputs_ou_metadados_privados():
    nb=dict(cells=[dict(cell_type='code',source=['print(1)'],metadata={'path':'privado'},
        outputs=[{'text':'registro individual'}],execution_count=1)],metadata={'widgets':{'dado':'privado'}})
    clean=json.loads(limpar_notebook(json.dumps(nb)))
    assert clean['cells'][0]['source']==['print(1)']
    assert clean['cells'][0]['outputs']==[] and clean['cells'][0]['metadata']=={}
    assert clean['metadata']=={}


def test_manifesto_detecta_arquivo_modificado(tmp_path):
    p=tmp_path/'relatorio.txt';p.write_bytes(b'original')
    (tmp_path/'manifesto_sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()}))
    assert conferir_manifesto(tmp_path)==1
    p.write_bytes(b'modificado')
    with pytest.raises(ValueError,match='integridade'):conferir_manifesto(tmp_path)


def test_manifesto_rejeita_arquivo_extra(tmp_path):
    (tmp_path/'manifesto_sha256.json').write_text('{}')
    (tmp_path/'dados_individuais.csv').write_text('user_id')
    with pytest.raises(ValueError,match='Lista de arquivos'):conferir_manifesto(tmp_path)
