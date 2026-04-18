# Learning Tracker PWA — UI Kit

A pixel-faithful React recreation of `source/original_index.html`. Everything is mocked client-side with `useState` — no Supabase, no service worker, no persistence. Start from `index.html`.

## Files

- `index.html` — interactive demo. Log in with `raylan` or `scarlett` (any password — it's a mock gate). Flip between Calendar and Grid tabs; add/check/delete plans; expand tasks and tap cells to advance progress.
- `styles.css` — all visual tokens and component CSS, lifted from the original.
- `Header.jsx` — sticky frosted header + sync status pill
- `TabBar.jsx` — segmented Calendar / Grid tab switcher
- `Calendar.jsx` — month grid with today/selected/dot states
- `PlanList.jsx` — day detail card with checkable plan items
- `TaskCard.jsx` — collapsible task with subtasks + 60-cell progress grid (`SubtaskItem`, `CellGrid`, `Legend` inside)
- `Chrome.jsx` — `Modal`, `AuthScreen`, `Fab`

## Known shortcuts

- Long-press-to-undo (touch timer 600 ms) from the original is omitted — click-to-advance only.
- Sync status is a static pill; no real debounced write.
- No day-change reset (`doneToday` flags don't clear at midnight in the mock).
- No service worker registration (demo only).

Pull individual components into new designs; they all attach to `window.*` so any `<script type="text/babel">` on the same page can use them.
