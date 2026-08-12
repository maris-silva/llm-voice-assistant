from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import musica as musica_module
from musica import Player


def test_tocar_avisa_quando_pasta_nao_tem_wav(tmp_path, capsys):
    player = Player()
    player.tocar(tmp_path)

    saida = capsys.readouterr().out
    assert "Nenhum .wav encontrado" in saida


def test_tocar_escolhe_arquivo_e_monta_comando_aplay(tmp_path):
    (tmp_path / "a.wav").touch()
    (tmp_path / "b.wav").touch()

    with patch.object(musica_module.subprocess, "Popen") as mock_popen:
        mock_popen.return_value = MagicMock()
        player = Player(dispositivo_audio="hw:2,0")
        player.tocar(tmp_path, aleatorio=False)

    comando = mock_popen.call_args.args[0]
    assert comando[0] == "aplay"
    assert "-D" in comando and "hw:2,0" in comando
    assert comando[-1] == str(tmp_path / "a.wav")  # aleatorio=False -> primeiro da lista


def test_parar_termina_processo_em_execucao():
    player = Player()
    processo_fake = MagicMock()
    processo_fake.poll.return_value = None
    player._processo = processo_fake

    player.parar()

    processo_fake.terminate.assert_called_once()
    processo_fake.wait.assert_called_once()
    assert player._processo is None


def test_parar_sem_processo_nao_quebra():
    player = Player()
    player.parar()  # não deve levantar exceção
    assert player._processo is None


def test_tocando_reflete_estado_do_processo():
    player = Player()
    assert player.tocando() is False

    processo_fake = MagicMock()
    processo_fake.poll.return_value = None
    player._processo = processo_fake
    assert player.tocando() is True


# --- Sanidade de configuração -------------------------------------------
# Player.tocar() só reconhece arquivos .wav (pasta.glob("*.wav")).

@pytest.mark.xfail(
    reason="Player só toca .wav, mas musicas/ só tem .mp3 — comando de voz de música não funciona hoje",
    strict=True,
)
def test_pasta_musicas_tem_arquivo_no_formato_que_o_player_espera():
    raiz = Path(__file__).resolve().parent.parent
    pasta_musicas = raiz / "musicas"

    wavs = list(pasta_musicas.glob("*.wav"))
    assert wavs, (
        f"Nenhum .wav em '{pasta_musicas}' "
        f"(encontrado: {[p.name for p in pasta_musicas.iterdir()]})"
    )
