---
name: ps5-garlic-save-recovery
description: Recover and migrate user-owned PS5 saves between accounts or consoles through an existing Garlic Manager on the LAN. Use for imported saves that cannot load, account-binding mismatch, or requested save resigning and restoration; includes verified local backups and real-console acceptance. Does not install exploits, change firmware, or grant access to accounts.
---

# PS5 Garlic Save Recovery

Restore the user's existing progress with the least necessary change. Work through the already-running local Garlic Manager. Treat its installed frontend and matching upstream implementation as the protocol reference; a firmware number alone does not establish compatibility.

Directory convention: `SKILL.md` is the workflow; `references/` holds conditional protocol/case notes; `scripts/` holds read-only validation; `agents/` holds discovery metadata. Never store saves, account identifiers, raw manager logs, or recovery outputs inside this skill. Do not automatically clean up recovery artifacts.

## Establish the recovery target

- Distinguish a game that cannot launch, an invisible save, and a visible save that cannot load. Capture the error without account identifiers.
- Inspect the supplied manager address and known source archive locally. Discover redirected Downloads folders when relevant. Do not assume a past IP, title ID, file path, slot name, account, or inventory count.
- Determine encrypted images versus decrypted folders, game title ID and game update version, current user selection, and whether a fresh current-account save loads. Game update version and console firmware are different checks.
- Before any mount/staging/import, establish that the game is fully closed and other manager clients are idle. After a real-console test, establish this again before more writes. Prepare local copies while waiting.
- Identify which progress should be retained and the authorized replacement scope. A request for one slot does not authorize a batch. Read-only inspection needs no extra approval; obtain any approvals required by the user's actual workspace rules for overwrites/restoration or other consequential actions.

## Preserve before changing

Use a user-approved local, unsynced recovery directory. Define `source/` for unchanged originals, `before/<snapshot>/` for immutable pre-write images, `candidate/` for extracted sources and repaired exports, and `records/` for sanitized manifests. Write files with create-new semantics; never silently replace a prior snapshot.

1. Copy the source archive and verify its SHA-256. Fully validate the ZIP, not merely its central-directory listing. Use `scripts/inspect_recovery.py --archive <archive.zip>` if Python is available; do not install global dependencies to run it. For a local snapshot, pass `--backup-dir <snapshot> --manifest <manifest.json>` (entries contain `Save`, `Length`, `SHA256`). The tool never uploads, extracts or edits saves, and does not replace a second console read.
2. Enumerate the actual current user's game saves, including `sce_bu_` backup images. Resolve each raw-download index from a fresh inventory. Do not output paths containing user IDs.
3. Download all relevant images without mounting installed saves. Record safe save names, byte lengths and SHA-256; verify local files and a second console read. If the inventory or bytes change, stop and obtain a stable snapshot.
4. Take a fresh snapshot before a later batch, preserving new saves produced during testing. Validate required entries and unique names rather than freezing a previous total. New slots are evidence to inspect, not a reason to discard progress.

A filename ending in `_dec.zip` does not prove it is a valid decrypted export. Archive integrity does not prove that an encrypted image's internal game data is valid.

## Inspect copies and prove the proposed fix

Read [references/garlic-protocol.md](references/garlic-protocol.md) before native API operations or recovery-script adaptation.

**Mount/unmount is not read-only for an installed save.** Garlic can copy a mounted image back on unmount and change its encrypted bytes even without editing a game file. Inspect non-target saves by raw-downloading them and staging copies in the manager's temporary area. Do not call an installed-slot mount endpoint merely to discover account metadata.

- Use a user-confirmed working current-account save as the baseline. If the user cannot name its slot, inspect candidate copies and corroborate account/user fields with the manager's current-user registry lookup. Consistent metadata alone is not proof of game loadability.
- Parse SFO key/data tables with bounds checks. Validate PS5 format, title ID, internal savedata directory, account ID and local-user binding. For a supported PS5 SFO, verify the PARAMS user-binding layout against the actual upstream implementation; do not assume a fixed absolute byte offset.
- Compare relevant integrity metadata as evidence, never copy it blindly. Compare internal game files separately from SFO fields that legitimately change during account rebinding. Do not dump SFO contents or cryptographic fields to logs.
- If source mounting, SFO parsing, title/directory checks or target-account lookup fails, stop before committing. Do not force a zeroed SFO, fabricate account identifiers, rename a region, or patch a guessed checksum/version field.
- If encrypted bytes changed during an inspection, compare all decrypted files of the before/current **copies**. Do not restore an installed slot automatically or repeat installed mounts to investigate. Ask before an actual restore if required by the user's rules.

## Import one slot, then expand within scope

1. Select one source primary save as a pilot and verify its archive-derived checksum. Keep `sce_bu_` images as backup sources; do not import them as ordinary playable slots.
2. Stage the encrypted source for the explicitly selected current user. Check the returned metadata and current registry account against the baseline before the final import request. For decrypted sources, follow the installed manager's full supported import path; do not treat a folder as an encrypted image.
3. Let the manager perform account/user rebinding and image finalization. After a successful `import_finish`, the save may already be unmounted: do not interpret a second 'nothing mounted' unmount response as an import failure. Do not retry a completed write because post-write verification stopped.
4. Raw-download the installed result. Verify a temporary copy's binding/title/directory/integrity metadata and hash its internal files against the source, excluding only the specific SFO changes authorized by rebinding. Export the repaired image locally. Record commit success before verification so partial progress is recoverable.
5. Ask the user to load the old progress on PS5, save to another slot, fully exit, and reload. Backend success is not acceptance. Wait for this pilot test before a batch; preserve the accepted pilot and the new test save.
6. When authorized, migrate remaining primary slots sequentially. Recheck the target against its fresh backup before every write, verify each result and checkpoint immediately. Game-specific system metadata goes last only when the restore scope includes it and its structure is understood. Verify all non-target images remain unchanged.

On the first failed import or validation, stop the batch, preserve backups and report exactly which writes completed. Re-list current state and checkpoint before any retry. Do not replay the whole batch, auto-delete files, or automatically roll back. If aligned metadata still fails in-game, investigate game-specific binding, dependencies and version compatibility using evidence before proposing any content edit.

## Handoff

Report imported slots, preserved progress, backup location, checks performed, and real-console tests still pending. Keep account/user identifiers and raw server logs out of records, commits and external services. Remain local unless the user specifically authorizes another destination. Do not silently update a payload, firmware, firewall, registry or account configuration.

For the demonstrated Ghost of Yōtei case and the limits of that evidence, read [references/validated-case.md](references/validated-case.md). Successful use on that case is not a universal support claim.
