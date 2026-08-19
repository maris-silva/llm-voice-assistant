from backend import state_log


def test_registrar_inicio_sem_historico_nao_gera_aviso(tmp_path, monkeypatch):
    monkeypatch.setattr(state_log, "ARQUIVO_SESSAO", tmp_path / "sessao.log")

    aviso = state_log.registrar_inicio()

    assert aviso is None
    assert "INICIO" in state_log.ARQUIVO_SESSAO.read_text(encoding="utf-8")


def test_registrar_inicio_apos_encerramento_normal_nao_gera_aviso(tmp_path, monkeypatch):
    monkeypatch.setattr(state_log, "ARQUIVO_SESSAO", tmp_path / "sessao.log")

    state_log.registrar_inicio()
    state_log.registrar_fim()
    aviso = state_log.registrar_inicio()

    assert aviso is None


def test_registrar_inicio_detecta_sessao_anterior_sem_fim(tmp_path, monkeypatch):
    monkeypatch.setattr(state_log, "ARQUIVO_SESSAO", tmp_path / "sessao.log")

    state_log.registrar_inicio()  # sessão "anterior": nunca chama registrar_fim (simula queda de energia)
    aviso = state_log.registrar_inicio()

    assert aviso is not None
    assert "INICIO" in aviso
