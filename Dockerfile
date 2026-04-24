# syntax=docker/dockerfile:1.7

FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    uv pip install --system \
    https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl && \
    uv pip install --system \
    fastapi uvicorn

EXPOSE 7689
CMD ["python", "KittenTTS-WEBUI.py"]