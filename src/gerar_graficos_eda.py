"""Gráficos corrigidos, ADR 020. Associação retrospectiva não é previsão."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_auc_score
from metricas_semana5 import proporcao_saida_90d

ROOT=Path(__file__).resolve().parents[1]

def cobertura_pesquisa(assinaturas,eventos,survey):
    ev=eventos[eventos.evento.eq("assinatura_expirada")]
    datas=pd.to_datetime(ev.data_hora_br)
    ids=set(ev.loc[datas.ge("2026-06-01") & datas.lt("2026-10-01"),"user_id"])
    a=assinaturas[assinaturas.user_id.isin(ids)]
    loja=a.canal_cobranca.isin(["app_store","google_play"])
    resposta=a.user_id.isin(set(survey.user_id))
    counts={"Lojas sem resposta":int((loja & ~resposta).sum()),
            "Lojas com resposta":int((loja & resposta).sum()),
            "Web sem resposta":int((~loja & ~resposta).sum()),
            "Web com resposta":int((~loja & resposta).sum())}
    assert sum(counts.values())==len(a)
    return counts

def main():
    prata=ROOT/"dados/processados/prata"; out=ROOT/"saidas"
    a=pd.read_parquet(prata/"assinaturas_limpas.parquet")
    e=pd.read_parquet(prata/"eventos_assinatura_limpos.parquet")
    q=pd.read_parquet(prata/"pesquisa_saida_limpa.parquet")
    counts=cobertura_pesquisa(a,e,q)
    fig,ax=plt.subplots(figsize=(9,4)); ax.barh(list(counts),list(counts.values()),color="#375fa0")
    for i,n in enumerate(counts.values()): ax.text(n+10,i,str(n),va="center")
    ax.set(xlabel="Pessoas com expiração entre junho e setembro de 2026",title="Cobertura da pesquisa no período em que ela existia")
    fig.tight_layout();fig.savefig(out/"ponto_cego_cancelamentos.png",dpi=160);plt.close(fig)
    pd.DataFrame([counts]).to_csv(out/"tabelas/cobertura_pesquisa_corrigida.csv",index=False)
    coorte=proporcao_saida_90d(a,pd.Timestamp("2026-09-30 23:59:59"))
    fig,ax=plt.subplots(figsize=(8,4));ax.bar(coorte.plano,coorte.taxa*100,color=["#d67b32","#375fa0"])
    ax.set(ylabel="Saída em até 90 dias (%)",title="Entrantes desde 2025 com 90 dias completos de observação")
    fig.tight_layout();fig.savefig(out/"curva_sobrevivencia_lifetime.png",dpi=160);plt.close(fig)
    f=pd.read_parquet(ROOT/"dados/processados/ouro/features_eda_corte_set2026.parquet")
    cols=["atividades_ultimos_30d","media_atividades_mes","media_posts_mes","n_modalidades_distintas"]
    fig,axs=plt.subplots(1,2,figsize=(10,4))
    for ax,col in zip(axs,cols[:2]):
        ax.boxplot([f.loc[f.churn.eq(i),col].dropna() for i in [0,1]],tick_labels=["Ativos","Saídos"],showfliers=False)
        ax.set(title=col)
    fig.suptitle("Comparação retrospectiva — janelas alinhadas a desfechos diferentes")
    fig.tight_layout();fig.savefig(out/"boxplot_assimetria_uso.png",dpi=160);plt.close(fig)
    auc=[]
    for c in cols:
        v=roc_auc_score(f.churn,f[c].fillna(f[c].median())); auc.append(max(v,1-v))
    fig,ax=plt.subplots(figsize=(10,4));ax.barh(cols,auc,color="#375fa0");ax.axvline(.5,color="gray",ls="--")
    ax.set(xlabel="AUC na mesma base; não avalia previsão",title="Associação retrospectiva — não usar como desempenho preditivo",xlim=(0,1))
    fig.tight_layout();fig.savefig(out/"auc_roc_ranking.png",dpi=160);plt.close(fig)

if __name__=="__main__":
    main()
