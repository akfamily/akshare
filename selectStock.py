import time
import akshare as ak
import pandas as pd

## A 股上市公司的实时行情数据
stock_zh_a_spot_df = ak.stock_zh_a_spot()
#print(stock_zh_a_spot_df)
##取前300测试
##取前300测试
df_stock = stock_zh_a_spot_df[['代码','名称']][:20]
anyData = {'stock':'00','name':'name_test','指标1':'var1','指标1':'var1','指标2':'var2','指标3':'var3','指标4':'var4','综合评估':'varAll'}
dfResult = pd.DataFrame(anyData,index=[0])
 
for row_index, row in df_stock.iterrows():
    try:
    # print(row['code'])
    # print(row['name'])
        r_code = row['代码'][2:]
        r_name = row['名称']
 
        print(r_code)
        ##指标1 - 过去5年来平均净资产收益率高于14%
        df = ak.stock_financial_analysis_indicator(r_code)# 财务指标数据 工行财报
        # print(df.head())
        df = df.set_index(df['日期'])
        print(df.head())
        df1 = df[df.index>'2015-01-01']['净资产收益率(%)']
        df1_sum = df1.replace('--',0).astype(float).sum(axis = 0, skipna = True)
        df1_count = df1.count()
        var1 = (df1_sum / df1_count)>14
 
        ##指标2- 市盈率低于30 并且大于 0 
        day = (datetime.datetime.now()- datetime.timedelta(days=30))
        dateStart = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)##过去30天的数据
        dateStart = datetime.datetime.strptime(str(dateStart),'%Y-%m-%d %H:%M:%S')
        dateStart = datetime.datetime.date(dateStart) 
        df2 = ak.stock_a_lg_indicator("601398")
        df2_mean = df2[df2.trade_date >dateStart ].pe.mean()
        var2 = df2_mean >0 and df2_mean < 30
 
 
        #指标3：经营现金流为正
 
        df3 = df#财务指标数据
        var3 = float( df3['每股经营性现金流(元)'].iat[1] ) > 0
        # print(var3)
 
        #指标4：新期的净利润大于前5年的净利润 取万元
 
        var4_1 = float(df3['扣除非经常性损益后的净利润(元)'].iat[1])/ 10000 
        var4_2 =  df3['扣除非经常性损益后的净利润(元)'].iloc[2:8].astype(np.float).max()/10000 
 
        var4 = var4_1 > var4_2
 
        ##综合评估
 
        varAll = var1 and var2 and var3 and var4
        if varAll == True:
            print(row)
        anyData = {'stock':r_code,'name':r_name,'指标1':var1,'指标1':var1,'指标2':var2,'指标3':var3,'指标4':var4,'综合评估':varAll}
        df_idex = row_index+1
        dfResult.loc[df_idex] = anyData
        print(dfResult)
    except:
        continue
    #time.sleep(7)