-- Set the pattern to scan for
local ans = {}
local pattern = ARGV[1]
local batchSize =  ARGV[2]
local cursor = '0'

repeat
    local result = redis.call('SCAN', cursor, 'MATCH', pattern, 'COUNT', batchSize)
        for _, key in ipairs(result[2]) do
            if key ~=nil and type(key) == "table" then
                 for k, v in pairs(t) do key = v; end;
            end;
            if key ~=nil then
            	local keyty = redis.pcall('type', key)['ok']
            	if keyty ~=nil then
                    if keyty == 'string' then
                        local count = redis.pcall("DEL",key)
                        ans[#ans+1] = key.." -> string type, removed : "..count;
                    elseif keyty == 'list' then
                        local count = redis.pcall("DEL",key)
                        ans[#ans+1] = key.." -> list type, removed : "..count; 
                    elseif keyty == 'set' then
                        local count = redis.pcall("DEL",key)
                        ans[#ans+1] = key.." -> set type, removed :"..count;
                    elseif keyty == 'zset' then
                        local count = redis.pcall("DEL",key)
                        ans[#ans+1] = key.." -> sortedset type, removed :"..count;
                    elseif keyty=='hash' then
                        local count = redis.pcall("DEL",key)
                        ans[#ans+1] = key.." -> hash type, removed :"..count;
                    else 
                        local count = redis.pcall("DEL",key)
                        ans[#ans+1] = key.." -> unknown type, removed :"..count;
                    end
            	end;
            	if keyty ==nil then
               		ans[#ans+1] = key.." Empty type, not removed.";
            	end;
            end;
        end
    cursor = result[1]
until (cursor == '0')
return ans;


