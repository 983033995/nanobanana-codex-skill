# Nano Banana Skill for Codex

This repository contains a Codex-compatible skill for generating and editing images with Gemini Nano Banana models.

## Skill Path

The skill lives at:

`skills/nanobanana`

## What It Supports

- Text-to-image generation with `gemini-3.1-flash-image-preview`
- Optional Pro model via `gemini-3-pro-image-preview`
- Reference-image generation with repeated `--reference`
- Multi-image editing with repeated `--input`
- Optional `--preview` to open results automatically
- Automatic fallback to `NANOBANANA_API_KEY`, `GEMINI_API_KEY`, or `GOOGLE_API_KEY`
- Proxy support via `HTTP_PROXY` / `HTTPS_PROXY`
- Optional `NANOBANANA_PROXY_URL` override and fallback detection of common local proxy ports

## Requirements

- Python 3
- A Gemini API key in one of:
  - `NANOBANANA_API_KEY`
  - `GEMINI_API_KEY`
  - `GOOGLE_API_KEY`

## Safety Notes

- Do not commit `.env` files or API keys
- Keep keys in local environment variables only
- Generated outputs are ignored by `.gitignore`
- The repo contains no user-specific paths or embedded secrets

## Install

Once this repo is published on GitHub, install it with:

```bash
npx skills add <owner>/<repo>
```

Or install just this skill path if needed:

```bash
npx skills add <owner>/<repo>/skills/nanobanana
```

## Example

```bash
python3 ~/.codex/skills/nanobanana/scripts/nanobanana.py generate \
  --prompt "a minimalist travel poster of Hangzhou West Lake at sunrise" \
  --out output/nanobanana/west-lake.png
```
