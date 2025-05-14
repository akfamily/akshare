local __config_helper_lua_path = debug.getinfo(1, "S").source:sub(2)
local __config_helper_lua_dir = __config_helper_lua_path:match("(.-)[\\/][^\\/]-$") .. "/"
dofile(__config_helper_lua_dir .. "table2json.lua")

-- lua文件使用%作为分隔符
-- ini文件使用&作为分隔符
local function eval(str)
    if type(str) == "string" then
        if #str > 0 then 
            return loadstring("return " .. str)()        
        end
    elseif type(str) == "number" then
        return loadstring("return " .. tostring(str))()
    else
        error("is not a string")
    end
end

local function split(str,sep)
        local ret={}
        local n=1
        for w in str:gmatch("([^" .. sep .. "]*)") do
            ret[n]=ret[n] or w -- only set once (so the blank after a string is ignored)
            if w=="" then n=n+1 end -- step forwards on a blank but not a string
        end
        return ret
end

function tableMerge(t1, t2)
    for k,v in pairs(t2) do
        if type(v) == "table" then
            if type(t1[k] or false) == "table" then
                tableMerge(t1[k] or {}, t2[k] or {})
            else
                t1[k] = v
            end
        else
            t1[k] = v
        end
    end
    return t1
end

local function genMap(key, value)
    local m = {}
    local items = split(key, "%.")
    local d = nil
    for i = 0, (#items -1) do
        local str = items[#items - i]
        if i == 0 then
            d = {}
            d[str] = eval(value)
        else
            local raw = d
            d = {}
            d[str] = raw                
        end
    end
    for k, v in pairs(d) do
        m[k] = v
    end
    return m
end

function parse(param, localMap)
    local ret = param
    for w in string.gmatch(param, "{{([^}]*)}}") do         
        local v = localMap[w]
        if v == nil then v = eval(w) end
        if v ~= nil then
            ret = string.gsub(ret, "{{" .. w .. "}}", v)
        end
    end
    return ret
end

local function getLocalFileMap(filePath)
    local ret = {}
    local file = io.open(__config_helper_lua_dir..filePath, "r")
    if file ~= nil then 
        local content = file:read("*a")
        local loadRet = loadstring(content)
        if loadRet == nil then
            loadRet = loadstring("return " .. content)
        end
        if loadRet ~= nil then
            ret = loadRet()
        end
    end
    return ret
end

local function getLocalMap()    
    m1 = getLocalFileMap("../config_local/customer.lua")
    m2 = getLocalFileMap("../config_local/machine.lua")
    return tableMerge(m1, m2)
end

function mergeLocal()
    local m = getLocalMap()
    local g_localMap = {}
    local g_globalMap = {}
    for k, v in pairs(m) do
        local r1, r2 = k:find("g_")
        if r1 == 1 then
            g_globalMap[k] = v
        else
            g_localMap[k] = v
        end
    end
    
    _G = tableMerge(_G, g_globalMap)    
    _G["g_localMap"] = g_localMap
    
end

function toIni(map)
    local ret = ""
    for key, value in pairs(map) do
        str = "[" .. key .. "]\n"
        for itemKey, itemValue in pairs(value) do
            if type(itemValue) == type("") then
                if itemValue:len() > 0 then
                    str = str .. itemKey .. "=" .. itemValue .. "\n"
                end
            elseif type(itemValue) == type(true) then
                local v = 1
                if itemValue then v = 1 else v = 0 end
                str = str .. itemKey .. "=" .. v .. "\n"
            else
                str = str .. itemKey .. "=" .. itemValue .. "\n"
            end
        end
        ret = ret .. str .. "\n"
    end 
    return ret
end

function getClientMap(tag)
    local CLINET_CONFIG = {
        tagTemplate = "",  --标签模版, 可以做正则匹配
        address = "127.0.0.1:80", -- 地址
        isGetdAddressFromNameServer = g_is_address_from_daemon, -- 是否从NameServer取得地址
        isUsedAloneIO = 0, -- 是否单独使用一个ioservice
        timeoutSecond = 600, -- 超时检测时间
        keepAliveCheckSecond = 5, -- 保活包
        reconnectSecond = 3, -- 断线重连时间间隔
        requestTimeoutSecond = 600, -- 请求超时时间
        isUseSSL = 0, --是否使用SSL            
        sslCaPath = "", -- SSL证书地址
        proxyType = "0", -- 代理类型， 0表示无， 1表示http， 2表示socket4， 3表示socket5
        proxyIp = "", -- 代理地址
        proxyPort = 80, -- 代理端口
        proxyNeedCheck = 0, -- 是否需要验证
        proxyUserName = "", -- 代理用户名
        proxyPassword = "", -- 代理密码
        packageDir = "", -- 存放网络包目录
    }
    local tagKey = "client_" .. tag
    local ret = {
        [tagKey] = CLINET_CONFIG
    }
    local address = g_defaultPorts[tag]
    if address == nil then address = "127.0.0.1:8000" end
    local m = {
        [tagKey] = {
            tagTemplate = tag,
            address = g_defaultPorts[tag]
        }
    }
    ret = tableMerge(ret, m)
    return ret
end


function getServerMap(tag)
    local SERVER_CONFIG = {
        tag = "",     -- 标签模版, 可以做正则匹配
        address = "0.0.0.0:80",         -- 地址
        isGetdAddressFromNameServer = 0,-- 是否从NameServer取得地址
        timeoutSecond = 600,              -- 超时检测时间
        maxConnectionNum = 1000000,           -- 最大连接数
        isAutoBind = g_is_address_from_daemon,                -- 是否自动绑定(即端口无法监听, 监听下一端口)
        isUseSSL = 0,                  -- 是否启用SSL
        crtPath = "",
        serverKeyPath = "",
        tempDhPath = "",
        sslPassword = "",
        packageDir = "", 
    }
    local port = 80    
    local address = g_defaultPorts[tag]
    if address ~= nil then 
        port = string.sub(address, string.find(address, ":") +1 ,#address)
    end
    
    local ret = {
        ["server_" .. tag] = SERVER_CONFIG
    }
    local m = {
        ["server_" .. tag] = {
            tag = tag,
            address = "0.0.0.0:" .. port,           
        }
    }    
    ret = tableMerge(ret, m)    
    ret["server"] = ret["server_" .. tag]
    return ret
end

function getLocalAppMap(tag)
    local ret = {
        app = {
            appName = tag,
            netThreadNum = 1,   -- 线程数
            dispatcherThreadNum = 1, -- 处理线程数            
            logPath = "", -- 日志文件路径
            reportSeconds = 60, -- 状态报告时间
            isReportLogCenter = 1 and g_is_report_logcenter or 0, -- 是否日志打印到logCenter
            serverDeployType = g_server_deploy_type, -- 部署类型
            host_ip = g_host_ip, -- 主机IP
            zkRunningDir = g_running_dir, -- 运行目录
            topology = 1 and g_is_topology_logcenter or 0, --是否发送拓扑数据
            topologyInterval = 20,   --发送拓扑数据时间间隔
        },
        client_NameService = {
            tagTemplate = "NameService",
            address = g_defaultPorts["xtdaemon"],
            reconnectSecond = 3,
        },
    quoter_config = {
            is_use_proxy_all_push = g_use_proxy_whole_quoter,
        is_use_future_all_push = g_use_future_whole_quoter,
        timeoutsec = 20,
        },
    }
    return ret
end

function getAppMap(serverTag, clients)
    local ret = getLocalAppMap(serverTag)
    if serverTag ~= nil then        
        local serverMap = getServerMap(serverTag)
        ret = tableMerge(ret, serverMap)
    end
    if clients ~= nil then
        for	i, v in pairs(clients) do
            local map = getClientMap(v)
            ret = tableMerge(ret, map)
        end
    end
    return ret
end

function getLog4cxx(tag)
    local d = [[
log4j.logger.TTStdFile=INFO,fa
log4j.logger.TTDbgFile=DEBUG,fa2

# 文件输出
log4j.appender.fa=org.apache.log4j.DailyRollingFileAppender
log4j.appender.fa.MaxFileSize=500MB
log4j.appender.fa.datePattern='.'yyyy-MM-dd
log4j.appender.fa.File=../userdata/log/{{tag}}.log
log4j.appender.fa.Append=true
log4j.appender.fa.layout=org.apache.log4j.PatternLayout
log4j.appender.fa.layout.ConversionPattern=%d [%p] [%t] %m%n

# 文件输出2
log4j.appender.fa2=org.apache.log4j.FileAppender
log4j.appender.fa2.MaxFileSize=500MB 
log4j.appender.fa2.MaxBackupIndex=10
log4j.appender.fa2.File=../userdata/log/{{tag}}_debug.log
log4j.appender.fa2.Append=true
log4j.appender.fa2.layout=org.apache.log4j.PatternLayout
log4j.appender.fa2.layout.ConversionPattern=%d [%p] [%t] %m%n

# 控制台输出
log4j.appender.ca=org.apache.log4j.ConsoleAppender
log4j.appender.ca.layout=org.apache.log4j.PatternLayout
log4j.appender.ca.layout.ConversionPattern=%d [%p] [%t] %m%n
]]
    d = parse(d, {["tag"] = tag})
    return d
end

local function getTableDepth(t, depth)    
    if type(t) == "table" then    
        depth = depth + 1      
        local maxDepth = depth
        for k, v in pairs(t) do
            if type(v) == "table" then 
                local d = getTableDepth(v, depth)
                if d > maxDepth then maxDepth = d end
            end
        end
        depth = maxDepth
    end
    return depth
end

-- 根据App名称取配置
local function getConfigTableByAppName(param, m)
    if m == nil then m = {} end
    if type(m) ~= "table" then
        m = {m}
    end
    local paramObj = _G[param]
    if paramObj == nil then
        local file = io.open(__config_helper_lua_dir .. param .. ".lua", "r")
        if file ~= nil then 
            local content = file:read("*a")
            if content ~= nil then       
                local loadRet = loadstring(content)
                if loadRet == nil then
                    loadRet = loadstring("return " .. content)
                end
                if loadRet ~= nil then
                    paramObj = loadRet()
                    _G[param] = paramObj
                end
            end
        end
    end
    if paramObj ==  nil then paramObj = {}  end 
    local t = {}
    if type(paramObj) == "function" then
        t = paramObj(unpack(m))
    elseif type(paramObj) == "table" then
        t = paramObj
    end
                  
    -- 合并本地数据
    local localMap = {}
    if g_localMap ~= nil then
        localMap = g_localMap[param]
    end
    if localMap == nil then localMap = {} end    
    t = tableMerge(t, localMap)
    return t
end

-- 根据App名称取配置
function getConfigByAppName(param, m)
    local t = getConfigTableByAppName(param, m)
    local depth = getTableDepth(t, 0)
    if depth == 2 then 
        return toIni(t)
    else
        return table2json(t)
    end
end

function getModulesHelper()
    return getLocalFileMap("../config_local/modules.lua")
end

-- 取Broker模块配置
function getBrokerModuleConfig(configTag, moduleTag)
    local t = getConfigTableByAppName(configTag)
    if moduleTag ~= nil then
        local tag = moduleTag
        local index = moduleTag:find("_")
        if index ~= nil then
            tag = moduleTag:sub(moduleTag:find("_", index+1) + 1)
        end        
        tag = configTag .. "/" .. tag
        local t1 = getConfigTableByAppName(tag)
        t = tableMerge(t, t1)
    end
    local depth = getTableDepth(t, 0)
    if depth == 2 then 
        return toIni(t)
    else
        return table2json(t)
    end
end

function getPlatform(tag)    
    for k, v in pairs(g_allPlatforms) do 
        local tTag = v["m_nType"] .. "_" .. v["m_nId"] .. "_" .. v["m_brokerId"]
        local r1, r2 = tag:find(tTag)
        if r1 == 1 then        
            return v
        end
    end
    return nil
end

local function genPlatformInfos()
    local allTypes = {g_future_platforms, g_stock_platforms, g_credit_platforms, g_stockoption_platforms, g_new3board_platforms, g_hgt_platforms, g_gold_platforms}
    for tk, tv in pairs(allTypes) do
        for k, v in pairs(tv) do
            table.insert(g_allPlatforms, v)
        end
    end
end

function genBrokerInfos()
    local key = "xtbroker_1_21001_9999"
    local ret = {}
    ret[key] = "127.0.0.1:" .. (58000 + 3)
    
    return ret
end

-- 参数:待分割的字符串,分割字符
-- 返回:子串表.(含有空串)
function lua_string_split(str, split_char)    
    local sub_str_tab = {};
    
    while (true) do        
        local pos = string.find(str, split_char);  
        if (not pos) then            
            local size_t = table.getn(sub_str_tab)
            table.insert(sub_str_tab,size_t+1,str);
            break;  
        end
        
        local sub_str = string.sub(str, 1, pos - 1);
        local size_t = table.getn(sub_str_tab);
        table.insert(sub_str_tab,size_t+1,sub_str);
        local t = string.len(str);
        str = string.sub(str, pos + 1, t);   
    end    
    return sub_str_tab;
end

function do_checkVersion(version, minVersion)
    local tableVersion = lua_string_split(version, "%.")
    local tempMinVersion = minVersion
    local tableGMinVersion = lua_string_split(tempMinVersion , "%.")
    local ret = false
    local tablesize = 0
    local isVShort = false
    if table.getn(tableVersion) < table.getn(tableGMinVersion) then
        isVShort = true
        tablesize = table.getn(tableVersion)
    else
        tablesize = table.getn(tableGMinVersion)
    end

    for i = 1, tablesize , 1 do
        tableVersion[i] = tonumber(tableVersion[i])
        tableGMinVersion[i] = tonumber(tableGMinVersion[i])
        if tableVersion[i] < tableGMinVersion[i] then
            ret = true
            return ret        
        elseif tableVersion[i] > tableGMinVersion[i] then 
            return ret            
        end
    end
    
    if isVShort then
        ret = true
    end

    return ret
end
    
function checkVersion(version)
    local ret = do_checkVersion(version, g_minVersion)
    local msg = ""
    if ret then
        msg = "您的客户端版本过低, 请联系" .. g_company .."获取最新版本!"
    end
    return msg
end

function checkMobileVersion(version)
    local ret = do_checkVersion(version, g_minMobileVersion)
    local msg = ""
    if ret then
        msg = "您的移动客户端版本过低, 请联系" .. g_company .."获取最新版本!"
    end
    return msg
end

-- 取地址Ip
function getIp(address)
    local ip = address:sub(1, address:find(":") - 1)
    return ip
end

-- 取地址端口
function getPort(address)
    local port = address:sub(address:find(":") + 1, address:len())
    return port
end

function  genFairyPlayUnitInfos()
    if g_fairplay_units == nil then return end
    for k, v in pairs(g_fairplay_units) do
        table.insert(g_fairPlayUnits, v)
    end
end

function getFairPlayUnit(tag)
    for k, v in pairs(g_fairPlayUnits) do
        local tTag = v["m_nType"] .. "_" .. v["m_nId"]
        local r1, r2 = tag:find(tTag)
        if r1 == 1 then
            return v
        end
    end
    return nil
end

function mergeBrokerInfos(brokerPorts)    
    if g_allBrokers == nil then
        g_allBrokers = {}
    end
    
    for k, v in pairs(brokerPorts) do
        if g_defaultPorts[k] == nil then
            g_defaultPorts[k] = v
        end
        table.insert(g_allBrokers, k)
    end    
end

-- 合并本地数据
mergeLocal()

if not g_is_address_from_daemon then 
    -- 产生平台信息
    genPlatformInfos()

    -- 产生券商信息
    if g_brokerPorts == nil then
        g_brokerPorts = genBrokerInfos()
    end    
    mergeBrokerInfos(g_brokerPorts)    

    --产生公平交易单元信息
    genFairyPlayUnitInfos()
end

function getExtraThreadPools(key)
    local threadNum = g_extra_thread_pools[key]
    if threadNum ~= nil then 
        return threadNum
    end
    return 0
end
