"""Atualiza apresentação e comparação de impacto sem reajustar os modelos."""
from pathlib import Path
import json
import hashlib
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from consolidar_semana5 import documentos, TAB, ROOT


def main():
    ler=lambda n:pd.read_csv(TAB/f'{n}.csv')
    qa=json.loads((TAB/'qa.json').read_text(encoding='utf-8'))
    documentos(ler('perfil_personas'),ler('coortes_60d'),ler('campanha'),ler('selecao_k'),qa,ler('prioridades'),ler('cenarios_financeiros'),ler('coorte_90d'))
    new=pd.read_parquet(ROOT/'dados/processados/ouro/segmentos_consolidados_set2026.parquet').set_index('user_id')
    assert new.index.is_unique
    baseline=ROOT/'dados/processados/ouro/segmentos_ativos_set2026.parquet'
    ari=None
    if baseline.exists():
        old=pd.read_parquet(baseline).set_index('user_id')
        assert set(old.index)==set(new.index)
        cruz=pd.crosstab(old.segmento,new.persona)
        cruz.to_csv(TAB/'comparacao_segmentacao_anterior.csv')
        ari=adjusted_rand_score(old.segmento,new.persona.reindex(old.index))
    proposta=ROOT/'saidas/deck_executivo/tabelas/perfil_personas.csv'
    newp=ler('perfil_personas').set_index('persona')
    impacto=pd.DataFrame({'consolidada_84d':newp.ativos})
    if proposta.exists():
        oldp=pd.read_csv(proposta,index_col=0)
        impacto.insert(0,'proposta_11nov',oldp.ativos.reindex(newp.index))
        impacto['diferenca']=impacto.consolidada_84d-impacto.proposta_11nov
        impacto.to_csv(TAB/'comparacao_proposta_11nov.csv')
    met=dict(populacao_preservada=True if baseline.exists() else None,ativos=len(new),ari_vs_16_atributos=ari,
             comparacao_individual='executada' if baseline.exists() else 'base historica opcional ausente',
             motivo_mudanca='Janela comum 84 dias; cinco variáveis; regularidade nos logs de todas as origens; estados por eventos.',
             fontes_codigo={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'src/consolidar_semana5.py',ROOT/'src/metricas_semana5.py']})
    (TAB/'impacto.json').write_text(json.dumps(met,ensure_ascii=False,indent=2),encoding='utf-8')
    comparacao=(f'População preservada frente à base antiga; ARI versus 16 atributos: **{ari:.3f}**. Isso é concordância, não qualidade absoluta.'
                if ari is not None else 'Base histórica individual não fornecida: comparação com a versão antiga não executada. Isso não impede a reprodução da entrega atual.')
    texto=f'''# QA e impacto — Semana 5 consolidada

## Resultado
Entrega local consolidada na dev (ADR 020). Relatório HTML de seis seções, mini deck HTML de cinco slides e fontes Markdown gerados dos mesmos agregados.

## O que mudou nos resultados
População atual: **{len(new):,} ativos únicos**. {comparacao}

{impacto.to_markdown()}

A mudança foi deliberada: janela comum de 84 dias, cinco atributos, regularidade pelos logs e exposição explícita. A proposta de 11/11 usava a vigência de janeiro até saída/corte. Não atribuir a diferença a perda de linhas por limpeza.

## Controles executados
- Runner completo Bronze → Prata → EDA → marcos → gráficos → consolidação → documentação, com logs em dados/execucoes_engenharia/. Resultado em `semana5_consolidada/tabelas/qa_pipeline.json`.
- Os 14 hashes Bronze foram preservados; Prata reproduzida byte a byte.
- A execução completa reproduziu as tabelas analíticas da primeira consolidação. Depois, a apresentação foi refinada e o IC do controle contra ele próprio foi fixado em zero; contagens, taxas e comparações dos tratamentos permaneceram iguais. Os modelos não foram reajustados nessas alterações finais. `qa_pipeline.json` preserva o retrato daquela execução; `qa_testes.txt`, `qa_visual.json` e `impacto.json` registram as verificações finais correspondentes.
- Testes semânticos de estados, futuro, exposição, coorte, intervalos e partição da pesquisa, além dos testes anteriores. Registro final em `semana5_consolidada/tabelas/qa_testes.txt`.
- Notebooks: registro em `tabelas/qa_notebooks_semana5.json`; consomem agregados e não substituem o runner.
- HTML: ver `semana5_consolidada/tabelas/qa_visual.json`; revisão de seções com screenshots locais, imagens carregadas e sem overflow horizontal.
- PDF: seis páginas de relatório e cinco slides exportados, todas as páginas renderizadas e inspecionadas. Registro da exportação em `semana5_consolidada/tabelas/qa_pdf.json`. PDFs requerem reexportação após alterações nos HTML, conforme README.

## Resultados estatísticos
Silhueta k=3 de 0,350 e cinco reamostragens bootstrap de todo pré-processamento com ARI médio {qa['bootstrap_ari_medio']:.3f}. É uma verificação exploratória de estabilidade, não prova de generalização. Coortes em maio/julho: modelo de maio congelado ao avaliar julho; todos os provisórios elegíveis permanecem nos desfechos. Taxas e incerteza em `coortes_60d.csv`.

Campanha principal reproduz controle 5,48%, cupom 4,64%, desafio 5,18% e conteúdo 6,13% de expiração em 30 dias. Sensibilidades estão separadas por plano, desfecho e horizonte. Não identificam efeito individual.

## Limites não encerrados por software
Abril: eventos e cadastro concordam em 1.158 perdas, contra 1.154 do enunciado; não são duplicatas. Nos cinco estados de renovação divergentes, há renovação após o último desligamento sem religamento explícito. A causa do conflito exige confirmação da fonte. Auditoria em `semana5_consolidada/tabelas/auditoria_divergencias.json`. A regra financeira usuário/valor/dia ainda aproxima o ciclo; extração de objetivos textuais não tem amostra humana validada e permanece fora das decisões operacionais. Histórico observado sob intervenções reais não é risco natural sem tratamento. Plano/canal sem evento usam fallback cadastral. Não há target de setembro observado até novembro.

## Entrega externa
Publicação no Drive, verificação de permissões e submissão na Adalove não foram realizadas. Não copiar dados individuais nem a pasta histórica para o pacote público. Começar por `../README.md`.
'''
    (ROOT/'saidas/qa_entrega_semana5.md').write_text(texto,encoding='utf-8')
    print(impacto.to_string());print('ARI',ari)

if __name__=='__main__':main()
