<h1 align="center">OPX//77 · opx_pool_assets</h1>
<p align="center"><strong>Open77 preload assets for the original OPX billiards practice module.</strong></p>
<p align="center">
  <a href="https://github.com/opx77-framework/opx_pool_assets/actions/workflows/check.yml">Checks</a> ·
  <a href="https://github.com/opx77-framework/opx_infinity">Framework</a> ·
  <a href="https://opx77-framework.github.io/opx77_doc/">Documentation</a>
</p>

---

## What it contains

A separate **Open77 asset resource**, not another gameplay implementation:

- Six cooked hosts: ordinary/attached variants of a cue ball, a yellow object
  ball and a horizontal cue. Motion blur settings from the supplied hosts remain.
- Ten supplied ArchiveXL table-cleanup patches.
- A deterministic builder and checked preload ZIP under `dist/`.
- Original source credits and provenance in [NOTICE.md](NOTICE.md).

**Three native aliases are reserved globally while this world pack is mounted:**

| Alias | OPX use |
| --- | --- |
| `recreation.tent` | White cue ball |
| `recreation.sleeping_bag` | Yellow object ball |
| `recreation.gym_equipment` | Horizontal cue |

Open77's current supported prop catalogue supplies the spawn-safe host slots.
These three slots must not be used for their original objects by other resources
on the same server. The legacy pack replaced 25 aliases; this package excludes
its food, medical and military replacements. It does **not** add native pool aliases
or claim to remove the platform's catalogue limitation.

## Installation

1. Install this repository as `resources/opx_pool_assets` alongside `opx_infinity`.
   The committed ZIP is ready; Python is needed only to rebuild it.
2. Require the official **indexed** ArchiveXL package through your server's
   `requiredMods.packages`, with `id: "archivexl"` and `minVersion: "1.27.1"`.
   It is distributed and verified by the Open77 signed index.
3. Add `opx_pool_assets` before `opx_infinity` in `resources.load`, preserving your
   other resources. **Do not load the `archivexl` resource on a secured server**:
   its automatic preload contains a DLL and is deliberately refused by Open77.
4. Keep `requiredMods.enabled: true` and your current security policy. The
   [configuration example](server-config.example.json) uses `unsecured: false`.
   Merge its entries into your existing configuration; do not replace the rest.
5. Stop loading `nc_pool` and its old preload on this world; loading both would
   reintroduce the original host conflicts.
6. **Restart the dedicated server. Every player must fully quit Cyberpunk and
   reconnect through the Open77 launcher.** It downloads/projects the new world
   package before starting the game. A Lua reload cannot mount archives mid-game.
7. Configure the practice table in `opx_infinity/config/pool.lua`. Model aliases
   must match the table above. The ten table presets are in the framework.

The launcher downloads `opx_pool_assets-assets` from your Open77 resource HTTP
endpoint and resolves ArchiveXL through the platform signed index. No Fivemanage key or manual player file copy is involved: these are
cooked 3D assets mounted at game boot.

## Layout and rebuilding

```
assets/hosts/cyberm/entities/props/       six cooked entity sources
assets/cleanup/archive/pc/mod/           supplied world-cleanup patches
asset-manifest.json                     source hashes, buffer sizes and mappings
tools/build.py                          Python 3.10+ standard-library builder
dist/opx_pool_assets.zip                 game-root relative preload
open77.lua                              resource and loader dependency
```

Run `python3 tools/build.py`, then `python3 -m unittest discover -s tests -v`.
The builder stores entity headers uncompressed and preserves the supplied KARK
buffers. It needs no game install or proprietary compressor. Rebuilding identical
sources produces identical bytes. Tests independently read archive headers,
indexes, CRC64, source segments and ZIP membership.

## Live validation

Server package publication and automated tests do not prove rendered shape,
pivot, size or table alignment. Check the white/yellow balls, horizontal cue,
movement, pockets and a second spectator after a **fresh launcher boot**.
ArchiveXL cleanup is tied to the recorded sector/node counts; a mismatched game
sector leaves its original decorations in place. Check ArchiveXL's client log.

## Contributing and credits

See [CONTRIBUTING.md](CONTRIBUTING.md), the organization's
[Code of Conduct](https://github.com/opx77-framework/.github/blob/main/CODE_OF_CONDUCT.md),
[Support](https://github.com/opx77-framework/.github/blob/main/SUPPORT.md) and
[Security](https://github.com/opx77-framework/.github/blob/main/SECURITY.md).
Read [NOTICE.md](NOTICE.md): the tooling licence excludes third-party assets.
