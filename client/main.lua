--- Resource-owned recorded billiard sounds; the archive still mounts before boot.
-- @author dop42
local clips = { cue = 'audio/cue.wav', ball = 'audio/ball.wav', rail = 'audio/ball.wav', pocket = 'audio/pocket.wav' }
local voices, cursor = {}, 0
local function number(v, lo, hi) return type(v) == 'number' and v == v and v >= lo and v <= hi end
local function clear()
	for index, id in pairs(voices) do Open77.audio.destroy(id);voices[index] = nil end
	cursor = 0
	return true
end
exports('pool_audio_clear', function()
	if GetInvokingResource() ~= 'opx_infinity' then return false, 'caller_not_allowed' end
	return clear()
end)
exports('pool_audio', function(events)
	if GetInvokingResource() ~= 'opx_infinity' then return false, 'caller_not_allowed' end
	if type(events) ~= 'table' or #events > 4 then return false, 'invalid_events' end
	for _, event in ipairs(events) do
		if type(event) ~= 'table' or not clips[event.kind] or type(event.position) ~= 'table'
			or not number(event.position.x, -20000, 20000) or not number(event.position.y, -20000, 20000)
			or not number(event.position.z, -2000, 5000) or not number(event.volume, 0, 1) then return false, 'invalid_event' end
	end
	for index, id in pairs(voices) do
		local state = Open77.audio.getState(id)
		if state and (state.status == 'ended' or state.status == 'error') then
			if state.status == 'error' then Open77.log.warn('[opx_pool_assets] audio decoder: ' .. tostring(state.error)) end
			Open77.audio.destroy(id); voices[index] = nil
		end
	end
	for _, event in ipairs(events) do
		cursor = cursor%8+1
		if voices[cursor] then Open77.audio.destroy(voices[cursor]);voices[cursor] = nil end
		local id, why = Open77.audio.play3D(clips[event.kind], event.position,
			{ volume = event.volume*(event.kind == 'rail' and 0.45 or 1), minDistance = 1, maxDistance = 12, loop = false })
		if not id then return false, why end
		voices[cursor] = id
	end
	return true
end)
AddEventHandler('onClientResourceStop', function(name)
	if name == 'opx_infinity' then clear() end
end)
