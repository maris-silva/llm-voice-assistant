import subprocess
from unittest.mock import MagicMock, patch

import tts as tts_module


def test_falar_monta_pipeline_espeak_para_aplay():
    with patch.object(tts_module.subprocess, "Popen") as mock_popen, patch.object(
        tts_module.subprocess, "run"
    ) as mock_run:
        mock_popen.return_value = MagicMock(stdout=MagicMock())

        tts_module.falar("Ola mundo", voz="pt-br")

    args_espeak, kwargs_espeak = mock_popen.call_args
    assert args_espeak[0] == ["espeak-ng", "-v", "pt-br", "--stdout", "Ola mundo"]
    assert kwargs_espeak["stdout"] == subprocess.PIPE

    args_aplay, _ = mock_run.call_args
    assert args_aplay[0] == ["aplay", "-D", "default"]


def test_falar_usa_pt_br_como_voz_padrao():
    with patch.object(tts_module.subprocess, "Popen") as mock_popen, patch.object(
        tts_module.subprocess, "run"
    ):
        mock_popen.return_value = MagicMock(stdout=MagicMock())

        tts_module.falar("oi")

    args_espeak, _ = mock_popen.call_args
    assert args_espeak[0][:3] == ["espeak-ng", "-v", "pt-br"]
