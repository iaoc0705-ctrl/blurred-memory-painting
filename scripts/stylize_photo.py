#!/usr/bin/env python3
"""Restyle one or more photos into a painting-style image via an OpenAI-compatible endpoint.

Calls POST /v1/images/edits with multipart/form-data. Configuration is read from
the same environment variables as the other local image helpers:

    O10_API_KEY     required
    O10_BASE_URL    optional, default https://o10.top/v1
    O10_IMAGE_MODEL optional, default gpt-image-2.5-sunburst

On Windows the helper also reads those variables from the current user's
Environment registry key, so a freshly saved variable works without restarting
the desktop app.

Examples:

    python scripts/stylize_photo.py --image photo.jpg --prompt-file p.txt --output out.png
    python scripts/stylize_photo.py --image a.jpg --image b.jpg --prompt-file p.txt --output out.png

Never pass the API key as a command-line argument.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


DEFAULT_BASE_URL = "https://o10.top/v1"
DEFAULT_MODEL = "gpt-image-2.5-sunburst"
DEFAULT_SIZE = "1024x1536"
MAX_IMAGE_BYTES = 50 * 1024 * 1024


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
        description="Restyle photos into a painted image using the configured account."
    )
    parser.add_argument(
        "--image",
        type=Path,
        action="append",
        required=True,
        help="Input photo. Repeat for more than one (up to three).",
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text.")
    prompt_group.add_argument("--prompt-file", type=Path, help="UTF-8 prompt file.")
    parser.add_argument("--output", type=Path, required=True, help="Output image path.")
    parser.add_argument("--model", default=config("O10_IMAGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--size", default=DEFAULT_SIZE)
    parser.add_argument("--base-url", default=config("O10_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--timeout", type=int, default=300)
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> str:
    prompt = (
        args.prompt_file.read_text(encoding="utf-8")
        if args.prompt_file is not None
        else args.prompt
    )
    prompt = (prompt or "").strip()
    if not prompt:
        raise ValueError("Prompt must not be empty.")
    return prompt


def load_images(args: argparse.Namespace) -> list[tuple[str, str, bytes]]:
    images: list[tuple[str, str, bytes]] = []
    for path in args.image:
        if not path.is_file():
            raise ValueError(f"Input image not found: {path}")
        content = path.read_bytes()
        if len(content) > MAX_IMAGE_BYTES:
            raise ValueError(f"Input image is larger than 50 MB: {path.name}")
        media_type = mimetypes.guess_type(path.name)[0] or "image/png"
        images.append((path.name, media_type, content))
    if len(images) > 3:
        raise ValueError("At most three input images are supported.")
    return images


def build_multipart(
    fields: dict[str, str],
    images: list[tuple[str, str, bytes]],
    boundary: str,
) -> bytes:
    body = bytearray()
    for name, value in fields.items():
        body += f"--{boundary}\r\n".encode("utf-8")
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8")
        body += str(value).encode("utf-8") + b"\r\n"
    field_name = "image[]" if len(images) > 1 else "image"
    for filename, media_type, content in images:
        body += f"--{boundary}\r\n".encode("utf-8")
        body += (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode("utf-8")
        body += f"Content-Type: {media_type}\r\n\r\n".encode("utf-8")
        body += content + b"\r\n"
    body += f"--{boundary}--\r\n".encode("utf-8")
    return bytes(body)


def request_image(
    args: argparse.Namespace,
    prompt: str,
    images: list[tuple[str, str, bytes]],
    api_key: str,
) -> dict:
    endpoint = f"{args.base_url.rstrip('/')}/images/edits"
    boundary = f"----blurred-memory-painting-{uuid.uuid4().hex}"
    fields = {"model": args.model, "prompt": prompt, "n": "1", "size": args.size}
    body = build_multipart(fields, images, boundary)
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": "blurred-memory-painting-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except json.JSONDecodeError:
            pass
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
        images = load_images(args)
        result = request_image(args, prompt, images, api_key)
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