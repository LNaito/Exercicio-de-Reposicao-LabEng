# Modelagem – HelpDesk Mini

## Diagrama de classes

```mermaid
classDiagram
    class Chamado {
        +int id
        +str titulo
        +str descricao
        +str solicitante
        +str prioridade
        +str status
        +str atendente
        +str solucao
        +str motivo_cancelamento
    }
    class ChamadoRepository {
        +adicionar(chamado) Chamado
        +buscar_por_id(chamado_id) Chamado
        +listar() list~Chamado~
    }
    class ChamadoService {
        +abrir(titulo, descricao, solicitante, prioridade) Chamado
        +listar(status) list~Chamado~
        +buscar(chamado_id) Chamado
        +iniciar(chamado_id, atendente) Chamado
        +resolver(chamado_id, solucao) Chamado
        +cancelar(chamado_id, motivo) Chamado
    }
    class ValidacaoError
    class ChamadoNaoEncontrado
    class TransicaoInvalida

    ChamadoService --> ChamadoRepository : usa
    ChamadoRepository o-- Chamado : guarda
    ChamadoService ..> Chamado : cria e altera
    ChamadoService ..> ValidacaoError : lança
    ChamadoService ..> ChamadoNaoEncontrado : lança
    ChamadoService ..> TransicaoInvalida : lança
```

## Tabela de transições

| Status atual | Operação | Status novo | Exige |
| --- | --- | --- | --- |
| `aberto` | iniciar | `em_andamento` | atendente válido |
| `em_andamento` | resolver | `resolvido` | solução válida |
| `aberto` | cancelar | `cancelado` | motivo válido |
| `em_andamento` | cancelar | `cancelado` | motivo válido |

Qualquer outra combinação gera `TransicaoInvalida`.

## Papel de cada classe

- **Chamado:** entidade que carrega os dados de um pedido de apoio.
- **ChamadoRepository:** guarda e recupera chamados em memória, sem regras de negócio.
- **ChamadoService:** valida campos, controla ids e aplica as transições de status.
- **ValidacaoError:** sinaliza campo fora da regra.
- **ChamadoNaoEncontrado:** sinaliza id inexistente.
- **TransicaoInvalida:** sinaliza mudança de status fora da tabela.
