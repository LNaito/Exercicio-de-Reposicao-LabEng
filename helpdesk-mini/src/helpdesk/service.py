from typing import Optional

from .errors import ChamadoNaoEncontrado, TransicaoInvalida, ValidacaoError
from .models import (
    ABERTO,
    CANCELADO,
    EM_ANDAMENTO,
    PRIORIDADES_VALIDAS,
    RESOLVIDO,
    STATUS_VALIDOS,
    Chamado,
)
from .repository import ChamadoRepository


class ChamadoService:
    def __init__(self, repository: Optional[ChamadoRepository] = None) -> None:
        self._repo = repository if repository is not None else ChamadoRepository()
        self._proximo_id = 1

    # ---------- validação ----------
    @staticmethod
    def _texto(nome: str, valor, minimo: int, maximo: Optional[int] = None) -> str:
        if not isinstance(valor, str):
            raise ValidacaoError(f"{nome} deve ser texto.")
        valor = valor.strip()
        if len(valor) < minimo:
            raise ValidacaoError(f"{nome} deve ter no mínimo {minimo} caracteres.")
        if maximo is not None and len(valor) > maximo:
            raise ValidacaoError(f"{nome} deve ter no máximo {maximo} caracteres.")
        return valor

    @staticmethod
    def _prioridade(valor) -> str:
        if not isinstance(valor, str):
            raise ValidacaoError("prioridade deve ser texto.")
        valor = valor.strip()
        if valor not in PRIORIDADES_VALIDAS:
            raise ValidacaoError(
                f"prioridade deve ser uma de: {', '.join(PRIORIDADES_VALIDAS)}."
            )
        return valor

    # ---------- operações ----------
    def abrir(self, titulo, descricao, solicitante, prioridade) -> Chamado:
        titulo = self._texto("título", titulo, 5, 80)
        descricao = self._texto("descrição", descricao, 15, 400)
        solicitante = self._texto("solicitante", solicitante, 3, 80)
        prioridade = self._prioridade(prioridade)

        chamado = Chamado(
            id=self._proximo_id,
            titulo=titulo,
            descricao=descricao,
            solicitante=solicitante,
            prioridade=prioridade,
            status=ABERTO,
        )
        self._repo.adicionar(chamado)
        self._proximo_id += 1
        return chamado

    def listar(self, status: Optional[str] = None) -> list[Chamado]:
        if status is not None and status not in STATUS_VALIDOS:
            raise ValidacaoError(
                f"status deve ser um de: {', '.join(STATUS_VALIDOS)}."
            )
        chamados = self._repo.listar()
        if status is None:
            return chamados
        return [c for c in chamados if c.status == status]

    def buscar(self, chamado_id) -> Chamado:
        chamado = self._repo.buscar_por_id(chamado_id)
        if chamado is None:
            raise ChamadoNaoEncontrado(f"Chamado {chamado_id} não encontrado.")
        return chamado

    def iniciar(self, chamado_id, atendente) -> Chamado:
        chamado = self.buscar(chamado_id)
        self._exigir_status(chamado, "iniciar", ABERTO)
        atendente = self._texto("atendente", atendente, 3, 80)
        chamado.atendente = atendente
        chamado.status = EM_ANDAMENTO
        return chamado

    def resolver(self, chamado_id, solucao) -> Chamado:
        chamado = self.buscar(chamado_id)
        self._exigir_status(chamado, "resolver", EM_ANDAMENTO)
        solucao = self._texto("solução", solucao, 15)
        chamado.solucao = solucao
        chamado.status = RESOLVIDO
        return chamado

    def cancelar(self, chamado_id, motivo) -> Chamado:
        chamado = self.buscar(chamado_id)
        self._exigir_status(chamado, "cancelar", ABERTO, EM_ANDAMENTO)
        motivo = self._texto("motivo", motivo, 10)
        chamado.motivo_cancelamento = motivo
        chamado.status = CANCELADO
        return chamado

    @staticmethod
    def _exigir_status(chamado: Chamado, operacao: str, *permitidos: str) -> None:
        if chamado.status not in permitidos:
            raise TransicaoInvalida(
                f"Não é possível {operacao} um chamado '{chamado.status}'."
            )
