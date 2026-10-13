from dataclasses import dataclass

ABERTO = "aberto"
EM_ANDAMENTO = "em_andamento"
RESOLVIDO = "resolvido"
CANCELADO = "cancelado"

STATUS_VALIDOS = (ABERTO, EM_ANDAMENTO, RESOLVIDO, CANCELADO)
PRIORIDADES_VALIDAS = ("baixa", "media", "alta")


@dataclass
class Chamado:
    id: int
    titulo: str
    descricao: str
    solicitante: str
    prioridade: str
    status: str = ABERTO
    atendente: str = ""
    solucao: str = ""
    motivo_cancelamento: str = ""
