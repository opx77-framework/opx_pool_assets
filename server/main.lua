--- The package is mounted before the client boots; no gameplay lives here.
-- @author dop42
AddEventHandler('onResourceStart', function(name)
	if name ~= GetCurrentResourceName() then return end
	Open77.log.info('[opx_pool_assets] preload ready: fifteen namespaced ball hosts, legacy cue models and table cleanup; restart clients through the launcher')
end)
