# ERNIE-Image API Guide

This guide covers the Baidu AI Studio ERNIE-Image models used by the
`ernie-image-skill` Claude Code skill.

## Scope and Privacy

The generation prompt and parameters are sent to Baidu AI Studio. Do not include
secrets, credentials, private personal data, or confidential business data in a
prompt. Follow Baidu AI Studio terms and applicable platform rules for generated
content.

## Models

| Model | Speed | Quality | Best for |
|---|---|---|---|
| `ERNIE-Image-Turbo` | Faster | Good | Drafts, iteration, batch previews |
| `ERNIE-Image` | Slower | Higher | Final images and detail-heavy prompts |

Use Turbo by default. Switch to `ERNIE-Image` when the user explicitly asks for
the best quality or when the prompt has many details.

## Sizes

| Size | Aspect ratio | Best for |
|---|---|---|
| `1024x1024` | 1:1 | General purpose |
| `1376x768` | 16:9 | Headers, wallpapers, presentation visuals |
| `1264x848` | 3:2 | Photography-style landscapes |
| `1200x896` | 4:3 | Product shots and traditional landscape layouts |
| `896x1200` | 3:4 | Portrait cards and print layouts |
| `848x1264` | 2:3 | Posters, covers, portraits |
| `768x1376` | 9:16 | Mobile wallpapers and story covers |

Choose vertical sizes for posters, portraits, and mobile scenes. Choose
horizontal sizes for covers, landscapes, and presentations. Use square when the
layout is unspecified.

## Parameters

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `prompt` | string | required | Max 1024 characters |
| `--model` | enum | `ERNIE-Image-Turbo` | `ERNIE-Image` or `ERNIE-Image-Turbo` |
| `--n` | integer | 1 | 1-4 images |
| `--size` | enum | `1024x1024` | One of the supported sizes |
| `--format` | enum | `b64_json` | `b64_json` or `url` |
| `--seed` | integer | random | Helps reproduce similar outputs |
| `--use-pe` | flag | off | Enables provider prompt enhancement |
| `--steps` | integer | provider default | 4-20 |
| `--guidance` | float | provider default | 1.0-7.5 |

## Prompt Writing

A strong prompt usually includes:

```text
Subject + setting + style + lighting + mood + composition
```

Good English example:

```text
A golden retriever puppy sitting in a sunflower field at sunset, warm golden light, shallow depth of field, professional photography
```

Good Chinese example:

```text
赛博朋克风格的未来城市街道，霓虹灯闪烁，雨天，湿润路面反射灯光，电影级构图
```

Short prompts work, but enabling `--use-pe` can help the provider expand them.
Disable prompt enhancement when exact control matters.

## Authentication

Create an access token at:

```text
https://aistudio.baidu.com/account/accessToken
```

Set it in the shell environment:

```bash
export AI_STUDIO_API_KEY="your_access_token_here"
```

PowerShell:

```powershell
$env:AI_STUDIO_API_KEY = "your_access_token_here"
```

Never commit this token, paste it into chat, or include it in prompts.

## Troubleshooting

| Error | Likely cause | Solution |
|---|---|---|
| `AI_STUDIO_API_KEY environment variable is not set` | Missing token | Set the environment variable locally |
| 401 or 403 | Invalid token or missing model permission | Create a fresh token or check account permissions |
| Content filtered | Provider rejected the prompt | Rephrase within provider and platform rules |
| Timeout or network failure | Slow API or temporary connectivity issue | Retry with `n=1`, then increase batch size |
| Invalid size | Unsupported dimensions | Use one of the seven supported sizes |
| Invalid prefix | Unsafe filename prefix | Use letters, numbers, `_`, `-`, or `.` |
| `uv run` fails | uv or Python missing | Install uv and use Python 3.11+ |

## Raw API Sketch

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AI_STUDIO_API_KEY"],
    base_url="https://aistudio.baidu.com/llm/lmapi/v3",
    default_headers={"X-Client-Platform": "aistudio"},
)

response = client.images.generate(
    model="ERNIE-Image-Turbo",
    prompt="一只可爱的橘猫坐在窗台上，柔和晨光，摄影风格",
    n=1,
    response_format="b64_json",
    size="1024x1024",
)
```
