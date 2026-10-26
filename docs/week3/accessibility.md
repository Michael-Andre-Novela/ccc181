# Accessibility Audit Report — NAIA ExpressPass

This report documents the accessibility audit performed for **NAIA ExpressPass** across the three primary application routes: `/join` (Join Queue), `/queue/<id>` (My Place), and `/staff` (Staff Counter Portal).

---

## 9a. Lighthouse Audit Scores

Automated accessibility audits were executed using Google Chrome DevTools Lighthouse (Mobile Mode).

| Screen | Route | Accessibility Score | Status |
| :--- | :--- | :---: | :---: |
| **Join Queue** | `/join` | ![Join](screenshots/join_queue.png) | Pass ✅ |
| **My Place** | `/queue/1` | ![My Place](screenshots/my_ticket.png) | Pass ✅ |
| **Staff Dashboard** | `/staff` | ![staff](screenshots/staff.png) | Pass ✅ |

### Audit Notes & Fixes
* **Form Field Labels:** Every `<input>` and `<select>` element in `join.html` has an explicit `<label for="...">` matching its element `id`.
* **Color Contrast:** All status badges (`.text-bg-warning`, `.text-bg-primary`, `.text-bg-success`) meet WCAG AAA contrast guidelines against light card backgrounds.
* **Touch Targets:** Buttons and interactive form elements meet minimum touch target dimensions (~44 × 44 px) on mobile viewports.

---

## 9b. Keyboard Navigation Audit

Full keyboard navigation testing was conducted using only `Tab`, `Shift + Tab`, `Enter`, `Space`, and arrow keys (mouse detached).

### Test Flow & Observations
1. **Homepage (`/`):** 
   - Initial `Tab` key press reveals the high-contrast **"Skip to main content"** link (`.visually-hidden-focusable`), jumping directly to `<main id="main">`.
   - Primary CTA button (**Join Bag Drop Queue**) uses a semantic `<a>` link with focus ring outlines, allowing instant navigation to `/join` via `Enter`.
2. **Join Queue (`/join`):**
   - Focus iterates cleanly through form inputs (`Full Name`, `Email`, `Flight Number`, `PNR`, `Bags`, `Service Lane`, `Slot Window`).
   - Validation errors properly link to fields via `aria-describedby` when submitted incomplete.
3. **Staff Dashboard (`/staff`):**
   - Keyboard focus navigates across service filter nav pills and moves down through individual ticket action buttons (`Call`, `Serve`, `No-show`).
   - Every action button includes explicit `aria-label` tags (e.g., `aria-label="Mark ticket 1 as served"`) so screen reader users hear unique contexts for each row.

---

## 9c. Manual Accessibility Checklist

| Checklist Item | Join (`/join`) | My Place (`/queue/1`) | Staff (`/staff`) |
| :--- | :---: | :---: | :---: |
| **Every input has a visible label** | ✅ | N/A | ✅ |
| **Error messages say what to do, in text** | ✅ | N/A | ✅ |
| **Status is shown in words, not only color** | N/A | ✅ | ✅ |
| **Text and buttons are readable at 375 px with no sideways scroll** | ✅ | ✅ | ✅ |
| **Buttons are at least about 44 × 44 px on a phone** | ✅ | ✅ | ✅ |
| **Page has one `<h1>` and headings in order** | ✅ | ✅ | ✅ |
| **`<html lang="en">` attribute is set** | ✅ | ✅ | ✅ |

---

## Conclusion

All screens pass manual and automated checks, meeting WCAG standards, full keyboard accessibility, and achieving a 100 Accessibility score in Lighthouse. Checkpoint 9 is complete.