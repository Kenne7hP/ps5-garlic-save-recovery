# Credits and provenance

This repository provides an independently maintained Codex skill and a read-only local save-backup validator. Its recovery workflow depends on Garlic SaveMgr; credit for the manager, its save-management features and payload implementation belongs to the upstream author and contributors.

## Garlic SaveMgr

- Project: [Garlic SaveMgr for PS5](https://github.com/earthonion/garlic-savemgr)
- Repository owner / author credited by project identity: [earthonion](https://github.com/earthonion)
- Implementation and embedded UI: [src/main.c](https://github.com/earthonion/garlic-savemgr/blob/main/src/main.c) and [src/ui.html](https://github.com/earthonion/garlic-savemgr/blob/main/src/ui.html)
- Releases: https://github.com/earthonion/garlic-savemgr/releases
- Attribution review date: 2026-10-08
- Upstream revision inspected: `ac651cbd72bf80a6ad0ce97cd182e4fb8eab6ecd`

The protocol notes summarize publicly inspectable manager behavior and link to the upstream implementation. This repository contains locally authored skill instructions and the local Python validation helper; it does not distribute Garlic SaveMgr source code, binaries, payloads or third-party game/save data.

At the inspected revision, the upstream repository root had no LICENSE file, and GitHub repository metadata declared no license. A public repository alone does not grant permission to redistribute its implementation under a chosen license. Use upstream links for the manager, and verify upstream terms before copying or modifying its code for redistribution. The [MIT License](LICENSE) in this repository applies only to this repository's original skill documentation and local validation helper. It does not license Garlic SaveMgr, PS5 Payload SDK, or game/save data.

## Other upstream acknowledgments

Garlic SaveMgr's README identifies [PS5 Payload SDK](https://github.com/ps5-payload-dev/sdk) as its build dependency. That relationship belongs to Garlic SaveMgr; this skill's read-only validation helper uses Python's standard library.

## Contributions to this skill

The skill was assembled through local recovery work and AI-assisted writing/code preparation. The validated case describes the limits of the observed results. Credits to Garlic SaveMgr do not imply upstream authorship, review or endorsement of this independent skill.
