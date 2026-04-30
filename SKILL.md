---
name: ernie-image
description: >-
  Generate images using Baidu AI Studio's ERNIE-Image and ERNIE-Image-Turbo models
  via the OpenAI-compatible API. Supports text-to-image generation with 7 size
  options (square, landscape, portrait), batch generation (1-4 images), seed-based
  reproducibility, and adjustable quality parameters (inference steps, guidance scale,
  prompt enhancement). Use when users ask to generate images, create AI art, make
  pictures, produce artwork, or need Chinese-language image generation. Also triggers
  on "ERNIE Image", "ERNIE-Image", "ERNIE-Image-Turbo", "Baidu image generation",
  "AI Studio image", "百度生图", "文生图", "生成图片", "AI绘图". Prefer this skill
  over generic image generation when the user mentions Baidu, ERNIE, AI Studio, or
  Chinese-language prompts.
homepage: https://github.com/AIwork4me/ernie-image-skill
metadata:
  openclaw:
    emoji: "\U0001F3A8"
    requires:
      env:
        - AI_STUDIO_API_KEY
    primaryEnv: AI_STUDIO_API_KEY
---

# ERNIE-Image Generation

Generate images using Baidu AI Studio's ERNIE-Image models through the OpenAI-compatible API. Two models are available:

- **ERNIE-Image-Turbo** (default): Fast generation, excellent for most use cases
- **ERNIE-Image**: Higher quality, slower generation for when detail matters

Both models understand Chinese prompts particularly well.

## Prerequisites

- Python 3.11+ with `uv` installed
- `AI_STUDIO_API_KEY` environment variable set to your Baidu AI Studio access token
- Get a token at: https://aistudio.baidu.com/account/accessToken

## Generation Workflow

### Step 1 -- Compose the prompt

Write a descriptive prompt (max 1024 characters, ~150 words). Chinese and English both work well. Be specific about subject, style, composition, and mood.

Good: "A golden retriever puppy sitting in a sunflower field at sunset, warm golden light, shallow depth of field, professional photography"
Bad: "dog"

### Step 2 -- Choose parameters

| Parameter | Values | Default |
|---|---|---|
| model | `ERNIE-Image-Turbo`, `ERNIE-Image` | `ERNIE-Image-Turbo` |
| size | `1024x1024`, `768x1376`, `1376x768`, `896x1200`, `1200x896`, `848x1264`, `1264x848` | `1024x1024` |
| n | 1-4 | 1 |
| seed | any integer | random |
| steps | 4-20 | 8 |
| guidance | 1.0-7.5 | 1.0 |
| use-pe | flag | off |

Select size based on content: portraits and posters use vertical (`768x1376`, `848x1264`, `896x1200`), landscapes and covers use horizontal (`1376x768`, `1264x848`, `1200x896`), general use `1024x1024`.

### Step 3 -- Run the generation script

Execute the bundled script with `uv run`:

```bash
uv run {baseDir}/scripts/generate.py "<PROMPT>" --model ERNIE-Image-Turbo --size 1024x1024
```

For batch generation:

```bash
uv run {baseDir}/scripts/generate.py "<PROMPT>" --n 4 --output ./output_dir
```

For higher quality with more inference steps and stronger guidance:

```bash
uv run {baseDir}/scripts/generate.py "<PROMPT>" --model ERNIE-Image --steps 16 --guidance 3.5
```

For reproducible results:

```bash
uv run {baseDir}/scripts/generate.py "<PROMPT>" --seed 42
```

### Step 4 -- Output

The script saves images as PNG files to the output directory and prints:

```
Saved: ernie_20260430_110100.png (1.7 MB)
MEDIA:/absolute/path/to/ernie_20260430_110100.png
```

The `MEDIA:` line enables automatic image attachment in compatible environments.

For JSON output, add `--json` to get structured results:

```json
{
  "success": true,
  "model": "ERNIE-Image-Turbo",
  "files": [{"path": "/abs/path/ernie_20260430_110100.png", "size_bytes": 1715660}],
  "prompt": "...",
  "parameters": {"size": "1024x1024", "seed": 42}
}
```

## Quick Triggers

When the user says any of these, treat the text after the trigger as the prompt and generate immediately with defaults:

- Chinese: "生成图片：xxx" / "文生图：xxx" / "百度生图：xxx" / "ERNIE生图：xxx"
- English: "generate image: xxx" / "ernie image: xxx" / "baidu image: xxx"

Defaults: model=`ERNIE-Image-Turbo`, size=`1024x1024`, n=1, b64_json format.

## Notes

- Images are saved locally as PNG files with `MEDIA:<path>` for auto-attach.
- Chinese prompts work particularly well with ERNIE models.
- Prompt enhancement (`--use-pe`) lets the model expand simple prompts into richer descriptions before generation. Enable for short prompts, disable for precise control.
- For full API reference, model comparison, all size options, parameter details, and troubleshooting, read `{baseDir}/references/api-guide.md`.
