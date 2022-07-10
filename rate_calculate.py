import json
import datetime
from numpy.random import *

#2019年のCNN Cafeの来店情報から到着率とサービス率を導出

json_open1 = open('queue_json/20191111-queue.json', 'r')
json_load1 = json.load(json_open1)

json_open2 = open('queue_json/20191112-queue.json', 'r')
json_load2 = json.load(json_open2)

json_open3 = open('queue_json/20191113-queue.json', 'r')
json_load3 = json.load(json_open3)

len1 = len(json_load1)
len2 = len(json_load2)
len3 = len(json_load3)

arival_rate = (len1 + len2 + len3) / 3

print("到着率")
print(int(arival_rate))

first_time = datetime.timedelta()
later_time = datetime.timedelta()

order_time = datetime.timedelta()
calc_time = datetime.timedelta()
handed_time = datetime.timedelta()


total = datetime.timedelta() # サービス時間の合計

for v in json_load1:
    t1 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00'))
    t2 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00'))
    total += (t2-t1)

for v in json_load2:
    t1 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00'))
    t2 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00'))
    total += (t2-t1)
    
for v in json_load3:
    t1 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00'))
    t2 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00'))
    total += (t2-t1)

service_time = (total / 2) / (len1 + len2 + len3)

t = datetime.timedelta()
t += (datetime.datetime.fromisoformat('2019-11-11T01:00:00.000+00:00') - datetime.datetime.fromisoformat('2019-11-11T00:00:00.000+00:00'))
service_rate = t /service_time #1時間を3日間の平均サービス時間で割る

print("サービス率")
print(service_rate)


# オペレーション時間の計算

for v in json_load1:
    t1 = datetime.datetime.fromisoformat(v['ordered_at'].replace('Z','+00:00')) #注文開始から
    t2 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00')) #決済完了まで
    t3 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00')) #決済完了から
    t4 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00')) #受け渡し完了まで

    first_time += (t2-t1)
    later_time += (t4-t3)

for v in json_load2:
    t1 = datetime.datetime.fromisoformat(v['ordered_at'].replace('Z','+00:00')) #注文開始から
    t2 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00')) #決済完了まで
    t3 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00')) #決済完了から
    t4 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00')) #受け渡し完了まで

    first_time += (t2-t1)
    later_time += (t4-t3)

for v in json_load3:
    t1 = datetime.datetime.fromisoformat(v['ordered_at'].replace('Z','+00:00')) #注文開始から
    t2 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00')) #決済完了まで
    t3 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00')) #決済完了から
    t4 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00')) #受け渡し完了まで

    first_time += (t2-t1)
    later_time += (t4-t3)

print('注文開始から決済終了までの平均')
print(first_time / (len1 + len2 + len3))
print('決済終了から受け渡し完了までの平均')
print(later_time / (len1 + len2 + len3))

for v in json_load1:
    t1 = datetime.datetime.fromisoformat(v['ordered_at'].replace('Z','+00:00'))
    t2 = datetime.datetime.fromisoformat(v['paymented_at'].replace('Z','+00:00'))
    t3 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00'))
    t4 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00'))

    order_time += t2 -t1
    calc_time += t3 - t2
    handed_time += t4 - t3

for v in json_load2:
    t1 = datetime.datetime.fromisoformat(v['ordered_at'].replace('Z','+00:00'))
    t2 = datetime.datetime.fromisoformat(v['paymented_at'].replace('Z','+00:00'))
    t3 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00'))
    t4 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00'))

    order_time += t2 -t1
    calc_time += t3 - t2
    handed_time += t4 - t3

for v in json_load3:
    t1 = datetime.datetime.fromisoformat(v['ordered_at'].replace('Z','+00:00'))
    t2 = datetime.datetime.fromisoformat(v['paymented_at'].replace('Z','+00:00'))
    t3 = datetime.datetime.fromisoformat(v['serviced_at'].replace('Z','+00:00'))
    t4 = datetime.datetime.fromisoformat(v['handed_at'].replace('Z','+00:00'))

    order_time += t2 -t1
    calc_time += t3 - t2
    handed_time += t4 - t3
