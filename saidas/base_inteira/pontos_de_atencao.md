# Pontos de atenção para discussão com o time — Semana 5

**Preparado por:** Lorena (revisão de consultoria) · **Base:** branch `dev`, pipeline reproduzido em 11/11/2026 · **Corte:** 30/09/2026

> Todos os números abaixo foram recalculados a partir da camada Prata do próprio repositório.
> Código: `src/pontos_atencao_consultoria.py` e `src/segmentacao_base_inteira.py`. Tabelas: `saidas/base_inteira/tabelas/`.

## Ponto de partida: o pipeline do time se reproduz

Rodei o pipeline inteiro com os dados brutos:

```text
auditar_bronze → limpeza_qualidade_dados → processar_eda → analisar_eda_marcos → segmentacao_clientes → gerar_graficos_eda → validar_entrega_semana5
```

- **Hashes dos brutos:** idênticos ao manifesto publicado.
- **Camada Prata:** byte a byte igual à versionada.
- **Métricas:** iguais até a 13ª casa decimal.
- **Testes:** 16 de 16 passaram.
- **Não executado:** `validar_engenharia_dados.py`, porque depende da baseline privada.

A engenharia está sólida. Os pontos abaixo tratam de **desenho analítico**, não de bugs.

## Resumo para a reunião

| # | Ponto | Prioridade | O que muda na entrega |
|---|---|---|---|
| 1 | A segmentação usa só quem sobreviveu até 30/09 | **Alta** | Refazer a clusterização com a base inteira (proposta pronta, ver relatório) |
| 2 | O efeito do cupom depende da janela e da elegibilidade | **Alta** | Rever a conclusão “nenhum braço teve efeito” |
| 3 | Objetivo com data é o maior sinal de churn e não é usado | **Alta** | Novo driver de churn por persona e gatilho de ação |
| 4 | Variáveis de uso da EDA têm cobertura desigual entre anos | Média | Rever o ranking de AUC (sessões deixa de ser “protetor”) |
| 5 | A taxonomia de modalidade depende da fonte | Média | Unir hiit e funcional antes de contar modalidades |
| 6 | 959 pares de contas duplicadas não tratados | Média | Registrar no tratamento; não muda a segmentação |
| 7 | Os segmentos dependem da forma de normalizar | Média | Declarar a escolha (log1p + z-score) como premissa |
| 8 | Detalhes de reconciliação | Baixa | Ajustes de texto |

---

## 1. A segmentação usa só quem sobreviveu até 30/09 — Alta

### O que vimos

O time clusterizou os **14.753 pagantes ativos no corte**. A base de pagantes já vistos tem **32.583** clientes, e **8.399 saíram entre jan e set/2026**, ficando fora dos grupos.

| Indicador | Ativos no corte | Saídas de 2026 |
|---|---:|---:|
| % no plano anual | 57,5% | 28,2% |
| % sem treino nos 30 dias antes de sair | — | 27,8% |
| … no plano mensal | — | 16,9% |
| … no plano anual | — | 55,5% |

### Por que importa

Filtrar por “ainda ativo” é usar a informação de quem saiu, o que o enunciado pede para evitar.

O efeito aparece no segmento “Adormecidos sem hábito”, com **98% de plano anual**. O mensalista que para de treinar cancela no mês seguinte e some da foto de 30/09. O anual fica na base até o aniversário. O segmento retrata **quem ainda não pôde sair**, e não o perfil “sem hábito” como um todo.

### Recomendação

Clusterizar todos os clientes com assinatura em vigor em jan–set/2026, ativos ou não. Medir o comportamento por mês de assinatura observado e usar churn só depois, para descrever os grupos. A proposta está em `customer_segmentation_report_base_inteira.md`.

**Resultado:** os três perfis do time se mantêm (ARI 0,71 entre os ativos), o grupo de baixo hábito passa a incluir mensalistas, e surge um quarto grupo.

### Pergunta ao time

Concordamos em trocar a população da Semana 5 para a base inteira de jan–set/2026?

---

## 2. O efeito do cupom depende da janela e da elegibilidade — Alta

### O que vimos

O time mediu o efeito da campanha em **30 dias** sobre todos os sorteados e concluiu que todos os ICs incluem zero.

| Janela e população | Cupom − controle | IC 95% |
|---|---:|---|
| 30 dias, todos os sorteados (time) | −0,95 p.p. | −1,99 a +0,09 |
| Até 30/09 (51 dias), todos | **−1,91 p.p.** | −3,24 a −0,59 |
| Até 30/09, só quem tinha renovação na janela | **−3,98 p.p.** | −6,52 a −1,43 |
| Desafio, só quem renova na janela | −2,59 p.p. | −5,15 a −0,02 |

### Por que importa

Um anual que não renova em agosto ou setembro **não pode** sair nesse período, então ele dilui o efeito. Restringindo aos elegíveis, o cupom reduz o churn em cerca de 4 p.p. (de 19,9% para 15,9%), e o desafio aparece no limite.

Esse resultado é a base do uplift da Semana 10. Concluir agora que “nada funcionou” pode descartar o melhor braço.

**Ressalva:** a restrição por elegibilidade é pós-sorteio, mas usa só a data de renovação, que é pré-tratamento. Não há correção para múltiplas comparações; com Bonferroni em 3 braços, o cupom continua significativo e o desafio não.

### Recomendação

- Reportar o efeito na população elegível e em toda a janela observada.
- Manter a leitura de 30 dias como sensibilidade.

### Pergunta ao time

Por que a janela de 30 dias? Há alguma premissa do case que eu não esteja vendo?

---

## 3. Objetivo com data é o maior sinal de churn e não é usado — Alta

### O que vimos

O texto livre `objetivo_texto` do onboarding só entra no pipeline como flag de preenchimento. Com expressões regulares (`src/objetivo_onboarding.py`):

| Indicador | Valor |
|---|---:|
| Onboardings com objetivo datado (formatura, prova, viagem, casamento) | 20,2% |
| Saíram na janela, entre clientes com evento nos ±60 dias | **62,5%** (1.028 clientes) |
| Saíram na janela, entre clientes sem prazo | 34,0% |
| Comentários da pesquisa de saída que citam meta cumprida ou evento | 50,7% |
| Quem marcou “preço” e comentou meta cumprida ou evento | 49,2% |

### Por que importa

- **É um driver claro:** o cliente assina para um evento e sai quando ele passa.
- **A leitura de preço muda:** metade de quem marca “preço” está dizendo “já cumpri meu objetivo”.
- **A janela de ação é previsível:** na base ativa de 30/09, **495 clientes** têm evento dentro de ±60 dias.

### Recomendação

- Incluir “objetivo com prazo” como driver de churn nos cartões de persona.
- Usar a data do evento como gatilho de contato, propondo um novo objetivo antes do evento.
- **Limite:** as datas vêm de regex e precisam de validação manual numa amostra de cerca de 200 textos. Essa validação também entra na Semana 10, que pede comparar a extração por GenAI com uma amostra rotulada.

---

## 4. Variáveis de uso da EDA têm cobertura desigual entre anos — Média

### O que vimos

`features_eda_corte_set2026` cobre assinaturas desde 2020, mas `uso_mensal` só começa em 01/2025:

- As **1.798 saídas de 2024 têm uso zero por construção**, e não por falta de uso.
- Em 2025, só **83–85%** dos assinantes têm linha em `uso_mensal`. Em 2026, são **97%**.

| Variável | AUC com todos | AUC só com cobertura |
|---|---:|---:|
| media_sessoes_mes | 0,559 | **0,489** |
| media_atividades_mes | 0,627 | 0,569 |
| media_minutos_mes | 0,624 | 0,565 |

### Por que importa

“Mais sessões, menos churn” (AUC 0,559) desaparece quando se retiram os anos sem dado. Parte do sinal de uso no ranking da EDA vem de cobertura, não de comportamento.

### Recomendação

Recalcular o ranking só com assinaturas cobertas (fim a partir de 2025, com meses registrados), ou trazer a janela para 2026.

---

## 5. A taxonomia de modalidade depende da fonte — Média

### O que vimos

`hiit` só existe na origem app: **0 de 109.626** treinos vêm de relógio. Os relógios gravam esses treinos como `funcional` (20,4% dos treinos de relógio contra 7,8% no app).

### Por que importa

- `n_modalidades_90d`, uma das 16 variáveis do cluster, conta uma modalidade a mais para quem usa o app.
- A “modalidade principal = hiit” do segmento vídeo é parcialmente artefato da fonte.

### Recomendação

Unir hiit e funcional antes de contar modalidades. Foi o que fiz na proposta.

---

## 6. Contas duplicadas não tratadas — Média

### O que vimos

- **959 pares** de contas (1.918 contas) têm o mesmo e-mail, mudando só maiúsculas e minúsculas.
- Nascimento e cidade coincidem em 100% dos pares.
- 472 dessas contas têm assinatura paga, e nenhum par tem duas assinaturas.

### Por que importa

- **Segmentação:** não muda (teste sem essas contas: ARI 1,00).
- **Contagem de contas e funil:** ficam inflados.
- **CRM:** a mesma pessoa pode receber mensagens em duas contas.

### Recomendação

Registrar no `registro_limpeza_tratamento_dados.md` e marcar as contas na Prata de usuários.

---

## 7. Os segmentos dependem da forma de normalizar — Média

### O que vimos

Na proposta da base inteira, o modelo é muito estável com a mesma normalização:
- **Outra semente:** ARI 1,00.
- **Bootstrap:** Jaccard médio entre 0,94 e 0,99.
- **Reajustado só com ativos ou só com quem saiu:** ARI acima de 0,92.

Já trocar a normalização muda o resultado:

| Normalização | ARI | Persona que se perde |
|---|---:|---|
| RobustScaler | 0,17 | “Treina em Companhia” |
| MinMaxScaler | 0,63 | “Treina em Companhia” |
| Sem log1p | 0,31 | A separação ar livre × indoor |

O grupo de **Hábito Fraco aparece em todos os cenários** (Jaccard ≥ 0,79).

### Recomendação

Declarar no relatório que log1p + z-score é uma premissa, explicando o motivo:
- dá peso igual às variáveis;
- o RobustScaler divide “% acompanhado” por um IQR de zero.

O time também deve registrar a mesma sensibilidade para os três segmentos publicados.

---

## 8. Detalhes de reconciliação — Baixa

- **Uma conta interna como pagante:** há 14.753 ativos não cortesia, um deles marcado como interno (`flag_conta_interna`). Pela regra de exclusão de internas, seriam 14.752.
- **Garmin nos adormecidos:** donos de Garmin são 29,6% dos adormecidos, contra 18,0% nos demais. Não achei viés de medição: a mediana de treinos em 90 dias é 1, com ou sem relógio. Fica como pergunta de produto: há algo na integração Garmin que desestimula o uso?
- **`regularidade_3m`:** vem de `uso_mensal`, que não registra treino de relógio (91,5% dos meses batem com a origem app). Na proposta, a regularidade é medida pelos treinos de todas as origens.

---

## Encaminhamentos sugeridos

1. **Decidir a população da Semana 5** (ponto 1) e, havendo acordo, adotar a segmentação da base inteira no Customer Segmentation Report.
2. **Atualizar a leitura da campanha** (ponto 2) no mini deck e na seção de hipóteses.
3. **Validar manualmente uma amostra das datas de evento** (ponto 3).
4. **Registrar os tratamentos** dos pontos 5 e 6 em uma ADR e no registro de limpeza.
5. **Atualizar `docs/plano_entrega_semana5.md` e `decisoes.md`** depois das decisões, como pede o AGENTS.md.
