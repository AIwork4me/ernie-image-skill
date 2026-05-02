---
name: ernie-image-skill
description: "Generate images with Baidu AI Studio ERNIE-Image models through an OpenAI-compatible API. Use when the user explicitly asks for ERNIE-Image, Baidu AI Studio image generation, or Chinese-language text-to-image output and has AI_STUDIO_API_KEY configured. Prompts are sent to Baidu AI Studio; do not use for secrets, private data, unsafe content, or requests that violate provider or platform rules."
license: MIT-0
metadata:
  version: "1.1.0"
  author: "aiwork4me"
  provider: "Baidu AI Studio"
  required_env:
    - AI_STUDIO_API_KEY
  openclaw:
    emoji: "\U0001F3A8"
    requires:
      env:
        - AI_STUDIO_API_KEY
    primaryEnv: AI_STUDIO_API_KEY
---

# ERNIE-Image Skill

Generate images with Baidu AI Studio's ERNIE-Image models through the
OpenAI-compatible API. This skill is best when the user specifically wants
Baidu/ERNIE generation, Chinese-language image prompts, or local PNG outputs
from a configured `AI_STUDIO_API_KEY`.

## Safety Boundary

- Use this skill only for explicit image-generation requests.
- Prompts and generation parameters are sent to Baidu AI Studio. Do not include
  secrets, credentials, private personal data, or confidential business data in
  prompts.
- Follow Baidu AI Studio terms and applicable platform rules. Decline unsafe,
  deceptive, exploitative, or rights-violating image requests.
- Do not print, store, or ask the user to paste `AI_STUDIO_API_KEY` into chat.
  The script reads it from the environment only.
- Generated files are written locally. Confirm the output directory when the
  user has not specified one.

## Models

| Model | Best for |
|---|---|
| `ERNIE-Image-Turbo` | Fast drafts, iteration, batch previews |
| `ERNIE-Image` | Slower, higher-quality final outputs |

Chinese prompts usually work especially well with these models.

## Before Running

Confirm that `AI_STUDIO_API_KEY` is set in the shell environment. If it is
missing, tell the user to create an access token at
`https://aistudio.baidu.com/account/accessToken` and set it locally.

Prefer `ERNIE-Image-Turbo`, `1024x1024`, `n=1`, and `b64_json` unless the user
asks for different parameters.

## Execution

Run from the skill directory so `uv` can use the bundled project metadata and
lockfile:

```bash
cd "${CLAUDE_SKILL_DIR}" && uv run scripts/generate.py "<PROMPT>" --model ERNIE-Image-Turbo --size 1024x1024
```

Batch generation:

```bash
cd "${CLAUDE_SKILL_DIR}" && uv run scripts/generate.py "<PROMPT>" --n 4 --output "<output_dir>"
```

Higher-quality generation:

```bash
cd "${CLAUDE_SKILL_DIR}" && uv run scripts/generate.py "<PROMPT>" --model ERNIE-Image --steps 16 --guidance 3.5
```

Reproducible generation:

```bash
cd "${CLAUDE_SKILL_DIR}" && uv run scripts/generate.py "<PROMPT>" --seed 42
```

Structured output:

```bash
cd "${CLAUDE_SKILL_DIR}" && uv run scripts/generate.py "<PROMPT>" --json
```

## Parameters

| Parameter | Values | Default |
|---|---|---|
| `--model` | `ERNIE-Image-Turbo`, `ERNIE-Image` | `ERNIE-Image-Turbo` |
| `--size` | `1024x1024`, `768x1376`, `1376x768`, `896x1200`, `1200x896`, `848x1264`, `1264x848` | `1024x1024` |
| `--n` | 1-4 | 1 |
| `--seed` | integer | random |
| `--steps` | 4-20 | provider default |
| `--guidance` | 1.0-7.5 | provider default |
| `--use-pe` | flag | off |
| `--prefix` | safe filename prefix | `ernie` |
| `--json` | flag | off |

Select vertical sizes for posters, portraits, and mobile layouts; horizontal
sizes for covers, wallpapers, and presentation visuals; square for general use.

## Output

The script saves PNG files and prints one `MEDIA:<absolute-path>` line per image
for compatible clients. With `--json`, it prints:

```json
{
  "success": true,
  "model": "ERNIE-Image-Turbo",
  "prompt": "...",
  "parameters": {"size": "1024x1024", "n": 1, "seed": 42},
  "files": [{"path": "/abs/path/ernie_20260502_140000.png", "size_bytes": 1715660}]
}
```

The script avoids overwriting existing files by adding a numeric suffix when
needed.

## Useful Triggers

Treat the text after these explicit triggers as the prompt:

- English: `ernie image: ...`, `baidu image: ...`, `AI Studio image: ...`
- Chinese: `文心生图：...`, `百度生图：...`, `生成图片：...`

For full API notes, prompt guidance, and troubleshooting, read
`references/api-guide.md`.
