# Nano Banana Skill for Codex

[![Release](https://img.shields.io/github/v/release/983033995/nanobanana-codex-skill)](https://github.com/983033995/nanobanana-codex-skill/releases/tag/v1.0.0)
[![License](https://img.shields.io/github/license/983033995/nanobanana-codex-skill)](./LICENSE)
[![Install](https://img.shields.io/badge/install-npx%20skills%20add%20983033995%2Fnanobanana--codex--skill-blue)](https://github.com/983033995/nanobanana-codex-skill)

A Codex-compatible skill for generating and editing images with Gemini Nano Banana models.

![Nano Banana Preview](./assets/nanobanana-preview.png)

[中文说明](#中文说明)

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

## 中文说明

这是一个适用于 Codex 的 Nano Banana 技能包，用来通过 Gemini Nano Banana 模型生成和编辑图片。

## 这个技能能做什么

- 用 `gemini-3.1-flash-image-preview` 生成图片
- 按需切换到 `gemini-3-pro-image-preview`
- 用重复 `--reference` 传入一张或多张参考图
- 用重复 `--input` 做多图编辑或合成
- 用 `--preview` 自动打开结果
- 兼容标准代理环境变量，也支持可选的 Nano Banana 代理覆盖

## 安装

安装整个仓库：

```bash
npx skills add 983033995/nanobanana-codex-skill
```

只安装这个技能目录：

```bash
npx skills add 983033995/nanobanana-codex-skill/skills/nanobanana
```

## 依赖

- Python 3
- 在以下任一环境变量中配置 Gemini API key：
  - `NANOBANANA_API_KEY`
  - `GEMINI_API_KEY`
  - `GOOGLE_API_KEY`

## 快速示例

生成图片：

```bash
python3 ~/.codex/skills/nanobanana/scripts/nanobanana.py generate \
  --prompt "a minimalist travel poster of Hangzhou West Lake at sunrise" \
  --out output/nanobanana/west-lake.png
```

结合参考图生成：

```bash
python3 ~/.codex/skills/nanobanana/scripts/nanobanana.py generate \
  --prompt "turn this banana into a clean app icon with a white background" \
  --reference ./banana.png \
  --out output/nanobanana/app-icon.png
```

多图编辑或合成：

```bash
python3 ~/.codex/skills/nanobanana/scripts/nanobanana.py edit \
  --input ./product-front.png \
  --input ./product-side.png \
  --prompt "combine these into one clean e-commerce hero image on a white background" \
  --out output/nanobanana/hero.png
```

## 安全说明

- 不要把 `.env` 文件或 API key 提交到仓库
- API key 只保存在本地环境变量里
- 生成产物已被 `.gitignore` 忽略
- 仓库里不包含你的本地绝对路径或嵌入式密钥
