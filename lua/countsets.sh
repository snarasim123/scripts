./redis-cli -h {elasticachehost} -a {password} -c --tls --eval  /work/countsets.lua , defaultTenantId:*:tid:*:statusDecoratorsCache:set:* 1000
