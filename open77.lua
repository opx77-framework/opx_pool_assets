-- Data-only billiards models and table cleanup, served by the Open77 launcher.
resource "opx_pool_assets"
version "0.1.0"
open77_version ">=2.50.0"
auto_start true
reload_policy "reconnect"
dependency "archivexl >=1.27.1"
preload_mod "dist/opx_pool_assets.zip"
server_script "server/main.lua"
