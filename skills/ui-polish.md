# SKILL: UI Polish (Micro-Interactions & Visual Refinement)
> Reference: [12. impeccable / 16. emilkowalski]
> Standard: Kinetic Polish, Visual Hierarchy & Pixel Rigor

---

## 1. When to Use
- Reviewing or creating React / HTML / CSS / Tailwind components.
- Adding feedback states (loading, disabled, hover, active, focus).
- Polishing dialogs, toasts, and page transitions.

---

## 2. Checklist

### 1. Spacing & Rhythm
- [ ] Are margins and paddings using the design tokens defined in `docs/DESIGN.md`?
- [ ] Is vertical rhythm consistent (e.g. standard 16px/24px card gutters)?
- [ ] Are borders hairline (1px solid `--border-subtle`) rather than heavy 2px lines?

### 2. Interaction & Feedback
- [ ] **Hover:** Subtle background brightness change (10-15%) with 150ms transition.
- [ ] **Active/Press:** Button scale down (`transform: scale(0.98)`) for physical tactile feedback.
- [ ] **Focus:** Accessible 2px offset focus ring on keyboard navigation.
- [ ] **Loading:** Animated skeleton or spinner replacing action text, preventing layout shifts.

### 3. Motion & Animation (Emil Kowalski Rules)
- [ ] Avoid generic linear transitions. Use spring curves or cubic bezier (`cubic-bezier(0.16, 1, 0.3, 1)`).
- [ ] Keep duration under 250ms for snappy interaction.
- [ ] Respect `prefers-reduced-motion` media queries.
