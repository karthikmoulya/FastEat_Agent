# FastEat — UI design handoff

Reference designs: `design/Main.dc.html` (upload page) and `design/Workspace.dc.html` (ingredients + recipe + chat).
They are design mockups, not production code: markup with inline styles, `{{holes}}` filled from a small
`renderVals()` class, `<sc-for>` = loop, `<sc-if>` = conditional. Use them for layout, spacing, copy and styling only.

## Design tokens

| Token | Value | Use |
|---|---|---|
| `--bg` | `#F5F6F0` | page background |
| `--surface` | `#FFFFFF` | cards, panels |
| `--surface-muted` | `#FAFBF7` | chat message area |
| `--ink` | `#16201A` | text, dark buttons, user chat bubbles |
| `--ink-2` | `#4A554D` | secondary text |
| `--ink-3` | `#5E6960` | tertiary text / labels |
| `--border` | `#E3E6DC` | card borders, dividers |
| `--border-strong` | `#9AA394` | outline buttons, chips |
| `--accent` | `#C8421F` | primary CTA, send button |
| `--have` | `#2F6B47` | "you have it", active toggles, progress |
| `--missing` | `#B5481F` | missing-ingredient icon/text |
| `--missing-bg` / `--missing-text` | `#FBEDE6` / `#8A3416` | substitute hint box |

Fonts (Google Fonts): **Bricolage Grotesque** 700/800 for headings and the logo; **DM Sans** 400/500/600 for body.
Radii: cards 20px, buttons 12–18px, chips fully rounded. Min touch target 44px.

## Pages

### 1. Upload (`/`)
- Header: logo, then the nav links "How it works" and "Saved recipes".
- Hero: two columns that wrap on mobile (`flex-wrap`, children `flex: 1 1 360px`).
  - Left side: badge, H1 (`clamp(2.4rem, 5vw, 4rem)`), intro paragraph.
  - Right side: dashed dropzone with three triggers:
    - `<input type="file" accept="image/*,.heic" capture="environment">`: opens the camera on mobile.
    - Drag-and-drop.
    - "Type ingredients instead": skips the photo.
- "How it works": 4 cards, `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))`.

### 2. Workspace (`/cook`)
A `flex-wrap` row with three panels that stack on mobile in this order:
1. **Ingredients aside** (`flex: 1 1 280px`):
   - Photo with detection boxes.
   - Removable chips.
   - "Add an ingredient" input.
   - Preference toggles: Vegetarian / Under 30 min / No oven / Spicy.
   - "Find another recipe" button.
2. **Recipe article** (`flex: 999 1 460px`):
   - Hero image, source link, title, and the meta line (time, serves, difficulty).
   - "You have X of Y" progress bar.
   - Ingredients list (have = green check; missing = orange dashed circle plus a substitute hint) next to numbered steps.
3. **Chat panel** (`flex: 1 1 320px`, fixed height ~44rem on desktop, with its own scroll):
   - Message list.
   - An agent reply can include a "Recipe changes" card with old → new swaps and an "Apply to recipe" button.
   - Quick-reply chips.
   - Text input and a send button.

## Data contract the UI needs from the agent

```json
{
  "detected_ingredients": ["Tomatoes", "Spinach", "Eggs"],
  "recipe": {
    "title": "Spinach & tomato egg bhurji",
    "source_name": "...", "source_url": "...", "image_url": "...",
    "time_minutes": 20, "servings": 2, "difficulty": "Easy", "tags": ["No oven"],
    "ingredients": [
      {"name": "Eggs", "qty": "4", "have": true},
      {"name": "Turmeric", "qty": "1/4 tsp", "have": false, "substitute": "Skip it, or a pinch of curry powder."}
    ],
    "steps": ["Heat ghee...", "Add tomatoes..."]
  }
}
```
Chat replies: `{ "message": "...", "changes": [{"from": "Eggs ×4", "to": "Firm tofu, 200 g"}] }`.

Accessibility: use real `<button>`, `<label>` and `<input>` elements; put `aria-label` on icon-only buttons; keep text contrast at least 4.5:1.
