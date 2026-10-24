# Contributing to opx_pool_assets

Follow the [organization guide](https://github.com/opx77-framework/.github/blob/main/CONTRIBUTING.md).
Work through an issue, branch and PR; never push source changes directly to main.

Keep cooked host files under `assets/hosts/` and table patches under
`assets/cleanup/archive/pc/mod/`. Record source names, buffer segment sizes and
SHA-256 values in `asset-manifest.json`; preserve credits in `NOTICE.md`.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/build.py`.
Commit the rebuilt `dist/opx_pool_assets.zip`. CI refuses a stale package.
Only the six reserved legacy host paths and fifteen namespaced
`open77/assets/opx_infinity/pool/ball_01.ent` through `ball_15.ent` may enter the archive. The latter
use resource-owned model registration, not global alias overrides. Run
`python3 tools/ball_hosts.py` after editing the recorded host template and
verify the generated files match. Do not restore unrelated
food, medical or military overrides from the source pack.

Changing a preload requires a dedicated-server restart and a fresh client boot
through the launcher. State in the PR whether the actual models, cue alignment,
ArchiveXL cleanup and removal/rejoin behavior were verified in game.
