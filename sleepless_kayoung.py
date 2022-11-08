#!/usr/local/bin/python3

"""
Copyright (C) 2022. YangSohee all rights reserved.
Author: Yang Sohee <ssoyapdev@gmail.com>

가영이를 위한 초파리 수면시간 측정 프로그램
"""

import pandas as pd

import re
import os
import sys
import datetime
from datetime import time

def help():
    print("""
    1. 이 프로그램과 초파리 수면 엑셀 데이터를 같은 폴더에 넣는다.
    2. 이 프로그램을 실행한다.
    3. 초파리 수면 엑셀 데이터 (이후 원본이라 칭함) 의 이름을 입력한다.
    """)

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


class Chopari:
    MIN_TIME = 5
    def __init__(self, name, movement_data):
        self.name = name
        self.movement_data = list(movement_data)

        self.total_sleep_time = 0
        self.sleep_count = 0
        self.max_sleep_time = 0
        self.first_sleep_at = -1

    def __str__(self):
        return f"[초파리{self.name}] 총수면 {self.total_sleep_time}m, 수면횟수{self.sleep_count}회, 최대수면 {self.max_sleep_time}m 수면도입시간 {self.first_sleep_at}m"

    def incr_total_sleep_time(self, time):
        self.total_sleep_time += time

    def incr_sleep_count(self, n=1):
        self.sleep_count += n

    def update_max_sleep_time(self, time):
        self.max_sleep_time = max(self.max_sleep_time, time)

    def update_first_sleep_at(self, time):
        if self.first_sleep_at < 0:
            self.first_sleep_at = time

    def check_sleep(self):
        time = 0
        for movement in self.movement_data + [-1]:
            if movement == 0:
                time += 1
                continue

            if time >= self.MIN_TIME:
                self.incr_total_sleep_time(time)
                self.incr_sleep_count()
                self.update_max_sleep_time(time)
                self.update_first_sleep_at(time)
            time = 0
            #print(f"time: {time} | movement: {movement} | self.sleep_count {self.sleep_count} | self.total_sleep_time {self.total_sleep_time}")

class HappyMachine:

    def __init__(self, start_time="22:01:00", end_time="10:00:00"):
        self.data_by_date = {}
        self.start_time = time.fromisoformat(start_time)
        self.end_time = time.fromisoformat(end_time)

        # [{ "0000-00-00": [{"C": 10}, {"D": 21}, ...}, ...]
        self.d_total_sleep_time = {}
        self.d_sleep_count = {}
        self.d_max_sleep_time = {}
        self.d_first_sleep_at = {}

    def get_real_date(self, _date, _time, idx):
        try:
            real_date = "skip"
            if _time >= self.start_time:
                real_date = _date
            elif _time <= self.end_time:
                real_date = _date - datetime.timedelta(days=1)
            return real_date
        except Exception as e:
            print(e)
            print(f"{idx} {_date} {_time}")

    def init_filename(self, filename):
        p = re.search(r"\/(?P<name>.*)[.].*$", filename)
        self.filename = p.group()

    def load_data(self, filename, start_idx=0):
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
        for date, data in self.data_by_date.items():
            print(f"{date.date()} 의 초파리 수면을 분석합니다...")

            for c in data.columns:
                if c in ["Kayoung", "Date", "Time", "group"]:
                    continue

                chopari = Chopari(c, data[c])
                chopari.check_sleep()

                self.update_data(c, date, chopari)
                print(chopari)

    def save_to_excel(self, output_filename=None):
        if not output_filename:
            output_filename = f"{self.filename.split('.')[0]}_{datetime.datetime.now().date()}.xlsx"
        output_filename = "output/" + output_filename

        print(f"분석 결과를 {output_filename} 으로 저장합니다...")
        mode = "a" if os.path.exists(output_filename) else "w"
        with pd.ExcelWriter(output_filename, mode=mode) as writer:
            for _type in ["total_sleep_time", "sleep_count", "max_sleep_time", "first_sleep_at"]:
                print(f"{_type} 저장중...")
                _data = getattr(self, f"d_{_type}")
                df = pd.DataFrame.from_dict(_data)
                df.to_excel(writer, sheet_name=_type)

        print(f"저장 완료")


input_file = sys.argv[1]
try:
    start_idx = int(sys.argv[2])
except:
    start_idx = 0

main = HappyMachine()
main.load_data(input_file, start_idx)
main.check_sleep()

main.save_to_excel()
