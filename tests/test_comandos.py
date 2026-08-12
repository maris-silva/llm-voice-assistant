import pytest

from main import COMANDOS, VOCAB_COMANDOS, identificar_comando


@pytest.mark.parametrize(
    "texto, nome_esperado",
    [
        ("ligar a luz", "acender_luz"),
        ("acender", "acender_luz"),
        ("horas", "horas"),
        ("que horas", "horas"),
        ("olivia", "olivia_rodrigo"),
        ("toca olivia rodrigo", "olivia_rodrigo"),
        ("parar a musica", "parar_musica"),
        ("cancelar", "cancelar"),
    ],
)
def test_identificar_comando_reconhece_gatilhos_conhecidos(texto, nome_esperado):
    nome, acao = identificar_comando(texto)
    assert nome == nome_esperado
    assert acao is COMANDOS[nome_esperado][1]


def test_identificar_comando_ignora_frase_desconhecida():
    nome, acao = identificar_comando("faça o cafe da manha")
    assert (nome, acao) == (None, None)


def test_vocab_comandos_contem_todos_os_gatilhos():
    gatilhos_esperados = [frase for gatilhos, _ in COMANDOS.values() for frase in gatilhos]
    assert VOCAB_COMANDOS == gatilhos_esperados
