"""Publica navegação e notebooks da ADR 020; arquiva versões superadas explicitamente."""
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def escrever(path,texto):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(texto,encoding='utf-8')


def arquivar(rel):
    # O pacote de entrega funciona sem Git e sem o histórico do repositório.
    if not (ROOT/'.git').exists():
        return
    destino=ROOT/'saidas/historico_antes_adr020'/rel
    if not destino.exists():
        r=subprocess.run(['git','show',f'abfac49:{rel}'],cwd=ROOT,capture_output=True)
        if r.returncode==0:
            destino.parent.mkdir(parents=True,exist_ok=True)
            destino.write_bytes('> HISTORICO SUPERADO PELA ADR 020. Contém resultados/interpretações não vigentes. Não usar na entrega.\n\n'.encode('utf-8')+r.stdout)


def notebook(nome,titulo,tabela,imagem):
    cells=[dict(cell_type='markdown',metadata={},source=[f'# {titulo}\n','Versão consolidada, ADR 020. Leia notebooks/12_consolidacao_semana5.md.\n',
            'Este notebook consome agregados; a reprodução do processamento é feita pelo pipeline. Não contém amostras individuais.']),
           dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=[
               'from pathlib import Path\nimport pandas as pd\nfrom IPython.display import display, Image\n',
               'ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()\n',
               f'df = pd.read_csv(ROOT / "saidas/semana5_consolidada/tabelas/{tabela}")\n',
               'display(df)\n',f'display(Image(filename=str(ROOT / "saidas/semana5_consolidada/{imagem}")))'])]
    for i,c in enumerate(cells):c['id']=f'adr020-{i}'
    extras = [('perfil_personas.csv','Carteira atual: contagens, exposição e receita equivalente.'),
              ('selecao_k.csv','Comparar k por separação, tamanho e parcimônia, sem selecionar pelo churn.'),
              ('prioridades.csv','Regras operacionais; não equivalem a classes causais de uplift.')] if nome.startswith('03') else [
              ('coorte_90d.csv','Entradas com 90 dias completos: inclui saídas precoces. Não é a taxa mensal da empresa.'),
              ('coortes_60d.csv','Modelo de maio aplicado a julho: atributos observados antes do desfecho. Filtrar população e plano antes de comparar.'),
              ('cenarios_financeiros.csv','Cenários hipotéticos do piloto; não estimativa de retorno observado.')]
    for i,(tab,nota) in enumerate(extras,2):
        cells.append(dict(cell_type='markdown',metadata={},id=f'adr020-nota-{i}',source=[nota]))
        cells.append(dict(cell_type='code',metadata={},execution_count=None,outputs=[],id=f'adr020-tab-{i}',
            source=[f'display(pd.read_csv(ROOT / "saidas/semana5_consolidada/tabelas/{tab}"))']))
    if nome.startswith('02'):
        for i,(tab,fig,nota) in enumerate([
            ('churn_mensal_2025_2026.csv','churn_mensal_2025_2026.png','Série mensal: investigar o reajuste de março sem atribuir causalidade à tendência.'),
            ('pesquisa_saida_cobertura.csv','marcos_2026.png','Marcos de março, junho e agosto: cobertura e denominadores precisam ser comparáveis.')],10):
            cells.append(dict(cell_type='markdown',metadata={},id=f'adr021-nota-{i}',source=[nota]))
            cells.append(dict(cell_type='code',metadata={},execution_count=None,outputs=[],id=f'adr021-tab-{i}',source=[
                f'display(pd.read_csv(ROOT / "saidas/tabelas/{tab}"))\n',
                f'display(Image(filename=str(ROOT / "saidas/{fig}")))']))
    escrever('notebooks/'+nome,json.dumps(dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3')),nbformat=4,nbformat_minor=5),ensure_ascii=False,indent=1))


def main():
    antigos=['saidas/customer_segmentation_report_semana5.md','saidas/mini_deck_eda_semana5.md',
             'saidas/eda_e_hipoteses_vitaliza.md','saidas/resolucao_case_vitaliza_semana5.md',
             'saidas/base_inteira/customer_segmentation_report_base_inteira.md','saidas/base_inteira/mini_deck_base_inteira.md',
             'saidas/base_inteira/pontos_de_atencao.md','notebooks/10_segmentacao_base_inteira.md','notebooks/11_personas_k3_deck_executivo.md']
    for p in antigos:arquivar(p)
    escrever('saidas/historico_antes_adr020/LEIA-ME.md','# Arquivo histórico\n\nVersões preservadas do commit abfac49. Contêm inconsistências e interpretações corrigidas. Não usar como fonte atual; links relativos internos são os da versão antiga e podem não resolver neste arquivo histórico. A entrega válida está em ../semana5_consolidada/ e nos relatórios atuais de saidas/.\n')
    for p in antigos[4:]:
        prefix='../' if p.startswith('notebooks/') else '../../' if '/base_inteira/' in p else '../'
        destino=prefix+'saidas/customer_segmentation_report_semana5.md' if p.startswith('notebooks/') else '../customer_segmentation_report_semana5.md'
        metodo='12_consolidacao_semana5.md' if p.startswith('notebooks/') else '../../notebooks/12_consolidacao_semana5.md'
        escrever(p,f'# Versão superada pela consolidação ADR 020\n\nO conteúdo anterior está preservado em `saidas/historico_antes_adr020/{p}` e no commit abfac49. Não misturar os números da proposta k=4 ou k=3 histórica com a janela consolidada de 84 dias.\n\n[Relatório vigente]({destino}) · [Método]({metodo})\n')
    escrever('saidas/eda_e_hipoteses_vitaliza.md','''# EDA — interpretação consolidada, ADR 020

O relatório antigo foi arquivado em historico_antes_adr020. As alegações de sobrevivência, "comprovação" de causalidade e efeitos protetores foram retiradas.

## Coorte de entrada
`semana5_consolidada/tabelas/coorte_90d.csv` inclui entradas desde 2025 com 90 dias completos até setembro. Saída precoce permanece no denominador. Não é uma curva Kaplan–Meier nem o churn mensal da empresa.

![Saída em 90 dias](curva_sobrevivencia_lifetime.png)

## Pesquisa
As categorias de canal/resposta são mutuamente exclusivas. Cancelamento involuntário é outra dimensão, não uma fatia adicional da mesma pizza. A janela junho–setembro corresponde ao período de existência da pesquisa.

![Cobertura](ponto_cego_cancelamentos.png)

## Associação não é previsão
As AUCs retrospectivas antigas não são desempenho prospectivo; seus atributos têm janelas condicionadas ao desfecho e cobertura desigual. Não devem alimentar a previsão da Semana 10 sem reconstrução temporal. A análise vigente mede cinco atributos antes do seguimento em coortes comuns, conforme `notebooks/12_consolidacao_semana5.md`.

## Hipóteses
Formação de hábito, continuidade de objetivos e relevância de conteúdo permanecem hipóteses. Nenhuma é "comprovada" por AUC, diferença descritiva ou comparação por duração. Declaração de não significância tampouco é equivalência.

## Evidências vigentes
[Relatório de negócios](customer_segmentation_report_semana5.md) · [Mini deck](mini_deck_eda_semana5.md) · [Marcos](eda_etapa3_marcos_2026.md).
''')
    escrever('saidas/resolucao_case_vitaliza_semana5.md',
             (ROOT/'docs/resolucao_mestre_semana5.template.md').read_text(encoding='utf-8'))
    notebook('02_eda_e_hipoteses.ipynb','EDA temporal e experimento','campanha.csv','campanha.png')
    notebook('03_segmentacao_clusters.ipynb','Segmentos e avaliação histórica','coortes_60d.csv','coorte_60d.png')


if __name__=='__main__':main()
