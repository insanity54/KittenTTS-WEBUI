# syntax=docker/dockerfile:1.7

FROM astral/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    uv pip install --system \
    https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl \
    fastapi uvicorn

RUN python -c "from kittentts import KittenTTS; KittenTTS('KittenML/kitten-tts-mini-0.8')"

FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    uv pip install --system \
    https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl \
    fastapi uvicorn

EXPOSE 7689
CMD ["python", "KittenTTS-WEBUI.py"]