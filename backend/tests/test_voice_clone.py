from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


async def _post_voice_clone(
    client: AsyncClient,
    *,
    text: str = "Hola",
    file_content: bytes = b"voice",
    filename: str = "voice.wav",
):
    files = {"reference": (filename, file_content, "audio/wav")}
    data = {"text": text}
    return await client.post("/api/v1/voice-clone/generate", data=data, files=files)


@pytest.mark.asyncio
async def test_generate_voice_success(monkeypatch, tmp_path):
    normalized_path = tmp_path / "normalized.wav"
    generated_path = tmp_path / "voice-mock.wav"

    async def fake_save(file):
        normalized_path.write_bytes(await file.read())
        return normalized_path

    async def fake_synthesize(text: str, reference_path: Path) -> Path:
        assert text == "Hola"
        assert reference_path == normalized_path
        generated_path.write_bytes(b"result")
        return generated_path

    monkeypatch.setattr("app.api.v1.voice_clone.save_and_normalize", fake_save)
    monkeypatch.setattr("app.api.v1.voice_clone.synthesize_voice", fake_synthesize)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await _post_voice_clone(client)

    assert response.status_code == 201
    payload = response.json()
    assert payload["ok"] is True
    assert payload["download_url"].endswith("files/voice-mock.wav")


@pytest.mark.asyncio
async def test_generate_voice_rejects_reference(monkeypatch):
    async def fake_save(file):
        raise ValueError("Reference audio exceeds the 20MB limit")

    async def fake_synthesize(*args, **kwargs):
        raise AssertionError("synthesize_voice should not be called")

    monkeypatch.setattr("app.api.v1.voice_clone.save_and_normalize", fake_save)
    monkeypatch.setattr("app.api.v1.voice_clone.synthesize_voice", fake_synthesize)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await _post_voice_clone(client)

    assert response.status_code == 400
    payload = response.json()
    assert payload["detail"] == "Reference audio exceeds the 20MB limit"


@pytest.mark.asyncio
async def test_generate_voice_handles_tts_failure(monkeypatch, tmp_path):
    normalized_path = tmp_path / "normalized.wav"

    async def fake_save(file):
        normalized_path.write_bytes(await file.read())
        return normalized_path

    async def fake_synthesize(*_args, **_kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("app.api.v1.voice_clone.save_and_normalize", fake_save)
    monkeypatch.setattr("app.api.v1.voice_clone.synthesize_voice", fake_synthesize)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await _post_voice_clone(client)

    assert response.status_code == 500
    payload = response.json()
    assert payload["detail"] == "Voice synthesis failed"

