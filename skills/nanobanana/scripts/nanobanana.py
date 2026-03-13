#!/usr/bin/env python3
"""Generate or edit images with Gemini Nano Banana models."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import urllib.error
import urllib.request


DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_OUTPUT_DIR = Path("output/nanobanana")
API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
COMMON_PROXY_PORTS = (7897, 7890, 7898)


def die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def get_api_key() -> str:
    for name in (
        "NANOBANANA_API_KEY",
        "NANOBANANA_GEMINI_API_KEY",
        "NANOBANANA_GOOGLE_API_KEY",
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
    ):
        value = os.getenv(name)
        if value:
            return value
    die(
        "没有找到可用的 Gemini API key。请先在环境变量中设置 NANOBANANA_API_KEY、GEMINI_API_KEY 或 GOOGLE_API_KEY。"
    )
    return ""


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex((host, port)) == 0


def _proxy_ports_from_env() -> tuple[int, ...]:
    raw = os.getenv("NANOBANANA_PROXY_PORTS", "")
    if not raw.strip():
        return COMMON_PROXY_PORTS
    ports: list[int] = []
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            ports.append(int(chunk))
        except ValueError:
            continue
    return tuple(ports) or COMMON_PROXY_PORTS


def configure_proxy() -> None:
    http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    if http_proxy or https_proxy:
        return

    explicit_proxy = os.getenv("NANOBANANA_PROXY_URL")
    if explicit_proxy:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler(
                {
                    "http": explicit_proxy,
                    "https": explicit_proxy,
                }
            )
        )
        urllib.request.install_opener(opener)
        return

    for port in _proxy_ports_from_env():
        if _port_open("127.0.0.1", port):
            proxy_url = f"http://127.0.0.1:{port}"
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler(
                    {
                        "http": proxy_url,
                        "https": proxy_url,
                    }
                )
            )
            urllib.request.install_opener(opener)
            return


def slugify(text: str, fallback: str = "image") -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return cleaned[:48] or fallback


def build_output_paths(out: str | None, prompt: str, count: int, fmt: str) -> list[Path]:
    ext = "." + fmt.lower().lstrip(".")
    if out:
        target = Path(out)
        if target.suffix:
            base = target.with_suffix(ext)
        else:
            base = target / (slugify(prompt) + ext) if target.exists() and target.is_dir() else target.with_suffix(ext)
    else:
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        base = DEFAULT_OUTPUT_DIR / f"{slugify(prompt)}{ext}"

    base.parent.mkdir(parents=True, exist_ok=True)
    if count == 1:
        return [base]
    return [base.with_name(f"{base.stem}-{index}{base.suffix}") for index in range(1, count + 1)]


def read_input_image(path: str) -> dict[str, str]:
    file_path = Path(path)
    if not file_path.exists():
        die(f"输入图片不存在: {file_path}")
    mime_type, _ = mimetypes.guess_type(file_path.name)
    if not mime_type:
        mime_type = "image/png"
    data = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return {"data": data, "mimeType": mime_type}


def read_input_images(paths: list[str] | None) -> list[dict[str, str]]:
    return [read_input_image(path) for path in (paths or [])]


def build_payload(prompt: str, inline_images: list[dict[str, str]] | None = None) -> dict:
    parts: list[dict] = [{"text": prompt}]
    for inline_image in inline_images or []:
        parts.append({"inlineData": inline_image})
    return {
        "contents": [
            {
                "role": "user",
                "parts": parts,
            }
        ]
    }


def extract_image_bytes(response_json: dict) -> bytes:
    candidates = response_json.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        for part in content.get("parts") or []:
            inline_data = part.get("inlineData") or {}
            if inline_data.get("data"):
                return base64.b64decode(inline_data["data"])
            text_data = part.get("text")
            if text_data:
                try:
                    decoded = base64.b64decode(text_data, validate=True)
                except Exception:
                    continue
                if len(decoded) > 1024:
                    return decoded
    error = response_json.get("error")
    if error:
        message = error.get("message") or json.dumps(error, ensure_ascii=False)
        die(f"Gemini API 返回错误: {message}")
    die("响应里没有找到可写入的图片数据。")
    return b""


def call_api(model: str, api_key: str, payload: dict) -> dict:
    url = API_URL_TEMPLATE.format(model=model, api_key=api_key)
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
            message = parsed.get("error", {}).get("message") or body
        except Exception:
            message = body
        die(f"Gemini API 请求失败 ({exc.code}): {message}")
    except urllib.error.URLError as exc:
        die(f"网络请求失败: {exc.reason}")
    return {}


def open_preview(path: Path) -> None:
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]
            return
        subprocess.Popen(["xdg-open", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as exc:
        print(f"Warning: 预览打开失败: {exc}", file=sys.stderr)


def run_generation(args: argparse.Namespace) -> int:
    api_key = get_api_key()
    outputs = build_output_paths(args.out, args.prompt, args.count, args.format)
    reference_images = read_input_images(args.reference)
    for index, output_path in enumerate(outputs, start=1):
        prompt = args.prompt if args.count == 1 else f"{args.prompt}\n\nVariation {index} of {args.count}."
        payload = build_payload(prompt, inline_images=reference_images)
        response_json = call_api(args.model, api_key, payload)
        image_bytes = extract_image_bytes(response_json)
        output_path.write_bytes(image_bytes)
        print(str(output_path.resolve()))
        if args.preview:
            open_preview(output_path.resolve())
    return 0


def run_edit(args: argparse.Namespace) -> int:
    api_key = get_api_key()
    outputs = build_output_paths(args.out, args.prompt, args.count, args.format)
    inline_images = read_input_images(args.input)
    for index, output_path in enumerate(outputs, start=1):
        prompt = args.prompt if args.count == 1 else f"{args.prompt}\n\nVariation {index} of {args.count}."
        payload = build_payload(prompt, inline_images=inline_images)
        response_json = call_api(args.model, api_key, payload)
        image_bytes = extract_image_bytes(response_json)
        output_path.write_bytes(image_bytes)
        print(str(output_path.resolve()))
        if args.preview:
            open_preview(output_path.resolve())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Nano Banana image generation for Codex skills.")
    parser.add_argument("--model", default=os.getenv("NANOBANANA_MODEL", DEFAULT_MODEL))
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate image(s) from text.")
    generate_parser.add_argument("--prompt", required=True)
    generate_parser.add_argument("--out")
    generate_parser.add_argument("--count", type=int, default=1)
    generate_parser.add_argument("--format", default="png")
    generate_parser.add_argument("--reference", action="append", default=[], help="Reference image path. Repeatable.")
    generate_parser.add_argument("--preview", action="store_true", help="Open generated image(s) after saving.")
    generate_parser.set_defaults(func=run_generation)

    edit_parser = subparsers.add_parser("edit", help="Edit an image with a text instruction.")
    edit_parser.add_argument("--input", action="append", required=True, help="Input image path. Repeatable.")
    edit_parser.add_argument("--prompt", required=True)
    edit_parser.add_argument("--out")
    edit_parser.add_argument("--count", type=int, default=1)
    edit_parser.add_argument("--format", default="png")
    edit_parser.add_argument("--preview", action="store_true", help="Open edited image(s) after saving.")
    edit_parser.set_defaults(func=run_edit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.count < 1 or args.count > 8:
        die("--count 必须在 1 到 8 之间。")
    configure_proxy()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
