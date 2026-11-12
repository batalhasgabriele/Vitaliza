> HISTORICO SUPERADO PELA ADR 020. Contém resultados/interpretações não vigentes. Não usar na entrega.

# Racional — Segmentação da base inteira e pontos de atenção

## Pergunta

Os segmentos da Semana 5 se sustentam quando a população inclui todos os clientes da janela, e não só os ativos no corte?

## Arquivos

- **Entrada:** camada Prata (`dados/processados/prata/`) e `ouro/segmentos_ativos_set2026.parquet`, usado só para comparação.
- **Código:**
  - `src/segmentacao_base_inteira.py` (`--explorar` compara conjuntos de variáveis e valores de k);
  - `src/objetivo_onboarding.py`;
  - `src/pontos_atencao_consultoria.py`;
  - `src/graficos_base_inteira.py`.
- **Saídas:** `saidas/base_inteira/` (relatório, mini deck, pontos de atenção, gráficos e `tabelas/`).

## Regras

- Não alterar a Bronze nem as tabelas Prata e Ouro oficiais.
- Churn, status, renovação, pesquisa de saída, campanha, tickets, plano e receita não entram no K-Means.
- Treinos de todas as origens, com hiit unido a funcional. Taxas por mês de assinatura observado.
- Clientes com menos de 30 dias observados recebem grupo provisório.

## Reprodução

```powershell
.\.venv\Scripts\python.exe src\pontos_atencao_consultoria.py
.\.venv\Scripts\python.exe src\segmentacao_base_inteira.py --explorar
.\.venv\Scripts\python.exe src\segmentacao_base_inteira.py
.\.venv\Scripts\python.exe src\graficos_base_inteira.py
```

`pontos_atencao_consultoria.py` usa, no ponto 7, o módulo de EDA local em `../Dados Entrada/EDA`. Sem ele, o ponto aparece como “não calculado”.

## Resultado

### Escolha do conjunto de variáveis

| Conjunto | k=4: silhueta | k=4: estabilidade (ARI) |
|---|---:|---:|
| A (completo) | 0,159 | 0,99 |
| B (comportamento) | 0,201 | 0,92 |
| C (sem dispositivo) | **0,206** | **0,99** |

Escolhido o conjunto **C com k=4**. A concordância com os segmentos do time entre os ativos é ARI 0,71.

### Personas

| Persona | Participação |
|---|---:|
| Ativo ao Ar Livre | 44,9% |
| Treino Indoor Guiado | 31,6% |
| Hábito Fraco | 18,5% |
| Treina em Companhia | 5,0% |

O churn é usado só depois da formação dos grupos: Hábito Fraco tem 11,4% ao mês, contra 5,9% da base.

## Definition of done

- [x] Pipeline do time reproduzido.
- [x] Pontos de atenção com evidência.
- [x] Segmentação na base inteira com robustez.
- [x] Relatório e mini deck.
- [ ] Decisão do time sobre a população.
- [ ] Validação manual das datas de evento.
- [ ] ADR aprovada e índice de `decisoes.md` atualizado.
