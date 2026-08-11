---
name: flutter-view-conventions
description: "Structure, refactor, and review complex Flutter views with a clear hierarchy from native or third-party controls to business-independent controls, business controls, and pages. Use when Flutter page or component code has deeply nested Widget trees, obscured screen structure, mixed interaction handling, unclear component boundaries, or hard-to-read list and sub-list rendering. Do not use for state-management design alone or non-implementation discussion."
---

# Flutter View Conventions

Make Flutter views readable by exposing business structure and hiding stable layout details behind
meaningful control boundaries. Preserve behavior and rendering unless the user requests a change.

## Enforce the four-level hierarchy

Build abstractions upward in this order:

```text
原生或第三方控件 -> 业务无关控件 -> 业务控件 -> 页面
```

Allow upper levels to compose lower levels. Do not let a lower level import or depend on concepts
from a higher level. Classify each new or moved Widget before choosing its name and location.

### Native or third-party controls

Treat Flutter SDK and package Widgets as primitive rendering, layout, input, and platform
capabilities. Keep project business names, domain models, and business actions out of this level.

### Business-independent controls

Build reusable project controls from native or third-party controls. Keep their APIs generic and
independent of features, domain entities, page state, and business actions. Accept generic values,
children, builders, and callbacks.

Place these controls in the repository's shared UI or toolkit area. Do not promote a page-private
layout helper to this level merely because it is stateless or accepts `Widget` children.

### Business controls

Represent a meaningful feature region such as navigation, account tools, recommendations, ranking,
or a playback console. Compose lower-level controls and hide padding, decoration, traversal, and
primitive Widget details that the page does not need to understand.

- Prefer one coherent view model or main data source for a page-specific business control.
- Expose business interactions as callbacks; keep navigation and business decisions in the owner.
- Keep purely visual local state inside the control when it has no business meaning.
- Name the control after its business region rather than its visual container.
- Split a child into another business control only when it has independent business meaning, data,
  events, reuse, or maintenance ownership.

### Page

Use the page as the view composition root:

- Bind the repository's existing state and logic mechanism.
- Compose page skeleton helpers and business controls in visible screen order.
- Pass business controls their data and callbacks.
- Keep major regions and interaction entrances discoverable in the page.
- Keep detailed styling, primitive Widget trees, and list traversal out of the page.

Do not introduce or replace a state-management framework to satisfy this skill. Preserve the
repository's existing mechanism and apply this view flow:

```text
state/logic binding -> page -> data + callbacks -> business controls
```

## Expose meaningful structure

Treat the `children` of major `Row`, `Column`, and equivalent layouts as the readable outline of the
screen. When stable page-shell details bury that outline, extract them into a page-private file such
as `widget/[module]_function.dart`.

Let page-private skeleton helpers own details such as the page shell, top/bottom or left/right split,
scrolling shell, fixed sizing, padding, and alignment. Keep these helpers at page level; move one to
the shared UI layer only after its contract is genuinely independent of the page and feature.

Inside each business control:

1. Let `build` show named visible parts in order.
2. Move stable details into descriptive `_buildXxx` methods.
3. Keep background helpers responsible for margin, padding, alignment, decoration, and wrapping.
4. Keep data and callbacks as the public business contract.

Avoid creating a file for every icon or label. Prefer private methods until a child earns an
independent boundary.

## Structure collections without hiding behavior

For a small or fixed business collection, use an `itemBuilder` callback when it keeps traversal out
of the visible structure while leaving the per-item composition readable. For nested business data,
use `itemBuilder + subBuilder` so both levels expose the correct business item.

For large, dynamic, paginated, or unbounded collections, preserve lazy construction with
`ListView.builder`, slivers, or the repository's equivalent. Extract item and sub-item composition
without replacing lazy construction with eager `List.generate`.

## Apply the workflow

1. Read repository instructions, the target page, related controls, and existing state/logic.
2. Map the page's major regions in visible order.
3. Classify touched controls into the four levels and check dependency direction.
4. Identify each business region, its coherent data input, and its business callbacks.
5. Make the page compose business controls and bind their callbacks to the owning logic.
6. Extract page-private skeleton helpers only when stable layout details obscure composition.
7. Make each business control's `build` expose named parts.
8. Apply item and sub-item builders where they improve collection readability.
9. Reuse or create business-independent controls only for genuinely generic project behavior.
10. Preserve appearance, state ownership, scrolling, rebuild semantics, accessibility, and keys.
11. Run the narrowest relevant formatter, analyzer, widget test, or visual check.

Read [view structure examples](references/view-structure-examples.md) only when classifying an
ambiguous control, restructuring a complex page, or applying the item/sub-item builder pattern.

## Validate the result

Reject the result when:

- The page still contains long primitive Widget trees or hidden collection traversal.
- A business control invokes page logic directly instead of exposing business callbacks.
- A business-independent control imports feature state, domain entities, or business logic.
- A page-private skeleton helper is presented as a generic shared control.
- Extraction only renames `Container`, `Row`, or `Column` without clarifying a boundary.
- Excessive extraction fragments one business region into navigation noise.
- A previously lazy collection becomes eager without a measured reason.

Accept the result when the page reads as ordered business composition, each business control reads
as named visible parts, and a maintainer can locate a region's data and interaction entry directly.
