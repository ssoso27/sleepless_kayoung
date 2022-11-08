#!/usr/local/bin/python3

"""
Copyright (C) 2022. YangSohee all rights reserved.
Author: Yang Sohee <ssoyapdev@gmail.com>

가영이를 위한 초파리 수면시간 측정 프로그램
"""

import pandas as pd

import datetime
from datetime import time

def help():
    print("""
    1. 이 프로그램과 초파리 수면 엑셀 데이터를 같은 폴더에 넣는다.
    2. 이 프로그램을 실행한다.
    3. 초파리 수면 엑셀 데이터 (이후 원본이라 칭함) 의 이름을 입력한다.
    """)

def get_headers(length):
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
    headers[0] = "Date"
    headers[1] = "Time"
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

    def load_data(self, filename):
        df = pd.read_excel(filename, header=None)
        header = get_headers(df.shape[1])
        df.columns = header

        # make group tag
        df["group"] = [ self.get_real_date(row['Date'], row['Time'], idx) for idx, row in df.iterrows() ]

        groups = df.groupby(df["group"])
        for g in groups.groups.keys():
            if g != "skip":
                self.data_by_date[g] = groups.get_group(g)

    def init_date(self, _date):
        _date = str(_date.date())
        self.d_total_sleep_time[_date] = {}
        self.d_sleep_count[_date] = {}
        self.d_max_sleep_time[_date] = {}
        self.d_first_sleep_at[_date] = {}

    def update_data(self, _date, _name, _chopari):
        _date = str(_date.date())
        self.d_total_sleep_time[_date][_name] = _chopari.total_sleep_time
        self.d_sleep_count[_date][_name] = _chopari.sleep_count
        self.d_max_sleep_time[_date][_name] = _chopari.max_sleep_time
        self.d_first_sleep_at[_date][_name] = _chopari.first_sleep_at

    def check_sleep(self):
        for date, data in self.data_by_date.items():
            print(f"{date.date()} 의 초파리 수면을 분석합니다...")

            self.init_date(date)

            for c in data.columns:
                if c in ["Date", "Time", "group"]:
                    continue

                chopari = Chopari(c, data[c])
                chopari.check_sleep()

                self.update_data(date, c, chopari)
                print(chopari)

main = HappyMachine()
main.load_data("220829.xlsx")
main.check_sleep()

d1 = main.d_total_sleep_time
df1 = pd.DataFrame.from_dict(d1)
print(df1)
