# Learning Tracker — Design System

A compact iOS-native aesthetic for a bilingual (Chinese-first) personal learning tracker PWA. The app helps users plan daily study tasks on a calendar and visualise progress on a 60-cell grid where each cell is one completed session toward a 30-session target.

## Sources

- **Codebase:** `raylanlin/learning-tracker-pwa` (GitHub, `master` branch). Current state of the app is `index.html` at repo root (v5 polish — single-file HTML + CSS + JS, Supabase for sync, service worker for offline shell).
- **Live URL:** Netlify-hosted, not public. The app is PWA-installable.
- **No Figma file provided.**

## Products represented

There is **one product**: a mobile-first PWA (`学习追踪器` / "Learning Tracker"). It is a single-page HTML app that works standalone on iOS/Android via manifest.json, with Supabase (REST) for cross-device sync. There is no marketing site, no docs, no native client — the PWA is the whole surface.

Core surfaces:
- **Auth** — username + password login (two hard-coded accounts mapped to Supabase emails)
- **Calendar tab** — month view with dots for days that have sessions or completed plans; tapping a day reveals its plan list. Carry-forward card surfaces yesterday's unfinished plans.
- **Grid tab** — list of tasks, each expanding to subtasks rendered as a 5×12 grid of 60 cells (30 target + 30 bonus). Quick-chip buttons add +1 / +5 / +10 at once. Per-task color swatches.
- **Stats tab** — 13-week GitHub-style activity heatmap, per-task ranking bars, lifetime-cell milestones strip, and a streak / today / total KPI hero.
- **Modals** — new task / subtask / calendar plan (single text input + confirm)
- **FAB** — floating "add" pill, context-aware (`添加任务` on grid, `添加计划` on calendar, hidden on stats)
- **Header controls** — sync-status pill · theme switcher (auto / light / dark) · account button (initial letter badge, opens logout menu)

---

## Index

| File | Purpose |
|---|---|
| `README.md` | This file. High-level context, content & visual foundations, iconography. |
| `colors_and_type.css` | All CSS variables — colors, type scale, shadows, radii, motion. v5 tokens + v4 legacy aliases. |
| `SKILL.md` | Cross-compatible skill manifest so the system can be loaded by Claude Code. |
| `index.html` | The canonical running app — v5 polish. All HTML + CSS + JS in one file. |
| `manifest.json`, `sw.js` | PWA manifest and service worker (install + offline shell). |
| `assets/` | Logos, icons, illustrations. `icon-512.svg` is the installable PWA icon. |
| `preview/` | Swatches, type specimens, component cards rendered as static HTML for the Design System tab. |
| `ui_kits/pwa/` | **v4** React recreation of the PWA (pixel-faithful to the original iOS palette, pre-v5 polish). No v5 UI kit yet. |

---

## Content fundamentals

**Language.** All user-facing copy is **Simplified Chinese (zh-CN)**. There is no English in the UI; no i18n layer. Treat zh-CN as canonical.

**Voice.** Terse, functional, affectionate-adjacent — a personal tool, not a product pitched at strangers.

- Labels are **1–4 characters** wherever possible: `日历` (Calendar), `网格` (Grid), `登录` (Login), `取消` / `确认` (Cancel / Confirm), `删除任务` (Delete task).
- Buttons and tabs use a **noun or verb phrase, no terminal punctuation**.
- Placeholders use an **ellipsis** to signal open-endedness: `任务名称…`, `输入今天的计划…`, `账号`, `密码`.
- Confirmations are short questions with trailing `？`: `确定删除这个任务？`.
- Status strings are **prefix-symbol + short phrase**: `● 在线`, `⏳ 同步中…`, `⚠ 同步失败`, `○ 离线`, `● 已同步`.
- Empty states lean warm and lightly playful: `还没有任务` + `点击下方按钮添加一个`, `今天还没有计划`.
- Auth hint uses an emoji as a soft reassurance: `数据将安全保存在云端 ☁️`.
- Legends explain tersely: `未完成`, `已完成`, `今日`, `超额（>30）`.

**Pronouns & tone.** No `你` / `您` — the app never addresses the user directly. It refers to *things* (tasks, plans, days), not *you*. This matches the diary / dashboard register: the user is the subject, the app is the notebook.

**Numerals & dates.** Dates are rendered in mixed format: `2025年4月` for month headers, `4月18日 周五` for inline day labels (`周` + single-char weekday). Progress is `N / 30` always. Weekday headers are single-char `日 一 二 三 四 五 六`.

**Emoji usage.** Sparingly, as **functional glyphs, never decoration**:
- Tab labels (`📅 日历`, `🔲 网格`)
- Status (`☁️` in auth hint, `📚` as the only-empty-state illustration)
- Warm-sign only, never in section titles or buttons.

**Punctuation.** Full-width `、` `，` `。` `？` when they appear in sentences. Interpunct `·` as a separator (`4月18日 · 计划`). ASCII `/` for ratios (`12 / 30`). Ellipsis `…` (single-char, not three dots).

**Error copy.** Blunt and literal: `账号不存在`, `密码错误`, `请输入账号和密码`. No apology, no "please try again later".

---

## Visual foundations

**Aesthetic family.** iOS 16-era "systemGroupedBackground" look, softened. v5 pulled the palette one notch off raw iOS system colors — blues, greens, yellows, purples, oranges all slightly desaturated — to reduce the candy-bright feel on modern high-DPI screens. Still flat, still card-on-gray, still SF-first. No gradients. No glassmorphism except a single frosted header. No illustrations beyond emoji. Added in v5: a full dark theme and an explicit `auto / light / dark` switch.

### Color (light theme)
- **Canvas** `--bg` `#f7f7f9` — everywhere behind cards.
- **Elevated canvas** `--bg-elev` `#eceef2` — inset groups, inactive tabs, icon-button background.
- **Card / surface** `--card` `#ffffff`.
- **Hairline** `--border` `#ececf0` — 1px dividers. `--border-strong` `#dcdce3` on inputs (1.5px) and pressed icon-buttons.
- **Text:** `--text-primary` `#1c1c1e`, `--text-secondary` `#8a8a92`, `--text-tertiary` `#b4b4bc` (empty-state captions, hints, day-detail headers).
- **Accents — semantic, not decorative.** Each accent gets two siblings: `*-soft` for tinted backgrounds, `--accent-ink` for pressed blue:
  - `--accent` `#4a7dff` → primary action, today highlight (calendar day), link-like text, FAB
  - `--accent-soft` `#e8efff` → account badge, accent tags, syncing pill bg
  - `--accent-ink` `#2d5fe0` → pressed auth button, stats heatmap outline for today
  - `--green` `#3ec177` / `--green-soft` `#e2f5ea` → completed cells, milestones, heatmap gradient
  - `--yellow` `#f5b740` / `--yellow-soft` `#fff4dc` → "today-done" cell state, carry-forward card
  - `--purple` `#a668e0` / `--purple-soft` `#f1e7fb` → bonus cells (sessions beyond 30)
  - `--red` `#e5564b` / `--red-soft` `#fde9e7` → destructive actions, errors, sync-failed pill
  - `--orange` `#ef8a3d` → offline sync status
- **Grid cells pending** `--cell-pending` `#e9e9ee` — the default "not yet done" state.

### Color (dark theme)
Triggered by `html[data-theme="dark"]`, or `html[data-theme="auto"]` when the OS reports dark. Canvas drops to `#0f0f12`, cards to `#1a1a1f`, borders to `#26262c` / `#33333a`. Accents lift slightly (`--accent` `#6a94ff`, `--green` `#4fcc88`, `--purple` `#b880ea`, `--red` `#ef685c`), and the `*-soft` backgrounds become deep low-chroma versions of their hue (`--accent-soft` `#1d2a4a` etc.). Shadows switch to pure black at higher opacity.

### Typography
- **Family:** system stack `-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif`. **No custom webfonts are loaded** — the app intentionally defers to the OS so Chinese renders with PingFang SC on Apple and Noto/system-default elsewhere.
- **Scale:** 11 / 12 / 13 / 14 / 15 / 16 / 17 / 18 / 22 / 28 px. See `colors_and_type.css`.
- **Weights used:** 500 / 600 / 700 / 800. The auth title is **800 (black)**, header & modal titles 700, most labels 600, KPI numbers 800 with `-0.8px` letter-spacing.
- **Letter-spacing, line-height:** mostly default. Tightened on display / KPI numerals only.

### Spacing & layout
- **4 px grid.** Dominant paddings are 12 / 14 / 16 px.
- **Content width** caps at **560 px** (was 520 in v4); the whole app is phone-centric.
- Header: sticky, frosted, padding `calc(12px + safe-area-top) 20px 10px`.
- FAB fixed 32 px above `env(safe-area-inset-bottom)`, centered.
- Cards have internal `16 px` padding; modals `24 20 20`.
- Tab bar: 3 tabs (Calendar / Grid / Stats), segmented control with animated pill indicator.

### Corner radii
A consistent radii ladder, now explicitly named in the `--r-*` scale:
- `--r-sm` `8 px` small (tag-like buttons, subtask cells, heatmap squares)
- `--r-md` `12 px` inputs, tab bar, small cards, subtask-item container
- `--r-lg` `16 px` default card — the most common radius in the app
- `--r-xl` `20 px` modal
- `24 px` auth card (inline, no token)
- `--r-pill` `999 px` FAB, chips, sync pill, milestones
- `50%` round dots, delete × buttons

### Shadows
A three-tier elevation system plus the one tinted exception:
- `--shadow-sm` `0 1px 2px rgba(20,20,30,0.04), 0 1px 1px rgba(20,20,30,0.03)` — sync-pill, tab-indicator
- `--shadow-md` `0 2px 8px rgba(20,20,30,0.05), 0 1px 2px rgba(20,20,30,0.03)` — default cards
- `--shadow-lg` `0 8px 28px rgba(20,20,30,0.08), 0 2px 6px rgba(20,20,30,0.04)` — auth card, popovers
- `--shadow-fab` `0 6px 20px rgba(74,125,255,0.32), 0 2px 6px rgba(74,125,255,0.18)` — the one colored shadow, tinted to the FAB's accent.
- Today-cell in the grid gets a yellow glow ring instead of a shadow: `0 0 0 3px rgba(245, 183, 64, 0.35)`.

### Backgrounds
Solid colors only. **No images, no illustrations, no patterns, no gradients** anywhere in the UI — with one deliberate exception: the **auth-card logo chip** uses a subtle `linear-gradient(135deg, --accent → --accent-ink)` to give the brand mark depth against the auth background. Elsewhere: flat. The 512-px launch icon is the only brand illustration, and it's a flat abstraction of the app itself (a stylised checklist card).

### Transparency & blur
- Header uses `backdrop-filter: saturate(1.6) blur(20px)` over `color-mix(in srgb, var(--bg) 82%, transparent)`. This is the only frosted surface in the app.
- Modal overlay uses `backdrop-filter: blur(4px)` over `rgba(0,0,0,0.4)` dimmer.
- Loading overlay uses a blurred wash over the canvas color (defined but effectively unreached in v5 — the app is now offline-first and no longer shows a blocking loader on startup).

### Borders
- 1 px `--border` for card-internal dividers (`day-detail` rows, modal sections).
- **1.5 px solid `--border-strong`** on interactive inputs and small pill buttons — slightly heavier than hairline.
- **1.5 px dashed `--border`** on the "+ add subtask" empty slot — a deliberate "ghost" affordance.

### Animation
Minimal, utilitarian, no bounce except modal entry:
- **Modal enter:** `transform` from `scale(0.92) translateY(10px)` over 0.25s with spring ease `cubic-bezier(0.34, 1.56, 0.64, 1)` (`--ease-spring`). This is the one expressive easing in the system.
- **Accordion expand:** `max-height` 0→3000 px over 0.32s `var(--ease-out)`. Chevron rotates 180° on the same timing.
- **Tab indicator:** slides horizontally over `--t-slow` — the pill follows the active tab.
- **Progress bars:** `width` 0.3–0.5s `ease`.
- **Fades:** overlay opacity 0.2s.
- **Tab-page entry:** `fadeInUp` 6px translate + opacity over 0.25s when switching tabs.
- **No entrance animations** on initial page load.

### Press & hover states
- **Press (most common):** `opacity` or `transform: scale(0.9–0.96)` on `:active`, applied to headers, buttons, list rows.
- **Press + scale:** FAB uses `transform: translateX(-50%) scale(0.96)`. Calendar-nav and icon-btn `scale(0.9–0.92)` + background shift to `--border-strong`. Cells scale down lightly.
- **No hover states** — the app is mobile-only by design. `:hover` is unused except on the stats heatmap cells, which lift 1.25× on hover as a desktop-preview affordance only.
- Long-press on cells (~550 ms) undoes the last yellow cell; this is the one gesture beyond tap.

### Cards
- White fill (`--card`), 16 px radius (`--r-lg`), `--shadow-md`, 1px `--border`. Content stacks vertically; header row + expandable body separated by a 1 px `--border` internal line. Inside cards, grouped content sits on `--bg` inside rounded 12 px wrappers — the same gray-on-white-on-gray recursion Apple uses for Settings-style groups.

### Focus states
- Inputs: `border-color` transitions from `--border-strong` to `--accent` over 0.2s on `:focus`; background shifts from `--bg-elev` to `--card`. No ring, no outline.
- `outline: none` everywhere. `-webkit-tap-highlight-color: transparent` globally.

### Layout rules (fixed elements)
- Header: `position: sticky; top: 0`. Frosted. Contains sync-pill + theme button + account button on the right.
- FAB: `position: fixed; bottom: calc(32px + safe-area-bottom); left: 50%` centered, pill-shaped. Hidden on the stats tab.
- Modal overlay: `position: fixed; inset: 0`.
- (v4 had a fixed sync-status pill at `top:70px, right:16px`; v5 moved it into the header flow.)

### Color vibe of imagery
No imagery. If/when imagery is introduced, keep it warm-neutral and low-contrast; the current palette is cool-leaning so a slight warm push would create a useful counterpoint without clashing.

---

## Iconography

**Approach: extremely minimal, inline SVG, with emoji only as Chinese-reading "punctuation".** There is no icon library, no icon font, no SVG sprite, no CDN-linked set.

- **Inline SVG** — all icons are hand-rolled inline SVG in the HTML:
  - `plus` (FAB and add buttons) — 16×16, 2.2 stroke, white on blue
  - `chevron-down` (task/subtask expand, cal nav) — 14–20 px, 1.8–2 stroke, rotated 180° when open
  - `calendar / grid / stats` tab glyphs — 14×14, 1.8 stroke, `currentColor`
  - `sun / moon / auto-circle` theme glyphs — 14×14, 1.8 stroke
  - `logout` arrow — 14×14, 1.8 stroke
  - `check` (plan checkbox, menu select) — 12×12 / 16×16, 2 stroke
- **Emoji as icons** — used only in the auth hint (`☁️` cloud) and stats milestones tooltip context. Tab labels switched to inline SVG in v5.
- **Unicode glyphs as icons** — `●` / `○` sync status dot, `×` delete, `↻` carry-forward.
- **Checkbox** — custom styled span with SVG check glyph; not a styled native input.

**Recommendation going forward.** Keep this bar: new icons should be **monochrome inline SVG at 1.5–2.2 stroke, 14–20 px**, single-color (`currentColor` or a semantic var). If a library is ever needed, **Lucide** matches the weight and flat-rounded feel closest. Never draw decorative illustrations — the app's personality is restraint.

**Logo.** `assets/icon-512.svg` — a rounded blue square with a stylised white checklist card (two tasks, green check and yellow in-progress pills). It's both the app icon and the only brand mark. PWA installs use `icon-192.png`, `icon-512.png`, and `apple-touch-icon.png` at the repo root.

---

## Caveats

- **No Figma file, no brand guide document.** All tokens are reverse-engineered from `index.html`. If an authoritative brand doc exists, supply it and this system will be re-aligned.
- **`ui_kits/pwa/` is v4.** It predates the v5 polish (softer palette, stats tab, theme toggle, offline-first init). A v5 UI kit has not been built yet; use `index.html` as source of truth for current visual state.
- **Fonts are system-only by design.** If a future version wants a branded typeface, Inter / SF Pro Text ship closest to current rendering on non-Apple devices.
