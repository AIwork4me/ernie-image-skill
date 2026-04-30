# ERNIE-Image Skill

Generate images using Baidu AI Studio's ERNIE-Image and ERNIE-Image-Turbo models via the OpenAI-compatible API. A Claude Code skill for high-quality text-to-image generation with excellent Chinese language support.

## Features

- Two model tiers: ERNIE-Image-Turbo (fast) and ERNIE-Image (high quality)
- 7 supported image sizes covering square, landscape, and portrait ratios
- Batch generation (1-4 images per request)
- Seed-based reproducibility for consistent results
- Adjustable quality parameters (inference steps, guidance scale)
- Prompt enhancement for automatic prompt optimization
- Excellent Chinese and English prompt support

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Baidu AI Studio access token ([get one here](https://aistudio.baidu.com/account/accessToken))

## Quick Start

1. Set your API key:

```bash
export AI_STUDIO_API_KEY="your_access_token"
```

2. Generate an image:

```bash
uv run scripts/generate.py "一只可爱的猫咪坐在窗台上"
```

3. With options:

```bash
uv run scripts/generate.py "sunset over the ocean" --model ERNIE-Image --size 1376x768 --steps 16 --guidance 3.0
```

## CLI Options

| Option | Default | Description |
|---|---|---|
| `prompt` | (required) | Image description, max 1024 chars |
| `--model` | `ERNIE-Image-Turbo` | Model: `ERNIE-Image` or `ERNIE-Image-Turbo` |
| `--size` | `1024x1024` | Image dimensions (7 options) |
| `--n` | 1 | Number of images (1-4) |
| `--output` | `.` | Output directory |
| `--seed` | random | Reproducibility seed |
| `--steps` | 8 | Inference steps (4-20) |
| `--guidance` | 1.0 | Guidance scale (1.0-7.5) |
| `--use-pe` | off | Enable prompt enhancement |
| `--prefix` | `ernie` | Output filename prefix |
| `--json` | off | Output structured JSON |

## Supported Sizes

| Size | Ratio | Best For |
|---|---|---|
| `1024x1024` | 1:1 | General purpose (default) |
| `1376x768` | 16:9 | Desktop wallpapers, headers |
| `1264x848` | 3:2 | Photography landscapes |
| `1200x896` | 4:3 | Traditional landscape |
| `896x1200` | 3:4 | Instagram, print photos |
| `848x1264` | 2:3 | Portrait photography |
| `768x1376` | 9:16 | Mobile wallpapers, stories |

## Install as Claude Code Skill

Copy the skill folder to your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -r SKILL.md scripts references .claude/skills/ernie-image/
```

Or install from ClawHub:

```bash
clawhub install ernie-image
```

## Follow Me

Scan the QR code to follow:

<p align="center">
  <img src="assets/aiwork4me.jpg" alt="Scan to follow" width="200">
</p>

## License

MIT-0
