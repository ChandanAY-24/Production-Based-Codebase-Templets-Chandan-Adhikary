# DESIGN: UI/UX Guidelines, Tokens & Motion Rules
> Reference: [12. impeccable / 13. ui-ux-pro-max / 14. taste-skill / 16. emilkowalski]
> Standard: Modern Minimalist, Accessible, High Polish

---

## 1. Core Principles
1. **Content First, Chrome Second:** Eliminate unnecessary borders, deep shadows, and distracting visual noise. Prioritize typography and hierarchy.
2. **Subtle & Deliberate Motion (Emil Kowalski rules):**
   - Micro-interactions must feel physically grounded.
   - Spring animations preferred over linear easings (stiffness: 260, damping: 20).
   - Enter/exit animations <= 200ms; never delay user intent.
3. **High Accessibility (WCAG 2.1 AA):** Minimum contrast ratio of 4.5:1 for standard text; full keyboard navigation support with visible focus rings.

---

## 2. Design Tokens

### Spacing Scale
```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1.0rem;   /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2.0rem;   /* 32px */
```

### Color Palette (Zinc Dark Mode Primary)
```css
--bg-primary: #09090b;       /* Dark canvas */
--bg-surface: #18181b;       /* Card / container surface */
--border-subtle: #27272a;    /* Hairline borders */
--text-primary: #f4f4f5;     /* High contrast body */
--text-muted: #a1a1aa;       /* Secondary details */
--accent-primary: #3b82f6;   /* Action blue */
--accent-danger: #ef4444;    /* Destructive alert */
```

---

## 3. Component Interaction Standard
- **Buttons:** Active press scales down slightly (`scale(0.98)`). Hover shows smooth background shift in 120ms.
- **Modals / Dialogs:** Backdrop blur (`backdrop-blur-md`), scale-in from 0.95 to 1.0 with ease-out.
- **Inputs:** Clear focus ring with `--accent-primary` at 2px offset.
