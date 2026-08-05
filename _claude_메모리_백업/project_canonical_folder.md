---
name: canonical-folder
description: "For the 놀라운 한국어 500 해설집 project, edits must go to D:\\OneDrive\\놀라운 한국어 500 해설집 — NOT to d:\\놀라운 한국어 500 해설집 (which is a separate, possibly orphaned copy)."
metadata: 
  node_type: memory
  type: project
  originSessionId: a8a53b45-da27-4b8d-af7f-8f1671af07ef
---

**Canonical project folder: `D:\OneDrive\놀라운 한국어 500 해설집\`**

**Why:** The user clarified on 2026-05-28 that the working/source-of-truth files live in the OneDrive folder. The session's default cwd was `d:\놀라운 한국어 500 해설집` (no OneDrive in the path), which turns out to be a separate, divergent copy. Edits applied there do not reach the user's actual study files.

**How to apply:**
- When the user references "the file" or a numeric range like "260~265" without a full path, look in `D:\OneDrive\놀라운 한국어 500 해설집\` first.
- Do NOT edit files under `d:\놀라운 한국어 500 해설집\` (no OneDrive segment) — those are stale.
- Do NOT edit files under `D:\OneDrive\놀라운 한국어 500 해설집\임시\` — those are 통합본 (concatenated all-in-one builds) that get regenerated; touching them is wasted work.
- Skill/task tools that take paths should be given the OneDrive absolute path.
- If a session's cwd is `d:\놀라운 한국어 500 해설집`, treat that as a wrong-folder symptom and switch to the OneDrive path explicitly.
