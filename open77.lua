-- Data-only billiards models and table cleanup, served by the Open77 launcher.
resource "opx_pool_assets"
version "0.1.2"
-- Client manifests use the runtime version (0.0.1), not the game build (2.50).
open77_version ">=0.0.1"
auto_start true
reload_policy "reconnect"
-- Decoration cleanup needs the Cyberpunk 2.5 ArchiveXL port; see README.
-- Do not request an indexed loader ID absent from the platform catalogue.
-- Do not preload its DLL resource on a secured world.
preload_mod "dist/opx_pool_assets.zip"
server_script "server/main.lua"

-- Keep this dependency present in the signed client resource set.
client_script "client/main.lua"
