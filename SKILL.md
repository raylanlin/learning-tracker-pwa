---
name: learning-tracker-design
description: Use this skill to generate well-branded interfaces and assets for the Learning Tracker PWA (学习追踪器), a Chinese-first iOS-native study tracker. Covers essential design guidelines, colors, type, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick map

- `README.md` — full system documentation (content fundamentals, visual foundations, iconography)
- `colors_and_type.css` — CSS variable tokens; import this first
- `assets/icon-512.svg` — the one brand mark
- `ui_kits/pwa/` — React recreation; reference for component structure and styles
- `source/original_index.html` — the canonical original implementation
- `preview/` — rendered design-system cards

## Key invariants to preserve

1. **Chinese-first copy.** All UI strings in zh-CN. Terse, 3rd-person, ellipsis placeholders, full-width punctuation.
2. **System fonts only.** `-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif`. Never a webfont.
3. **Flat iOS palette.** Six semantic accents on a cool-gray canvas. No gradients, no illustrations, no patterns.
4. **One glass surface.** Frosted header only. Everything else is solid.
5. **Mobile width 520 px.** Phone-centric; no desktop layouts.
6. **Press = opacity 0.7** (sometimes + scale). No hover.
7. **Icons = inline SVG + emoji + unicode.** No icon library.
