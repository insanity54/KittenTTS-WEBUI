# KittenTTS GUI

[![CI](https://github.com/insanity54/KittenTTS-WEBUI/actions/workflows/ci.yml/badge.svg)](https://github.com/insanity54/KittenTTS-WEBUI/actions/workflows/ci.yml) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/insanity54/kittentts-webui) [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/insanity54/KittenTTS-WEBUI)

A sleek, web-based interface for the **KittenTTS** text-to-speech engine. This application allows you to generate high-quality audio from text using various voices and automatically saves the output as unique WAV files.

## Features

- **Web GUI**: Easy-to-use interface built with FastAPI.
- **REST API**: OpenAPI (Swagger) JSON spec and ReDoc.
- **High Quality**: Uses the `KittenML/kitten-tts-mini-0.8` model for great voice quality.
- **Multiple Voices**: Choose from a variety of male and female voices (Bella, Kiki, Luna, Rosie, Bruno, Hugo, Jasper, Leo).
- **Auto-Saving**: Audio files are automatically saved to an `output/` directory with unique timestamps.
- **CPU Efficient**: Works seamlessly without requiring a GPU.

## Usage

    docker run --rm --name kittentts -p 7689:7689 -it insanity54/kittentts

Visit http://localhost:7689 in your web browser.

![Web UI Example](https://raw.githubusercontent.com/insanity54/KittenTTS-WEBUI/main/static/example.png)

Alternatively, you can use the REST API.

    http POST localhost:7689/api/speech "text=hello world" "voice=Kiki"
    HTTP/1.1 200 OK
    content-length: 58
    content-type: application/json
    date: Fri, 24 Apr 2026 07:18:46 GMT
    server: uvicorn

    {
        "filename": "Kiki_20260424-071847.wav",
        "status": "success"
    }


## Changelog

### 2026-04-23

Created fork of https://github.com/KittenML/KittenTTS, with opinionated changes. The WebUI has been made more user friendly, and the CSS has been simplified. OpenAPI (Swagger) has been added at `/docs`. Added Dockerfile and goreleaser CI script.


## Dev notes

    uv run src/kittentts_webui

## See also

  * https://clowerweb.github.io/kitten-tts-web-demo/
  * https://github.com/DipFlip/KittenTTSWeb


## Contributing

Please feel free to open an issue or start a discussion. I run this TTS as part of my Twitch.tv streamer tools website https://confettihat.com so I want to keep it working good for myself and the community.