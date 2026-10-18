#!/usr/bin/env bash
# Append one snapshot line under "## Dev Snapshot" in today's wensai daily note.
# Writes the Markdown file directly: the Obsidian CLI can hang when the app is closed,
# and `daily:append` adds a duplicate heading on every call.
# Never creates the daily note; exits 1 if it is missing.
# Usage: append_snapshot.sh "[<date>] <repo>: <summary>"
set -eu
line="$1"
vault_dir="${WENSAI_VAULT:-$HOME/work/wensai/wensai}"
[ -d "$vault_dir/.obsidian" ] || { echo "Not recorded: no vault at $vault_dir" >&2; exit 1; }
today=$(date +%Y-%m-%d)
note="$vault_dir/journal/$(date +%Y)/$(date +%m)/$today.md"
# Never create the daily note: Obsidian builds it from the user's template.
[ -f "$note" ] || { echo "Not recorded: today's daily note does not exist yet ($note); open it in Obsidian first" >&2; exit 1; }
heading="## Dev Snapshot"
if ! grep -qx "$heading" "$note"; then
  printf '\n%s\n\n> %s\n' "$heading" "$line" >> "$note"
else
  # Insert after the last line of the existing section, before the next heading of level 1-2.
  temporary="$note.snapshot_tmp"
  awk -v heading="$heading" -v entry="> $line" '
    { lines[NR] = $0 }
    $0 == heading { start = NR }
    END {
      stop = NR
      if (start) for (i = start + 1; i <= NR; i++) if (lines[i] ~ /^##? /) { stop = i - 1; break }
      last = stop
      while (last > start && lines[last] ~ /^[[:space:]]*$/) last--
      for (i = 1; i <= last; i++) print lines[i]
      print ""; print entry
      if (stop < NR) print ""
      for (i = last + 1; i <= NR; i++) if (i > stop || lines[i] !~ /^[[:space:]]*$/) print lines[i]
    }' "$note" > "$temporary"
  /bin/mv -f "$temporary" "$note"
fi
echo "Recorded to $note"
