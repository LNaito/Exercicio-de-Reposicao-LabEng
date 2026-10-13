# Requisitos – HelpDesk Mini

## História 1 – Abrir chamado
Como solicitante, quero abrir um chamado com prioridade para que o laboratório saiba o que atender primeiro.

**Critério de aceitação:** um chamado válido nasce com status `aberto`, id positivo (começando em 1 e crescendo de um em um) e prioridade igual à informada. Dados inválidos geram `ValidacaoError` e nenhum chamado é criado.

## História 2 – Consultar a fila
Como solicitante, quero consultar a fila de chamados para acompanhar o andamento do meu pedido.

**Critério de aceitação:** `listar()` devolve os chamados em ordem crescente de id; `listar(status="aberto")` devolve apenas os abertos; `buscar` de id inexistente gera `ChamadoNaoEncontrado`.

## História 3 – Iniciar e resolver
Como atendente, quero iniciar e resolver um chamado para registrar quem atendeu e como o problema foi solucionado.

**Critério de aceitação:** `iniciar` em chamado `aberto` grava o atendente e muda para `em_andamento`; `resolver` em chamado `em_andamento` grava a solução e muda para `resolvido`; `resolver` em chamado `aberto` gera `TransicaoInvalida`.

## História 4 – Cancelar
Como solicitante ou atendente, quero cancelar um chamado ainda não encerrado para que pedidos desnecessários saiam da fila.

**Critério de aceitação:** `cancelar` em chamado `aberto` ou `em_andamento` grava o motivo e muda para `cancelado`; em chamado `resolvido` ou `cancelado` gera `TransicaoInvalida` e o status permanece o mesmo.
