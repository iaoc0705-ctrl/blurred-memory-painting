#!/usr/bin/env python3
"""Generate one image from text through an OpenAI-compatible o10.top endpoint.

Reads O10_API_KEY (required), O10_BASE_URL (optional, default https://o10.top/v1) and
O10_IMAGE_MODEL (optional, default gpt-image-2.5-sunburst). On Windows the variables
are also read from the current user Environment registry key.

    python scripts/generate_image.py --prompt-file prompt.txt --output out.png --size 1024x1280

Never pass the API key as a command-line argument.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "https://o10.top/v1"
DEFAULT_MODEL = "gpt-image-2.5-sunburst"


def windows_user_env(name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
            return str(value).strip() or None
    except (FileNotFoundError, OSError):
        return None


def config(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value:
        return value.strip()
    return windows_user_env(name) or default


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one image from text using the configured o10.top account."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text.")
    prompt_group.add_argument("--prompt-file", type=Path, help="UTF-8 prompt file.")
    parser.add_argument("--output", type=Path, required=True, help="Output image path.")
    parser.add_argument("--model", default=config("O10_IMAGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--size", default="1024x1280")
    parser.add_argument("--base-url", default=config("O10_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--timeout", type=int, default=180)
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> str:
    prompt = (
        args.prompt_file.read_text(encoding="utf-8")
        if args.prompt_file is not None
        else args.prompt
    )
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("Prompt must not be empty.")
    return prompt


def request_image(args: argparse.Namespace, prompt: str, api_key: str) -> dict:
    base_url = args.base_url.rstrip("/")
    endpoint = f"{base_url}/images/generations"
    payload = json.dumps(
        {"model": args.model, "prompt": prompt, "n": 1, "size": args.size}
    ).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "blurred-memory-painting-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(body).get("error", {}).get("message", body)
        except json.JSONDecodeError:
            detail = body
        raise RuntimeError(f"Image API returned HTTP {exc.code}: {detail[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Unable to reach the image API: {exc.reason}") from exc


def image_bytes(result: dict, timeout: int) -> bytes:
    try:
        item = result["data"][0]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Image API response did not contain data[0].") from exc

    encoded = item.get("b64_json")
    if encoded:
        try:
            return base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError) as exc:
            raise RuntimeError("Image API returned invalid base64 image data.") from exc

    image_url = item.get("url")
    if image_url:
        parsed = urllib.parse.urlparse(image_url)
        if parsed.scheme not in {"http", "https"}:
            raise RuntimeError("Image API returned an unsupported image URL.")
        with urllib.request.urlopen(image_url, timeout=timeout) as response:
            return response.read()

    raise RuntimeError("Image API response contained neither b64_json nor url.")


def main() -> int:
    args = parse_args()
    api_key = config("O10_API_KEY")
    if not api_key:
        print(
            "O10_API_KEY is not configured. Set it as a user environment variable.",
            file=sys.stderr,
        )
        return 2

    try:
        prompt = load_prompt(args)
        result = request_image(args, prompt, api_key)
        content = image_bytes(result, args.timeout)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(content)
    except (OSError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(str(args.output.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
