# Fechamento da Semana 5 — ADR 021

## Pergunta e escopo
O pacote atende aos requisitos do guia e pode ser reproduzido por outra pessoa, sem dados individuais ou histórico Git embutidos na entrega pública?

## Fontes e regras
Guia oficial em `instrucoes-case/`, enunciado, Prata, eventos Bronze somente leitura e artefatos da ADR 020. Preservar os mesmos clientes e métricas; mudanças exigem comparação. Nenhuma publicação externa é executada pelos scripts.

## Auditoria das ressalvas
`src/auditar_divergencias_semana5.py` publica apenas agregados. Abril tem 1.158 usuários distintos com expiração em Brasília e também 1.158 términos no cadastro. O texto do enunciado informa 1.154. O mês textual bruto tem 1.160 eventos, sem contas internas entre eles: nem duplicação nem simples uso do mês UTC resolvem a diferença.

Nos cinco casos de renovação, o cadastro diz ligada, o último toggle diz desligada e houve renovação posterior. Renovar um ciclo não prova que o toggle de renovação futura foi religado. Não há empate de timestamps na sequência examinada. Mantém-se a regra temporal da ADR 020 e registra-se o conflito para confirmação da fonte. Não ajustar o número para coincidir com o enunciado.

## Reprodução transportável
O pipeline exige as entradas do case em `dados/brutos/`; não exige o dataset individual de uma segmentação antiga nem checkout Git para arquivamento. Comparações antigas são opcionais e sua ausência é informada. Notebooks 02 e 03 também podem ser executados com os agregados do pacote, sem acesso ao dado individual; o notebook 01 precisa da Bronze.

Corrigido o fallback de receita para reconhecer os rótulos reais `cartao` e `pix_automatico`, além de aliases Web. Um teste usa ausência de pagamento para cobrir esse caminho. O relatório de fechamento registra se houve impacto nos valores observados.

## Pacote e validação
`src/montar_pacote_semana5.py` monta arquivos por lista explícita, valida hashes de HTML/PDF/notebooks, limpa outputs e metadados de notebooks, inclui matriz de requisitos e gera manifesto SHA-256. Não copia `dados/`, `.git`, ambientes, credenciais, materiais de aula ou relatórios históricos. A reprodução é verificada em diretório privado independente antes do fechamento.

## Definition of done
Validação independente concluída em `20261112T232847Z`: 28 testes, três notebooks e sete tabelas equivalentes. Prata byte a byte igual; 14 Bronze preservadas; 14.753 ativos com mesmas atribuições e receita. Resultado detalhado em `saidas/semana5_consolidada/tabelas/qa_fechamento.json`.

Requisitos localizados; testes aprovados; notebooks executáveis; PDF/HTML coerentes; equivalência das tabelas confirmada; pacote sem dados individuais; arquivos e integridade conferidos. Publicação no Drive e submissão individual continuam etapas externas do aluno.
