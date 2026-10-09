# Validated case: Ghost of Yōtei

On 2026-10-06, user-owned encrypted saves from another console/account were recovered through an existing Garlic Manager on a PS5 Pro running firmware 13.60. The user reported matching game update versions, a working fresh save, and failure loading imported old saves.

The source primary-save SFO was valid and its title/directory matched the game, but its account and local-user bindings differed from the target. One manual slot was re-bound and imported. The user confirmed loading old progress, saving separately, fully exiting and reloading. Remaining primary saves and system metadata were then migrated; the user reported success.

Lessons supported by this case:
- Installed-save mount/unmount changed encrypted bytes in baseline slots. Their decrypted files remained identical. Future inspection used raw-downloaded temporary copies.
- Successful finish already unmounted the save; an unnecessary second unmount incorrectly interrupted verification. Verification resumed without repeating import.
- A separate test save increased the inventory count. A fresh dynamic snapshot preserved it and the accepted pilot during batch migration.
- The original ZIP, pre-write snapshots and repaired exports stayed local; no save content or account identifier was packaged into this skill.

This case demonstrates the workflow, not support for all firmware, game versions, regions, encrypted formats or game-specific account/checksum schemes. Do not reuse its address, title ID, slots, paths, exact counts or signing assumptions as defaults for a new request.
