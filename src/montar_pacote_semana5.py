"""Monta entrega local por lista explícita, com manifesto e sem dados individuais."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = '''auditar_bronze limpeza_qualidade_dados processar_eda analisar_eda_marcos
gerar_graficos_eda consolidar_semana5 metricas_semana5 executar_semana5
auditar_divergencias_semana5 atualizar_documentacao_semana5 fechar_qa_semana5
revisar_notebooks_semana5 segmentacao_clientes validar_entrega_semana5
validar_engenharia_dados montar_pacote_semana5 validar_portabilidade_semana5'''.split()
DOCS = '''plano_entrega_semana5 registro_limpeza_tratamento_dados matriz_requisitos_semana5 resolucao_mestre_semana5.template'''.split()
NOTES = ['00_gate_reprodutibilidade_bronze.md','00_pipeline_etl_data_quality.md',
         '12_consolidacao_semana5.md','13_fechamento_entrega_semana5.md']
REPORTS = ['customer_segmentation_report_semana5.md','mini_deck_eda_semana5.md',
           'eda_e_hipoteses_vitaliza.md','eda_etapa3_marcos_2026.md',
           'resolucao_case_vitaliza_semana5.md','qa_entrega_semana5.md']
FIGURES = '''churn_mensal_2025_2026 marcos_2026 correlacao_controlada outliers_por_modalidade
curva_sobrevivencia_lifetime ponto_cego_cancelamentos'''.split()
TABLES = '''churn_mensal_2025_2026 churn_mensal_por_plano_2025_2026 pesquisa_saida_cobertura
campanha_ago26_itt_30d outliers_por_modalidade correlacao_controlada cobertura_pesquisa_corrigida'''.split()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fontes_codigo(root=ROOT):
    paths = [Path('README.md'),Path('requirements-data.txt'),Path('requirements-notebooks.txt')]
    paths += [Path('src')/(s+'.py') for s in SCRIPTS]
    paths += [Path('src/verificar_html_semana5.cjs')]
    paths += [p.relative_to(root) for p in sorted((root/'tests').glob('test_*.py'))]
    paths += [Path('docs')/(d+'.md') for d in DOCS]
    paths += [Path('notebooks')/n for n in NOTES]
    paths += [p.relative_to(root) for p in sorted((root/'notebooks').glob('0[123]_*.ipynb'))]
    paths += [Path('decisoes.md')]
    paths += [p.relative_to(root) for p in sorted((root/'decisoes').glob('*.md'))]
    return paths


def limpar_notebook(raw):
    nb = json.loads(raw)
    nb['metadata'] = {k:v for k,v in nb.get('metadata',{}).items() if k in {'kernelspec','language_info'}}
    for cell in nb['cells']:
        cell['metadata'] = {}
        cell.pop('attachments',None)
        if cell['cell_type']=='code':
            cell['outputs'] = []
            cell['execution_count'] = None
    return json.dumps(nb,ensure_ascii=False,indent=1).encode('utf-8')


def conferir_apresentacoes(root=ROOT):
    folder=root/'saidas/semana5_consolidada'
    pdf=json.loads((folder/'tabelas/qa_pdf.json').read_text(encoding='utf-8'))
    visual=json.loads((folder/'tabelas/qa_visual.json').read_text(encoding='utf-8'))
    for rec in pdf:
        p=folder/rec['arquivo']
        if sha(p)!=rec['sha256'] or sha(p.with_suffix('.html'))!=rec['fonte_html_sha256']:
            raise ValueError('PDF desatualizado: '+p.name)
    for rec in visual:
        if sha(folder/rec['file'])!=rec['sha256'] or rec['horizontalOverflow']:
            raise ValueError('HTML não corresponde ao QA visual')


def conferir_manifesto(folder):
    manifest=json.loads((folder/'manifesto_sha256.json').read_text(encoding='utf-8'))
    actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file() and p.name!='manifesto_sha256.json'}
    if actual!=set(manifest):
        raise ValueError('Lista de arquivos difere do manifesto')
    for name,expected in manifest.items():
        p=(folder/name).resolve()
        if not p.is_relative_to(folder.resolve()) or sha(p)!=expected:
            raise ValueError('Falha de integridade: '+name)
    return len(actual)


def main(root=ROOT):
    conferir_apresentacoes(root)
    qa=json.loads((root/'saidas/semana5_consolidada/tabelas/qa_fechamento.json').read_text(encoding='utf-8'))
    if not qa['aprovado']:
        raise ValueError('Fechamento ainda não aprovado pelos controles locais')
    testes_aprovados=next(line.split()[0] for line in qa['testes'].splitlines() if ' passed' in line)
    dst=root/'saidas/entrega_semana5'
    files={}
    for rel in fontes_codigo(root):
        files['03_codigo_documentacao/'+rel.as_posix()]=root/rel
    for name in REPORTS:
        files['03_codigo_documentacao/saidas/'+name]=root/'saidas'/name
    for name in FIGURES:
        files['03_codigo_documentacao/saidas/'+name+'.png']=root/'saidas'/(name+'.png')
    for name in TABLES:
        files['03_codigo_documentacao/saidas/tabelas/'+name+'.csv']=root/'saidas/tabelas'/(name+'.csv')
    for name in ['qa_notebooks_semana5.json','metricas_etapa3.json']:
        files['03_codigo_documentacao/saidas/tabelas/'+name]=root/'saidas/tabelas'/name
    # Pasta dedicada contém somente apresentações e agregados; extensões e subpastas controladas.
    current=root/'saidas/semana5_consolidada'
    for p in sorted(current.rglob('*')):
        if p.is_file() and p.suffix in {'.pdf','.html','.png','.csv','.json','.txt'}:
            if p.parent not in {current,current/'tabelas'}:
                raise ValueError('Subpasta inesperada na entrega consolidada')
            files['03_codigo_documentacao/'+p.relative_to(root).as_posix()]=p
    files['01_relatorio_executivo.pdf']=current/'relatorio_executivo.pdf'
    files['02_mini_deck.pdf']=current/'mini_deck.pdf'
    files['04_validacao_final.json']=current/'tabelas/qa_fechamento.json'
    extra={'00_LEIA-ME.md','manifesto_sha256.json'}
    if dst.exists():
        unexpected={p.relative_to(dst).as_posix() for p in dst.rglob('*') if p.is_file()}-set(files)-extra
        if unexpected:
            raise ValueError('Arquivos não gerenciados no destino; não sobrescrever: '+str(sorted(unexpected)))
    for name,source in files.items():
        target=dst/name;target.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix=='.ipynb':target.write_bytes(limpar_notebook(source.read_text(encoding='utf-8')))
        else:shutil.copy2(source,target)
    (dst/'00_LEIA-ME.md').write_text(f'''# Vitaliza — entrega da Semana 5

Prazo do guia: 15/11/2026, até 23:59. Corte analítico: 30/09/2026.

**Fechamento local concluído:** {testes_aprovados} testes aprovados, três notebooks executados, 14 arquivos brutos preservados e sete tabelas analíticas equivalentes na reprodução independente. Permaneceram os mesmos 14.753 ativos, segmentos atribuídos e valores de receita da consolidação.

## Ordem de leitura
Começar pela [resolução mestre em leitura consolidada](03_codigo_documentacao/saidas/resolucao_case_vitaliza_semana5.md), que reúne contexto, método, resultados, interpretação e próximos passos em um único texto.

1. [Negócios: relatório executivo, seis páginas](01_relatorio_executivo.pdf).
2. [Tecnologia: mini deck, cinco slides](02_mini_deck.pdf).
3. [Matriz de requisitos e evidências](03_codigo_documentacao/docs/matriz_requisitos_semana5.md).
4. [Código e instruções](03_codigo_documentacao/README.md), [método](03_codigo_documentacao/notebooks/12_consolidacao_semana5.md) e [decisões](03_codigo_documentacao/decisoes.md).
5. [Validação final](04_validacao_final.json).

## Reproduzir
Abrir um terminal em `03_codigo_documentacao/`. Os notebooks 02 e 03 leem os agregados incluídos. Para recalcular desde a origem, obter as 12 tabelas e os dois ZIPs de heatmaps do data room autorizado e colocá-los em `dados/brutos/`, conforme o contrato de `src/auditar_bronze.py`. Executar os comandos do README. Essa distribuição contém código e agregados; não contém linhas individuais, GPS ou textos do case. Notebooks foram entregues sem outputs individuais.

Os scripts legados de validação/segmentação permanecem apenas onde testes os importam. A entrada vigente é `src/executar_semana5.py`. Não executar geradores antigos em paralelo. As ADRs preservam autoria e histórico; ADRs 020/021 definem a entrega atual.

## Ressalvas
Quatro perdas de abril divergem do enunciado; cinco estados de renovação divergem entre eventos e cadastro. A auditoria está incluída. Texto sem validação humana não orienta ações. As ações são hipóteses; nenhuma campanha foi executada. Modelo supervisionado, GenAI e ROI final são escopo da Semana 10.

## Envio
Enviar o conteúdo desta pasta ao Drive, mantendo os dois PDFs visíveis para pré-visualização. Compartilhar a pasta e os arquivos conforme o guia. Conferir o acesso por uma sessão sem login. Cada aluno submete o link da pasta na Adalove. O ZIP é uma cópia transportável; não substitui o link público da pasta. Nenhuma publicação/submissão foi feita automaticamente.

O manifesto lista SHA-256 de cada arquivo. No projeto de código, `python -c "from pathlib import Path; from src.montar_pacote_semana5 import conferir_manifesto; print(conferir_manifesto(Path('..')))"` confere a integridade do pacote.
''',encoding='utf-8')
    manifest={p.relative_to(dst).as_posix():sha(p) for p in sorted(dst.rglob('*')) if p.is_file() and p.name!='manifesto_sha256.json'}
    (dst/'manifesto_sha256.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    n=conferir_manifesto(dst)
    archive=root/'saidas/entrega_semana5.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dst.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(dst).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist())==n+1
    print(f'Pacote pronto: {n} arquivos + manifesto; ZIP {archive.stat().st_size:,} bytes')


if __name__=='__main__':main()
