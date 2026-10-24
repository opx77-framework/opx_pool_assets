# Asset credits and scope

Original OPX packaging, builder, tests and documentation are MIT licensed,
copyright (c) 2026 Luís MOUTA. The MIT licence does not grant rights to the supplied
third-party cooked assets, game content or trademarks.

The operator supplied `nc_pool` 1.0.21 by **Darkpickle**. Its `0_nc_pool_props.archive`
provided the six host templates used here. The templates are preserved internally
and re-keyed into three explicitly reserved recreation slots; 44 unrelated host
overrides are excluded. The original horizontal cue template is `market.kiosk`.

The supplied table-cleanup measurements/ArchiveXL patches credit **JudoChopMods**,
*Street Games - Playable Pool and Billiards* / *Night City Billiards*:
https://www.nexusmods.com/cyberpunk2077/mods/33361
Additional supplied Afterlife, Coyote HQ and 6th Street patches credit Darkpickle.
Original provenance and SHA-256 values are recorded in `asset-manifest.json`.

The fifteen additional `opx/pool/ball_*.ent` visual hosts derive from the same
supplied object-ball host. Their compiled-data buffer changes only the vanilla
mesh reference; unchanged cooked buffers and original authorship are preserved.
The decoded source buffer, hashes and deterministic derivation are recorded in
`asset-manifest.json` and `tools/ball_hosts.py`. No additional vanilla meshes or
textures are redistributed.

The unused `night_city_billiards_balls.archive` and all nc_pool gameplay Lua/WebUI
scripts are excluded. Vanilla meshes remain in the player's Cyberpunk 2077 install
and belong to CD PROJEKT RED. This is an unofficial fan project with no CDPR
endorsement. Preserve the source authors' notices and conditions when distributing
third-party files; OPX does not relicense them.

## Recorded pool audio

The three PCM WAV clips in `audio/` are derived from real billiard recordings
released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/):

- [billiard ball clack by Za-Games](https://freesound.org/people/Za-Games/sounds/539854/).
- [Pool_Table_Ball_Hit_Sink.WAV by AmberdeMeillon](https://freesound.org/people/AmberdeMeillon/sounds/443066/), cue excerpt.
- [Pool_Table_Ball_Hit.WAV by AmberdeMeillon](https://freesound.org/people/AmberdeMeillon/sounds/443067/), pocket excerpt.

The public HQ previews were trimmed, converted to mono PCM16/44.1 kHz, faded
and level adjusted. Exact source/output hashes and cuts are in `audio/sources.json`.
These recordings retain their CC0 dedication. They are not synthesized effects.
