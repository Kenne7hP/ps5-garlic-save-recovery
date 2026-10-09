# Garlic Manager protocol notes

Read this when automating native HTTP operations. The following routes were observed in a working manager, not a version-independent API contract. Re-read the installed frontend and a matching source/release before mutation.

Primary references:
- https://github.com/earthonion/garlic-savemgr
- https://github.com/earthonion/garlic-savemgr/blob/main/src/main.c
- https://github.com/earthonion/garlic-savemgr/blob/main/src/ui.html
- https://github.com/earthonion/garlic-savemgr/releases

## Route semantics

| Route | Observed behavior | Consequence |
| --- | --- | --- |
| `GET /api/users` | Current users, with local IDs | Keep identifiers in memory |
| `GET /api/saves` | Save inventory with title, filename, platform, backup/user fields | Resolve indexes freshly; output an allowlist |
| `GET /api/download_raw?idx=...` | Stream the encrypted image without mounting it | Use for backups and non-target copies |
| `POST /api/import_encrypted?uid=...` | Raw `application/octet-stream` image upload to `_tmp_import`; mounts the temporary copy and returns metadata/account comparison | Staging is a mutation, though it does not finish a slot import |
| `GET /api/files` | Recursive current mount file list: name, dir, size | A nonempty list before staging signals another mounted save; pause |
| `GET /api/download_file?name=...` | Download one file from current mount | URL-encode the relative path; verify response length |
| `GET /api/import_finish?uid=...` | Rebind, unmount, copy image into target slot and update system save registration | This GET is a write; commit only after checks and authorization |
| `GET /api/unmount` | Finalize mount, potentially copy back an installed image | Not a read-only operation; avoid duplicate unmount after finish |
| `GET /api/mount?idx=...` | Mount installed save, potentially using a local copy | Avoid for non-target inspection |

Use an explicit target UID for staging and finishing. Never output the composed UID-bearing URL. Keep returned `save_aid` and `user_aid` in memory. Test error fields and content type, not just status 200; JSON errors may arrive with HTTP success. Check an image is actually binary before saving it.

Upstream PS5 temporary staging uses `/data/save_files/_tmp_import`; `mount_by_path` clears the local-copy pointer. Unmounting that staged copy therefore does not invoke installed-image copyback in the demonstrated implementation. Confirm these semantics in the user's running variant. Never call `import_finish` for a copy used only for comparison.

## SFO verification

SFO has a 20-byte header, 16-byte index entries, a key table and a data table. Validate header, entry count, bounds and required fields before reading values. Use `TITLE_ID`, `SAVEDATA_DIRECTORY`, `FORMAT`, `ACCOUNT_ID` and relevant `PARAMS` fields. Observed PS5 format is `ppr`; PS4 format is `obs` and requires different handling.

The demonstrated upstream documents PARAMS user ID at relative `+0x04` and a 32-byte integrity field at `+0x08`. Verify this layout before reading. Do not write to a guessed absolute offset. Let the compatible manager handle rebinding. An integrity-field match was useful in the demonstrated case, but does not establish a universal signing rule or justify copying it between users.

Names prefixed `sdimg_sce_bu_` are backups, not ordinary save slots. Source ZIP layouts, title IDs, system-save dependencies and slot names are game-specific.

## Stop and resume

Persist a sanitized checkpoint immediately after a confirmed finish, before any later verification. If finish succeeded but verification failed, inspect the written result via a downloaded copy; do not repost or restore automatically. On an unknown network outcome, inspect inventory/current bytes and checkpoint before retrying. Leave the manager unmounted at handoff when this workflow owns the mount.
