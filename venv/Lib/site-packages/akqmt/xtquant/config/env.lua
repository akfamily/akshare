
g_minVersion = "2.0.1.600"
g_minMobileVersion = "1.0.0.0"
g_company = "睿智融科"
g_is_address_from_daemon = false
g_use_proxy_whole_quoter = 1
g_use_future_whole_quoter = 0
g_server_deploy_type = 0

g_defaultPorts = {
    xtdaemon="127.0.0.1:55000",
    xtservice="127.0.0.1:56000",
    xtindex="127.0.0.1:56001",
    xtmonitor="127.0.0.1:56002",
    xtwebservice="127.0.0.1:56003",
    xttraderservice="127.0.0.1:57000",
    xtquoter="127.0.0.1:59000",
    xtriskcontrol="127.0.0.1:60000",
    proxy="210.14.136.66:55300",
    proxy_backup="203.156.205.182:55300",
    xtcounter="127.0.0.1:61100",
    xtgateway="127.0.0.1:62100",
    xtsource="127.0.0.1:63000",
    xtitsmservice="127.0.0.1:63500",
    xttask="127.0.0.1:61000",
    xtquerybroker="127.0.0.1:65000",
    xtotp="127.0.0.1:64200",
    xtlogcenter="127.0.0.1:65100",
    xtctpservice="127.0.0.1:65200",
    xtapiservice="127.0.0.1:65300",
    xtclearservice="127.0.0.1:64100",
    xtdelegateservice="127.0.0.1:64300",
    xtalgoadapterservice="127.0.0.1:64500",
    xtmarket = "127.0.0.1:60100",
    xtfairplayservice="127.0.0.1:64600",
    xtnonstandardservice="127.0.0.1:64703",
    xtantisharefinancingservice = "127.0.0.1:64800",
    xtmysqlservice="127.0.0.1:64704",
    xtmobileservice="127.0.0.1:65400",
    xtmarketinfo="210.14.136.69:59500",
}

g_allPlatforms = {}
g_allBrokers = {}
g_fairPlayUnits = {}

g_ttservice_global_config = {
    m_maxClientCount=1,
    m_logCfg="ttservice.log4cxx",
    m_listenIP="0.0.0.0",
    m_nListenPort=56100,
    m_proxyIP="210.14.136.66",
    m_nProxyPort=55808,
    m_nWorkFlowPort=63000,
    m_workFlowIP="127.0.0.1",
    m_redisHost="127.0.0.1",
    m_redisPort=6379,
    m_nPortalThread=5,
    m_addrsPath="",
    m_nProductMaxPortfilio=100,
    m_debugAccounts="",
    m_nUseMd5=0,
}

g_future_quote_platforms = {
    {m_nId=20001, m_strName="CTP实盘", m_strAbbrName="sqsp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},    
    {m_nId=20002, m_strName="恒生实盘", m_strAbbrName="hssp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21018, m_strName="v8t实盘", m_strAbbrName="sqsp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},       
    {m_nId=21001, m_strName="CTP模拟", m_strAbbrName="gdmn", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21002, m_strName="恒生模拟", m_strAbbrName="hsmn", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21003, m_strName="v8t模拟", m_strAbbrName="gdmn", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=20000, m_strName="迅投高级行情", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21111, m_strName="资管实盘", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21112, m_strName="资管模拟", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=20013, m_strName="恒生实盘", m_strAbbrName="hshl", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21013, m_strName="恒生模拟", m_strAbbrName="hshl", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21015, m_strName="恒生大越", m_strAbbrName="hsdy", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21014, m_strName="恒生英大", m_strAbbrName="hsyd", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21017, m_strName="恒生金谷", m_strAbbrName="hsjg", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=21019, m_strName="恒生中原", m_strAbbrName="hszy", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=20015, m_strName="恒生大越实盘", m_strAbbrName="hsdysp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=20014, m_strName="恒生英大实盘", m_strAbbrName="hsydsp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=20017, m_strName="恒生金谷实盘", m_strAbbrName="hsjgsp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
    {m_nId=20019, m_strName="恒生中原实盘", m_strAbbrName="hszysp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=1,},
}

g_futureoption_quote_platforms = {
    {m_nId=70001, m_strName="CTP实盘", m_strAbbrName="sqsp", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=5,},     
    {m_nId=71001, m_strName="CTP模拟", m_strAbbrName="gdmn", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=5,},
    {m_nId=71111, m_strName="资管实盘", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=5,},
    {m_nId=71112, m_strName="资管模拟", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=5,},
}

g_stock_quote_platforms = {
    {m_nId=10000, m_strName="迅投高级行情", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=2,},
    {m_nId=1111, m_strName="资管实盘", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=2,},
    {m_nId=1112, m_strName="资管模拟", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=2,},
}

g_credit_quote_platforms = {
    {m_nId=10000, m_strName="迅投高级行情", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=3,},
}

g_stockoption_quote_platforms = {
    {m_nId=10001, m_strName="迅投高级行情", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=6,},
    {m_nId=1211, m_strName="资管实盘", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=6,},
    {m_nId=1212, m_strName="资管模拟", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=6,},
}

g_hgt_quote_platforms = {
    {m_nId=10003, m_strName="迅投高级行情", m_strAbbrName="hgtmn", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=7,},
    {m_nId=1411, m_strName="资管实盘", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=7,},
    {m_nId=1412, m_strName="资管模拟", m_strAbbrName="xtgj", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=7,},
}

g_new3board_quote_platforms = {
    {m_nId=10002, m_strName="迅投高级行情", m_strAbbrName="neeq", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=10,},
    {m_nId=1311, m_strName="资管实盘", m_strAbbrName="neeq", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=10,},
    {m_nId=1312, m_strName="资管模拟", m_strAbbrName="neeq", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=10,},
}

g_gold_quote_platforms = {
	{m_nId=31003, m_strName="迅投高级行情", m_strAbbrName="zxjtgold", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=4,},
    {m_nId=31111, m_strName="资管实盘", m_strAbbrName="zxjtgold", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=4,},
    {m_nId=31112, m_strName="资管模拟", m_strAbbrName="zxjtgold", m_strLogo="broker_logo_1", m_strBrokerTag="xtbroker", m_strQuoterTag="xtquoter", m_nType=4,},
}

g_future_order_limits = {
    {m_strProductID="IF", m_nLimit=200},
    {m_strProductID="AU", m_nLimit=100},
}

g_banks = {
    {m_strLogo="bank_logo_1", m_strId="1", m_strName="工商银行",},
    {m_strLogo="bank_logo_2", m_strId="2", m_strName="农业银行",},
    {m_strLogo="bank_logo_3", m_strId="3", m_strName="中国银行",},
    {m_strLogo="bank_logo_4", m_strId="4", m_strName="建设银行",},
    {m_strLogo="bank_logo_5", m_strId="5", m_strName="交通银行",},
    {m_strLogo="bank_logo_6", m_strId="6", m_strName="深圳建行",},
    {m_strLogo="bank_logo_Z", m_strId="Z", m_strName="其它银行",}
}  

g_batchOrder_config = {
    -- 是否采用批量下单, 0 表示 不使用
    is_batch_ordinaryOrder = 1,
    -- 如果 采用批量下单，设置多少毫秒发送一次缓冲数据
    buffer_clear_duration_milli_sec = 100,
    buffer_clear_max_order_num = 100,
    -- apiserver 单位时间内的 下单量
    api_order_upper_limit = 1000,
    -- 如果设置了 下单量上限，设置多少毫秒达到这个上限才打回请求
    api_order_duration_milli_sec = 1000,
    -- 设置算法单最小下单间隔 为 0.5s
    api_min_algorithm_order_duration_milli_sec = 500,
    -- 设置组合单最小下单间隔为 10s
    api_min_group_order_duration_milli_sec = 10000,
    max_order_duration_milli_sec = -1,
    max_order_count = -1,
}
