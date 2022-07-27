import json
import datetime
from unittest import result
from numpy.random import *

#2019年のCNN Cafeの来店情報から到着率とサービス率を導出

# --------------------jsonファイルのロード--------------------
json_open1 = open('queue_json/20191111-queue.json', 'r')
json_load1 = json.load(json_open1)

json_open2 = open('queue_json/20191112-queue.json', 'r')
json_load2 = json.load(json_open2)

json_open3 = open('queue_json/20191113-queue.json', 'r')
json_load3 = json.load(json_open3)

# --------------------各日数の人数--------------------
len1 = len(json_load1)
len2 = len(json_load2)
len3 = len(json_load3)

# --------------------待ち時間やオペレーション時間の計算メソッド--------------------
#決済終了から受け渡しまでの待ち時間を算出
def wait_calculate(json):
    global total
    for v in json:
        t1 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00'))
        t2 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00'))
        total += (t2-t1)

#オペレーション時間を算出する。(決済開始〜決済終了、決済終了〜受け渡し完了)
def operation_calculate(json):
    global first_time,later_time 
    for v in json:
        t1 = datetime.datetime.fromisoformat(v['ordered_at'].replace('Z','+00:00')) #注文開始から
        t2 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00')) #決済完了まで
        t3 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00')) #受け渡し完了まで
        first_time += (t2 - t1)
        later_time += (t3 - t2)


# --------------------各パラメータの宣言--------------------
# 到着率(人/時間)を計算
arival_rate = (len1 + len2 + len3) / 3

print("到着率")
print(int(arival_rate))

first_time = datetime.timedelta()
later_time = datetime.timedelta()
total = datetime.timedelta() # サービス時間の合計

# --------------------サービス時間-----------------------------
# 全ての日数のサービス時間の合計をとる
wait_calculate(json_load1)
wait_calculate(json_load2)
wait_calculate(json_load3)

service_time = (total / 2) / (len1 + len2 + len3)
print("総人数：" + str(len1 + len2 + len3))
print("サービス時間：" + str(total))
print("平均サービス時間：" + str(service_time))
t = datetime.timedelta()
t += (datetime.datetime.fromisoformat('2019-11-11T01:00:00.000+00:00') - datetime.datetime.fromisoformat('2019-11-11T00:00:00.000+00:00'))
service_rate = t /service_time #1時間を3日間の平均サービス時間で割る

print("サービス率")
print(service_rate)


# --------------------オペレーション時間の計算--------------------
operation_calculate(json_load1)
operation_calculate(json_load2)
operation_calculate(json_load3)

print('注文開始から決済終了までの平均')
print(first_time / (len1 + len2 + len3))
print('決済終了から受け渡し完了までの平均')
print(later_time / (len1 + len2 + len3))

