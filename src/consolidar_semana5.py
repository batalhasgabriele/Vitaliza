"""Entrega autoritativa Semana 5, ADR 020. Lê Prata; publica apenas agregados.

python src/consolidar_semana5.py
Modelos de segmentos são descritivos. Coorte de maio ajusta transformações/K-Means
antes de observar saídas; julho é projetado no mesmo modelo. Setembro tem ajuste
próprio para descrever carteira atual. Nenhum target participa da escolha de k.
"""
from __future__ import annotations
import base64
import hashlib
import html
import json
import os
from pathlib import Path
from statistics import NormalDist

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler

from metricas_semana5 import estado_no_corte, wilson, diferenca_proporcoes, proporcao_saida_90d

ROOT = Path(__file__).resolve().parents[1]
PRATA = ROOT / "dados/processados/prata"
OUT = ROOT / "saidas/semana5_consolidada"
TAB = OUT / "tabelas"
CORTE = pd.Timestamp("2026-09-30 23:59:59")
COLS = ["dias_semana_pretendidos", "treinos_mes", "regularidade", "n_modalidades", "pct_ar_livre"]
NOMES = ["Atleta ao Ar Livre", "Treino em Casa Guiado", "Hábito Fraco"]


def ler(nome):
    return pd.read_parquet(PRATA / f"{nome}.parquet")


def fontes():
    a, ev, at, onb = (ler(x) for x in ["assinaturas_limpas", "eventos_assinatura_limpos", "atividades_limpas", "onboarding_limpo"])
    assert a.user_id.is_unique
    a["inicio"] = pd.to_datetime(a.inicio)
    ev["data_hora_br"] = pd.to_datetime(ev.data_hora_br)
    at["inicio_dt_br"] = pd.to_datetime(at.inicio_dt_br)
    onb["respondido_em"] = pd.to_datetime(onb.respondido_em)
    return a, ev, at, onb


def atributos(a, ev, at, onb, corte):
    """84 dias de calendário, limitados à assinatura. Recém-chegados são provisórios."""
    estado = estado_no_corte(a, ev, corte)
    b = a.set_index("user_id").loc[estado.index[estado.ativa], ["inicio"]].copy()
    b = b.join(estado[["plano", "canal_cobranca", "renovacao_ligada"]])
    inicio_janela = corte.normalize() - pd.Timedelta(days=83)
    b["inicio_observacao"] = b.inicio.clip(lower=inicio_janela)
    b["dias_observados"] = (corte.normalize()-b.inicio_observacao.dt.normalize()).dt.days+1
    b["provisorio"] = b.dias_observados.lt(30)
    t = at[at.user_id.isin(b.index) & at.inicio_dt_br.le(corte) & at.inicio_dt_br.ge(inicio_janela)].copy()
    t = t[t.inicio_dt_br >= t.user_id.map(b.inicio_observacao)]
    t["dia"] = t.inicio_dt_br.dt.normalize()
    # Blocos de sete dias ancorados no fim da janela, não semanas ISO parciais.
    t["semana"] = ((corte.normalize()-t.dia).dt.days // 7)
    t["outdoor"] = t.tipo_canonico.isin(["corrida", "caminhada", "pedal"])
    g = t.groupby("user_id").agg(n_treinos=("atividade_id", "size"), semanas=("semana", "nunique"),
                                n_modalidades=("tipo_canonico", "nunique"), pct_ar_livre=("outdoor", "mean"))
    b = b.join(g)
    b[["n_treinos", "semanas", "n_modalidades"]] = b[["n_treinos", "semanas", "n_modalidades"]].fillna(0)
    b["treinos_mes"] = b.n_treinos / (b.dias_observados/30.4375)
    b["regularidade"] = b.semanas / np.ceil(b.dias_observados/7)
    o = onb[onb.respondido_em.le(corte)].sort_values("respondido_em").drop_duplicates("user_id",keep="last").set_index("user_id")
    b["dias_semana_pretendidos"] = pd.to_numeric(o.dias_semana_pretendidos.reindex(b.index),errors="coerce")
    assert b.index.is_unique and b.dias_observados.between(1,84).all()
    return b


def transformar(b, par):
    x = b[COLS].copy().astype(float)
    x["dias_semana_pretendidos"] = x.dias_semana_pretendidos.fillna(par["mediana"])
    x = x.fillna(0)
    for c in ["treinos_mes", "n_modalidades", "dias_semana_pretendidos"]:
        x[c] = x[c].clip(upper=par["p99"][c])
    x["treinos_mes"] = np.log1p(x.treinos_mes)
    return x


def ajustar(b, k=3, seed=42):
    fit = b.loc[~b.provisorio]
    par = {"mediana": float(fit.dias_semana_pretendidos.median()),
           "p99": {c:float(fit[c].quantile(.99)) for c in ["treinos_mes","n_modalidades","dias_semana_pretendidos"]}}
    scaler = StandardScaler().fit(transformar(fit,par))
    x = scaler.transform(transformar(fit,par))
    km = KMeans(n_clusters=k,n_init=30,random_state=seed).fit(x)
    z = pd.DataFrame(km.cluster_centers_,columns=COLS)
    nomes = {i:f"Grupo {i}" for i in range(k)}
    if k == 3:
        fraco = int(z.treinos_mes.idxmin())
        rest = [i for i in range(3) if i != fraco]
        nomes = {fraco:NOMES[2],max(rest,key=lambda i:z.loc[i,"pct_ar_livre"]):NOMES[0],
                 min(rest,key=lambda i:z.loc[i,"pct_ar_livre"]):NOMES[1]}
    return par, scaler, km, nomes


def atribuir(b, modelo):
    par, scaler, km, nomes = modelo
    return pd.Series(km.predict(scaler.transform(transformar(b,par))),index=b.index).map(nomes)


def avaliar_k(b):
    fit = b[~b.provisorio]
    rows=[]
    for k in range(2,9):
        par, sc, km, _ = ajustar(b,k)
        x = sc.transform(transformar(fit,par))
        rows.append(dict(k=k,elegivel=k in [3,4],silhueta=silhouette_score(x,km.labels_,sample_size=min(2500,len(x)),random_state=42),
                         davies_bouldin=davies_bouldin_score(x,km.labels_),inercia=km.inertia_,menor_grupo_pct=np.bincount(km.labels_).min()/len(x)*100))
    return pd.DataFrame(rows)


def estabilidade(b, modelo):
    fit = b[~b.provisorio]
    ref = atribuir(fit,modelo)
    rng = np.random.default_rng(42)
    scores=[]
    # Reajusta mediana, teto, escala e K-Means em cada bootstrap.
    for _ in range(5):
        amostra = fit.iloc[rng.choice(len(fit),len(fit),replace=True)]
        m = ajustar(amostra)
        scores.append(adjusted_rand_score(ref,atribuir(fit,m)))
    return {"bootstrap_ari_medio":float(np.mean(scores)),"bootstrap_ari_min":float(np.min(scores)),"reamostras":5}


def historico(b, modelo, a, ev, corte):
    b = b.copy()
    b["persona"] = atribuir(b,modelo)
    futuro = estado_no_corte(a,ev,corte+pd.Timedelta(days=60)).reindex(b.index)
    b["expirada_60d"] = ~futuro.ativa
    b["saida_composta_60d"] = ~futuro.ativa | ~futuro.renovacao_ligada
    rows=[]
    # Primário: renovação ligada no início; secundário: todos ativos e perda de acesso.
    for publico,mask,outcome in [("renovacao_ligada",b.renovacao_ligada,"saida_composta_60d"),
                                 ("todos_ativos",pd.Series(True,index=b.index),"expirada_60d")]:
        for plano in ["todos","mensal","anual"]:
            s=b[mask & (True if plano=="todos" else b.plano.eq(plano))]
            for persona in NOMES+["Base"]:
                g=s if persona=="Base" else s[s.persona.eq(persona)]
                n,e=len(g),int(g[outcome].sum())
                lo,hi=wilson(e,n)
                resto=s[~s.index.isin(g.index)]
                d,dl,dh,p=diferenca_proporcoes(e,n,int(resto[outcome].sum()),len(resto))
                rows.append(dict(corte=str(corte.date()),publico=publico,desfecho=outcome,plano=plano,persona=persona,
                                 n=n,saidas=e,taxa_pct=e/n*100 if n else np.nan,ic95_inf=lo*100,ic95_sup=hi*100,
                                 cobertura_saidas_pct=e/s[outcome].sum()*100 if s[outcome].sum() else np.nan,
                                 diferenca_resto_pp=d,ic95_diferenca_inf=dl,ic95_diferenca_sup=dh,provisorios=int(g.provisorio.sum())))
    return pd.DataFrame(rows)


def campanha(a,ev):
    c=ler("campanha_ago26_limpa")
    inicio=pd.Timestamp("2026-08-10 00:00:00")
    inicial=estado_no_corte(a,ev,inicio-pd.Timedelta(seconds=1))
    c=c.join(inicial[["plano","renovacao_ligada"]],on="user_id")
    rows=[]
    for dias in [30,51]:
        fim=inicio+pd.Timedelta(days=dias)
        exp=ev[ev.evento.eq("assinatura_expirada") & ev.data_hora_br.ge(inicio) & ev.data_hora_br.lt(fim)]
        c["expiracao"] = c.user_id.isin(exp.user_id)
        final=estado_no_corte(a,ev,fim-pd.Timedelta(seconds=1))
        c["composto"] = c.user_id.map(~final.ativa | ~final.renovacao_ligada)
        for alvo in ["expiracao","composto"]:
            # ITT principal completo; composto é subgrupo pré-atribuição, explicitamente separado.
            pop=c if alvo=="expiracao" else c[c.renovacao_ligada]
            for plano in ["todos","mensal","anual"]:
                s=pop if plano=="todos" else pop[pop.plano.eq(plano)]
                ctl=s[s.grupo.eq("controle")]
                for grupo in ["controle","cupom","desafio","conteudo"]:
                    g=s[s.grupo.eq(grupo)]
                    n,e=len(g),int(g[alvo].sum())
                    d,lo,hi,p=diferenca_proporcoes(e,n,int(ctl[alvo].sum()),len(ctl))
                    if grupo == 'controle':
                        # A referência é o próprio grupo, não uma segunda amostra independente.
                        d,lo,hi,p=0.,0.,0.,np.nan
                    rows.append(dict(dias=dias,desfecho=alvo,plano=plano,grupo=grupo,n=n,eventos=e,taxa_pct=e/n*100 if n else np.nan,
                                     controle_n=len(ctl),controle_eventos=int(ctl[alvo].sum()),diferenca_pp=d,ic95_inf=lo,ic95_sup=hi,p=p))
    r=pd.DataFrame(rows)
    # Família primária 3 braços/expiração30d; restante exploratório, família separada.
    primaria=r.dias.eq(30)&r.desfecho.eq("expiracao")&r.plano.eq("todos")
    r["familia"]=np.where(primaria,"primaria","exploratoria")
    for familia in ["primaria","exploratoria"]:
        mask=r.familia.eq(familia)&r.grupo.ne("controle")
        r.loc[mask,"p_bonferroni"]=np.minimum(1,r.loc[mask,"p"]*mask.sum())
    return r


def receita_atual(b):
    p=ler("pagamentos_limpos")
    p=p[p.status.eq("aprovado") & ~p.flag_duplicata_aprovada_dia & p.valor_num.gt(0) & pd.to_datetime(p.data_hora_br).le(CORTE)]
    ult=p.sort_values("data_hora_br").drop_duplicates("user_id",keep="last").set_index("user_id")
    taxas=b.canal_cobranca.map({"app_store":.15,"google_play":.15,"cartao":.035,
                              "pix_automatico":.0099,"web_cartao":.035,"web_pix":.0099})
    if taxas.isna().any():
        raise ValueError('Canal sem taxa definida na receita equivalente')
    fallback=pd.Series(np.where(b.plano.eq("anual"),299.90,39.90),index=b.index)*(1-taxas)
    valor=ult.valor_liquido.reindex(b.index).fillna(fallback)
    return valor/np.where(b.plano.eq("anual"),12,1)


def perfil(b):
    return b.groupby("persona").agg(ativos=("persona","size"),provisorios=("provisorio","sum"),
        treinos_mes_mediana=("treinos_mes","median"),regularidade_mediana=("regularidade","median"),
        ar_livre_mediana=("pct_ar_livre","median"),receita_equivalente=("receita","sum"),
        renovacao_desligada=("renovacao_desligada","sum")).reindex(NOMES).reset_index()


def prioridade(b):
    fraco=b.persona.eq(NOMES[2]); off=~b.renovacao_ligada
    nivel=np.select([off,fraco&b.plano.eq("mensal"),fraco],
                    ["1 Diagnóstico da renovação desligada","2 Formação de hábito mensal","3 Investigar antes de contato"],
                    "4 Monitorar continuidade")
    return b.assign(prioridade=nivel).groupby("prioridade").agg(clientes=("persona","size"),receita_equivalente=("receita","sum")).reset_index()


def financeiro():
    # Piloto único sem desconto/GenAI, não soma populações ou benefícios sobrepostos.
    rows=[]
    for delta in [-.02,0,.02,.05]:
        n=200; horizonte=3; receita=27.49; servir=4.20; contato=n*.01
        margem=n*delta*horizonte*(receita-servir)
        rows.append(dict(tratados=n,controle=200,horizonte_meses=horizonte,delta_retencao_assumido=delta,
                         receita_liquida_mensal_assumida=receita,custo_servir_mensal=servir,
                         custo_contato=contato,custo_oferta=0,custo_api=0,contribuicao_incremental=margem-contato))
    return pd.DataFrame(rows)


def graficos(p,h,c,sobrevida):
    plt.rcParams.update({"font.size":10,"figure.dpi":150})
    fig,ax=plt.subplots(figsize=(9,4)); ax.barh(p.persona,p.ativos,color=["#157a6e","#375fa0","#d67b32"])
    for i,n in enumerate(p.ativos): ax.text(n+30,i,f"{n:,}".replace(',','.'),va="center")
    ax.set(xlabel="Pagantes ativos em 30/09/2026",xlim=(0,p.ativos.max()*1.16),title="Três perfis comportamentais; todos os ativos representados")
    fig.tight_layout(); fig.savefig(OUT/"personas.png"); plt.close(fig)
    v=h[h.corte.eq("2026-07-31")&h.publico.eq("renovacao_ligada")&h.plano.eq("todos")&h.persona.ne("Base")]
    fig,ax=plt.subplots(figsize=(9,4)); ax.barh(v.persona,v.taxa_pct,color="#375fa0",xerr=[v.taxa_pct-v.ic95_inf,v.ic95_sup-v.taxa_pct],capsize=4)
    ax.set(xlabel="Saída composta em 60 dias (%) · IC95 Wilson",title="Julho projetado no modelo ajustado em maio")
    fig.tight_layout();fig.savefig(OUT/"coorte_60d.png");plt.close(fig)
    v=c[c.dias.eq(30)&c.desfecho.eq("expiracao")&c.plano.eq("todos")&c.grupo.ne("controle")]
    fig,ax=plt.subplots(figsize=(9,4));ax.errorbar(v.diferenca_pp,v.grupo,xerr=[v.diferenca_pp-v.ic95_inf,v.ic95_sup-v.diferenca_pp],fmt="o",capsize=5)
    ax.axvline(0,color="gray",ls="--");ax.set(xlabel="Diferença de expiração vs. controle (p.p.) · IC95 não simultâneo",title="Campanha: todos os sorteados, 30 dias completos")
    fig.tight_layout();fig.savefig(OUT/"campanha.png");plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4));ax.bar(sobrevida.plano,sobrevida.taxa*100,color=["#d67b32","#375fa0"])
    ax.set(ylabel="Saída em até 90 dias (%)",title="Coorte de entrada com 90 dias completos de acompanhamento")
    fig.tight_layout();fig.savefig(OUT/"saida_90d.png");fig.savefig(ROOT/"saidas/curva_sobrevivencia_lifetime.png");plt.close(fig)


def apresentacao(df):
    d=df.copy()
    for c in ['regularidade_mediana','ar_livre_mediana','taxa']:
        if c in d: d[c]=d[c]*100
    labels={'persona':'Perfil','ativos':'Ativos','provisorios':'Provisórios','receita_equivalente':'Receita equivalente (R$/mês)',
            'treinos_mes_mediana':'Treinos/mês (mediana)','regularidade_mediana':'Semanas com treino (%)',
            'renovacao_desligada':'Renovação desligada','n':'Pessoas','saidas':'Saídas','taxa_pct':'Taxa (%)',
            'ic95_inf':'IC95 inferior','ic95_sup':'IC95 superior','cobertura_saidas_pct':'Cobertura das saídas (%)',
            'grupo':'Braço','eventos':'Expirações','diferenca_pp':'Diferença (p.p.)','p_bonferroni':'p ajustado',
            'prioridade':'Prioridade operacional','clientes':'Clientes','plano':'Plano','saidas_90d':'Saídas em 90 dias','taxa':'Saída em 90 dias (%)'}
    for c in d:
        if pd.api.types.is_numeric_dtype(d[c]):
            def fmt(v):
                if pd.isna(v):return '—'
                if c in ['ativos','provisorios','renovacao_desligada','n','saidas','eventos','clientes','saidas_90d']:return f'{int(v):,}'.replace(',','.')
                return f'{v:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
            d[c]=d[c].map(fmt)
    return d.rename(columns=labels)


def tabela(df):
    return apresentacao(df).to_markdown(index=False)


def exportar_html(titulo,sections,path,slides=False):
    """HTML autossuficiente (sem CDN); tabelas e imagens incorporadas."""
    css="""body{margin:0;background:#edf1f2;color:#172e3e;font:17px/1.5 Arial,sans-serif}main{max-width:1100px;margin:auto}section{background:white;padding:48px;margin:24px 0;border-top:6px solid #157a6e;break-after:page}h1{font-size:34px;line-height:1.15}h2{color:#157a6e}table{border-collapse:collapse;width:100%;font-size:13px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}th{background:#e9f2f0}img{max-width:100%;max-height:440px;object-fit:contain}small{color:#516777}li{margin:8px 0}@media print{body{background:white}section{margin:0;padding:18px}main{max-width:none}}"""
    if slides:
        css+='section{min-height:690px;padding:30px 40px;box-sizing:border-box}h1{font-size:30px}p{font-size:16px;margin:8px 0}img{max-height:280px;display:block;margin:12px auto}table{font-size:12px}td,th{padding:6px} @media print{@page{size:landscape}section{min-height:0}}'
    body=[]
    for i,(heading,paragraphs,frame,figure) in enumerate(sections,1):
        content=f"<section><small>VITALIZA · SEMANA 5 · {i}/{len(sections)} · 12/11/2026</small><h1>{html.escape(heading)}</h1>"
        content+="".join(f"<p>{html.escape(x)}</p>" for x in paragraphs)
        if frame is not None: content+=apresentacao(frame).to_html(index=False,border=0,escape=True)
        if figure:
            data=base64.b64encode((OUT/figure).read_bytes()).decode()
            content+=f'<img alt="{html.escape(heading)}" src="data:image/png;base64,{data}">'
        body.append(content+"</section>")
    path.write_text(f'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(titulo)}</title><style>{css}</style><main>'+"".join(body)+"</main></html>",encoding="utf-8")


def documentos(p,h,c,k,qa,prior,fin,sobrevida):
    fig,ax=plt.subplots(figsize=(9,4))
    ax.barh(['Diagnosticar renovação desligada','Formar hábito no mensal','Investigar antes de contato','Monitorar continuidade'],prior.clientes,color=['#d67b32','#dfae58','#375fa0','#157a6e'])
    for i,n in enumerate(prior.clientes):ax.text(n+60,i,f'{n:,}'.replace(',','.'),va='center')
    ax.set(xlabel='Pessoas · públicos mutuamente exclusivos',xlim=(0,prior.clientes.max()*1.16),title='Prioridade operacional na carteira atual')
    fig.tight_layout();fig.savefig(OUT/'prioridades.png',dpi=150);plt.close(fig)
    hist=h[h.corte.eq("2026-07-31")&h.publico.eq("renovacao_ligada")&h.plano.eq("todos")]
    hc=hist[["persona","n","saidas","taxa_pct","ic95_inf","ic95_sup","cobertura_saidas_pct"]]
    cp=c[c.dias.eq(30)&c.desfecho.eq("expiracao")&c.plano.eq("todos")][["grupo","n","eventos","taxa_pct","diferenca_pp","ic95_inf","ic95_sup","p_bonferroni"]]
    contexto="A série mensal reconstruída observa médias de 5,68% em 2025 e 6,68% em jan–set/2026. Abril registra 1.158 perdas contra 1.154 no case; divergência preservada, ainda sem causa reconciliada. O aumento após o reajuste não demonstra efeito causal de preço."
    metodo="Cinco atributos: intenção de dias/semana, treinos por mês observado, regularidade, diversidade e proporção ao ar livre. Janela de 84 dias até cada corte; somente atividade dentro da assinatura. Mediana/P99/log1p/z-score são ajustados sem churn. Pessoas com menos de 30 dias são classificadas provisoriamente, mas permanecem nas contagens e desfechos."
    limite="Maio ajusta transformações e K-Means; julho usa o modelo congelado antes de observar os 60 dias seguintes, até 29/09. População primária: ativos com renovação ligada no início. Saída composta: sem acesso ou renovação desligada no fim. As taxas são históricas, sob as campanhas que ocorreram no período, não risco individual atual nem efeito causal. Setembro tem seu próprio ajuste descritivo; não transferimos automaticamente as taxas de julho à carteira atual."
    cards=[
        (NOMES[0],"Rotina predominantemente ao ar livre", "Hipótese: concluir uma meta pode reduzir o valor percebido da assinatura mesmo com treino frequente. Os registros atuais não comprovam esse motivo; a extração textual ainda requer validação humana.","Para elegíveis com renovação desligada, testar continuidade de treino versus controle, sem desconto automático; medir assinatura ativa com renovação ligada após 60 dias."),
        (NOMES[1],"Treinos registrados predominantemente em ambiente fechado; o nome da persona não prova uso de orientação guiada", "Hipótese: conteúdo pouco relevante ou dificuldade de encaixar a rotina pode reduzir a continuidade. A modalidade observada, sozinha, não comprova essas causas.","Para elegíveis com queda de regularidade, testar seleção editorial de conteúdo versus controle; medir retomada em 30 dias, saída em 60 dias e descadastro."),
        (NOMES[2],"Pouca frequência e regularidade registradas", "Hipótese: dificuldade em formar rotina reduz valor percebido. Ausência de registro não revela lesão, motivação ou abandono de atividade física; contratos anuais adiam a perda financeira.","Separar mensal em formação de hábito, renovação já desligada e anual que renova. Testar rotina inicial de treino entre elegíveis versus controle; medir retomada em 30 dias e continuidade em 60 dias.")]
    sections=[("Retenção: segmentar, medir e testar",[contexto,metodo],p[["persona","ativos","provisorios","receita_equivalente"]],"personas.png")]
    for nome,setup,conflito,acao in cards:
        row=p[p.persona.eq(nome)]
        sections.append((nome,[f"Contexto: {setup}.",f"Conflito e limite: {conflito}","Aprendizado: combinar comportamento com estado da assinatura; o perfil orienta a hipótese, mas não determina a resposta ao contato.",f"Decisão: {acao}","Evidência abaixo: carteira de setembro. A comparação de saída usa outra população, a coorte histórica da seção seguinte. Ampliar uma ação exige benefício líquido e ausência de dano; o piloto pequeno avalia viabilidade."],row[["ativos","treinos_mes_mediana","regularidade_mediana","renovacao_desligada"]],None))
    sections.append(("Evidência histórica e campanha",[limite,"Campanha primária: todos os sorteados em 10/08, expiração no intervalo [10/08,09/09). ICs não simultâneos; p ajustado para três comparações. Não significância não comprova ausência de efeito. Sensibilidades por plano, 51 dias e saída composta constam nas tabelas e têm correção separada para múltiplas comparações."],hc,"coorte_60d.png"))
    sections.append(("Prioridades, viabilidade e limites",["Prioridades são regras operacionais, não classes causais de persuadíveis ou sleeping dogs. Verificar elegibilidade e preferências de contato; atendimento necessário não é negado.","Piloto proposto: até 400 elegíveis com renovação desligada, estratificados por plano e persona; 200 e-mails editoriais e 200 controles. Custo R$ 2; sem desconto, WhatsApp, CS proativo ou API. Desfecho: ativa com renovação ligada em 60 dias; retomada em 30 dias e reclamações são secundários. Não executado. Se faltarem elegíveis, reduzir os dois braços igualmente. Dimensionar amostra antes de expandir. Cenários financeiros são hipóteses, não ROI comprovado.","Pesquisa: 353 respondentes entre 3.389 saídas de junho–setembro (~10,4%); 641 respondentes totais incluem ativos. Motivos Web não representam lojas. Datas em textos não orientam ação até validação manual. Receita equivalente não é margem nem receita em risco.",f"Qualidade: silhueta {float(k.loc[k.k.eq(3),'silhueta'].iloc[0]):.3f}; bootstrap com todo pré-processamento reajustado, ARI médio {qa['bootstrap_ari_medio']:.3f}. Cinco atributos não descrevem necessidades individuais; cortes com menos de 30 dias têm atribuição provisória."],prior,None))
    md=["# Customer Segmentation Report — Semana 5","> Versão consolidada autoritativa, ADR 020. Corte: 30/09/2026. Gerado por src/consolidar_semana5.py."]
    for title,paras,df,img in sections:
        md.extend([f"## {title}",*paras,tabela(df) if df is not None else "",f"![{title}](semana5_consolidada/{img})" if img else ""])
    md.extend(["## Campanha primária",tabela(cp),"## Cenários de contribuição — hipóteses, não previsão",tabela(fin),"Receita líquida mensal assumida R$ 27,49; custo de servir R$ 4,20; permanência incremental assumida de três meses. Não somar CAC evitado sem demonstrar redução real de aquisição. API e ofertas são zero porque este piloto é editorial. Uma expansão exige custo oficial de API e contabilização dos compromissos futuros.","## Rastreabilidade","Tabelas completas e QA em `semana5_consolidada/tabelas/`. Método e reprodução em `../notebooks/12_consolidacao_semana5.md`. Gráficos, modelos e números anteriores são históricos, não devem ser misturados com esta versão."])
    (ROOT/"saidas/customer_segmentation_report_semana5.md").write_text("\n\n".join(md),encoding="utf-8")
    exportar_html("Vitaliza — Relatório Semana 5",sections,OUT/"relatorio_executivo.html")
    deck=[("Três perfis para orientar a retenção",["A carteira tem 14.753 pagantes; a segmentação usa cinco atributos em 84 dias, sem churn.","O churn mensal subiu de 5,68% em 2025 para 6,68% em jan–set/2026; a série não isola o efeito do preço.","Os grupos descrevem comportamento; não são tipos humanos fixos nem scores de risco."],p[['persona','ativos','provisorios']],"personas.png"),
          ("Qualidade muda a interpretação",["Bronze preservada; exposição e ausência de cobertura são diferentes de zero uso.","A coorte de entrada inclui todos com 90 dias completos, mesmo quem saiu cedo; não é churn mensal.","A pesquisa cobre Web: 353 respondentes entre 3.389 saídas desde junho, cerca de 10,4%."],sobrevida[['plano','n','saidas_90d','taxa']],"saida_90d.png"),
          ("Hábito fraco concentra maior taxa, mas não todas as saídas",["Julho foi projetado no modelo de maio; atributos anteriores aos 60 dias de acompanhamento.","O alvo inclui perda de acesso ou renovação desligada, entre quem renovava no início.","A leitura é histórica, sob as campanhas do período; não é previsão para setembro nem efeito causal."],hc[['persona','n','taxa_pct','cobertura_saidas_pct']],"coorte_60d.png"),
          ("A campanha exige distinguir intenção e perda financeira",["ITT: todos os sorteados, expiração em 30 dias; ICs individuais e p ajustado para três contrastes.","Os intervalos incluem zero; isso não comprova ausência de efeito ou equivalência.","Desfecho composto, planos e 51 dias são sensibilidades exploratórias, sem identificação de uplift individual."],cp[['grupo','n','taxa_pct','diferenca_pp','p_bonferroni']],"campanha.png"),
          ("Priorizar diagnóstico e aprender antes de ampliar",["Renovação desligada exige diagnóstico; mensal com hábito fraco pode receber teste de formação de rotina.","Piloto editorial proposto: 200 e-mails e 200 controles, custo R$ 2; não comprova pequenos efeitos.","Validar elegibilidade e danos; ampliar com efeito e economia sustentáveis. Cenários não são retorno observado."],prior,"prioridades.png")]
    exportar_html("Vitaliza — Mini deck",deck,OUT/"mini_deck.html",True)
    lines=["# Mini deck — versão consolidada","> Cinco slides. Abrir `semana5_consolidada/mini_deck.html`; tabelas completas no relatório."]
    for title,paras,df,img in deck:
        lines += ["---",f"## {title}",*paras,tabela(df) if df is not None else "",f"![{title}](semana5_consolidada/{img})" if img else ""]
    (ROOT/"saidas/mini_deck_eda_semana5.md").write_text("\n\n".join(lines),encoding="utf-8")


def main():
    TAB.mkdir(parents=True,exist_ok=True)
    a,ev,at,onb=fontes()
    bases={}
    for data in ["2026-05-31 23:59:59","2026-07-31 23:59:59",str(CORTE)]:
        corte=pd.Timestamp(data); bases[str(corte.date())]=atributos(a,ev,at,onb,corte)
        print("Atributos",data,len(bases[str(corte.date())]),flush=True)
    atual=bases["2026-09-30"]
    assert len(atual)==14753, f"Reconciliação necessária: {len(atual)} ativos por eventos"
    km=avaliar_k(atual); modelo=ajustar(atual)
    atual["persona"]=atribuir(atual,modelo)
    atual["receita"]=receita_atual(atual)
    atual["renovacao_desligada"]=~atual.renovacao_ligada
    qa=estabilidade(atual,modelo)
    print("Segmentação e bootstrap concluídos",flush=True)
    passado=ajustar(bases["2026-05-31"])
    hist=pd.concat([historico(bases[d],passado,a,ev,pd.Timestamp(d+" 23:59:59")) for d in ["2026-05-31","2026-07-31"]],ignore_index=True)
    camp=campanha(a,ev)
    p=perfil(atual); prior=prioridade(atual); fin=financeiro(); sobrevida=proporcao_saida_90d(a,CORTE)
    antigo=ler("assinaturas_limpas").set_index("user_id")
    snap=antigo.renovacao_automatica.eq("nao").reindex(atual.index)
    qa.update(ativos=len(atual),provisorios=int(atual.provisorio.sum()),renovacao_desligada_eventos=int(atual.renovacao_desligada.sum()),renovacao_desligada_snapshot=int(snap.sum()),divergencias_renovacao=int(snap.ne(atual.renovacao_desligada).sum()),
              inputs={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(PRATA.glob("*.parquet"))})
    for nome,df in [("perfil_personas",p),("coortes_60d",hist),("campanha",camp),("selecao_k",km),("prioridades",prior),("cenarios_financeiros",fin),("coorte_90d",sobrevida)]:
        df.to_csv(TAB/f"{nome}.csv",index=False)
    (TAB/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8")
    # Artefato individual permanece fora do pacote público; base antiga preservada.
    destino=ROOT/"dados/processados/ouro/segmentos_consolidados_set2026.parquet"
    atual.reset_index().to_parquet(destino,index=False)
    graficos(p,hist,camp,sobrevida)
    documentos(p,hist,camp,km,qa,prior,fin,sobrevida)
    print(p.to_string(index=False),flush=True)
    print(json.dumps({k:v for k,v in qa.items() if k!='inputs'},ensure_ascii=False),flush=True)


if __name__=="__main__":
    main()
