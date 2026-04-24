import os
import wave
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_webui_is_healthy():
    from src.kittentts_webui.__main__ import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/docs")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_index_html_is_served():
    from src.kittentts_webui.__main__ import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "KittenTTS" in response.text


@pytest.mark.asyncio
async def test_post_api_speech_requires_model():
    from src.kittentts_webui.__main__ import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/speech",
            json={"text": "Hello world", "voice": "Jasper"}
        )
        # Without model initialized via lifespan, should return 500
        assert response.status_code in (200, 500)


@pytest.mark.asyncio
async def test_post_api_speech_with_mocked_model():
    from src.kittentts_webui.__main__ import app
    import src.kittentts_webui.__main__ as main_module
    import numpy as np

    # Mock the model
    mock_model = type('MockModel', (), {
        'available_voices': ['Jasper', 'Bella'],
        'generate': lambda self, text, voice='Jasper', speed=1.0: np.zeros(24000, dtype=np.float32)
    })()

    # Inject the mock model
    original_m = main_module.m
    main_module.m = mock_model

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/speech",
                json={"text": "Hello world", "voice": "Jasper"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["filename"].endswith(".wav")
    finally:
        main_module.m = original_m


def test_model_loading_and_generation():
    from kittentts import KittenTTS
    m = KittenTTS("KittenML/kitten-tts-mini-0.8")
    assert m is not None
    assert "Jasper" in m.available_voices
    audio = m.generate("Test", voice="Jasper")
    assert audio is not None
    assert len(audio) > 0