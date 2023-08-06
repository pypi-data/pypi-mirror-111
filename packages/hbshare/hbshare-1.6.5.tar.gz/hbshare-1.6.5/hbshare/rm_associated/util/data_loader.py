#!/usr/bin/python
#coding:utf-8
import pandas as pd
import numpy as np
import datetime
import requests
import json
import hbshare as hbs
from sqlalchemy import create_engine
from hbshare.rm_associated.util.config import style_name, engine_params


class NavAttributionLoader:
    def __init__(self, fund_id, fund_type, start_date, end_date, factor_type, benchmark_id):
        self.fund_id = fund_id
        self.fund_type = fund_type
        self.start_date = start_date
        self.end_date = end_date
        self.factor_type = factor_type
        self.benchmark_id = benchmark_id
        self._init_api_params()

    def _init_api_params(self):
        self.url = 'http://fdc-query.intelnal.howbuy.com/query/data/commonapi?dataTrack=xxxxx'
        self.headers = {'Content-Type': 'application/json'}
        self.post_body = {"database": "readonly", "sql": None}

    def fetch_data_batch(self, sql_script):
        post_body = self.post_body.copy()
        post_body['sql'] = sql_script
        post_body["ifByPage"] = False
        res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
        n = res['pages']
        all_data = []
        for i in range(1, n + 1):
            post_body["ifByPage"] = True
            post_body['pageNum'] = i
            res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
            all_data.append(pd.DataFrame(res['data']))
        all_data = pd.concat(all_data)

        return all_data

    def _load_calendar(self):
        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            self.start_date, self.end_date)
        post_body = self.post_body
        post_body['sql'] = sql_script
        res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)
        df['month'] = df['calendarDate'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d').month)
        df['isQuarterEnd'] = np.where((df['isMonthEnd'] == 1) & (df['month'].isin([3, 6, 9, 12])), 1, 0)
        df['isQuarterEnd'] = df['isQuarterEnd'].astype(int)

        return df[['calendarDate', 'isOpen', 'isWeekEnd', 'isMonthEnd', 'isQuarterEnd']]

    def _load_fund_data(self):
        if self.fund_type == 'mutual':
            sql_script = "SELECT a.jjdm fund_id, b.jzrq tradeDate, b.hbcl accumulate_return from " \
                         "funddb.jjxx1 a, funddb.jjhb b where a.cpfl = '2' and a.jjdm = b.jjdm " \
                         "and a.jjzt not in ('3', 'c') " \
                         "and a.m_opt_type <> '03' and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                         "order by b.jzrq".format(self.fund_id, self.start_date, self.end_date)
            post_body = self.post_body
            post_body['sql'] = sql_script
            res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
            data = pd.DataFrame(res['data'])
            data['ADJ_NAV'] = 0.01 * data['ACCUMULATE_RETURN'] + 1
        else:
            sql_script = "SELECT a.jjdm fund_id, b.jzrq tradeDate, b.fqdwjz as adj_nav from " \
                         "fundapp.jjxx1 a, fundapp.smlj b where a.cpfl = '4' and a.jjdm = b.jjdm " \
                         "and a.jjzt not in ('3') " \
                         "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                         "order by b.jzrq".format(self.fund_id, self.start_date, self.end_date)
            post_body = self.post_body
            post_body['sql'] = sql_script
            res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
            data = pd.DataFrame(res['data'])

        data.rename(columns={"FUND_ID": "fund_id", "TRADEDATE": "tradeDate", "ADJ_NAV": "adj_nav"}, inplace=True)

        return data.set_index('tradeDate')['adj_nav']

    def _load_bond_index(self):
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE " \
                     "ZQDM = 'H11001' and JYRQ >= {} and JYRQ <= {}".format(self.start_date, self.end_date)
        post_body = self.post_body
        post_body['sql'] = sql_script
        res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
        data = pd.DataFrame(res['data'])
        data.rename(columns={"TCLOSE": "中证全债"}, inplace=True)

        return data.set_index('TRADEDATE')[['中证全债']]

    def _load_factor_data(self):
        factor_type = self.factor_type
        bond_index = self._load_bond_index()
        if factor_type == "style_allo":
            # index_names = ['大盘价值', '大盘成长', '中盘价值', '中盘成长', '小盘价值', '小盘成长']
            index_codes = ['399373', '399372', '399375', '399374', '399377', '399376']
            sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE " \
                         "ZQDM in ({}) and JYRQ >= {} and " \
                         "JYRQ <= {}".format(','.join("'{0}'".format(x) for x in index_codes),
                                             self.start_date, self.end_date)
            factor_data = self.fetch_data_batch(sql_script).rename(
                columns={"INDEXNAME": "factor_name", "TRADEDATE": "trade_date"})
            factor_data = pd.pivot_table(
                factor_data, index='trade_date', columns='factor_name', values='TCLOSE').sort_index()
            factor_data = pd.merge(factor_data, bond_index, left_index=True, right_index=True)
        elif factor_type == "style":
            sql_script = "SELECT * FROM factor_return where TRADE_DATE >= {} and TRADE_DATE <= {}".format(
                self.start_date, self.end_date)
            engine = create_engine(engine_params)
            factor_data = pd.read_sql(sql_script, engine)
            factor_data['trade_date'] = \
                factor_data['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
            factor_data = pd.pivot_table(
                factor_data, index='trade_date', columns='factor_name', values='factor_ret').sort_index()[style_name]
            factor_data = (1 + factor_data).cumprod()
            # sql_script = "SELECT * FROM st_ashare.r_st_barra_factor_return where " \
            #              "TRADE_DATE >= '{}' and TRADE_DATE <= '{}'".format(self.start_date, self.end_date)
            # res = hbs.db_data_query('alluser', sql_script, page_size=5000)
            # factor_data = pd.DataFrame(res['data'])
            # factor_data = pd.pivot_table(
            #     factor_data, index='trade_date', columns='factor_name', values='factor_ret').sort_index()[style_name]
            # factor_data = (1 + factor_data).cumprod()
        elif factor_type == "sector":  # TODO 目前先用临时数据库中的数据, 后续交由DB自动更新
            sql_script = "SELECT * FROM sector_return where TRADEDATE >= {} and TRADEDATE <= {}".format(
                self.start_date, self.end_date)
            engine = create_engine(engine_params)
            factor_data = pd.read_sql(sql_script, engine)
            factor_data['TRADEDATE'] = \
                factor_data['TRADEDATE'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
            factor_data.rename(columns={"TRADEDATE": "trade_date", "BIGFINANCE": "大金融",
                                        "CONSUMING": "消费", "CYCLE": "周期", "MANUFACTURE": "制造"}, inplace=True)
            factor_data = factor_data.set_index('trade_date').sort_index()
            del factor_data['id']
            factor_data = (1 + factor_data).cumprod()
            factor_data = pd.merge(factor_data, bond_index, left_index=True, right_index=True)
        else:
            factor_data = pd.DataFrame()

        return factor_data

    def _load_benchmark_data(self):
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format(self.benchmark_id, self.start_date, self.end_date)
        post_body = self.post_body
        post_body['sql'] = sql_script
        res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
        data = pd.DataFrame(res['data'])
        data.rename(columns={"TCLOSE": "benchmark"}, inplace=True)

        return data.set_index('TRADEDATE')[['benchmark']]

    def load(self):
        calendar_df = self._load_calendar()
        fund_adj_nav = self._load_fund_data()
        factor_data = self._load_factor_data()
        benchmark_series = self._load_benchmark_data()

        data = {"calendar_df": calendar_df,
                "fund_nav_series": fund_adj_nav,
                "factor_data": factor_data,
                "benchmark_series": benchmark_series}

        return data


class SectorIndexCalculatorLoader:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def load(self):
        start_dt = datetime.datetime.strptime(self.start_date, '%Y%m%d')
        pre_date = (start_dt - datetime.timedelta(days=30)).strftime('%Y%m%d')

        sql_script = "SELECT * FROM st_market.t_st_zs_hyzsdmdyb where fljb = {} and hyhfbz = 2".format('1')
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        data = pd.DataFrame(res['data']).rename(columns={"zsdm": "SYMBOL", "flmc": "INDEXSNAME"})
        map_dict = data.set_index('SYMBOL')['INDEXSNAME'].to_dict()
        industry_index = []
        for key, value in map_dict.items():
            sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE, LTSZ as NEG_MKV " \
                         "FROM funddb.ZSJY WHERE " \
                         "ZQDM = '{}' and JYRQ >= {} and " \
                         "JYRQ <= {}".format(key, pre_date, self.end_date)
            res = hbs.db_data_query('readonly', sql_script, page_size=5000)
            df = pd.DataFrame(res['data'])
            df['INDEXNAME'] = value
            industry_index.append(df)
        industry_index = pd.concat(industry_index)

        return industry_index
