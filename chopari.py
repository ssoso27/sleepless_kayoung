"""
Copyright (C) 2023. YangSohee all rights reserved.
Author: Yang Sohee <ssoyapdev@gmail.com>

초파리 객체 (Model)
객체 별 수면시간, 수면횟수, 최대수면시간, 수면도입시간을 갖는다.
"""
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
        for i, movement in enumerate(self.movement_data + [-1]):
            if movement == 0:
                time += 1
                continue

            if time >= self.MIN_TIME:
                self.incr_total_sleep_time(time)
                self.incr_sleep_count()
                self.update_max_sleep_time(time)
                self.update_first_sleep_at(i-time+1)
            time = 0
            #print(f"time: {time} | movement: {movement} | self.sleep_count {self.sleep_count} | self.total_sleep_time {self.total_sleep_time}")
