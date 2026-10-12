#!/usr/bin/env bash
# Compact dev-state snapshot shared by one-sentence, handover, and journal.
# Args: optional git range (A..B) or today|week|month; other words are ignored.
# Always exits 0: a failing command would abort Claude Code skill injection.
log_args=(--since="24 hours ago" -20)
for arg in "$@"; do
  case "$arg" in
    *..*) log_args=("$arg") ;;
    today) log_args=(--since=midnight) ;;
    week) log_args=(--since="1 week ago") ;;
    month) log_args=(--since="1 month ago") ;;
  esac
done

root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
repo=$(basename "$root")
today=$(date +%Y-%m-%d)
branch=$(git branch --show-current 2>/dev/null)
echo "date: $today"
echo "repo: $repo"
echo "branch: ${branch:-none}"
default_branch=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
[ -z "$default_branch" ] && default_branch=$(git rev-parse --verify -q main >/dev/null 2>&1 && echo main || echo master)
echo "default_branch: $default_branch"
echo "remote: $(git remote 2>/dev/null | head -1)"

echo; echo "## Commits (${log_args[*]})"
git log --oneline "${log_args[@]}" 2>/dev/null | head -30

echo; echo "## Uncommitted"
git status --short 2>/dev/null | head -20
git diff --stat HEAD 2>/dev/null | tail -1

latest_journal=$(ls -t "$root"/docs/journal/*.md 2>/dev/null | head -1)
if [ -n "$latest_journal" ]; then
  echo; echo "## Latest repo journal: ${latest_journal#$root/} (first 40 lines)"
  head -40 "$latest_journal"
fi

if [ -f "$root/docs/todo.md" ]; then
  echo; echo "## Completed todo items (last 15)"
  grep -E '^[[:space:]]*- \[x\]' "$root/docs/todo.md" | tail -15
fi

memory_file="$HOME/.claude/projects/$(echo "$root" | sed 's/[^A-Za-z0-9]/-/g')/memory/MEMORY.md"
if [ -f "$memory_file" ]; then
  echo; echo "## Project memory: Current State"
  awk '/^## .*[Cc]urrent [Ss]tate/{p=1;print;next} /^## /{p=0} p' "$memory_file" | head -30
fi

# ponytail: vault path hard-coded; `obsidian vault info` can hang when the app is closed.
vault_dir="$HOME/work/wensai"
if [ -d "$vault_dir/.obsidian" ]; then
  journal_base="$vault_dir/development/$repo/${repo}_${branch//\//-}_${today}"
  journal_path="$journal_base.md"
  suffix=2
  while [ -e "$journal_path" ]; do journal_path="${journal_base}_$suffix.md"; suffix=$((suffix + 1)); done
  echo; echo "journal_target: $journal_path"
fi
exit 0
