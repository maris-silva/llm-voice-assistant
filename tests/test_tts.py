import subprocess
from unittest.mock import MagicMock, patch

import tts as tts_module


def test_falar_monta_pipeline_espeak_para_aplay():
    """Checa só o essencial (binário, flag de voz, --stdout + texto no fim) —
    não a lista inteira, pra sobreviver a flags novas como -s de velocidade."""
    with patch.object(tts_module.subprocess, "Popen") as mock_popen, patch.object(
        tts_module.subprocess, "run"
    ) as mock_run:
        mock_popen.return_value = MagicMock(stdout=MagicMock())

        tts_module.falar("Ola mundo", voz="pt-br")

    comando = mock_popen.call_args.args[0]
    assert comando[0] == "espeak-ng"
    assert comando[1:3] == ["-v", "pt-br"]
    assert comando[-2:] == ["--stdout", "Ola mundo"]
    assert mock_popen.call_args.kwargs["stdout"] == subprocess.PIPE

    args_aplay, _ = mock_run.call_args
    assert args_aplay[0] == ["aplay", "-D", "default"]


def test_falar_usa_pt_br_como_voz_padrao():
    with patch.object(tts_module.subprocess, "Popen") as mock_popen, patch.object(
        tts_module.subprocess, "run"
    ):
        mock_popen.return_value = MagicMock(stdout=MagicMock())

        tts_module.falar("oi")

    comando = mock_popen.call_args.args[0]
    assert comando[:3] == ["espeak-ng", "-v", "pt-br"]


def test_falar_usa_velocidade_padrao_de_120():
    with patch.object(tts_module.subprocess, "Popen") as mock_popen, patch.object(
        tts_module.subprocess, "run"
    ):
        mock_popen.return_value = MagicMock(stdout=MagicMock())

        tts_module.falar("oi")

    comando = mock_popen.call_args.args[0]
    assert "-s" in comando
    assert comando[comando.index("-s") + 1] == "120"
