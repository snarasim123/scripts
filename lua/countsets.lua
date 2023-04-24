-- Set the pattern to scan for
local ans = {}
local pattern = ARGV[1]
local batchSize =  ARGV[2]
local cursor = '0'

-- Repeat until the cursor is '0'
repeat
    -- Scan for keys matching the pattern
    local result = redis.call('SCAN', cursor, 'MATCH', pattern, 'COUNT', batchSize)
        for _, key in ipairs(result[2]) do
            if key ~=nil and type(key) == "table" then
                 for k, v in pairs(t) do key = v; end;
            end;
            if key ~=nil then
            	local keyty = redis.pcall('type', key)['ok']
            	if keyty ~=nil then
                    -- if keyty == 'string' then
                    --     local count = redis.pcall("STRLEN",key)
                    --     ans[#ans+1] = key.." -> string type : "..count;
                    -- elseif keyty == 'list' then
                    --     local count = redis.pcall("LLEN",key)
                    --     ans[#ans+1] = key.." -> list type : "..count; 
                    -- elseif keyty == 'set' then
                    --     local count = redis.pcall("SCARD",key)
                    --     ans[#ans+1] = key.." -> set type"..count;
                    -- elseif keyty == 'zset' then
                    --     local count = redis.pcall("ZCARD",key)
                    --     ans[#ans+1] = key.." -> sortedset type"..count;
                    -- elseif keyty=='hash' then
                    --     local count = redis.pcall("HLEN",key)
                    --     ans[#ans+1] = key.." -> hash type"..count;
                    -- end
                    if keyty == 'set' then
                            local count = redis.pcall("SCARD",key)
                            ans[#ans+1] = key.." -> set type"..count;
                    end
            	end;
            	if keyty ==nil then
               		ans[#ans+1] = key.." Empty type";
            	end;
            end;
        end
    cursor = result[1]
until (cursor == '0')
return ans;


