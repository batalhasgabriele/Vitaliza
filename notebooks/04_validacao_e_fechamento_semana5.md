# Racional de validação e fechamento

## Pergunta
Os segmentos persistem quando removemos variáveis contratuais? Qual a incerteza dos efeitos experimentais?

## Dados e regras
Entrada: Ouro de segmentação e agregados ITT da Etapa 3. Não modificar Bronze. Não utilizar churn para formar ou selecionar grupos. Não transportar os resultados didáticos de julho para setembro.

## Reprodução
Na raiz do projeto, executar:

```powershell
$env:UV_CACHE_DIR='.uv-cache'
$env:OMP_NUM_THREADS='2'
uv run --with-requirements requirements-data.txt python src/validar_entrega_semana5.py
uv run --with-requirements requirements-data.txt pytest -q
uv run --with-requirements requirements-notebooks.txt python src/revisar_notebooks_semana5.py
```

O script compara três especificações em k=2…8, cinco bootstraps para k=3 e k=4, e estima IC normal não agrupado das diferenças ITT. Saídas: `saidas/validacao_semana5.md` e duas tabelas agregadas. O script não refaz a Prata: executar o pipeline existente se as entradas mudarem.

Em 08/11, os notebooks 01, 02 e 03 foram executados em kernels isolados sem erro. Os outputs não foram persistidos; o registro com hashes está em `saidas/tabelas/qa_notebooks_semana5.json`.

## Interpretação e decisão
Sem plano/canal, k=3 preserva a partição (ARI 0,988). A versão compacta tem silhueta 0,336 e ARI 0,931 frente à publicada. A melhora ocorre em outro espaço de atributos e não é prova direta de superioridade. Preservamos a publicação de 16 atributos como referência, com a limitação explícita de separação baixa. A versão compacta usa 90 dias como proxy, enquanto a aula propõe 12 semanas: não equivale à implementação literal.

Bootstrap reajusta o StandardScaler, mas conserva imputação e tetos estimados na população. Portanto, não mede toda a incerteza do pipeline. A janela pós-setembro não está completa: não reportar churn futuro por segmento. Os ICs experimentais incluem zero, sem demonstrar equivalência.

## Critério de pronto e continuidade
Resultados reproduzidos, personas vinculadas a perfis, hipóteses identificadas, orçamento explícito e mini deck com fontes. Pendências metodológicas para evolução: auditar exposição desde cadastro/assinatura, reconstruir coorte histórica com atributos disponíveis no corte e observar saída posterior; validar versão compacta e aprovar eventual migração com atualização integral dos documentos. Não chamar a entrega de validação prospectiva.
