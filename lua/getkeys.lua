local ans, has, cursor = {}, {}, "0";
local calls = 0

repeat
    local t = redis.call("SCAN", cursor, "MATCH", "defaultTenantId:"..ARGV[1]..":*", "COUNT", 1000000000);
    local list = t[2];
    for i = 1, #list do
        local s = list[i];
        local val = redis.pcall("GET",s);
        local typevar = type(val)
        ans[#ans + 1] = "Del :"..s.." :Type -->"..typewar;
        -- if typevar == "string" then
        --         ans[#ans] = ans[#ans].." --> val : "..val;
        -- elseif typevar == "table" then
        --         for k, v in pairs(val) do
        --                 if type(v) == "string" then
        --                         -- ans[#ans] = ans[#ans].." --> val : "..v;
        --                 end;
        --         end
        -- else
        --         ans[#ans] = ans[#ans].." --> val : "..val;
        -- end;
    end;
    cursor = t[1];
until cursor == "0";
return ans;