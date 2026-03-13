# Nano Banana Skill for Codex

A Codex-compatible skill for generating and editing images with Gemini Nano Banana models.

![Nano Banana Preview](./assets/nanobanana-preview.png)

## Why this skill

This skill packages a practical Gemini image workflow into a reusable Codex skill:

- Generate images with `gemini-3.1-flash-image-preview`
- Switch to `gemini-3-pro-image-preview` when you want higher quality
- Use one or more reference images with repeated `--reference`
- Edit or combine multiple source images with repeated `--input`
- Open outputs automatically with `--preview`
- Work with standard proxy environment variables and optional Nano Banana proxy overrides

## Skill path

The skill lives at:

`skills/nanobanana`

## Install

Install the repo:

```bash
npx skills add 983033995/nanobanana-codex-skill
```

Or install just this skill path:

```bash
npx skills add 983033995/nanobanana-codex-skill/skills/nanobanana
```

## Requirements

- Python 3
- A Gemini API key in one of:
  - `NANOBANANA_API_KEY`
  - `GEMINI_API_KEY`
  - `GOOGLE_API_KEY`

## Quick examples

Generate:

```bash
python3 ~/.codex/skills/nanobanana/scripts/nanobanana.py generate \
  --prompt "a minimalist travel poster of Hangzhou West Lake at sunrise" \
  --out output/nanobanana/west-lake.png
```

Generate with a reference image:

```bash
python3 ~/.codex/skills/nanobanana/scripts/nanobanana.py generate \
  --prompt "turn this banana into a clean app icon with a white background" \
  --reference ./banana.png \
  --out output/nanobanana/app-icon.png
```

Edit with multiple inputs:

```bash
python3 ~/.codex/skills/nanobanana/scripts/nanobanana.py edit \
  --input ./product-front.png \
  --input ./product-side.png \
  --prompt "combine these into one clean e-commerce hero image on a white background" \
  --out output/nanobanana/hero.png
```

## Safety notes

- Do not commit `.env` files or API keys
- Keep keys in local environment variables only
- Generated outputs are ignored by `.gitignore`
- This repo contains no embedded secrets or user-specific absolute paths
