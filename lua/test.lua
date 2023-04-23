local ans, has, cursor = {}, {}, "0";

repeat
    local t = redis.call("SCAN", cursor, "MATCH", "defaultTenantId:"..ARGV[1]..":*", "COUNT", 1000000000);
    local list = t[2];
    for i = 1, #list do
        local s = list[i];
        local val = redis.call("GET",s);
        if has[s] == nil then has[s] = 1; ans[#ans + 1] = s.." --> "..val; end;
    end;
    cursor = t[1];
until cursor == "0";
return ans;