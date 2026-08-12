import json
from unittest.mock import MagicMock, patch

import pytest

import stt as stt_module
from stt import SpeechToText


def test_extrair_palavras_quebra_frases_em_palavras_unicas_minusculas():
    palavras = SpeechToText._extrair_palavras(["Ligar A Luz", "acender"])
    assert palavras == sorted({"ligar", "a", "luz", "acender"})


@pytest.fixture
def stt_mockado():
    """SpeechToText com Model/KaldiRecognizer/RawInputStream falsos —
    nenhum microfone real ou modelo Vosk é tocado."""
    with patch.object(stt_module, "Model") as mock_model, patch.object(
        stt_module, "KaldiRecognizer"
    ) as mock_rec_cls, patch.object(stt_module.sd, "RawInputStream") as mock_stream_cls:
        mock_rec_cls.return_value = MagicMock()
        mock_stream_cls.return_value = MagicMock()

        instancia = SpeechToText()
        instancia.start()  # usa o stream mockado, não abre microfone real

        yield instancia, mock_rec_cls


def test_set_vocabulario_usa_gramatica_restrita_ao_vosk(stt_mockado):
    instancia, mock_rec_cls = stt_mockado
    mock_rec_cls.reset_mock()

    instancia.set_vocabulario(["Ativar", "Cancelar"])

    args, _ = mock_rec_cls.call_args
    grammar = json.loads(args[2])
    assert "ativar" in grammar
    assert "cancelar" in grammar
    assert "[unk]" in grammar


def test_set_vocabulario_vazio_usa_reconhecedor_livre(stt_mockado):
    instancia, mock_rec_cls = stt_mockado
    mock_rec_cls.reset_mock()

    instancia.set_vocabulario(None)

    args, _ = mock_rec_cls.call_args
    assert len(args) == 2  # (model, sample_rate) — sem grammar


def test_escutar_emite_texto_reconhecido_em_minusculo_e_sem_espacos(stt_mockado):
    instancia, _ = stt_mockado
    instancia._rec.AcceptWaveform.return_value = True
    instancia._rec.Result.return_value = json.dumps({"text": "  ATIVAR  "})
    instancia._queue.put(b"\x00\x00")

    texto = next(instancia.escutar())

    assert texto == "ativar"


def test_escutar_ignora_resultado_vazio_e_segue_pro_proximo(stt_mockado):
    instancia, _ = stt_mockado
    instancia._rec.AcceptWaveform.side_effect = [True, True]
    instancia._rec.Result.side_effect = [
        json.dumps({"text": ""}),
        json.dumps({"text": "horas"}),
    ]
    instancia._queue.put(b"\x00\x00")
    instancia._queue.put(b"\x00\x00")

    texto = next(instancia.escutar())

    assert texto == "horas"
