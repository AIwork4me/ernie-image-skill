# AIwork4me/ernie-image-skill

[![Validate skill](https://github.com/AIwork4me/ernie-image-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/AIwork4me/ernie-image-skill/actions/workflows/validate.yml)

`ernie-image-skill` is a Claude Code skill for generating local PNG images with
Baidu AI Studio's ERNIE-Image and ERNIE-Image-Turbo models through an
OpenAI-compatible API. The Claude skill name is `ernie-image`.

It is designed for explicit ERNIE/Baidu image-generation requests, especially
Chinese-language text-to-image workflows. Prompts are sent to Baidu AI Studio,
so do not include secrets, credentials, private personal data, or confidential
business content.

## Features

- ERNIE-Image-Turbo for fast drafts and ERNIE-Image for higher-quality outputs.
- Seven supported sizes across square, landscape, and portrait ratios.
- Batch generation from 1 to 4 images.
- Optional seed for reproducible generations.
- Adjustable inference steps, guidance scale, and prompt enhancement.
- Local PNG output with `MEDIA:<absolute-path>` lines for compatible clients.
- JSON output for automation and tests.
- Safe output filenames that avoid path traversal and accidental overwrites.

## Install as a Claude Code Skill

Copy this repository into a skill directory named `ernie-image`:

```bash
mkdir -p ~/.claude/skills
cp -r ernie-image-skill ~/.claude/skills/ernie-image
```

Project-level install:

```bash
mkdir -p .claude/skills
cp -r ernie-image-skill .claude/skills/ernie-image
```

The directory name must match the skill name in `SKILL.md`: `ernie-image`.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Baidu AI Studio access token:
  <https://aistudio.baidu.com/account/accessToken>

Set your API key locally:

```bash
export AI_STUDIO_API_KEY="your_access_token"
```

PowerShell:

```powershell
$env:AI_STUDIO_API_KEY = "your_access_token"
```

## CLI Examples

Generate one image:

```bash
uv run scripts/generate.py "A cinematic sunset over the ocean, wide angle, warm light"
```

Use the higher-quality model:

```bash
uv run scripts/generate.py "A futuristic city at night, rain, neon reflections" --model ERNIE-Image --size 1376x768 --steps 16 --guidance 3.0
```

Chinese prompt:

```bash
uv run scripts/generate.py "一只可爱的橘猫坐在窗台上，柔和晨光，摄影风格" --size 1024x1024
```

Structured JSON output:

```bash
uv run scripts/generate.py "minimal product photo of a ceramic mug" --json
```

## CLI Options

| Option | Default | Description |
|---|---|---|
| `prompt` | required | Image description, max 1024 characters |
| `--model` | `ERNIE-Image-Turbo` | `ERNIE-Image` or `ERNIE-Image-Turbo` |
| `--size` | `1024x1024` | Image dimensions |
| `--n` | 1 | Number of images, 1-4 |
| `--output` | `.` | Output directory |
| `--format` | `b64_json` | API response format: `b64_json` or `url` |
| `--seed` | random | Reproducibility seed |
| `--steps` | provider default | Inference steps, 4-20 |
| `--guidance` | provider default | Guidance scale, 1.0-7.5 |
| `--use-pe` | off | Enable prompt enhancement |
| `--prefix` | `ernie` | Safe output filename prefix |
| `--json` | off | Print structured JSON |

## Supported Sizes

| Size | Ratio | Best for |
|---|---|---|
| `1024x1024` | 1:1 | General purpose |
| `1376x768` | 16:9 | Headers, wallpapers, presentation visuals |
| `1264x848` | 3:2 | Photography-style landscapes |
| `1200x896` | 4:3 | Product shots and traditional landscape layouts |
| `896x1200` | 3:4 | Portrait cards and print layouts |
| `848x1264` | 2:3 | Posters, covers, portraits |
| `768x1376` | 9:16 | Mobile wallpapers and story covers |

## Development

Run tests:

```bash
uv run python -m unittest discover -s tests
```

Validate the skill structure from a directory named `ernie-image`:

```bash
uvx --from skills-ref agentskills validate /path/to/ernie-image
```

## License

MIT-0
