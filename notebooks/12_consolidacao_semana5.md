# Consolidação temporal — Semana 5

Data: 12/11/2026. Autor: Codex, autorizado por Igor. Branch: dev. ADR 020.

## Pergunta
Quais perfis descrevem a carteira atual, quais diferenças de saída aparecem em coortes históricas e quais ações merecem um teste?

## Fontes e granularidade
Prata: assinaturas, eventos, atividades, onboarding, pagamentos e campanha. Uma linha por usuário em cada corte; eventos até o instante de observação, nunca status final como atributo de um corte passado. Relatórios/tabelas são agregados. Dados individuais ficam em `dados/processados/ouro/segmentos_consolidados_set2026.parquet` e não integram o pacote público.

## Populações
- Atual: 14.753 pagantes ativos por eventos em 30/09/2026.
- Histórico: ativos em 31/05 e 31/07. Desfecho primário inclui apenas renovação ligada no início; secundário mede perda de acesso entre todos os ativos.
- Novos com menos de 30 dias permanecem na descrição e nos desfechos, mas recebem classificação provisória e não ajustam os centroides. Não há exclusão por saída precoce futura.
- A retrospectiva de 23.152 clientes de 2026 pertence à proposta anterior e não é o denominador do relatório atual.

## Temporalidade
84 dias de calendário, incluindo o dia do corte, limitados à data de início da assinatura. Regularidade usa blocos de sete dias ancorados no fim da janela e divisão pelos blocos observáveis. Logs de todas as origens; diversidade continua sujeita a cobertura de modalidade. Usar só a vigência paga é uma definição do atributo, não uma afirmação de que treino freemium é erro.

Cinco variáveis: intenção de dias/semana, treinos por mês observado, regularidade, modalidades e proporção ao ar livre. Proporção ausente quando não há treino é preenchida com zero apenas na matriz; considerar conjuntamente frequência para não interpretar zero como preferência indoor. Mediana de intenção, P99, log1p de frequência e StandardScaler são ajustados na população de treino. Bootstrap reajusta todo esse pré-processamento. k=3/4 elegíveis pelo guia; k=2…8 diagnóstico. k=3 favorece parcimônia e a silhueta entre elegíveis; não é escolhido pelo churn. k=4 pode melhorar Davies–Bouldin, mas não obriga maior complexidade.

Modelo histórico ajustado em maio; julho é projetado no mesmo modelo. Modelo de setembro ajustado separadamente para descrever a carteira atual. Os nomes são alinhados por perfis, mas a taxa histórica não é uma previsão individual para os integrantes de setembro. O histórico sofre influência das campanhas realmente executadas, incluindo agosto.

## Estado e alvo
Estado ativo: início até o corte, atualizado por início/renovação/carência, expiração ou reembolso. Um chargeback isolado não prova perda de acesso: há um caso ativo no snapshot com chargeback em setembro. Renovação ligada/desligada usa último toggle conhecido; sem toggle assume ligada. Plano/canal usam último evento, com fallback do cadastro de assinatura quando não há evento (limitação de reconstrução).

Saída composta em 60 dias: sem acesso OU renovação desligada ao fim, entre quem tinha renovação ligada no início. Perda de acesso é mostrada separadamente. IC95 Wilson para proporções; diferença para restante usa aproximação normal. Desligamento revertido antes do horizonte não conta no alvo de estado final. Métricas são descritivas, não efeito de tratamento.

## Campanha
O contraste do grupo controle consigo mesmo é referência zero, sem teste de hipótese. A coorte auxiliar de entrada em 90 dias usa plano cadastral e data de término: é descritiva, não estima efeito causal de trocar de plano nem substitui os alvos reconstruídos por eventos.

Mantém todos os sorteados na análise principal, incluindo eventuais divergências de elegibilidade. Janela principal [10/08 00h, 09/09 00h), 30 dias; evento de expiração. Três comparações versus controle e Bonferroni. Sensibilidades: 51 dias completos, por plano pré-campanha, e composto no subconjunto com renovação ligada antes da atribuição. Família exploratória com correção separada, ICs individuais não simultâneos. Não escolher janela porque deu significância. Oferta de cupom significa 30% por três meses no mensal ou um mês no anual; efeito misto não é efeito só do mês grátis.

## Receita, ação e custos
Receita equivalente: último aprovado não duplicado antes do corte, líquido de taxa, anual/12, fallback de preço. Não é margem nem receita em risco. Não há retorno causal demonstrado. Cenários do piloto calculam contribuição incremental por hipótese, com horizonte e custo de servir explícitos. Sem IA/discounts no piloto editorial, esses custos são zero; expansão requer custo de API oficial e compromissos mensais. Não somar CAC automaticamente.

Objetivos extraídos de texto são exploratórios sem validação humana; retirados do ranqueamento causal e das listas de envio. Não usar nomes de persona para presumir condições de saúde ou motivação. Não contato é regra operacional, não prova de sleeping dog.

Piloto proposto, ainda não executado: até 400 elegíveis com renovação desligada, randomizados 1:1 e estratificados por plano/persona. Medir assinatura ativa com renovação ligada após 60 dias; retomada em 30 dias e reclamações como secundários. O tamanho de 200 por braço é de viabilidade e não demonstra poder para detectar pequenos efeitos. Ações específicas dos cartões são hipóteses adicionais, não campanhas simultâneas já financiadas.

## Reprodução
Da raiz, com Bronze autorizada disponível:
```powershell
$env:UV_CACHE_DIR='.uv-cache'
uv run --with-requirements requirements-notebooks.txt python src/executar_semana5.py
uv run --with-requirements requirements-notebooks.txt python src/revisar_notebooks_semana5.py
```
Reprocessar apenas a consolidação sobre Prata existente:
```powershell
uv run --with-requirements requirements-data.txt python src/consolidar_semana5.py
```
O runner completo registra hash de entrada, logs privados e comparação de saídas. As fontes de apresentação são regeneradas das tabelas. HTML incorpora imagens e não depende de internet. Notebooks 02/03 demonstram consumo dos agregados; não substituem execução do runner.

## Critério de pronto
Os PDFs são exportações dos HTML, com seis páginas de relatório e cinco slides. Após regenerar os HTML, executar `node src/verificar_html_semana5.cjs --pdf` em ambiente com Playwright e Edge e revisar a renderização. Python não atualiza esses binários automaticamente.

Testes temporais e semânticos; 14.753 ativos únicos; população preservada; comparação de resultados; campanha primária reconciliada; relatórios e gráficos coerentes; HTML revisado; hashes Bronze conservados. Publicação/Adalove e validação humana da extração textual não são declaradas concluídas.
