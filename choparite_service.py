"""
Copyright (C) 2023. YangSohee all rights reserved.
Author: Yang Sohee <ssoyapdev@gmail.com>

Choparite 서비스 (service)
"""
import pandas as pd

import re
import os
import datetime
from datetime import time

from chopari import Chopari


def get_headers(length, start_idx=0):
    alpabet = [ chr(i) for i in range(ord('A'), ord('Z')+1)]
    headers = []

    for idx in range(-1, 5):
        if idx < 0:
            names = alpabet
        else:
            names = [alpabet[idx] + a for a in alpabet]

        if length <= len(names):
            headers.extend(names[ :length])
            break
        else:
            headers.extend(names)
            length = length - len(names)
    headers[0+start_idx] = "Date"
    headers[1+start_idx] = "Time"
    if start_idx > 0:
        headers[0] = "Kayoung"
    return headers


class ChopariteService:
    def __init__(self, start_time="22:01:00", end_time="10:00:00"):
        self.data_by_date = {}
        self.start_time = time.fromisoformat(start_time)
        self.end_time = time.fromisoformat(end_time)

        # [{ "0000-00-00": [{"C": 10}, {"D": 21}, ...}, ...]
        self.d_total_sleep_time = {}
        self.d_sleep_count = {}
        self.d_max_sleep_time = {}
        self.d_first_sleep_at = {}

        self.logger = None

    def set_logger(self, logger):
        self.logger = logger

    def log(self, msg):
        if self.logger:
            self.logger(str(msg))
        print(msg)

    def get_real_date(self, _date, _time, idx):
        try:
            assert isinstance(_date, datetime.date)
            assert isinstance(_time, datetime.time)

            real_date = "skip"
            if _time >= self.start_time:
                real_date = _date
            elif _time <= self.end_time:
                real_date = _date - datetime.timedelta(days=1)
            return real_date
        except AssertionError as e:
            self.log(f"{idx+1}행 날짜/시간 오류 ({_date}/{_time}). SKIP")
            return "skip"
        except Exception as e:
            self.log(f"{idx+1}행 날짜/시간 오류 ({_date}/{_time}). TERMINATE")
            raise

    def init_filename(self, filename):
        p = re.search(r"\/(?P<name>.*)[.].*$", filename)
        self.filename = p.group()

    def load_data(self, filename, start_idx=1):
        self.log("START load data...")
        self.init_filename(filename)
        df = pd.read_excel(filename, header=None)
        header = get_headers(df.shape[1], start_idx)
        df.columns = header
        self.init_data(header[2+start_idx:])

        # make group tag
        df["group"] = [ self.get_real_date(row['Date'], row['Time'], idx) for idx, row in df.iterrows() ]

        groups = df.groupby(df["group"])
        for g in groups.groups.keys():
            if g != "skip":
                self.data_by_date[g] = groups.get_group(g)
        self.log("END load data.")
        return self.filename

    def init_data(self, _names):
        self.d_total_sleep_time = {_name: {} for _name in _names}
        self.d_sleep_count = {_name: {} for _name in _names}
        self.d_max_sleep_time = {_name: {} for _name in _names}
        self.d_first_sleep_at = {_name: {} for _name in _names}

    def update_data(self, _name, _date, _chopari):
        _date = str(_date.date())
        self.d_total_sleep_time[_name][_date] = _chopari.total_sleep_time
        self.d_sleep_count[_name][_date] = _chopari.sleep_count
        self.d_max_sleep_time[_name][_date] = _chopari.max_sleep_time
        self.d_first_sleep_at[_name][_date] = _chopari.first_sleep_at

    def check_sleep(self):
        self.log("START check_sleep...")
        for date, data in self.data_by_date.items():
            self.log(f"{date.date()} 의 초파리 수면을 분석합니다...")

            for c in data.columns:
                if c in ["Kayoung", "Date", "Time", "group"]:
                    continue

                chopari = Chopari(c, data[c])
                chopari.check_sleep()

                self.update_data(c, date, chopari)
                self.log(chopari)
        self.log("END check_sleep...")
        return True

    def make_filename(self):
        return f"{self.filename.split('.')[0]}_{datetime.datetime.now().date()}.xlsx"

    def save_to_excel(self, output_filename=None):
        if not output_filename:
            output_filename = self.make_filename()

        self.log(f"분석 결과를 {output_filename} 으로 저장합니다...")
        mode = "w+"
        with pd.ExcelWriter(output_filename, mode=mode) as writer:
            for _type in ["total_sleep_time", "sleep_count", "max_sleep_time", "first_sleep_at"]:
                self.log(f"{_type} 저장중...")
                _data = getattr(self, f"d_{_type}")
                df = pd.DataFrame.from_dict(_data)
                df.to_excel(writer, sheet_name=_type)

        self.log(f"저장 완료")
        return output_filename