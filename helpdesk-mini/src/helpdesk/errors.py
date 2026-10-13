class ValidacaoError(Exception):
    """Campo fora da regra."""


class ChamadoNaoEncontrado(Exception):
    """Id de chamado inexistente."""


class TransicaoInvalida(Exception):
    """Mudança de status fora da tabela de transições."""
