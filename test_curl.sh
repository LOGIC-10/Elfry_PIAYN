
#!/bin/bash

curl -X POST https://bccb-2601-14d-4884-1ca0-b086-1a9-8b80-8f7.ngrok-free.app/generate \
-H "Content-Type: application/json" \
-d '{
    "google_api_key": "YOUR_API_KEY",
    "model_name": "gemini-pro-vision",
    "prompt": "Describe these images in detail",
    "images": [
        "'$(base64 -i /Users/logic/Downloads/elf.png)'"
    ],
    "temperature": 0.7,
    "max_tokens": 4096
}'