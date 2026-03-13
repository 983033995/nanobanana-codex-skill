---
name: nanobanana
description: Use when the user asks to generate or edit images with Nano Banana, Gemini image models, `gemini-3.1-flash-image-preview`, `gemini-3-pro-image-preview`, or says things like “用 Gemini 出图”, “用 Nano Banana 生成图片”, “改图”, “多张变体”, “海报/插画/图标”. Prefer the bundled CLI at `scripts/nanobanana.py` instead of ad-hoc requests.
license: MIT
metadata:
  version: 1.0.1
---

# Nano Banana Skill

Use this skill for Gemini image generation and lightweight image editing through Nano Banana models.

## When to use
- The user explicitly mentions `nanobanana`, `Nano Banana`, Gemini image generation, or a Gemini image model name
- The user wants to generate one or more images from a prompt
- The user wants to generate images based on one or more reference images
- The user wants to edit an existing image with a text instruction

## Workflow
1. Decide whether this is `generate` or `edit`.
2. Check that one of these environment variables is set: `NANOBANANA_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`.
3. Run the bundled script:
   - Generate: `python3 scripts/nanobanana.py generate --prompt "..." --out output/nanobanana/result.png`
   - Generate with references: `python3 scripts/nanobanana.py generate --prompt "..." --reference ref1.png --reference ref2.jpg`
   - Edit: `python3 scripts/nanobanana.py edit --input path/to/input.png --prompt "..." --out output/nanobanana/result.png`
4. If the user asks for multiple variants, add `--count N`.
5. If the user provides one or more reference images, pass them with repeated `--reference`.
6. If the user asks for Pro quality, add `--model gemini-3-pro-image-preview`.
7. If the user wants the result to pop open automatically, add `--preview`.
8. Return the output path and, when helpful, show the generated image in the response.

## Defaults
- Default model: `gemini-3.1-flash-image-preview`
- Default output format: `png`
- Default output directory when `--out` is omitted: `output/nanobanana/`
- `edit` accepts repeated `--input` so multiple source images can be combined in one request

## Proxy notes
- If the machine relies on a local proxy, keep `HTTP_PROXY` and `HTTPS_PROXY` in the environment before running the script.
- If needed, set `NANOBANANA_PROXY_URL` explicitly.
- If neither proxy variable is set, the script will try a few common local proxy ports as a fallback.

## Rules
- Prefer the bundled script over handwritten `curl` requests.
- Do not ask the user to paste API keys into chat.
- For edits, preserve the original image unless the user explicitly asks to overwrite it.
- If generation fails, surface the exact API error message and suggest switching model or checking key/project status.

## Examples

```bash
python3 scripts/nanobanana.py generate \
  --prompt "a minimalist travel poster of Hangzhou West Lake at sunrise" \
  --out output/nanobanana/west-lake.png
```

```bash
python3 scripts/nanobanana.py generate \
  --prompt "three flat vector app icons for a note-taking app" \
  --count 3 \
  --model gemini-3-pro-image-preview \
  --out output/nanobanana/notes.png
```

```bash
python3 scripts/nanobanana.py generate \
  --prompt "create a mascot sticker based on the banana reference, with a playful black outline" \
  --reference assets/banana.png \
  --preview
```

```bash
python3 scripts/nanobanana.py edit \
  --input assets/photo.png \
  --prompt "replace the background with a clean warm beige studio backdrop" \
  --out output/nanobanana/photo-edit.png
```

```bash
python3 scripts/nanobanana.py edit \
  --input assets/product-front.png \
  --input assets/product-side.png \
  --prompt "combine these into one clean e-commerce hero image on a white background" \
  --preview
```
