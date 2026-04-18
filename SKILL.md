---
name: learning-tracker-design
description: Use this skill to generate well-branded interfaces and assets for the Learning Tracker PWA (学习追踪器), a Chinese-first iOS-native study tracker. Covers essential design guidelines, colors, type, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick map

- `README.md` — full system documentation (content fundamentals, visual foundations, iconography, dark theme)
- `colors_and_type.css` — CSS variable tokens (v5); import this first
- `index.html` — canonical running PWA (v5). Source of truth for current visual state.
- `manifest.json`, `sw.js` — PWA manifest and service worker
- `assets/icon-512.svg` — the one brand mark
- `preview/` — rendered design-system cards (swatches, type, components)
- `ui_kits/pwa/` — **v4** React recreation (predates the v5 polish; use as legacy reference only)

## Key invariants to preserve

1. **Chinese-first copy.** All UI strings in zh-CN. Terse, 3rd-person, ellipsis placeholders, full-width punctuation.
2. **System fonts only.** `-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif`. Never a webfont.
3. **Softened iOS palette.** Six semantic accents, each with a `*-soft` tint and `--accent-ink` deep-blue variant. Cool-gray canvas. No gradients anywhere except the auth-logo chip. No illustrations, no patterns.
4. **One glass surface.** Frosted header only. Everything else is solid.
5. **Three tabs.** Calendar / Grid / Stats — all at `--content-max: 560 px`, phone-centric.
6. **Press = scale or opacity.** Most interactive surfaces press to `scale(0.9–0.96)` or `opacity: 0.7`. No hover (except stats heatmap).
7. **Icons = inline SVG, with Unicode for calendar/status glyphs.** No icon library. Emoji used only in the auth hint.
8. **Dark theme is first-class.** Tokens have dark values; the theme switch (auto / light / dark) lives in the header.
9. **Offline-first.** Local cache renders instantly on launch; cloud sync runs in the background and updates the UI when it arrives.
