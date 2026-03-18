# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This directory holds HTML files exported from ClickUp. The task is to clean them up into minimal, readable semantic HTML by stripping ClickUp-specific markup, the embedded design-system CSS, and proprietary custom elements.

## Cleanup Rules

### 1. Drop the entire `<head>` — replace with a minimal one
The `<head>` contains ~700 KB of ClickUp's design-system CSS. Replace with:
```html
<head><meta charset="UTF-8"><title>DOCUMENT TITLE</title></head>
```

### 2. Unwrap ClickUp/Quill structural divs
Remove (keeping their children) the wrapper divs that add no semantic value:
- `<body class="cu-pdf-export">` → `<body>`
- `<div class="cu-editor-wrapper doc-editor">`
- `<div class="cu-editor-content">`
- `<div class="cu-editor ql-container ql-snow">`
- `<div class="ql-editor">`
- `<div class="page-0">`

### 3. Remove custom elements entirely
- `<cu-table-content-inline-dynamic>` — ClickUp's table of contents widget; drop it (the headings already provide structure)
- `<cu-doc-page-avatar-dynamic>` — document emoji/icon; drop it
- `<a class="cu-table-content__anchor">` — internal anchor shims; drop them

### 4. Simplify headings
`<h1 data-block-id="..." data-collapsable-block="true" data-collapse-state="expanded" class="ql-heading">` → `<h1>`
Strip all `data-*` attributes and `class="ql-heading"` from every heading element.

### 5. Simplify lists
- `<ul class="ql-rendered-list-container" data-test="..." data-is-root="true">` → `<ul>`
- `<ol class="ql-rendered-list-container" ...>` → `<ol>`
- `<li class="ql-rendered-bullet-list" data-test="...">` → `<li>`
- `<li class="ql-rendered-ordered-list" data-test="...">` → `<li>`

### 6. Convert banners to `<blockquote>`
`<div class="ql-advanced-banner" data-advanced-banner-color="yellow">` blocks contain callout content. Convert to `<blockquote>`. The `<div class="ql-advanced-banner__icon">` child holds raw icon text (e.g. `icon:fas:rectangle-xmark`) — drop it.

### 7. Simplify user/group mentions
`<a class="cu-mention__user-group cu-mention_readonly"><span>@team-name</span></a>` → keep the inner `<span>` text as plain text, or render as `@team-name` inline.

### 8. Images
`<img class="ql-image" src="...">` → `<img src="...">` (strip class, keep src).

### 9. Color/style spans
`<span class="ql-color-red">`, `<span class="ql-bg-purple">` etc. — strip the class (or drop the span entirely if it has no other attributes).

### 10. Remove all remaining `data-*` attributes and ClickUp/Quill classes
After the targeted passes above, strip any remaining `data-*` attributes and any class that starts with `cu-`, `ql-`, or `doc-`.

### 11. Drop empty block elements
Remove `<p></p>`, `<div></div>`, and other empty block elements left behind after stripping.

## Output Target

The cleaned file should be plain semantic HTML using only: `html`, `head`, `body`, `h1`–`h4`, `p`, `ul`, `ol`, `li`, `strong`, `em`, `u`, `a`, `img`, `blockquote`, `span` (only where needed for inline text that has no better element). No classes, no `data-*`, no inline styles.
