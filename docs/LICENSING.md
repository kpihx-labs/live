# Licensing — live

> Not legal advice. Confirm with counsel before a commercial launch or fundraising.

## Goal matrix

| Goal | Fitting license |
|------|-----------------|
| **Maximum control** — no one may copy, host, or sell your stack without permission | **Proprietary** (All Rights Reserved) — current `LICENSE` |
| **Open code, force derivatives to stay open** (including network/SaaS) | **AGPL-3.0** |
| **Open code, permissive reuse** (libraries, tools) | MIT or Apache-2.0 |
| **Delayed open source** (commercial exclusivity for N years) | BSL 1.1 (custom change date) |

## Why not MIT for `live`

MIT allows anyone to use, modify, and **commercialize** your code with minimal obligations. That fits **generic OSS utilities**, not a **strategic product** (voice UI, Scene IR, conductor).

## Current choice: proprietary

The repository ships under **All Rights Reserved** (`LICENSE` at repo root).

- **Copyright** exists automatically when you create the work (EU/FR droit d'auteur).
- The **license file** states what others **may** do with published copies (GitHub/GitLab).
- **Trademark** (`live`, `KpihX`, logos) is separate — register if you brand publicly.

## Practical checklist

1. Keep **secrets and keys** out of git (`.env` gitignored).
2. Add **copyright headers** on key source files if counsel recommends it.
3. For **contributors**: `CONTRIBUTING.md` + CLA only if you accept external patches.
4. **Dependencies**: audit licenses (`uv pip tree`, SBOM) — avoid GPL in proprietary stack unless you accept copyleft.
5. **Public repo + proprietary license** = source visible, **no right to use** without permission; stronger than no LICENSE file, weaker than a private repo.

## If you switch later

| Target | When |
|--------|------|
| AGPL-3.0 | Community self-host OK, no closed SaaS forks |
| Apache-2.0 | Open SDK layers only |
| Private repo | Maximum secrecy before launch |

Document in `CHANGELOG.md` and replace `LICENSE` in one commit.
