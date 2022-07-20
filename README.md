## 策略介绍
#### 买入卖出判断：
1. 当 kline 5 向上穿过 kline 60， 则执行买入。
2. 当 kline 5 向下穿过 kline 60， 则执行卖出。
3. 当没有交叉，存仓有盈利，根据盈利多少批量清仓
#### 可控：
1. 限制每次买入u


## 快速使用

1、获取币安API的 api_key 和 api_secret

申请api_key地址:

[币安API管理页面](https://www.binance.com/cn/usercenter/settings/api-management)


2、注册钉钉自定义机器人Webhook，用于推送交易信息到指定的钉钉群

[钉钉自定义机器人注册方法](https://m.dingtalk.com/qidian/help-detail-20781541)


3、修改app目录下的authorization文件

```
api_key='你的币安key'
api_secret='你的币安secret'
dingding_token = '申请钉钉群助手的token'   # 强烈建议您使用
```


4、交易策略配置信息 strategyConfig.py
设置你的配置信息：

```
# 均线, ma_x 要大于 ma_y
ma_x = 5
ma_y = 60

# 币安
binance_market = "SPOT"#现货市场
kLine_type = '15m' # 15分钟k线类型，你可以设置为5分钟K线：5m;1小时为：1h;1天为：1d
```
当 kline 5 向上穿过 kline 60， 则执行买入。

当 kline 5 向下穿过 kline 60， 则执行卖出。

你可根据自己的喜好，调整 ma_x 和 ma_y 的值。 

你也可以调整 kLine_type ，来选择 5分钟K线、15分钟K线、30分钟K线、1小时K线、1天K线等；

不同的K线，最终效果也是不一样的。


5、同时交易多币种

robot-run.py中

创建多个订单管理对象：
```
# 使用 USDT 购买 DOGE,限定最多100个USDT
orderManager_doge = OrderManager("USDT", 100,"DOGE", binance_market)
# 使用 USDT 购买 ETH,限定最多100个USDT
orderManager_eth = OrderManager("USDT", 100,"ETH", binance_market)
```

将orderManager_doge 和 orderManager_eth 加入定时执行的方法中：
```
def binance_func():
    orderManager_doge.binance_func()
    time.sleep(10)
    orderManager_eth.binance_func()

```

程序可同时监控 DOGE 和 ETH 的均线，并根据策略执行交易。
使用时，可根据自身需要，增加其他币种。



6、运行程序(记得先开科学上网)
```
python robot-run.py
```



## 服务器部署
购买服务器，建议是海外服务器，可以访问币安API

### 我的配置：
Linux, 1核CPU, 2G内存(1G也可)

我是在阿里云购买的日本东京服务器(传说币安服务器就在东京)

也可选择 新加坡、香港服务器

[阿里云，新人优惠](https://www.aliyun.com/activity?userCode=zs5is7pi)

[阿里云，最新活动](https://www.aliyun.com/1111/new?userCode=zs5is7pi)

