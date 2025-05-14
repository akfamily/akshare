local __config_lua_path = debug.getinfo(1, "S").source:sub(2)
local __config_lua_dir = __config_lua_path:match("(.-)[\\/][^\\/]-$") .. "/"
local function testDofile(path)
    local abs_path = __config_lua_dir .. path
    local file = io.open(abs_path, "r")
    if file ~= nil then 
        dofile(abs_path)
        return true
    else
        return false
    end
end

g_is_address_from_daemon = 0
g_is_server = true
g_is_report_logcenter = false
g_system_tag = ""
g_is_topology_logcenter = false

g_ftCategory = {
    ["2101"]="ag",
    ["2102"]="al",
    ["2103"]="au",
    ["2104"]="bu",
    ["2105"]="cu",
    ["2106"]="fu",
    ["2107"]="hc",
    ["2108"]="pb",
    ["2109"]="rb",
    ["2110"]="ru",
    ["2111"]="wr",
    ["2112"]="zn",
    ["2113"]="ni",
    ["2114"]="sn",
    
    ["2151"]="IF",
    ["2152"]="T",
    ["2153"]="TF",
    ["2154"]="IC",
    ["2155"]="IH",
    
    ["2201"]="SP a&a",
    ["2202"]="SP b&b",
    ["2203"]="SP bb&bb",
    ["2204"]="SP c&c",
    ["2205"]="SP cs&cs",
    ["2206"]="SP fb&fb",
    ["2207"]="SP i&i",
    ["2208"]="SP j&j",
    ["2209"]="SP jd&jd",
    ["2210"]="SP jm&jm",
    ["2211"]="SP l&l",
    ["2212"]="SP m&m",
    ["2213"]="SP p&p",
    ["2214"]="SP pp&pp",
    ["2215"]="SP v&v",
    ["2216"]="SP y&y",
    ["2217"]="SPC a&m",
    ["2218"]="SPC c&cs",
    ["2219"]="SPC fb&bb",
    ["2220"]="SPC i&j",
    ["2221"]="SPC i&jm",
    ["2222"]="SPC j&jm",
    ["2223"]="SPC l&pp",
    ["2224"]="SPC l&v",
    ["2225"]="SPC v&pp",
    ["2226"]="SPC y&p",
    ["2227"]="a",
    ["2228"]="b",
    ["2229"]="bb",
    ["2230"]="c",
    ["2231"]="cs",
    ["2232"]="fb",
    ["2233"]="i",
    ["2234"]="j",
    ["2235"]="jd",
    ["2236"]="jm",
    ["2237"]="l",
    ["2238"]="m",
    ["2239"]="p",
    ["2240"]="pp",
    ["2241"]="v",
    ["2242"]="y",

    ["2251"]="CF",
    ["2252"]="FG",
    ["2253"]="IPS SF&SM",
    ["2254"]="JR",
    ["2255"]="LR",
    ["2256"]="MA",
    ["2257"]="ME",
    ["2258"]="OI",
    ["2259"]="PM",
    ["2260"]="RI",
    ["2261"]="RM",
    ["2262"]="RS",
    ["2263"]="SF",
    ["2264"]="SM",
    ["2265"]="SPD CF&CF",
    ["2266"]="SPD FG&FG",
    ["2267"]="SPD JR&JR",
    ["2268"]="SPD LR&LR",
    ["2269"]="SPD MA&MA",
    ["2270"]="SPD ME&ME",
    ["2271"]="SPD OI&OI",
    ["2272"]="SPD PM&PM",
    ["2273"]="SPD RI&RI",
    ["2274"]="SPD RM&RM",
    ["2275"]="SPD RS&RS",
    ["2276"]="SPD SF&SF",
    ["2277"]="SPD SM&SM",
    ["2278"]="SPD SR&SR",
    ["2279"]="SPD TA&TA",
    ["2280"]="SPD TC&TC",
    ["2281"]="SPD WH&WH",
    ["2282"]="SR",
    ["2283"]="TA",
    ["2284"]="TC",
    ["2285"]="WH"
}

testDofile("../config/platform.lua")
testDofile("../config/serverEnv.lua")
if testDofile("../config/clientEnv.lua") or testDofile("../config/itsmClientEnv.lua") then g_is_server = false end
testDofile("../config/env.lua")
testDofile("../config/xtdaemon.lua")
testDofile("../config/clientEnv.lua")
testDofile("../config/itsmClientEnv.lua")
testDofile("../config/serverEnv.lua")
testDofile("../config/fairplaytables.lua")
testDofile("../config/configHelper.lua")
testDofile("../config/xtstocktype.lua")

function getFutureOrderLimits()
    return table2json({content = g_future_order_limits})
end

function getFuturePlatforms()
	return table2json({content = g_future_platforms})
end

function getStockPlatforms()
	return table2json({content = g_stock_platforms})
end

function getCreditPlatforms()
	return table2json({content = g_credit_platforms})
end

function getHGTPlatforms()
	return table2json({content = g_hgt_platforms})
end

function getHGTQuotePlatforms()
	return table2json({content = g_hgt_quote_platforms})
end

function getFutureQuotePlatforms()
	return table2json({content = g_future_quote_platforms})
end

function getStockQuotePlatforms()
	return table2json({content = g_stock_quote_platforms})
end

function getStockOptionPlatforms()
	return table2json({content = g_stockoption_platforms})
end

function getStockOptionQuotePlatforms()
	return table2json({content = g_stockoption_quote_platforms})
end

function getNew3BoardPlatforms()
    return table2json({content = g_new3board_platforms})
end

function getNew3BoardQuotePlatforms()
    return table2json({content = g_new3board_quote_platforms})
end

function getGoldPlatforms()
    return table2json({content = g_gold_platforms})
end

function getGoldQuotePlatforms()
    return table2json({content = g_gold_quote_platforms})
end

function getBanks()
    return table2json({content = g_banks})
end

function getTTServiceGlobalConfig()
    return table2json(g_ttservice_global_config)
end

function getMysqlConfig()
    return table2json(g_mysql_config)
end

function getMysqlConfigWhiteListFlowControl()
    return table2json(g_mysql_config_white_list_flow_control)
end

function getRabbitMqConfig()
    return table2json(g_rabbitMq_config)
end

function getBatchOrderConfig()
    return table2json(g_batchOrder_config)
end

function getPlatformInfo()
	return getConfigByAppName("calcConfigEnv")
end

function getSystemTag()
    return g_system_tag
end

-- 获取股票分类
function getXtStockType()
    return toIni(g_stocktype_info)
end

function getBrokerAddressWithReInit(brokerType, platformId, brokerId, accountId, reInit)
    if reInit then print("true") else print("false") end
    local key = "xtbroker_" .. brokerType .. "_" .. platformId .. "_" ..brokerId
    local address = g_defaultPorts[key]
    if address == nil then
        key = "xtbroker_" .. brokerType .. "_" .. platformId
        address = g_defaultPorts[key]
        if address == nil then 
            key = "xtbroker_" .. brokerType
            address = g_defaultPorts[key]
            if address == nil then 
                key = "xtbroker"
                address = g_defaultPorts[key]
            end
        end
    end
    
    if address == nil then
        if reInit then  
            g_brokerPorts = genBrokerInfos()
            mergeBrokerInfos(g_brokerPorts)
            address = getBrokerAddressWithReInit(brokerType, platformId, brokerId, accountId, false)
        end
    end
    if address == nil then address = "" end
    return address
end

function getBrokerAddress(brokerType, platformId, brokerId, accountId)
    return getBrokerAddressWithReInit(brokerType, platformId, brokerId, accountId, true)
end

-- tag即platformId
function getBrokerConfig(tag)
    return getConfigByAppName("xtbroker", {tag})
end

function getSfitMdquoterConfig(tag)
    return getConfigByAppName("sfitMdquoter", {tag})
end

function getXtQuoterConfig()
    return getConfigByAppName("xtquoter")
end

-- 取TTService配置
function getXtServiceConfig()
    return getConfigByAppName("xtservice")
end

-- 取交易服务配置
function getXtTraderServiceConfig()
    return getConfigByAppName("xttraderservice")
end

-- 取风控服务配置
function getXtRiskControlConfig()
    return getConfigByAppName("xtriskcontrol")
end

-- 取MysqlService配置
function getXtMysqlServiceConfig()
    return getConfigByAppName("xtmysqlservice")
end

function getXtSourceConfig()
	return getConfigByAppName("xtsource")
end

function getXtTaskConfig(tag)
    return getConfigByAppName("xttask", {tag})
end

function getXtMobileServiceConfig()
    return getConfigByAppName("xtmobileservice")
end

function getParam(param)
    return table2json(_G[param])
end

function getXtClientConfig()
    return getConfigByAppName("xtclient")
end

function getXtMiniQmtConfig()
    return getConfigByAppName("xtminiqmt")
end

function getXtMiniQuoteConfig()
    return getConfigByAppName("xtminiquote")
end

function getXtQuantServiceConfig()
    return getConfigByAppName("xtquantservice")
end

function getXtItsmClientConfig()
    return getConfigByAppName("xtitsmclient")
end

function getXtItsmServiceConfig()
    return getConfigByAppName("xtitsmservice")
end

function getXtQueryBrokerConfig()
    return getConfigByAppName("xtquerybroker")
end

function getXtOtpConfig()
    return getConfigByAppName("xtotpservice")
end

function getXtLogCenterConfig()
    return getConfigByAppName("xtlogcenter")
end

function getCtpServiceConfig()
    return getConfigByAppName("xtctpservice")
end

function getXtApiServiceConfig()
    return getConfigByAppName("xtapiservice")
end

function getXtClearServiceConfig()
    return getConfigByAppName("xtclearservice")
end

function getDelegateServiceConfig()
    return getConfigByAppName("xtdelegateservice")
end

function getFtProduct()
    return table2json(g_ftCategory)
end

function getAlgoAdapterServiceConfig()
    return getConfigByAppName("xtalgoadapterservice")
end

function getXtFairPlayServiceConfig(tag)
    return getConfigByAppName("xtfairplayservice", {tag} )
end

function getXtNonStandardServiceConfig()
    return getConfigByAppName("xtnonstandardservice")
end

function getModules()
    modules = getModulesHelper()
    return table2json(modules["modules"])
end
--获取客服经理的信息
function getCustomerServiceConfig()
    return getConfigByAppName("customerservice")
end

function getBrokerProxy()
    return getConfigByAppName("xtbrokerproxy")
end

function getHttpUrlConfig()
    return getConfigByAppName("xthttpurlconfig")
end

--require "std"
--require "io"
local function main()       
    if arg == nil then
        return ""
    end
    
    if arg[1] ~= nil then
        local d = _G[ arg[1] ]
        if d ~= nil then
            if type(d) == "function" then
                local newArg = {}
                for i = 1, 100 do 
                    if arg[1 + i] ~= nil then
                        table.insert(newArg, arg[1 + i])
                    else
                        break
                    end
                end
                return d(unpack(newArg))
            elseif type(d) == "table" then                
                return table2json(d)
            end
        else
            local newArg = {}
            for i = 1, 100 do 
                if arg[1 + i] ~= nil then
                    table.insert(newArg, arg[1 + i])
                else
                    break
                end
            end                
            return getConfigByAppName(arg[1], newArg)
        end
    end
end

print(main())
--print(getXtClientConfig())
--[[
print(main())
print(getPlatform(""))
print("=====================")
print(getXtServiceConfig())
print("=====================")
print(getXTTraderServiceConfig())
print("=====================")
print(getXtQuoterConfig())
print("=====================")
print(getXtTaskConfig("xttask"))
print("=====================")
print(getBrokerConfig("1_21001_1001"))
--print(getConfigByAppName("sfit"))
]]
