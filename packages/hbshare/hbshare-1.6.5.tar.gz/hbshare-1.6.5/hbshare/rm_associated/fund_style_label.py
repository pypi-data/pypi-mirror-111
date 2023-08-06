"""
基金风格标签模块
"""
import pandas as pd

import hbshare as hbs


class FundStyleLabelCalculator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._load_data()

    @staticmethod
    def fetch_data_batch(user_name, sql_script):
        res = hbs.db_data_query(user_name, sql_script, is_pagination=False)
        n = res['pages']
        all_data = []
        for i in range(1, n + 1):
            res = hbs.db_data_query(user_name, sql_script, page_num=i, is_pagination=True)
            all_data.append(pd.DataFrame(res['data']))
        all_data = pd.concat(all_data)

        return all_data

    def _load_data(self):
        # mutual
        db_name = 'st_fund'
        user_name = 'funduser'
        sql_script = "SELECT * FROM {}.r_st_nav_attr_df where tjrq >= {} and tjrq <= {}".format(
            db_name, self.start_date, self.end_date)
        res = self.fetch_data_batch(user_name, sql_script)

        return res


if __name__ == '__main__':
    FundStyleLabelCalculator(start_date='20200131', end_date='20210629')