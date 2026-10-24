local published, live, nextId, destroyed, caller, events = {}, {}, 0, 0, 'opx_infinity', {}
local env = setmetatable({ exports=function(name,fn) published[name]=fn end,GetInvokingResource=function() return caller end,
 AddEventHandler=function(name,fn) events[name]=fn end,
 Open77={audio={getState=function() return {status='playing'} end,play3D=function(path,position,options)
  assert(path:match('^audio/[%w]+%.wav$') and options.loop==false and options.maxDistance==12)
  nextId=nextId+1;live[nextId]=true;return nextId
 end,destroy=function(id) assert(live[id]);live[id]=nil;destroyed=destroyed+1;return true end}} },{__index=_G})
assert(loadfile('client/main.lua','t',env))()
local play,clear=published.pool_audio,published.pool_audio_clear
local event={kind='ball',position={x=10,y=20,z=1},volume=0.5}
caller='other';assert(not play({event}) and nextId==0 and not clear(),'foreign caller used the pool service')
caller='opx_infinity'
assert(not play({event,{kind='bad'}}) and nextId==0,'invalid batch partly played')
for _=1,20 do assert(play({event})) end
local count=0;for _ in pairs(live) do count=count+1 end
assert(count==8 and destroyed==12,'voice cap was exceeded')
assert(clear() and next(live)==nil)
assert(play({event}));events.onClientResourceStop('opx_infinity');assert(next(live)==nil,'dependent stop leaked voices')
print('recorded audio: caller ownership, atomic validation, voice cap and cleanup passed')
