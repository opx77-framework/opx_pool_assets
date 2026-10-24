-- Data-only billiards models and table cleanup, served by the Open77 launcher.
resource "opx_pool_assets"
version "0.1.1"
open77_version ">=2.50.0"
auto_start true
reload_policy "reconnect"
-- ArchiveXL is required through server.jsonc requiredMods.packages (indexed).
-- Do not preload its DLL resource on a secured world.
preload_mod "dist/opx_pool_assets.zip"
server_script "server/main.lua"
