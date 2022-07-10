from numpy.random import *
import math

# 2019年 CNNCafe11月11日~13日の事前調査を基にしたシミュレーション

# パラメータを設定する
times = 1000 # シミュレーション回数

employee = 2 # 受け渡し口の従業員の数(並行して作業可)

arrival_rate = 65 # (人/時間) 平均して1時間に来店している客の人数を統計から設定する.(MOは除く)

service_rate = 85 # (人/時間) 平均して1時間に客を捌く率

order_wait = 33 # 平均で注文,会計にかかる時間(秒)

limit = 30 # 注文受け入れの上限

#mo_time = 60 * 5 #何秒ごとにMOを受け入れるか(店ごとに設定,QueueingTheoryから導いてるわけではない)

# 初期値
all_num = 0 # 試行回数全てを通しての客の数(待ち時間などの平均を取るため)
shop_num = 0 # MO無しの店舗注文の利用客の人数
all_wait = 0 #全ての人数に対しての注文終了時から受け取り時刻までで定義した待ち時間の累計
all_wait2 = 0 #MO無しの利用客の人数に対しての注文終了時から受け取り時刻までで定義した待ち時間の累計
minmax = [] #wait_time2の最大最小を出すための配列

# 秒数timeを配列[時間,分,秒]で返すメソッド
def time_conversion(time):
    hour = int(time / 3600)
    min = int((time % 3600) / 60)
    second = int(time % 60)

    a = [hour,min,second]

    return a

print('上限:{:>2.0f}人'.format(limit))
# 指定回数シミュレーションを行う
for t in range( 0, times ):
    # 初期値
    arrival_time = 0 # 到着時間
    order_time = 2 # 注文終了時間
    cook_time = 1
    end_time = [0] * employee # 受け取り終了時間(商品準備の従業員の数だけ用意する)
    arrival_hour = 12 # 12時スタート(設定)
    j = 1 # シミュレーション1回ごとの利用客の総数をカウントする
    mo_num = 1 #MOの利用客 

    arr = 60 #* int(normal(4,2)) # MOの到着時間
    arr_mo = arr
    wait_mo = 0
    end_mo = 0

    counter = []

    order = [] #[注文終了orMOの来店時刻,No]
    time = [] # 最後の表示用の配列(No,arrival,wait,start,order,end,wait2)
    
    #print('客No    到着時刻           待ち時間    注文開始時刻   注文終了時刻      受け取り時刻         待ち時間')

    # お客さんごとにシミュレーション
    while True:
        # ランダムに来るお客の時刻を決める
        inter = 3600 / arrival_rate
        interval = int(normal(inter,30)) # 間隔
        arrival_time += interval
        
        # 13：00で終了
        if arrival_time > 3600:
            break
        
        # mo_timeごとに来るか来ないかを決めて来店させる
        while True:
            if mo_num > limit: # 上限を超えればMOは受け入れない
                break
            if  arrival_time > arr:
                arr_mo = arr #Moの客の到着時刻(指定時間通り来てる想定)
                r = True

                order.append([arr_mo,j,True])
                time.append([j,arr_mo,0,0,0,0,0,True])
                j += 1
                inter_mo = 60 * int(normal(2,1)) #Moの間隔
                arr += inter_mo # 間隔の分だけ足す
                mo_num += 1

            else:
                break
        
        # MO終了

        # 時間を計算する
        start_time = arrival_time + int(normal(5,2)) if arrival_time > order_time else order_time + int(normal(10,2)) #注文開始 arrival_time ,注文待ちをしてた場合はorder_timeのタイミングから数秒入れ替わる時間を考慮
        order_time = start_time + int(normal(order_wait,10))  #注文終了時間,注文開始時刻からorder_waitに従った正規分布からの乱数分を足す
        order.append([order_time,j,False]) # 最後にsortで昇順にしてend_timeを決める
        wait_time = start_time - arrival_time # 到着してから注文を始めるまでに待った時間

        time.append([j,arrival_time,wait_time,start_time,order_time,0,0,False])

        all_wait += wait_time
        j += 1
        shop_num += 1
    all_num += j
        
    # end_time
    newList = sorted(order) #[注文終了orMOの来店時刻,No]を時刻の昇順にソート
    no = [] #[No,end_time,wait_time2] 後でNo順にソートして元に戻すための配列

    for o in newList:
        service_time = int(normal(84,15))
        ret = True
        for i in end_time:
            # 空いてる従業員を探す
            if o[0] > i: # 空いている従業員がいたら
                index = end_time.index(i)
                # MOかどうか判別して受け取り時刻を決める
                end_time[index] = o[0] + int(normal(40,4)) if o[2] else o[0] + service_time
                ret = False
                wait_time2 = end_time[index] - o[0] # MOは加算しない。店舗注文だけ計算
                all_wait2 += 0 if o[2] else wait_time2 # MOは加算しない。店舗注文だけ計算
                # Noを基にtime[]を更新する
                minmax.append(wait_time2) if o[2] else 0
                no.append([o[1],end_time[index],wait_time2])
                break
        if ret: # 1人も従業員が空いていなければ
            index = end_time.index(min(end_time))
            end_time[index] = min(end_time) + int(normal(40,4)) if o[2] else min(end_time) + service_time # 1番早く手が空く従業員からサービス時間を足す
            wait_time2 = end_time[index] - o[0] # MOは加算しない。店舗注文だけ計算
            all_wait2 += 0 if o[2] else wait_time2 # MOは加算しない。店舗注文だけ計算
            minmax.append(wait_time2) if o[2] else 0
            no.append([o[1],end_time[index],wait_time2])
    no_sort = sorted(no)

    time_length = len(time)
    for i in range(0,time_length):
        time[i][5] = no_sort[i][1]
        time[i][6] = no_sort[i][2]
        
        # 時刻変換。配列で返ってくるので,[0]→時間,[1]→分,[2]→秒
        a = time_conversion(time[i][1])
        w = time_conversion(time[i][2])
        s = time_conversion(time[i][3])
        o = time_conversion(time[i][4])
        e = time_conversion(time[i][5])
        w2 = time_conversion(time[i][6])

        #if time[i][7]: # MOかどうか
        #    print('No{:>2d}   {:>2.0f}:{:>2.0f}:{:>2.0f} '
        #    '     {:>2.0f}時間{:>2.0f}分{:>2.0f}秒                                        {:>2.0f}:{:>2.0f}:{:>2.0f}     {:>2.0f}時間{:>2.0f}分{:>2.0f}秒'
        #    .format(i + 1, a[0] + arrival_hour, a[1], a[2], w[0], w[1], w[2],e[0] + arrival_hour, e[1], e[2], w2[0], w2[1], w2[2]))

        #else:
        #    print('No{:>2d}   {:>2.0f}:{:>2.0f}:{:>2.0f}      {:>2.0f}時間{:>2.0f}分{:>2.0f}秒        {:>2.0f}:{:>2.0f}:{:>2.0f}       {:>2.0f}:{:>2.0f}:{:>2.0f}         {:>2.0f}:{:>2.0f}:{:>2.0f}     {:>2.0f}時間{:>2.0f}分{:>2.0f}秒'
        #    .format( i + 1, a[0] + arrival_hour, a[1], a[2], w[0], w[1], w[2],s[0] + arrival_hour, s[1], s[2], o[0] + arrival_hour, o[1], o[2], e[0] + arrival_hour, e[1], e[2], w2[0],w2[1],w2[2]))

        
a_w = time_conversion((int)(all_wait / shop_num)) # 全ての客の注文までの平均待ち時間
a_w2 = time_conversion((int)(all_wait2 / shop_num)) # MO無しの利用客の中で会計終了時から受け取り時刻までの待ち時間の平均
print('平均注文待ち時間: {:>2.0f}時間{:>2.0f}分{:>2.0f}秒'.format(a_w[0],a_w[1],a_w[2]))
print('平均受け取り待ち時間: {:>2.0f}時間{:>2.0f}分{:>2.0f}秒'.format(a_w2[0],a_w2[1],a_w2[2]))
print('平均来店人数: {:>3.0f}人'.format((all_num - 1) / times))

min2 = time_conversion(min(minmax))
max2 = time_conversion(max(minmax))
print('平均受け取り待ち時間の最小値: {:>2.0f}時間{:>2.0f}分{:>2.0f}秒'  .format(min2[0],min2[1],min2[2]))
print('平均受け取り待ち時間の最大値: {:>2.0f}時間{:>2.0f}分{:>2.0f}秒'  .format(max2[0],max2[1],max2[2]))

average = all_wait2 / shop_num
hensa = 0
for i in minmax:
    hensa += (average - i) * (average -i)
    
hensa = math.sqrt(hensa / len(minmax))

print('標準偏差: {:>3.0f}'.format(hensa))