from typing import Optional

from .models import Chamado


class ChamadoRepository:
    def __init__(self) -> None:
        self._chamados: dict[int, Chamado] = {}

    def adicionar(self, chamado: Chamado) -> Chamado:
        self._chamados[chamado.id] = chamado
        return chamado

    def buscar_por_id(self, chamado_id: int) -> Optional[Chamado]:
        return self._chamados.get(chamado_id)

    def listar(self) -> list[Chamado]:
        return [self._chamados[i] for i in sorted(self._chamados)]
