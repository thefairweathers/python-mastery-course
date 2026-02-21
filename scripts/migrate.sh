#!/usr/bin/env bash
set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ORIGINAL="$REPO_ROOT/_original"
DOCS="$REPO_ROOT/src/content/docs"
SCAFFOLDS="$REPO_ROOT/public/scaffolds"

# ── Lab title lookup (bash 3.x compatible) ────────────────────────────
get_lab_title() {
  case "$1" in
    "week-01/lab_01_verify")   echo "Lab 1.1: Environment Verification" ;;
    "week-01/lab_02_repl")     echo "Lab 1.2: REPL Exploration" ;;
    "week-02/lab_01_types")    echo "Lab 2.1: Type Explorer" ;;
    "week-02/lab_02_strings")  echo "Lab 2.2: String Processor" ;;
    "week-03/lab_01_fizzbuzz") echo "Lab 3.1: FizzBuzz Three Ways" ;;
    "week-04/lab_01_memoize")  echo "Lab 4.1: Memoization" ;;
    "week-05/lab_01_inventory") echo "Lab 5.1: Inventory System" ;;
    "week-06/lab_01_events")   echo "Lab 6.1: Event System" ;;
    "week-07/lab_01_config")   echo "Lab 7.1: Config Manager" ;;
    "week-08/lab_01_processor") echo "Lab 8.1: Resilient Processor" ;;
    "week-10/lab_01_testing")  echo "Lab 10.1: Test Suite" ;;
    "week-11/lab_01_pipeline") echo "Lab 11.1: Log Pipeline" ;;
    "week-12/lab_01_api")      echo "Lab 12.1: API Client" ;;
    "week-13/lab_01_agent")    echo "Lab 13.1: AI Research Agent" ;;
    *) echo "" ;;
  esac
}

# ── Step 1: Move week directories to _original/ ──────────────────────
echo "==> Moving week directories to _original/"
mkdir -p "$ORIGINAL"
for week_dir in "$REPO_ROOT"/week-[0-9][0-9]; do
  [ -d "$week_dir" ] || continue
  week=$(basename "$week_dir")
  echo "    $week"
  mv "$week_dir" "$ORIGINAL/$week"
done

# ── Step 2: Migrate lessons (README.md → week-NN/index.md) ──────────
echo "==> Migrating lesson pages"
for week_dir in "$ORIGINAL"/week-[0-9][0-9]; do
  [ -f "$week_dir/README.md" ] || continue
  week=$(basename "$week_dir")
  dest_dir="$DOCS/$week"
  mkdir -p "$dest_dir"

  readme="$week_dir/README.md"

  # Extract title from first H1 line: "# Week N: Title"
  title=$(head -1 "$readme" | sed 's/^# //')

  tmpfile=$(mktemp)

  # Write frontmatter
  cat > "$tmpfile" <<FRONT
---
title: "$title"
sidebar:
  order: 0
---

FRONT

  # Append body (skip first line = H1 heading)
  tail -n +2 "$readme" >> "$tmpfile"

  # Strip navigation lines (various patterns)
  sed -i '' '/^\[← Week.*](\.\.\/week-.*\/README\.md)/d' "$tmpfile"
  sed -i '' '/^\[Next: Week.*](\.\.\/week-.*\/README\.md)/d' "$tmpfile"
  sed -i '' '/^\[Back to Course Overview\]/d' "$tmpfile"
  # Combined nav lines: "[← Week 12...] · [Back to Course...]" or "[← Week N] · [Week N+1 →]"
  sed -i '' '/^\[← Week.*· \[/d' "$tmpfile"

  # Rewrite .py lab links: (labs/lab_01_verify.py) → (./lab-01-verify)
  sed -i '' -E 's|\(labs/lab_([0-9]+)_([a-zA-Z0-9_]+)\.py\)|(./lab-\1-\2)|g' "$tmpfile"

  # Rewrite .md lab links: (labs/lab_02_repl.md) → (./lab-02-repl)
  sed -i '' -E 's|\(labs/lab_([0-9]+)_([a-zA-Z0-9_]+)\.md\)|(./lab-\1-\2)|g' "$tmpfile"

  # Convert remaining underscores in rewritten lab link paths to hyphens
  while grep -qE '\(\.\/lab-[0-9]+-[a-zA-Z0-9-]*_' "$tmpfile"; do
    sed -i '' -E 's|\(\.\/lab-([0-9]+)-([a-zA-Z0-9-]*)_|\(./lab-\1-\2-|g' "$tmpfile"
  done

  # Replace labs/ directory link with inline code
  sed -i '' 's|\[labs/\](labs/)|`labs/`|g' "$tmpfile"

  # Also handle labs/ link without trailing slash
  sed -i '' 's|\[labs/\](labs)|`labs/`|g' "$tmpfile"

  mv "$tmpfile" "$dest_dir/index.md"
  echo "    $week/index.md"
done

# ── Step 3: Migrate .py labs (scaffold + markdown wrapper) ───────────
echo "==> Migrating Python lab files"
for week_dir in "$ORIGINAL"/week-[0-9][0-9]; do
  [ -d "$week_dir/labs" ] || continue
  week=$(basename "$week_dir")
  week_num="${week#week-}"

  for lab_file in "$week_dir"/labs/lab_[0-9][0-9]_*.py; do
    [ -f "$lab_file" ] || continue
    filename=$(basename "$lab_file")
    # e.g. lab_01_verify.py → lab_num=01, slug_part=verify
    lab_num=$(echo "$filename" | sed -E 's/lab_([0-9]+)_.*/\1/')
    slug_part=$(echo "$filename" | sed -E 's/lab_[0-9]+_(.*)\.py/\1/' | tr '_' '-')
    slug="lab-${lab_num}-${slug_part}"

    # Look up title
    title_key="$week/$(echo "$filename" | sed 's/\.py$//')"
    title=$(get_lab_title "$title_key")
    if [ -z "$title" ]; then
      title="Lab ${week_num#0}.${lab_num#0}: ${slug_part}"
    fi

    # Compute sidebar order from lab number
    order=$((10#$lab_num))

    # Copy to public/scaffolds/
    scaffold_dir="$SCAFFOLDS/$week"
    mkdir -p "$scaffold_dir"
    cp "$lab_file" "$scaffold_dir/$filename"
    echo "    scaffold: $week/$filename"

    # Create markdown wrapper
    dest_dir="$DOCS/$week"
    mkdir -p "$dest_dir"

    cat > "$dest_dir/$slug.md" <<EOF
---
title: "$title"
sidebar:
  order: $order
---

> **Download:** [\`$filename\`](/python-mastery-course/scaffolds/$week/$filename)

\`\`\`python
$(cat "$lab_file")
\`\`\`

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
EOF

    echo "    $week/$slug.md"
  done
done

# ── Step 4: Migrate .md labs directly ─────────────────────────────────
echo "==> Migrating markdown lab files"
for week_dir in "$ORIGINAL"/week-[0-9][0-9]; do
  [ -d "$week_dir/labs" ] || continue
  week=$(basename "$week_dir")
  week_num="${week#week-}"

  for lab_file in "$week_dir"/labs/lab_[0-9][0-9]_*.md; do
    [ -f "$lab_file" ] || continue
    filename=$(basename "$lab_file")
    lab_num=$(echo "$filename" | sed -E 's/lab_([0-9]+)_.*/\1/')
    slug_part=$(echo "$filename" | sed -E 's/lab_[0-9]+_(.*)\.md/\1/' | tr '_' '-')
    slug="lab-${lab_num}-${slug_part}"

    # Look up title
    title_key="$week/$(echo "$filename" | sed 's/\.md$//')"
    title=$(get_lab_title "$title_key")
    if [ -z "$title" ]; then
      title="Lab ${week_num#0}.${lab_num#0}: ${slug_part}"
    fi

    order=$((10#$lab_num))

    dest_dir="$DOCS/$week"
    mkdir -p "$dest_dir"

    # Prepend frontmatter to the existing markdown content (skip any existing H1)
    tmpfile=$(mktemp)
    cat > "$tmpfile" <<FRONT
---
title: "$title"
sidebar:
  order: $order
---

FRONT

    # Check if the file starts with an H1 and skip it (we use frontmatter title instead)
    first_line=$(head -1 "$lab_file")
    if echo "$first_line" | grep -q '^# '; then
      tail -n +2 "$lab_file" >> "$tmpfile"
    else
      cat "$lab_file" >> "$tmpfile"
    fi

    mv "$tmpfile" "$dest_dir/$slug.md"
    echo "    $week/$slug.md"
  done
done

echo ""
echo "==> Migration complete!"
echo "    Lessons:   $(find "$DOCS" -name 'index.md' | wc -l | tr -d ' ')"
echo "    Labs:      $(find "$DOCS" -name 'lab-*.md' | wc -l | tr -d ' ')"
echo "    Scaffolds: $(find "$SCAFFOLDS" -name '*.py' 2>/dev/null | wc -l | tr -d ' ')"
