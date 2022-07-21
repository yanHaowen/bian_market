#coding=utf-8

import json
import numpy as np
import pandas as pd
import time
import datetime

class DoubleAverageLines:

    def __init__(self):
        pass

    # [
    #     1499040000000, // 开盘时间
    # "0.01634790", // 开盘价
    # "0.80000000", // 最高价
    # "0.01575800", // 最低价
    # "0.01577100", // 收盘价(当前K线未结束的即为最新价)
    # "148976.11427815", // 成交量
    # 1499644799999, // 收盘时间
    # "2434.19055334", // 成交额
    # 308, // 成交笔数
    # "1756.87402397", // 主动买入成交量
    # "28.46694368", // 主动买入成交额
    # "17928899.62484339" // 请忽略该参数
    # ]

    def klinesToDataFrame(self,klines):

        if klines is None:
            print("klinesToDataFrame---error:klines is None.")
            return None

        openTimeList = []
        openPriceList = []
        maxPriceList = []
        minPriceList = []
        closePriceList = []
        dealVoluMeList = []
        closeTimeList = []
        dealTotalMoneyList = []
        dealCountList = []
        dealBuyVolumeList = []
        dealBuyTotalMoneyList = []


        for kline in klines:
            if (type(kline)).__name__ == 'list':
                openTimeList.append(self.stampToTime(kline[0]))
                openPriceList.append(kline[1])
                maxPriceList.append(kline[2])
                minPriceList.append(kline[3])
                closePriceList.append(kline[4])
                dealVoluMeList.append(kline[5])
                closeTimeList.append(self.stampToTime(kline[6]))
                dealTotalMoneyList.append(kline[7])
                dealCountList.append(kline[8])
                dealBuyVolumeList.append(kline[9])
                dealBuyTotalMoneyList.append(kline[10])
            else:
                print("error: kline is not list.")

        kLinesDict = {"openTime": openTimeList, "openPrice": openPriceList, "maxPrice": maxPriceList, "minPrice":minPriceList, "closePrice":closePriceList, "closeTime":closeTimeList,"openTime2": openTimeList}

        klines_df = pd.DataFrame(kLinesDict)

        # for index, row in klines_df.iterrows():
        #     print(str(row["openTime"]) + "\t" +row["openPrice"] + "\t" +row["maxPrice"] + "\t"+row["minPrice"] + "\t"+row["closePrice"] + "\t"+str(row["closeTime"]) + "\t")

        return klines_df


    def readJsonFromFile(self, filePath):
        # Opening JSON file
        f = open(filePath, )
        data = json.load(f)
        f.close()
        # Iterating through the json
        # list
        print("readJsonFromFile =")
        if (type(data)).__name__ == 'list':
            for i in data:
                print(i)
            # Closing file
            return data

        return None

        
    def release_trade_stock(self, ma_x_line, ma_y_line, code, df):

        def get_TRIX(df,N=12,M=20):
            """三重平滑平均线
        原理：
            长线操作时采用本指标的讯号，可以过滤掉一些短期波动的干扰，避免交易次数过于频繁，造成部分无利润的买卖，及手续费的损失。本指标是一项超长周期的指标，长时间按照本指标讯号交易，获利百分比大于损失百分比，利润相当可观。
        算法：
        先计算收盘价的三重N日指数平滑移动平均，记为TR
        TRIX线　(TR－昨日TR)／昨日TR×100
        TRMA线　TRIX线的M日移动平均
        参数：N、M　 天数，一般为12、9
        用法：
            1、打算进行长期控盘或投资时，趋向类指标中以TRIX最适合。
            2、TRIX由下向上交叉TRMA时，买进。
            3、TRIX由上向下交叉TRMA时，卖出。
            4、参考MACD用法。"""
            for i in range(len(df)):
                if i==0:
                    df.ix[i,'ema']=df.ix[i,'close']
                if i>0:
                    df.ix[i,'ema']=(2*df.ix[i-1,'close']+(N-1)*df.ix[i,'close'])/(N+1)
            for i in range(len(df)):
                if i==0:
                    df.ix[i,'ema1']=df.ix[i,'ema']
                if i>0:
                    df.ix[i,'ema1']=(2*df.ix[i-1,'ema']+(N-1)*df.ix[i,'ema'])/(N+1)
            for i in range(len(df)):
                if i==0:
                    df.ix[i,'tr']=df.ix[i,'ema1']
                if i>0:
                    df.ix[i,'tr']=(2*df.ix[i-1,'ema1']+(N-1)*df.ix[i,'ema1'])/(N+1)
            trix=100*(df['tr']-df['tr'].shift(1))/df['tr'].shift(1)
            trma=df['trix'].rolling(M).mean()
            return trix,trma

        def MA(df, n):
            MA = Series(pd.rolling_mean(df['closePrice'], n), name = 'MA_' + str(n))
            df = df.join(MA)
            return df
        
        print('\n' + code + ' 均线 ' + str(ma_x_line) + ' 和 ' + str(ma_y_line) + ' :')

        df[["openTime"]] = df[["openTime"]].astype(str)  # int类型 转换 成str类型，否则会被当做时间戳使用，造成时间错误
        df[["openTime2"]] = df[["openTime2"]].astype(str)  # int类型 转换 成str类型，否则会被当做时间戳使用，造成时间错误

        # print("===========================================\n")
        df['openTime'] = pd.to_datetime(df['openTime'])
        df['openTime2'] = pd.to_datetime(df['openTime2'])

        df.set_index('openTime2', inplace=True)
        df = df.sort_index(ascending=True)

        # 求出均线
        maX = df['closePrice'].rolling(ma_x_line).mean()
        maY = df['closePrice'].rolling(ma_y_line).mean()
        # ema
        maX = df['closePrice'].astype(float).ewm(span=ma_x_line, min_periods=0, adjust=False, ignore_na=False).mean()
        maY = df['closePrice'].astype(float).ewm(span=ma_y_line, min_periods=0, adjust=False, ignore_na=False).mean()
        
        df = df[ma_y_line:]  # 这个切片很重要，否则会报错，因为数据不匹配
        # 因为 ma_x_line < ma_y_line ,所以均线 切到 ma_y_line
        maX = maX[ma_y_line:]  # 切片，与 df 数据条数保持一致
        maY = maY[ma_y_line:]  # 切片，与 df 数据条数保持一致

        # print("df数据行数=" +str(len(df)))
        # print(df)
        # 从尾部，删除1行
        # df.drop(df.tail(1).index, inplace=True)

        # print("tmp_last_df--数据切片：")
        # for index, row in df.iterrows():
        #     print(str(row["openTime"]) + "\t" +row["openPrice"] + "\t" +row["maxPrice"] + "\t"+row["minPrice"] + "\t"+row["closePrice"] + "\t"+str(row["closeTime"]) + "\t")

        print("最后一行数据：")
        last_row = df.iloc[-1,:] #第1行，所有列
        print(str(last_row["openTime"]) + "\t" +last_row["openPrice"] + "\t" +last_row["maxPrice"] + "\t"+last_row["minPrice"] + "\t"+last_row["closePrice"] + "\t"+str(last_row["closeTime"]) + "\t")

        print("-------------------------------------------------------\n")
        s1 = maX < maY  # 得到 bool 类型的 Series
        s2 = maX > maY

        #短期均线向上穿越长期均线叫金叉，反之短期均线向下穿越长期均线为死叉。
        death_ex = s1 & s2.shift(1)  # 判定死叉的条件
        death_date = df.loc[death_ex].index  # 死叉对应的日期

        golden_ex = ~(s1 | s2.shift(1))  # 判断金叉的条件
        golden_record = df.loc[golden_ex]
        golden_date = golden_record.index  # 金叉的日期

        s1 = pd.Series(data=1, index=golden_date)  # 1 作为金叉的标识
        s2 = pd.Series(data=0, index=death_date)  # 0 作为死叉的标识

        s = s1.append(s2)  # 合并
        s = s.sort_index(ascending=True)  # 排序

        # print("金叉和死叉对应的时间：")
        # print(s)

        hold = 0  # 持有的股数

        trade_buy_price = 0

        for i in range(0, len(s)):

            if s[i] == 1:
                time = s.index[i]
                close_price = float(df.loc[time]['closePrice'])  # 收盘价

                open_time = df.loc[time]['openTime']  # 开盘时间
                close_time = df.loc[time]['closeTime']  # 收盘时间

                # 交叉刚好在最后一个K线才执行买入（有骗炮风险，建议改成交叉后下个时间点）
                isRightTime = self.judgeCurrentTimeWithLastRecordTime(str(open_time), str(close_time))


                # print(open_price)
                trade_buy_price = close_price  # 记录买入的价格
                str_date = str(time)
                print(str_date + "\t" + "买入" + code + "\t" + str(round(close_price, 8))+"---"+str(isRightTime))
                if isRightTime:
                    print("release_trade_stock---buy")
                    return "buy,"+str(open_time)

            else:
                # 卖出股票的单价
                death_time = s.index[i]
                p_death = float(df.loc[death_time]['closePrice'])
                str_date = str(death_time)

                open_time = df.loc[death_time]['openTime']  # 开盘时间
                close_time = df.loc[death_time]['closeTime']  # 收盘时间
                isRightTime = self.judgeCurrentTimeWithLastRecordTime(str(open_time), str(close_time))

                print(str_date + "\t" + "卖出" + str(code) + "\t"+ str(round(p_death, 8)) +"---"+str(isRightTime))
                if isRightTime:
                    print("release_trade_stock---sell")
                    return "sell"

        print("release_trade_stock---None")

        return None




    # 判断当前时间，是否在k线时间范围内
    def judgeCurrentTimeWithLastRecordTime(self, openTime, closeTime):

        dateTime_interval = pd.to_datetime(closeTime) - pd.to_datetime(openTime)

        seconds_interval = dateTime_interval.seconds # int类型，秒数
        # print("seconds_interval 的类型=")
        # print(type(seconds_interval))
        # print(seconds_interval)

        now = int(round((time.time()-seconds_interval) * 1000))

        now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))

        if now02>=openTime and now02<=closeTime:
            # print("成功---"+openTime+"\t"+now02+"\t"+closeTime)
            return True
        else:
            # print("失败---"+openTime+"\t"+now02+"\t"+closeTime)
            return False


    def stampToTime(self, stamp):

        # now = int(round(time.time() * 1000))
        stamp_int = int(stamp)

        now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp_int / 1000))

        # mytime = datetime.datetime.fromtimestamp(stamp/1000)
        # # print(stamp)
        # print("mytime type is : " + type(now02).__name__)
        return now02

