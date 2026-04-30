#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=2.33.0"]
# ///
"""
ERNIE-Image generation script for Claude Code skill.

Generate images using Baidu AI Studio's ERNIE-Image models via the
OpenAI-compatible API.

Usage:
    uv run scripts/generate.py "prompt text" [options]

Environment:
    AI_STUDIO_API_KEY  Required. Your Baidu AI Studio access token.
                       Get one at: https://aistudio.baidu.com/account/accessToken
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

from openai import OpenAI

API_BASE_URL = "https://aistudio.baidu.com/llm/lmapi/v3"
VALID_SIZES = [
    "1024x1024",
    "1376x768",
    "1264x848",
    "1200x896",
    "896x1200",
    "848x1264",
    "768x1376",
]
VALID_MODELS = ["ERNIE-Image", "ERNIE-Image-Turbo"]
MAX_PROMPT_LENGTH = 1024


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate images using ERNIE-Image models via Baidu AI Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s "一只可爱的猫咪坐在窗台上"
  %(prog)s "a sunset over the ocean" --model ERNIE-Image --size 1376x768
  %(prog)s "mountain landscape" --n 2 --seed 42 --steps 12 --guidance 3.0
  %(prog)s "city skyline" --output ./images --prefix skyline --json
""",
    )
    parser.add_argument("prompt", help="Image generation prompt (max 1024 chars)")
    parser.add_argument(
        "--model",
        default="ERNIE-Image-Turbo",
        choices=VALID_MODELS,
        help="Model to use (default: ERNIE-Image-Turbo)",
    )
    parser.add_argument(
        "--size",
        default="1024x1024",
        choices=VALID_SIZES,
        help="Image dimensions (default: 1024x1024)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        choices=range(1, 5),
        metavar="1-4",
        help="Number of images to generate (default: 1)",
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--format",
        dest="response_format",
        default="b64_json",
        choices=["b64_json", "url"],
        help="Response format (default: b64_json)",
    )
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")
    parser.add_argument(
        "--steps",
        type=int,
        default=None,
        metavar="4-20",
        help="Number of inference steps (default: 8)",
    )
    parser.add_argument(
        "--guidance",
        type=float,
        default=None,
        help="Guidance scale 1.0-7.5 (default: 1.0)",
    )
    parser.add_argument(
        "--use-pe",
        action="store_true",
        default=False,
        help="Enable prompt enhancement",
    )
    parser.add_argument(
        "--prefix",
        default="ernie",
        help="Output filename prefix (default: ernie)",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output result as JSON to stdout",
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if len(args.prompt) > MAX_PROMPT_LENGTH:
        print(
            f"Error: Prompt is {len(args.prompt)} characters, "
            f"exceeding the {MAX_PROMPT_LENGTH} character limit.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.guidance is not None and (args.guidance < 1.0 or args.guidance > 7.5):
        print("Error: --guidance must be between 1.0 and 7.5", file=sys.stderr)
        sys.exit(1)

    if args.steps is not None and (args.steps < 4 or args.steps > 20):
        print("Error: --steps must be between 4 and 20", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        print(f"Error: {args.output} is not a directory", file=sys.stderr)
        sys.exit(1)


def build_extra_body(args: argparse.Namespace) -> dict:
    extra = {}
    if args.seed is not None:
        extra["seed"] = args.seed
    if args.use_pe:
        extra["use_pe"] = True
    if args.steps is not None:
        extra["num_inference_steps"] = args.steps
    if args.guidance is not None:
        extra["guidance_scale"] = args.guidance
    return extra


def generate_image(args: argparse.Namespace) -> object:
    api_key = os.environ.get("AI_STUDIO_API_KEY")
    if not api_key:
        print(
            "Error: AI_STUDIO_API_KEY environment variable is not set.\n"
            "Get your access token at: https://aistudio.baidu.com/account/accessToken",
            file=sys.stderr,
        )
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url=API_BASE_URL,
        default_headers={"X-Client-Platform": "aistudio"},
    )

    extra_body = build_extra_body(args)

    try:
        response = client.images.generate(
            model=args.model,
            prompt=args.prompt,
            n=args.n,
            size=args.size,
            response_format=args.response_format,
            extra_body=extra_body if extra_body else None,
        )
    except Exception as e:
        error_msg = str(e)
        print(f"Error: API call failed: {error_msg}", file=sys.stderr)
        if "401" in error_msg or "403" in error_msg:
            print(
                "Hint: Check that your AI_STUDIO_API_KEY is valid.\n"
                "Get a fresh token at: https://aistudio.baidu.com/account/accessToken",
                file=sys.stderr,
            )
        sys.exit(1)

    return response


def save_images(response, args: argparse.Namespace) -> list[dict]:
    output_dir = Path(args.output).resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    files = []

    for i, img_data in enumerate(response.data):
        suffix = f"_{i + 1}" if args.n > 1 else ""
        filename = f"{args.prefix}_{timestamp}{suffix}.png"
        filepath = output_dir / filename

        if args.response_format == "b64_json":
            img_bytes = base64.b64decode(img_data.b64_json)
            filepath.write_bytes(img_bytes)
        else:
            urllib.request.urlretrieve(img_data.url, str(filepath))

        size_bytes = filepath.stat().st_size
        files.append({
            "path": str(filepath),
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
        })

    return files


def main():
    parser = create_parser()
    args = parser.parse_args()
    validate_args(args)

    if not args.json_output:
        print(f"Generating image with {args.model}...")
        print(f'Prompt: "{args.prompt}"')
        details = f"Size: {args.size}"
        if args.seed is not None:
            details += f", Seed: {args.seed}"
        if args.steps is not None:
            details += f", Steps: {args.steps}"
        if args.guidance is not None:
            details += f", Guidance: {args.guidance}"
        print(details)

    response = generate_image(args)
    files = save_images(response, args)

    if args.json_output:
        result = {
            "success": True,
            "model": args.model,
            "prompt": args.prompt,
            "parameters": {
                "size": args.size,
                "n": args.n,
                "seed": args.seed,
                "steps": args.steps,
                "guidance": args.guidance,
                "use_pe": args.use_pe,
            },
            "files": files,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for f in files:
            print(f"\nSaved: {Path(f['path']).name} ({f['size_mb']} MB)")
            print(f"MEDIA:{f['path']}")


if __name__ == "__main__":
    main()
