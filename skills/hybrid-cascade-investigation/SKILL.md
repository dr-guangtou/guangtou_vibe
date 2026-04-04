---
name: hybrid-cascade-investigation
description: Systematic multi-agent workflow combining quick redundancy scanning with targeted deep dives for comprehensive research coverage
title: Hybrid Cascade Multi-Agent Investigation
version: 1.0.0
author: Hermes Agent
date: 2025-01-04
category: research
---

# Hybrid Cascade Multi-Agent Investigation

## Quick Reference

```yaml
Use when:
  - Researching new or unfamiliar topics
  - Literature reviews requiring comprehensive coverage
  - Exploring cutting-edge/frontier research areas
  - When you suspect "unknown unknowns"

Do NOT use when:
  - Simple factual lookups
  - Well-understood topics with consensus
  - Time-critical responses

Workflow:
  1. Phase 1: Quick redundancy scan (2 agents, 4-5 searches each)
  2. Gap analysis: Identify consensus vs gaps
  3. Phase 2: Targeted deep dives (1 agent per gap, 8-12 searches)
  4. Synthesis: Combine, verify citations, generate Obsidian output

Output:
  - Obsidian-formatted markdown with frontmatter
  - Citation verification log
  - Raw agent outputs for audit
  - Saved to ~/Desktop/qibin/investigations/
```

## Description

A systematic multi-agent workflow that combines **quick redundancy scanning** with **targeted deep dives** to efficiently investigate complex topics. Optimized for discovery of unknown unknowns while maintaining depth on critical findings.

This workflow is particularly effective when:
- You don't know what you don't know about a topic
- Missing a key method or paper would be costly
- The topic is actively evolving (new papers, debates)
- You need both breadth and depth

## When to Use

**Use for:**
- Researching new or unfamiliar topics
- Literature reviews requiring comprehensive coverage
- Exploring cutting-edge/frontier research areas
- When you suspect there are "unknown unknowns"
- Topics where methods/techniques are scattered across disciplines

**Don't use for:**
- Simple factual lookups (single agent is faster)
- Well-understood topics with established consensus
- Time-critical responses where "good enough" suffices
- Very narrow technical questions

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: QUICK REDUNDANCY SCAN (Parallel)                      │
│  ├── 2 agents investigate same broad question                   │
│  ├── Limited scope: 4-5 searches each                           │
│  └── Goal: Identify consensus vs gaps                           │
├─────────────────────────────────────────────────────────────────┤
│  GAP ANALYSIS                                                   │
│  ├── Extract consensus (2+ agents agree)                        │
│  ├── Identify gaps (found by only 1 agent)                      │
│  └── Flag recent/surprising findings for deep dive              │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 2: TARGETED DEEP DIVES (Parallel)                        │
│  ├── Delegate 1 agent per identified gap                        │
│  ├── Full depth: 8-12 searches each                             │
│  └── Goal: Comprehensive coverage of gaps                       │
├─────────────────────────────────────────────────────────────────┤
│  SYNTHESIS & OUTPUT                                             │
│  ├── Combine all findings                                       │
│  ├── Verify citations and links                                 │
│  └── Generate Obsidian-formatted summary                        │
└─────────────────────────────────────────────────────────────────┘
```

## Procedure

### Step 1: Initialize Investigation

Create output directory:

```
~/Desktop/qibin/investigations/
└── YYYY-MM-DD_topic-name/
    ├── YYYY-MM-DD_topic-name.md          # Main Obsidian file
    ├── raw_findings_phase1.json          # Phase 1 outputs
    ├── raw_findings_phase2.json          # Phase 2 outputs
    ├── citation_log.csv                  # Verification status
    ├── gap_analysis.md                   # Phase 1 → 2 mapping
    └── README.md                         # Quick orientation
```

### Step 2: Phase 1 - Quick Redundancy Scan

Spawn 2 agents in parallel with identical prompts:

```
Goal: "Quick survey: {topic}. List main methods/techniques, 
2-3 key papers per method, and any recent surprises or debates 
(last 2-3 years). Focus on breadth over depth. Limit to 4-5 searches."

Context: "Phase 1 of HYBRID CASCADE. This is a QUICK redundancy 
pass to identify coverage and gaps. Focus on finding what exists 
and what's controversial/recent."

Toolsets: ["web"]
Max iterations: 15
```

### Step 3: Gap Analysis

Parse both outputs and categorize:

**Consensus** (found by both agents):
- Mark as HIGH confidence
- Note for synthesis but skip deep dive

**Gaps** (found by only 1 agent):
- Mark as candidate for Phase 2
- Prioritize by: recency, uniqueness, relevance to topic

**Surprises** (unexpected, controversial, very recent):
- Always prioritize for deep dive

### Step 4: Phase 2 - Targeted Deep Dives

For each identified gap, spawn 1 agent:

```
Goal: "Deep dive: {gap_topic}. Cover: (1) core concept, 
(2) key quantitative findings, (3) limitations/challenges, 
(4) 3-5 key papers with full citations and working links."

Context: "Phase 2 of HYBRID CASCADE - Deep dive on a gap identified 
in Phase 1. Be thorough - extract papers if accessible."

Toolsets: ["web", "research"]
Max iterations: 50
```

### Step 5: Citation Verification

For each cited paper, verify:

1. **Existence**: Search arXiv, ADS, or journal database
2. **Accessibility**: Full text vs abstract only
3. **Claim validation**: Agent summary matches actual paper
4. **Link preservation**: Prefer arXiv > DOI > ADS abstract

**Verification status:**
- ✅ **Verified**: Full text checked, claims validated
- ⚠️ **Abstract only**: Source found, full text inaccessible
- 🔍 **Pending**: Citation exists but not fully checked
- ❌ **Not found**: Cannot locate source

### Step 6: Generate Obsidian Output

Create main markdown file with complete frontmatter:

```yaml
---
title: "{topic}"
date: {YYYY-MM-DD HH:MM}
date_created: {ISO timestamp}
investigation_type: hybrid_cascade
agents_phase1: {n}
agents_phase2: {n}
total_agents: {total}
total_duration_minutes: {mm}
phase1_duration: {mm}
phase2_duration: {mm}
confidence_level: {high|medium|low}
citations_count: {n}
citations_verified: {n}
topics_identified: {n}
gaps_found: {n}
gaps_investigated: {n}
obsidian_vault_copy: {status}
obsidian_location: {path or "N/A"}
tags:
  - research
  - investigation
  - hybrid_cascade
  - {topic_specific_tags}
aliases:
  - "{short_topic_name}"
---
```

**Body sections:**
1. Executive Summary
2. Investigation Log
3. Consensus Findings (Phase 1)
4. Gap Deep Dives (Phase 2)
5. Emerging Themes
6. Method Comparison
7. Source Verification Table
8. Recommendations
9. Appendix: Full Agent Outputs
10. Vault Copy Status (if applicable)

### Step 7: Copy to Obsidian Vault

**Default behavior**: Automatically copy investigation to appropriate Obsidian folder.

```python
def determine_category(topic):
    """Determine Obsidian folder based on topic keywords."""
    topic_lower = topic.lower()
    astro_keywords = [
        'astronomy', 'astrophysics', 'galaxy', 'cosmology', 'dark matter',
        'black hole', 'star', 'exoplanet', 'planet', 'telescope', 'survey',
        'halo', 'lensing', 'supernova', 'nebula', 'cluster', 'stellar'
    ]
    
    if any(kw in topic_lower for kw in astro_keywords):
        return 'astro'
    return 'agentic'  # default

def copy_to_obsidian(source_dir, topic):
    """Copy investigation to Obsidian vault."""
    category = determine_category(topic)
    vault_path = Path.home() / 'work' / 'wensai' / 'investigation' / category
    
    try:
        vault_path.mkdir(parents=True, exist_ok=True)
        dest_dir = vault_path / source_dir.name
        
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(source_dir, dest_dir)
        
        return {
            'success': True,
            'location': str(dest_dir),
            'category': category
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'attempted_location': str(vault_path)
        }
```

**Notification rules:**
- ✅ Success: Add to frontmatter, no user notification needed
- ⚠️ Failure: Add warning to output, notify user with:
  - Error message
  - Source location (preserved)
  - Attempted destination

## Output Structure

### Primary Output (Default Location)

```
~/Desktop/qibin/investigations/
└── YYYY-MM-DD_topic-name/
    ├── YYYY-MM-DD_topic-name.md          # Main Obsidian file
    ├── raw_findings_phase1.json          # Phase 1 outputs
    ├── raw_findings_phase2.json          # Phase 2 outputs
    ├── citation_log.csv                  # Verification status
    ├── gap_analysis.md                   # Phase 1 → 2 mapping
    └── README.md                         # Quick orientation
```

### Secondary Output (Obsidian Vault)

**Default behavior**: Automatically copy results to Obsidian vault at:
```
~/work/wensai/investigation/{category}/YYYY-MM-DD_topic-name/
```

**Category determination:**
| Keywords in topic | Destination folder |
|-------------------|-------------------|
| astronomy, astrophysics, galaxy, cosmology, dark matter, black hole, star, exoplanet | `astro/` |
| AI, agent, LLM, machine learning, neural network, workflow, automation | `agentic/` |
| (ambiguous or other) | `agentic/` (default) |

**Copy behavior:**
- ✅ Success: Silently copied, link added to main file
- ⚠️ Warning: If copy fails, notify user with error details
- Original location always preserved

### Supporting Files

| File | Purpose |
|------|---------|
| `raw_findings_phase1.json` | Complete Phase 1 agent outputs |
| `raw_findings_phase2.json` | Complete Phase 2 agent outputs |
| `citation_log.csv` | All sources with verification status |
| `gap_analysis.md` | Mapping of Phase 1 → Phase 2 |
| `README.md` | Quick orientation for revisiting |

## Quality Checklist

Before completing:

- [ ] All citations have working links (arXiv preferred)
- [ ] Verification status marked for each source
- [ ] Consensus items clearly identified
- [ ] Gaps investigated with appropriate depth
- [ ] Obsidian frontmatter complete and accurate
- [ ] Files saved to ~/Desktop/qibin/investigations/
- [ ] README created for orientation
- [ ] Total time and agent count logged
- [ ] **Copy to Obsidian vault attempted**
  - [ ] Category determined (astro vs agentic)
  - [ ] Copy successful OR warning issued to user
  - [ ] Copy status recorded in frontmatter

## Pitfalls to Avoid

1. **Don't skip Phase 1**: Even for seemingly simple topics
2. **Don't deep dive everything**: Only identified gaps
3. **Don't trust citations blindly**: Always verify existence
4. **Don't exceed search limits**: Enforce max per agent
5. **Don't forget synthesis**: Raw output ≠ useful knowledge

## Variations

### Quick Mode
- Phase 1: 2 agents, 3 searches each
- Phase 2: Skip if confidence high
- Output: Summary only

### Deep Mode
- Phase 1: 3 agents, 6 searches each
- Phase 2: All gaps + selected consensus
- Verification: Full text for key papers
- Output: Comprehensive + annotated bibliography

## Credits
- Pattern: Ensemble methods in ML + divide-and-conquer
- Refined through: Dark matter halo shape investigations
- Format: Zettelkasten/Obsidian best practices
- Default output: ~/Desktop/qibin/investigations/
