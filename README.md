# Learning Tracker — Design System

A compact iOS-native aesthetic for a bilingual (Chinese-first) personal learning tracker PWA. The app helps users plan daily study tasks on a calendar and visualise progress on a 60-cell grid where each cell is one completed session toward a 30-session target.

## Sources

- **Codebase:** `raylanlin/learning-tracker-pwa` (GitHub, `master` branch, commit `e789fb7`). Imported to `source/` in this project — `source/original_index.html` is the full single-file app, `source/manifest.json` is the PWA manifest, `source/sw.js` the service worker.
- **Live URL:** (Netlify-hosted, not public). The app is PWA-installable.
- **No Figma file provided.**

## Products represented

There is **one product**: a mobile-first PWA (`学习追踪器` / "Learning Tracker"). It is a single-page HTML app that works standalone on iOS/Android via manifest.json, with Supabase (REST) for cross-device sync. There is no marketing site, no docs, no native client — the PWA is the whole surface.

Core surfaces:
- **Auth** — username + password login (two hard-coded accounts mapped to Supabase emails)
- **Calendar tab** — month view with dots for days that have sessions or completed plans; tapping a day reveals its plan list
- **Grid tab** — list of tasks, each expanding to subtasks rendered as a 5×12 grid of 60 cells (30 target + 30 bonus)
- **Modals** — new task / subtask / calendar plan (single text input + confirm)
- **FAB** — floating "add" pill, context-aware (`添加任务` on grid, `添加计划` on calendar)

---

## Index

| File | Purpose |
|---|---|
| `README.md` | This file. High-level context, content & visual foundations, iconography. |
| `colors_and_type.css` | All CSS variables — colors, type scale, shadows, radii, motion. |
| `SKILL.md` | Cross-compatible skill manifest so the system can be loaded by Claude Code. |
| `source/` | Original imported source (`original_index.html`, `manifest.json`, `sw.js`). Read-only reference. |
| `assets/` | Logos, icons, illustrations. `icon-512.svg` is the installable PWA icon. |
| `fonts/` | (Empty — app uses system fonts only, see Typography below.) |
| `preview/` | Swatches, type specimens, component cards rendered as static HTML for the Design System tab. |
| `ui_kits/pwa/` | High-fidelity React recreation of the PWA. `index.html` is the interactive prototype; component JSX files are modular. |

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

**Aesthetic family.** iOS 16-era "systemGroupedBackground" look: flat light-gray canvas, pure-white cards, SF-alike sans, saturated iOS system accent colors used only for semantic intent. No gradients. No glassmorphism except a single frosted header. No illustrations beyond emoji.

### Color
- **Canvas** `--bg` `#f2f2f7` — everywhere behind cards.
- **Card / surface** `--card` `#ffffff`.
- **Hairline** `--border` `#e5e5ea` — 1px dividers and input borders (used at 1.5px on inputs).
- **Primary text** `#1c1c1e`. **Secondary text** `#8e8e93`. **Neutral fill** `#d1d1d6`.
- **Accents are semantic, not decorative:**
  - `--accent` blue `#007aff` → primary action, today highlight, link-like text
  - `--green` `#34c759` → completed cells, import button
  - `--yellow` `#ffcc00` → "today" cell state & selected calendar day
  - `--purple` `#af52de` → bonus cells (sessions beyond the 30-target)
  - `--red` `#ff3b30` → destructive actions, errors
  - `--orange` `#ff9500` → offline sync status

### Typography
- **Family:** system stack `-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif`. **No custom webfonts are loaded** — the app intentionally defers to the OS so Chinese renders with PingFang SC on Apple and Noto/system-default elsewhere.
- **Scale:** 11 / 12 / 13 / 14 / 15 / 16 / 17 / 18 / 22 / 28 px. See `colors_and_type.css`.
- **Weights used:** 500 / 600 / 700 / 800. The auth title is **800 (black)**, header & modal titles 700, most labels 600.
- **Letter-spacing, line-height:** default. No tracking tweaks.

### Spacing & layout
- **4 px grid.** Dominant paddings are 12 / 14 / 16 px.
- **Content width** caps at **520 px**; the whole app is phone-centric.
- Header: `16 20 12` padding, sticky, frosted.
- FAB fixed 32 px from bottom, centered.
- Cards have internal `16 px` padding; modals `24 20 20`.

### Corner radii
A consistent radii ladder:
- `8 px` small (tag-like buttons, subtask cells)
- `12 px` inputs, tab bar, small cards, subtask-item container
- `14 px` auth inputs & primary buttons
- **`16 px`** default card (`--radius`) — the most common radius in the app
- `20 px` modal
- `24 px` auth card, FAB pill
- `50%` round dots, delete × buttons

### Shadows
- **Card shadow** `0 2px 12px rgba(0, 0, 0, 0.08)` — soft, nearly flat.
- **FAB shadow** `0 4px 20px rgba(0, 122, 255, 0.4)` — the one colored shadow in the system, tinted to the FAB's accent.
- **Sync-pill mini shadow** `0 1px 6px rgba(0, 0, 0, 0.08)`.
- Today-cell gets a **3px yellow glow ring** instead of a shadow: `0 0 0 3px rgba(255, 204, 0, 0.35)`.

### Backgrounds
Solid colors only. **No images, no illustrations, no patterns, no gradients** anywhere in the UI. The 512-px launch icon is the only brand illustration, and it's a flat abstraction of the app itself (a stylised checklist card).

### Transparency & blur
- Header uses `backdrop-filter: blur(20px)` over `rgba(242,242,247,0.85)`. This is the only frosted surface in the app.
- Modal overlay uses `backdrop-filter: blur(4px)` over `rgba(0,0,0,0.4)` dimmer.
- Loading overlay uses `rgba(242,242,247,0.9)` with `blur(10px)`.

### Borders
- 1 px `--border` for card-internal dividers (`day-detail` rows, modal sections).
- **1.5 px solid `--border`** on interactive inputs and small pill buttons — slightly heavier than hairline.
- **1.5 px dashed `--border`** on the "+ add subtask" empty slot — a deliberate "ghost" affordance.

### Animation
Minimal, utilitarian, no bounce except modal entry:
- **Modal enter:** `transform` from `scale(0.92) translateY(10px)` over 0.25s with spring ease `cubic-bezier(0.34, 1.56, 0.64, 1)`. This is the one expressive easing in the system.
- **Accordion expand:** `max-height` 0→3000 px over 0.35s `cubic-bezier(0.4, 0, 0.2, 1)` (standard material ease). Chevron rotates 180° on the same timing.
- **Progress bars:** `width` 0.3s `ease`.
- **Fades:** overlay opacity 0.2s.
- **No entrance animations** on page load. No parallax, no scroll-linked, no marquee.

### Press & hover states
- **Press (most common):** `opacity: 0.7` on `:active`, applied to headers, buttons, list rows.
- **Press + scale:** FAB uses `transform: translateX(-50%) scale(0.96)`. Backup buttons `scale(0.96)` + `opacity: 0.7`. Cells `scale(0.92)`.
- **No hover states** — the app is mobile-only by design. `:hover` is unused.
- Long-press on cells (600 ms) undoes the last yellow cell; this is the one gesture beyond tap.

### Cards
- White fill, 16 px radius, soft card shadow, no border. Content stacks vertically; header row + expandable body separated by a 1 px `--border` internal line. Inside cards, grouped content sits on `--bg` (#f2f2f7) inside rounded 12 px wrappers — so the same gray-on-white-on-gray recursion Apple uses for Settings-style groups.

### Focus states
- Inputs: `border-color` transitions from `--border` to `--accent` over 0.2s on `:focus`. No ring, no outline.
- `outline: none` everywhere. `-webkit-tap-highlight-color: transparent` globally.

### Layout rules (fixed elements)
- Header: `position: sticky; top: 0`. Frosted.
- Sync status: `position: fixed; top: 70px; right: 16px` — a small pill that lives just under the header.
- FAB: `position: fixed; bottom: 32px; left: 50%` centered, pill-shaped.
- Modal overlay & loading overlay: `position: fixed; inset: 0`.

### Color vibe of imagery
No imagery. If/when imagery is introduced, keep it warm-neutral and low-contrast; the current palette is cool-leaning so a slight warm push would create a useful counterpoint without clashing.

---

## Iconography

**Approach: extremely minimal, inline SVG, with emoji for playful labels.** There is no icon library, no icon font, no SVG sprite, no CDN-linked set.

- **Inline SVG** — all ~6 icons are hand-rolled inline SVG in the HTML:
  - `plus` (FAB and add buttons) — 18×18, 2.2 stroke, white on blue
  - `chevron-down` (task/subtask expand) — 20×20 or 16×16, 2-stroke, rotated 180° when open
  - `export` / `import` arrows — small 13×13, paired with `--accent` or `--green` color
- **Emoji as icons** — used for tab labels and empty states: `📅` calendar, `🔲` grid, `📚` empty library, `☁️` cloud backup.
- **Unicode glyphs as icons** — `◀ ▶` calendar nav, `●` / `○` sync status dot, `⏳` syncing, `⚠` error, `×` delete, `+` add.
- **Checkbox** — native `<input type="checkbox">` with `accent-color: var(--accent)`; not styled.

**Recommendation going forward.** Keep this bar: new icons should be **monochrome inline SVG at 1.5–2.2 stroke, 13–20 px**, single-color (`currentColor` or a semantic var). If a library is ever needed, **Lucide** matches the weight and flat-rounded feel closest. Never draw decorative illustrations — the app's personality is restraint.

**Logo.** `assets/icon-512.svg` — a rounded blue square with a stylised white checklist card (two tasks, green check and yellow in-progress pills). It's both the app icon and the only brand mark.

---

## Caveats

- **No Figma file, no brand guide document.** All tokens below are reverse-engineered from the single source file. If an authoritative brand doc exists, supply it and this system will be re-aligned.
- **Two icon sizes are referenced by `manifest.json`** (`icon-192.png`, `icon-512.png`) but only `icon-512.svg` exists in the repo. PNG renders aren't included.
- **Fonts are system-only by design.** If a future version wants a branded typeface, Inter / SF Pro Text ship closest to current rendering on non-Apple devices.
