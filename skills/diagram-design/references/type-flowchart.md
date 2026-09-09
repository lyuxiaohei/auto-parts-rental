# Flowchart

**Best for:** decision logic, algorithms, user-facing branching flows ("Should I…?"), onboarding routing, support-triage trees.

## Layout conventions
- Shape carries type, not color:
  - **Oval** (`rx=20`) — start / end
  - **Rectangle** (`rx=6`) — step / action
  - **Diamond** — decision (≤3 exits)
  - **Small filled ink dot** (`r=4`) — merge point where branches rejoin
- Flow runs top→down. From a diamond, conventional exits: Yes to the right, No below — but label every outgoing arrow regardless.
- Use coral on the happy path *or* on the single most consequential decision — never on every decision.
- If two arrows must cross, use a small arc jump on one so the crossing is readable.

## Arrow connectivity rules

Arrows must visually connect to node edges. Common mistakes and their fixes:

| Mistake | Wrong | Right |
|---------|-------|-------|
| Horizontal arrow from node center | `x1` = center_x of source | `x1` = `source.x + source.width` (right edge) |
| Horizontal arrow to before node | `x2` stops short of target | `x2` = `target.x` (left edge) |
| Vertical arrow below source bottom | `y1` > source bottom edge | `y1` = `source.y + source.height` (bottom edge) |
| Diamond exit from interior | Start inside diamond polygon | Start from diamond vertex point |
| Loop-back to wrong node | End at y/x of a different node | End at correct target's edge coordinates |
| Orphaned arrow | End at coords with no node | Remove or route to an actual node |

### Computing edge coordinates

```
Node: { x, y, width, height }
  right_edge  = x + width
  bottom_edge = y + height
  center_x    = x + width / 2
  center_y    = y + height / 2

Diamond (polygon): { top, right, bottom, left } — use the four vertex points directly
  e.g. points="480,96 560,144 480,192 400,144"
    top    = (480, 96)    ← incoming arrow target
    right  = (560, 144)   ← NO exit
    bottom = (480, 192)   ← YES exit
    left   = (400, 144)   ← YES exit
```

### Row-wrap transitions (multi-row layouts)

When a flow wraps from end of row N to start of row N+1:
1. Start from the **last node's center bottom** (`cx, y + height`)
2. Go down to a horizontal rail y
3. Go left to the **first node's center x**
4. Go down to the **first node's top** (`cx, y`)

```
Last node center bottom: (864, 88)
  → (864, 116)  vertical down
  → (208, 116)  horizontal left
  → (208, 144)  vertical down to first node top (with marker-end)
```

### Self-check before output

For every `<line>` or `<path>` with `marker-end`:
- [ ] Start coordinate lies on a node edge or diamond vertex
- [ ] End coordinate lies on a node edge or diamond vertex
- [ ] No arrow originates from node center (unless center is also the edge for ovals/dots)

## Anti-patterns
- Using fill color to signal node type (shape does that).
- Decision diamond with 4+ exits — refactor into nested diamonds.
- Unlabeled decision branches.

## Examples
- `assets/example-flowchart.html` — minimal light
- `assets/example-flowchart-dark.html` — minimal dark
- `assets/example-flowchart-full.html` — full editorial
