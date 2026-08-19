from datetime import datetime
from pathlib import Path

ARQUIVO_SESSAO = Path(__file__).resolve().parent.parent / "sessao.log"


def registrar_inicio():
    """Registra o início da sessão atual e detecta se a sessão anterior não
    encerrou corretamente (queda de energia/crash, já que nesse caso o
    processo nunca chega a rodar registrar_fim()).

    Retorna a mensagem de aviso se detectar isso, senão None.
    """
    aviso = None

    if ARQUIVO_SESSAO.exists():
        linhas = ARQUIVO_SESSAO.read_text(encoding="utf-8").splitlines()
        if linhas and "INICIO" in linhas[-1] and "FIM" not in linhas[-1]:
            aviso = f"⚠️ Sessão anterior não encerrou corretamente (última atividade: {linhas[-1]})"

    with ARQUIVO_SESSAO.open("a", encoding="utf-8") as arquivo:
        arquivo.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | INICIO\n")

    return aviso


def registrar_fim():
    """Marca a sessão atual como encerrada corretamente."""
    with ARQUIVO_SESSAO.open("a", encoding="utf-8") as arquivo:
        arquivo.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | FIM (encerramento normal)\n")
