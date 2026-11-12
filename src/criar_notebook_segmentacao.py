"""Gera o notebook narrativo e reproduzível da Etapa 4."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / "notebooks" / "03_segmentacao_clusters.ipynb"


def markdown(texto: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": texto.splitlines(keepends=True)}


def code(codigo: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": codigo.splitlines(keepends=True),
    }


def main() -> None:
    cells = [
        markdown(
            "# Etapa 4 — Segmentação dos pagantes ativos\n\n"
            "**Pergunta:** quais grupos comportamentais acionáveis existem entre os 14.753 pagantes ativos em 30/09/2026?\n\n"
            "**Regra central:** os clusters são formados sem churn, status de saída, pesquisa de saída, campanha ou qualquer fato posterior ao corte. "
            "Demografia e renovação automática são reservadas apenas para auditoria e perfil posterior."
        ),
        markdown(
            "## 1. Fontes e linhagem\n\n"
            "O processamento consome exclusivamente Parquets da camada Prata: assinaturas, usuários, onboarding, atividades, uso mensal, pagamentos, amizades, feed e suporte. "
            "O script oficial é `src/segmentacao_clientes.py`; os produtos individuais permanecem na camada Ouro e apenas agregados seguros são exportados para `saidas/tabelas/`."
        ),
        code(
            "from pathlib import Path\n"
            "import json\n"
            "import pandas as pd\n"
            "from IPython.display import Image, display\n\n"
            "ROOT = Path('..')\n"
            "TABELAS = ROOT / 'saidas' / 'tabelas'\n"
            "OURO = ROOT / 'dados' / 'processados' / 'ouro'\n"
            "metadados = json.loads((TABELAS / 'metadados_segmentacao.json').read_text(encoding='utf-8'))\n"
            "metadados"
        ),
        markdown(
            "## 2. Definition of Done e controles\n\n"
            "- exatamente 14.753 usuários únicos;\n"
            "- uma linha por pagante ativo;\n"
            "- nenhuma feature de saída ou pós-tratamento;\n"
            "- comparação de 3 e 4 clusters;\n"
            "- tamanho mínimo de 5%;\n"
            "- estabilidade por reamostragem;\n"
            "- perfil estatístico e validação nos cinco critérios de negócio."
        ),
        code(
            "features = pd.read_parquet(OURO / 'features_segmentacao_ativos_set2026.parquet')\n"
            "assert len(features) == 14_753\n"
            "assert features['user_id'].is_unique\n"
            "proibidas = {'churn','motivo_fim','data_fim','motivo_pesquisa_saida','abriu_push','abriu_email','clicou'}\n"
            "assert not proibidas.intersection(metadados['features_cluster'])\n"
            "features.shape"
        ),
        markdown(
            "## 3. Escolha de k\n\n"
            "K-Means foi avaliado com inicializações múltiplas. A solução oficial é escolhida apenas entre `k=3` e `k=4`; `k=5` funciona como diagnóstico. "
            "Silhouette e Davies–Bouldin medem separação, enquanto o ARI médio mede estabilidade frente a reamostragens."
        ),
        code(
            "metricas = pd.read_csv(TABELAS / 'metricas_clusterizacao.csv')\n"
            "display(metricas)\n"
            "display(Image(filename=str(ROOT / 'saidas' / 'segmentacao_validacao_k.png')))"
        ),
        markdown(
            "## 4. Perfis encontrados\n\n"
            "A solução de três grupos separa um conjunto sem hábito recente e dois conjuntos ativos, diferenciados principalmente pelo modo de treino: atividades ao ar livre versus vídeos guiados. "
            "Os nomes descrevem centroides agregados; não são rótulos psicológicos nem inferências sobre indivíduos."
        ),
        code(
            "perfil = pd.read_csv(TABELAS / 'perfil_segmentos.csv')\n"
            "display(perfil)\n"
            "display(Image(filename=str(ROOT / 'saidas' / 'segmentacao_heatmap_perfis.png')))\n"
            "display(Image(filename=str(ROOT / 'saidas' / 'segmentacao_tamanho_receita.png')))"
        ),
        markdown(
            "## 5. Separação e limitação\n\n"
            "A estabilidade elevada não elimina a sobreposição entre os dois grupos ativos. A projeção PCA e o silhouette baixo mostram que a base não contém fronteiras naturais fortes em todas as dimensões. "
            "A segmentação deve ser usada como estrutura descritiva e acionável, não como verdade ontológica nem como modelo de churn."
        ),
        code(
            "display(Image(filename=str(ROOT / 'saidas' / 'segmentacao_pca.png')))\n"
            "pd.read_csv(TABELAS / 'criterios_segmentacao.csv')"
        ),
        markdown(
            "## 6. Próximo uso\n\n"
            "Na Etapa 5, os três perfis serão convertidos em cartões de persona baseados em dados, hipóteses de drivers e priorização preliminar. "
            "A taxa de renovação desligada pode ajudar a interpretar os clusters depois de formados, mas não participou da distância do algoritmo."
        ),
    ]
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    DESTINO.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Notebook criado: {DESTINO}")


if __name__ == "__main__":
    raise SystemExit('Gerador histórico desativado pela ADR 020. Execute src/atualizar_documentacao_semana5.py.')
