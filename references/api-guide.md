# ERNIE-Image API Reference

Complete reference for the ERNIE-Image and ERNIE-Image-Turbo image generation models via Baidu AI Studio.

## Table of Contents

1. [Model Comparison](#model-comparison)
2. [Supported Image Sizes](#supported-image-sizes)
3. [Generation Parameters](#generation-parameters)
4. [Prompt Writing Guide](#prompt-writing-guide)
5. [Authentication](#authentication)
6. [Troubleshooting](#troubleshooting)
7. [Raw API Example](#raw-api-example)

---

## Model Comparison

| Feature | ERNIE-Image-Turbo | ERNIE-Image |
|---|---|---|
| Speed | Fast (~3-5s) | Slower (~8-15s) |
| Quality | Good | Excellent |
| Detail | Standard | High detail, better textures |
| Best for | Quick iterations, batch generation | Final output, complex scenes |
| Default steps | 8 | 8 (benefits more from higher steps) |

**Recommendation**: Use ERNIE-Image-Turbo for exploration and prototyping. Switch to ERNIE-Image when you need the best quality for final output.

---

## Supported Image Sizes

Seven sizes are supported, covering all common aspect ratios:

| Size | Aspect Ratio | Best For |
|---|---|---|
| `1024x1024` | 1:1 (Square) | General purpose, social media posts, profile pictures, thumbnails |
| `1376x768` | 16:9 (Landscape) | Desktop wallpapers, website headers, YouTube thumbnails, presentations |
| `1264x848` | 3:2 (Landscape) | Photography style landscapes, photo prints, blog headers |
| `1200x896` | 4:3 (Landscape) | Traditional photo prints, product shots, blog headers |
| `896x1200` | 3:4 (Portrait) | Instagram posts, print photos, magazine layouts |
| `848x1264` | 2:3 (Portrait) | Photography style portraits, book covers, posters |
| `768x1376` | 9:16 (Portrait) | Mobile wallpapers, stories, short video covers, phone lock screens |

**Selection guide**: Portraits and posters → vertical sizes. Landscapes and covers → horizontal sizes. Unsure → use default `1024x1024`.

---

## Generation Parameters

### Core Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `prompt` | string | Yes | — | Text description of the desired image. Max 1024 characters, ~150 words recommended. |
| `model` | string | Yes | — | `ERNIE-Image` or `ERNIE-Image-Turbo` |
| `n` | int | No | 1 | Number of images to generate (1-4) |
| `size` | string | No | `1024x1024` | One of the 7 supported sizes |
| `response_format` | string | No | `b64_json` | `b64_json` (direct image data) or `url` (7-day link) |

### Advanced Parameters (via extra_body)

#### seed (integer, optional)
- **Purpose**: Fix the random seed for reproducible results
- **Behavior**: Same seed + same prompt + same parameters = highly similar images
- **Use case**: Batch production with consistent style, A/B testing prompt variations
- **Example**: `--seed 42`

#### use_pe (boolean, default: false)
- **Purpose**: Prompt Enhancement — let the model automatically expand your prompt
- **When to enable**: Simple or short prompts that need more visual detail
- **When to disable**: Precise prompts where you want exact control over the output
- **Example**: `--use-pe`

#### num_inference_steps (integer, 4-20, default: 8)
- **Purpose**: Control the number of denoising iterations
- **Trade-off**: Higher = better quality but slower generation
- **Recommended**: 8 for ERNIE-Image-Turbo, 12-16 for ERNIE-Image
- **Example**: `--steps 12`

#### guidance_scale (float, 1.0-7.5, default: 1.0)
- **Purpose**: Control how closely the output follows the prompt
- **Low values (1.0-2.0)**: More creative, freer interpretation
- **Medium values (2.0-4.0)**: Balanced adherence
- **High values (4.0-7.5)**: Very literal, closely follows prompt, may look less natural
- **Example**: `--guidance 3.0`

---

## Prompt Writing Guide

### Recommended Structure

```
Subject + Setting + Style + Lighting + Mood
```

### Good Examples

**English**:
> "A golden retriever puppy sitting in a sunflower field at sunset, warm golden light, shallow depth of field, professional photography, 8K"

**Chinese**:
> "赛博朋克风格的未来城市街道，霓虹灯闪烁，雨天，倒影在湿润的路面上，8K超高清，电影级构图"

**Mixed**:
> "Chinese ink wash painting of a mountain landscape with mist, traditional style, monochrome, elegant brushstrokes, 水墨山水画"

### Bad Examples

- "pretty picture" — no visual content described
- "make it look good" — no subject or style
- 50+ word run-on sentences with no clear structure

### Chinese Prompt Tips

ERNIE models are trained extensively on Chinese data. Chinese prompts often produce better results for:
- Chinese cultural subjects (水墨画, 国画, 书法)
- Specific Chinese art styles and aesthetics
- Asian architecture and scenery
- Chinese festival themes (春节, 中秋, 龙舟)

---

## Authentication

### Getting Your Access Token

1. Visit https://aistudio.baidu.com/account/accessToken
2. Register or log in with your Baidu account
3. Copy your personal access token

### Setting the Environment Variable

**Linux/macOS**:
```bash
export AI_STUDIO_API_KEY="your_access_token_here"
```

**Windows (PowerShell)**:
```powershell
$env:AI_STUDIO_API_KEY = "your_access_token_here"
```

**Persistent (recommended)**: Add to your `.env` file or shell profile.

### Free Tier

AI Studio provides 1 million free tokens for each developer. Image generation consumes tokens based on model and parameters.

---

## Troubleshooting

| Error | Likely Cause | Solution |
|---|---|---|
| `AI_STUDIO_API_KEY not set` | Environment variable missing | Set the `AI_STUDIO_API_KEY` env var |
| 401 Unauthorized | Invalid or expired token | Generate a new access token at AI Studio |
| 403 Forbidden | No permission for the model | Check your AI Studio account permissions |
| Content filtered | Prompt contains restricted content | Rephrase the prompt to avoid sensitive topics |
| Timeout | Large `n` or complex prompt | Reduce `n`, simplify prompt, or increase timeout |
| Empty response | Temporary API issue | Retry after a few seconds |
| Invalid size | Size not in allowed list | Use one of the 7 supported sizes |
| `uv run` fails | uv not installed or Python < 3.11 | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

---

## Raw API Example

```python
import os
import base64
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("AI_STUDIO_API_KEY"),
    base_url="https://aistudio.baidu.com/llm/lmapi/v3",
    default_headers={"X-Client-Platform": "aistudio"},
)

# Basic generation
img = client.images.generate(
    model="ERNIE-Image-Turbo",
    prompt="一只可爱的猫咪坐在窗台上",
    n=1,
    response_format="b64_json",
    size="1024x1024",
)

# Save the image
with open("output.png", "wb") as f:
    f.write(base64.b64decode(img.data[0].b64_json))

# Advanced generation with all parameters
img = client.images.generate(
    model="ERNIE-Image",
    prompt="a majestic dragon flying over a medieval castle at sunset",
    n=2,
    response_format="b64_json",
    size="1376x768",
    extra_body={
        "seed": 42,
        "use_pe": True,
        "num_inference_steps": 16,
        "guidance_scale": 3.0,
    }
)

for i, item in enumerate(img.data):
    with open(f"output_{i}.png", "wb") as f:
        f.write(base64.b64decode(item.b64_json))
```

**Base URL**: `https://aistudio.baidu.com/llm/lmapi/v3`
**Required Header**: `X-Client-Platform: aistudio`
**Auth**: Bearer token via `api_key` parameter
