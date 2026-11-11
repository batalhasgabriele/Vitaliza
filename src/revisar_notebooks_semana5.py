"""Executa notebooks em kernels isolados, sem persistir outputs de dados pessoais."""
from pathlib import Path
import json
import hashlib
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    resultados = []
    for path in sorted((ROOT / 'notebooks').glob('0[123]_*.ipynb')):
        nb = nbformat.read(path, as_version=4)
        NotebookClient(nb, timeout=600, kernel_name='python3', resources={'metadata': {'path': str(ROOT / 'notebooks')}}).execute()
        resultados.append({'notebook': path.name, 'status': 'executado_sem_erros',
                           'celulas_codigo': sum(c.cell_type == 'code' for c in nb.cells),
                           'sha256_fonte': hashlib.sha256(path.read_bytes()).hexdigest()})
        print(path.name, 'OK', flush=True)
    (ROOT / 'saidas/tabelas/qa_notebooks_semana5.json').write_text(json.dumps(resultados, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
