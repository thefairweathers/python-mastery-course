# CLAUDE.md

## Project Overview

This is a 13-week Python course built as an Astro Starlight documentation site. Course content lives in `src/content/docs/` as Markdown files. Scaffold (starter code) files live in `public/scaffolds/`.

## Key Commands

- `npm run dev` — local dev server
- `npm run build` — production build (use to verify changes)
- `npm run preview` — preview production build locally

## Architecture

```
src/content/docs/week-NN/
  index.md          — Week lesson page
  lab-01-slug.md    — Lab page (code scaffold labs)
  lab-02-slug.md    — Lab page (walkthrough labs have no scaffold)

public/scaffolds/week-NN/
  lab_01_slug.py    — Downloadable scaffold file (underscores, not hyphens)

astro.config.mjs    — Sidebar navigation config (MUST be updated when adding pages)
```

## Adding a New Lab — Three Things Required

Adding a new lab requires changes in **three places**:

1. **Doc page**: Create `src/content/docs/week-NN/lab-XX-slug.md` with frontmatter:
   ```yaml
   ---
   title: "Lab N.X: Title"
   sidebar:
     order: X   # 0 = lesson index, 1+ = labs in order
   ---
   ```

2. **Scaffold file** (if applicable): Create `public/scaffolds/week-NN/lab_XX_slug.py`
   - Note: scaffolds use **underscores**, doc pages use **hyphens**
   - Walkthrough-style labs (like 9.2, 10.2) have no scaffold

3. **Sidebar config**: Add the slug to `astro.config.mjs` in the correct week's `items` array:
   ```js
   { slug: 'week-NN/lab-XX-slug' },
   ```
   **Pages will NOT appear in the sidebar navigation without this step.**

## Lab Doc Format

Code scaffold labs follow this pattern:
- Download link: `> **Download:** [\`lab_XX_slug.py\`](/python-mastery-course/scaffolds/week-NN/lab_XX_slug.py)`
- Python code in a single fenced code block with docstring, TODO stubs, and inline tests
- Checklist section at the bottom

Walkthrough labs (no scaffold) use step-by-step Markdown instructions instead of a code block.

## Week Index Format

Each week's `index.md` has a Labs section linking to its labs:
```markdown
## Labs

- **[Lab N.1: Title](./lab-01-slug)** — Short description
- **[Lab N.2: Title](./lab-02-slug)** — Short description
```

Use relative links with `./` prefix (not `labs/` or absolute paths).

## Naming Conventions

| Item | Pattern | Example |
|------|---------|---------|
| Doc filename | `lab-XX-slug.md` (hyphens) | `lab-02-filter.md` |
| Scaffold filename | `lab_XX_slug.py` (underscores) | `lab_02_filter.py` |
| Sidebar slug | `week-NN/lab-XX-slug` | `week-03/lab-02-filter` |
| Title format | `"Lab N.X: Title"` | `"Lab 3.2: Data Filter Pipeline"` |
| Download path | `/python-mastery-course/scaffolds/week-NN/lab_XX_slug.py` | — |

## Content Conventions

- Lessons and labs use standard GitHub-flavored Markdown
- Checkboxes (`- [ ]`) become interactive via `Head.astro` (persisted to localStorage)
- Internal links between pages use relative paths: `./lab-01-slug` (no `.md` extension)
- The `_original/` directory contains pre-migration source content (read-only reference)
