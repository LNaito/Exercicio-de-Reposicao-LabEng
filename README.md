# Exercício de Reposição - Léo de Paula Naito
## Descrição

Este é um exercício de reposição referente as aulas de Laboratório de Engenharia de Software (5 ADS) dos dias 14 e 16 de setembro de 2026, proposto pelo professor Juan Canuto Hassam.

O HelpDesk Mini é o núcleo de controle de chamados do laboratório de informática: Permite abrir, listar, buscar, iniciar, resolver e cancelar chamados, respeitando regras de campo e uma tabela de transições de status. A persistência é em memória.

## Estrutura do projeto

- `docs/` – requisitos (`requisitos.md`) e modelagem (`modelagem.md`).
- `src/helpdesk/models.py` – entidade `Chamado`.
- `src/helpdesk/errors.py` – `ValidacaoError`, `ChamadoNaoEncontrado`, `TransicaoInvalida`.
- `src/helpdesk/repository.py` – armazenamento em memória.
- `src/helpdesk/service.py` – regras de negócio.
- `tests/test_chamados.py` – os 10 cenários obrigatórios.

## Como rodar o projeto
Para rodar o projeto, basta a inserção dos seguintes comandos na pasta /helpdesk.
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Resultado esperado: `10 passed`.


## Decisões de projeto
- A validação de campos mora no `ChamadoService`, aplicada após `strip`.
- A transição de status também mora no serviço, via `_exigir_status`.
- O repositório só guarda (`adicionar`) e recupera (`buscar_por_id`, `listar`).
- O serviço valida tudo antes de alterar o chamado, então erro nunca deixa estado parcial.
- Os ids são gerados pelo serviço (contador iniciado em 1) e só avançam após sucesso.
- `listar` ordena por id e aceita filtro opcional por status.
- Os testes usam apenas a interface pública do `ChamadoService`.
- `pytest.ini` define `pythonpath = src` para os imports funcionarem sem instalar o pacote.
