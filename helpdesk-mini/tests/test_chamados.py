import pytest

from helpdesk.errors import ChamadoNaoEncontrado, TransicaoInvalida, ValidacaoError
from helpdesk.service import ChamadoService

DESCRICAO = "A lampada nao acende durante a aula."


@pytest.fixture
def service():
    return ChamadoService()


def abrir_valido(service, titulo="Projetor da sala 2"):
    return service.abrir(titulo, DESCRICAO, "Ana Souza", "alta")


def test_abrir_chamado_valido_cria_id_1_e_status_aberto(service):
    chamado = abrir_valido(service)
    assert chamado.id == 1
    assert chamado.status == "aberto"
    assert chamado.prioridade == "alta"
    assert chamado.atendente == ""
    assert chamado.solucao == ""


def test_segundo_chamado_recebe_id_2(service):
    abrir_valido(service)
    segundo = abrir_valido(service, "Teclado quebrado")
    assert segundo.id == 2


def test_titulo_curto_gera_validacao_error_e_lista_segue_vazia(service):
    with pytest.raises(ValidacaoError):
        service.abrir("abc", DESCRICAO, "Ana Souza", "alta")
    assert service.listar() == []


def test_prioridade_fora_do_conjunto_gera_validacao_error(service):
    with pytest.raises(ValidacaoError):
        service.abrir("Projetor da sala 2", DESCRICAO, "Ana Souza", "urgente")


def test_buscar_id_inexistente_gera_chamado_nao_encontrado(service):
    with pytest.raises(ChamadoNaoEncontrado):
        service.buscar(99)


def test_iniciar_chamado_aberto_grava_atendente_e_muda_status(service):
    abrir_valido(service)
    chamado = service.iniciar(1, "Carlos Lima")
    assert chamado.atendente == "Carlos Lima"
    assert chamado.status == "em_andamento"


def test_resolver_chamado_aberto_gera_transicao_invalida(service):
    abrir_valido(service)
    with pytest.raises(TransicaoInvalida):
        service.resolver(1, "Lampada substituida e teste de imagem ok.")
    assert service.buscar(1).status == "aberto"


def test_resolver_chamado_em_andamento_grava_solucao_e_muda_status(service):
    abrir_valido(service)
    service.iniciar(1, "Carlos Lima")
    solucao = "Lampada substituida e teste de imagem ok."
    chamado = service.resolver(1, solucao)
    assert chamado.solucao == solucao
    assert chamado.status == "resolvido"


def test_cancelar_chamado_resolvido_gera_transicao_invalida(service):
    abrir_valido(service)
    service.iniciar(1, "Carlos Lima")
    service.resolver(1, "Lampada substituida e teste de imagem ok.")
    with pytest.raises(TransicaoInvalida):
        service.cancelar(1, "Pedido duplicado, cancelando.")
    assert service.buscar(1).status == "resolvido"


def test_listar_por_status_devolve_so_abertos_em_ordem_de_id(service):
    abrir_valido(service, "Chamado numero 1")
    abrir_valido(service, "Chamado numero 2")
    abrir_valido(service, "Chamado numero 3")
    service.iniciar(2, "Carlos Lima")
    abertos = service.listar(status="aberto")
    assert [c.id for c in abertos] == [1, 3]
    assert all(c.status == "aberto" for c in abertos)
