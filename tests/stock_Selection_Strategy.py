import akshare as ak
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

def check_revenue_decline(code):
    """��鼾����������3�λ����»�������»���-10%"""
    try:
        # ��ȡ��������ݣ���ҳ7�ӿڣ�
        df = ak.stock_financial_benefit_ths(symbol=code)
        df = df[['��������', 'Ӫҵ����']].sort_values('��������', ascending=False)
        
        # ���㼾�Ȼ���������
        df['QoQ'] = df['Ӫҵ����'].pct_change(periods=-1) * 100  # �ϼ��ȵĻ���
        recent_qoq = df['QoQ'].head(3).tolist()
        
        # ������֤����ҳ7��������߼���
        if len(recent_qoq) <3: return False
        if all(x <0 for x in recent_qoq):  # ����3���»�
            annual_decline = np.mean(recent_qoq)  # ����»���
            return annual_decline <= -10
        return False
    except:
        return False

def check_pe_percentile(code):
    """��鵱ǰPE����5����ʷ20%��λ����"""
    try:
        # ��ȡ��ʷPE���ݣ���ҳ6������
        df = ak.stock_financial_analysis_indicator(symbol=code)
        df = df[['����', '��ӯ��(PE)']].dropna()
        df['����'] = pd.to_datetime(df['����'])
        df = df[df['����'] >= pd.Timestamp.now() - pd.DateOffset(years=5)]
        
        if len(df) < 4: return False  # ���ݲ���
        current_pe = df.iloc[0]['��ӯ��(PE)']
        percentile_20 = np.percentile(df['��ӯ��(PE)'].values, 20)
        return current_pe <= percentile_20
    except:
        return False

def get_industry_metrics(code):
    """��ȡ��ҵ3��PE/PB/PS/PC��λ��"""
    try:
        # ��ȡ��ҵ���ࣨ��ҳ3������ҵ��
        industry_df = ak.sw_index_spot()
        industry_code = industry_df[industry_df['�ɷֹɴ���'].str.contains(code)]['ָ������'].values[0]
        
        # ��ȡ��ҵ�ɷֹɣ���ҳ3������
        industry_stocks = ak.sw_index_cons(index_code=industry_code)['�ɷֹɴ���'].tolist()
        
        # �ռ���ҵָ�꣨��ҳ9��ֵ������
        metrics = []
        for stock in tqdm(industry_stocks, desc="��ҵ���ݲɼ�"):
            try:
                # ��ȡPE/PB/PS/PC��������=��ֵ/��Ӫ�ֽ�����
                df = ak.stock_financial_analysis_indicator(symbol=stock)
                cash_flow = ak.stock_financial_cash_ths(symbol=stock)['��Ӫ��������ֽ���������'].iloc[0]
                market_cap = ak.stock_zh_a_spot_em(symbol=stock)['����ֵ'].iloc[0]
                
                metrics.append({
                    'PE': df['��ӯ��(PE)'].iloc[0],
                    'PB': df['�о���(PB)'].iloc[0],
                    'PS': df['������(PS)'].iloc[0],
                    'PC': market_cap / cash_flow if cash_flow !=0 else np.nan
                })
            except: continue
        
        # ����30%��λ����ҳ10��ֵ�߼���
        df_metrics = pd.DataFrame(metrics).dropna()
        return df_metrics.quantile(0.3)
    except:
        return None

