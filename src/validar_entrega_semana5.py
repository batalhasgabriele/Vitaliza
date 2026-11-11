"""Robustez suplementar da entrega, sem substituir a segmentação publicada.

Executar da raiz: uv run --with-requirements requirements-data.txt python src/validar_entrega_semana5.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler
from segmentacao_clientes import FEATURES_CLUSTER, preparar_matriz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'saidas' / 'tabelas'


def intervalo_diferenca(eventos, n, eventos_controle, n_controle):
    """IC normal não agrupado de 95%, em pontos percentuais; amostras grandes."""
    p, q = eventos / n, eventos_controle / n_controle
    margem = 1.96 * np.sqrt(p * (1-p) / n + q * (1-q) / n_controle)
    return 100 * (p-q-margem), 100 * (p-q+margem)


def main():
    f = pd.read_parquet(ROOT / 'dados/processados/ouro/features_segmentacao_ativos_set2026.parquet')
    labels = pd.read_parquet(ROOT / 'dados/processados/ouro/segmentos_ativos_set2026.parquet')
    f = f.drop(columns=['cluster_id', 'segmento'], errors='ignore').merge(labels, on='user_id', validate='one_to_one')
    assert len(f) == 14753 and f.user_id.is_unique
    _, transformed, _ = preparar_matriz(f)
    variantes = {'original_16': FEATURES_CLUSTER,
                 'sem_contrato_14': [c for c in FEATURES_CLUSTER if c not in ['plano_anual', 'canal_loja']],
                 'comportamental_4_proxy': ['treinos_90d', 'recencia_treino_dias', 'tenure_meses', 'prop_ar_livre_3m']}
    resultados = []
    for nome, cols in variantes.items():
        if nome == 'comportamental_4_proxy':
            # Proxy explícita: 90 dias, não as 12 semanas exatas propostas em aula.
            raw = f[cols].fillna(0).astype(float)
            for c in cols[:-1]:
                raw[c] = np.log1p(raw[c].clip(lower=0, upper=raw[c].quantile(.99)))
        else:
            raw = transformed[cols]
        z = StandardScaler().fit_transform(raw)
        for k in range(2, 9):
            model = KMeans(n_clusters=k, n_init=10, random_state=0).fit(z)
            linha = dict(variante=nome, k=k, inercia=model.inertia_,
                silhouette=silhouette_score(z, model.labels_, sample_size=2500, random_state=0),
                menor_grupo_pct=100*np.bincount(model.labels_).min()/len(z),
                ari_vs_publicado=adjusted_rand_score(f.cluster_id, model.labels_))
            if k in (3, 4):
                scores = []
                for seed in range(5):
                    idx = np.random.default_rng(seed).choice(len(raw), len(raw), replace=True)
                    scaler = StandardScaler().fit(raw.iloc[idx])
                    boot = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(scaler.transform(raw.iloc[idx]))
                    scores.append(adjusted_rand_score(model.labels_, boot.predict(scaler.transform(raw))))
                linha.update(bootstrap_ari_media=float(np.mean(scores)), bootstrap_ari_min=float(np.min(scores)))
            resultados.append(linha)
    r = pd.DataFrame(resultados)
    r.to_csv(OUT / 'robustez_segmentacao_semana5.csv', index=False)
    campanha = pd.read_csv(OUT / 'campanha_ago26_itt_30d.csv')
    ctrl = campanha.loc[campanha.grupo.eq('controle')].iloc[0]
    for i, row in campanha.iterrows():
        if row.grupo != 'controle':
            lo, hi = intervalo_diferenca(row.perdas_30d, row.sorteados, ctrl.perdas_30d, ctrl.sorteados)
            campanha.loc[i, 'ic95_inferior_pp'] = lo
            campanha.loc[i, 'ic95_superior_pp'] = hi
            campanha.loc[i, 'p_bonferroni_3'] = min(1, row.p_valor_vs_controle * 3)
    campanha.to_csv(OUT / 'campanha_ago26_incerteza.csv', index=False)
    texto = '# Validação suplementar da Semana 5\n\n'
    texto += 'A segmentação publicada permanece como referência descritiva. Experimentos abaixo não foram selecionados pelo churn.\n\n'
    texto += r.to_markdown(index=False, floatfmt='.3f')
    texto += '\n\nSilhuetas usam a mesma amostra determinística de 2.500 pessoas. Não comparar diretamente com a amostra de 5.000 da primeira versão. ARI entre variantes mede sensibilidade à especificação, não qualidade absoluta. Bootstrap: cinco reamostras com reposição, com StandardScaler reajustado; imputação, teto e log permanecem fixados na base completa, portanto não avalia toda a incerteza do pré-processamento. A variante de quatro atributos é uma aproximação de 90 dias, não uma reprodução literal da aula.\n\n'
    texto += '## Incerteza do experimento\n\n' + campanha[['grupo','sorteados','perdas_30d','diferenca_vs_controle_pp','ic95_inferior_pp','ic95_superior_pp','p_bonferroni_3']].to_markdown(index=False, floatfmt='.3f')
    texto += '\n\nICs normais de 95% para diferença de proporções independentes, não simultâneos. P-valores corrigidos para três comparações por Bonferroni. Intervalo cruzando zero não comprova equivalência ou ausência de efeito. Não há atribuição individual de uplift.\n'
    (ROOT / 'saidas/validacao_semana5.md').write_text(texto, encoding='utf-8')
    print(r.to_string(index=False))
    print('Validação suplementar salva.')


if __name__ == '__main__':
    main()
