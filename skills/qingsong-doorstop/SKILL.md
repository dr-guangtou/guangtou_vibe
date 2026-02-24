---
name: qingsong-doorstop
description: Specialized knowledge for managing MUST requirements, risks, and interfaces using the Qingsong wrapper around Doorstop. Use when creating, updating, or analyzing the requirements network (REQ, RSK, IFC, DOC, DAT, NOTE).
---

# Qingsong Doorstop Management

This skill provides expert guidance for the "Requirements as Code" workflow used in the MUST project.

## 1. Domain Knowledge

### 1.1 Item ID Pattern
All items must follow: `MUST-<L1>-<L2>-<TYPE>-NNN`
- `<L1>`: Major system (FPS, SPS, DMS, SWG)
- `<L2>`: Subsystem (FID, DET, PIPE, etc.)
- `<TYPE>`: REQ, RSK, IFC, DOC, DAT, NOTE
- `<NNN>`: 3-digit sequence

### 1.2 Hierarchy & L3
- Items are stored in `doorstop/<TYPE>/<L1>/<L2>/`.
- For complex sub-assemblies, a deeper path is allowed: `doorstop/<TYPE>/<L1>/<L2>/<L3>/`.
- L3 items are first-class items with their own requirements and verification.

### 1.3 Link Types & Rules
| Link Type | Semantic Meaning | Source -> Target |
| :--- | :--- | :--- |
| `implements` | Satisfies a requirement | DOC, DAT, NOTE -> REQ |
| `verifies` | Provides verification evidence | DOC, DAT, NOTE -> REQ |
| `mitigates` | Risk mitigation | NOTE, DOC, REQ -> RSK |
| `impacts` | Risk impact area | RSK -> REQ, IFC, DOC |
| `derives_from`| Hierarchical link | REQ -> REQ |

## 2. Workflows

### 2.1 Creation
1. Verify the `<L1>/<L2>` path in `meta/hierarchy.yaml`.
2. Determine the next available sequence number.
3. Use the `qingsong new` CLI or `QingsongCore.create_item` API.
4. Ensure `owner` is a valid ID from `meta/people.yaml`.

### 2.2 Refactoring (Conceptual Design Phase)
When moving or merging systems:
1. Update `meta/hierarchy.yaml`.
2. Move files to the new directory structure.
3. Update IDs in the YAML files.
4. **Critical**: Search the entire repository for the old ID and update any links to point to the new ID.

### 2.3 Validation
Always run `qingsong validate` after any edit.
- No circular dependencies allowed in `derives_from` links.
- All link targets must exist in the repository or be marked `EXT:`.
- All owners and system paths must exist in `meta/`.

## 3. Storage Architecture
- **Source of Truth**: YAML files in `doorstop/`.
- **Query Engine**: SQLite cache in `index/qingsong.sqlite`.
- **Update Cycle**: Edit YAML -> Validate -> Rebuild Cache.
