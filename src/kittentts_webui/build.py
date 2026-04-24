#!/usr/bin/env python3
from huggingface_hub import snapshot_download
from kittentts import KittenTTS

print("Downloading and caching model...")
model_path = snapshot_download("KittenML/kitten-tts-mini-0.8")
m = KittenTTS(model_path=model_path)
print("Model ready!")