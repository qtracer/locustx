<h3 align="center"><p style="color: green;font-weight: bold; font-size: 68px;">locustx</p></h3>
<hr />


# 1.如何运行
### 1.1 数据准备
账号数据文件在/data中，token写入Redis。
```Terminal 
python .\dataStating.py
```
### 1.2 windows运行
```Terminal
locust -f .\locustfile.py
```

# 2.重点文件关注
### 2.1 apiJson
```
（1）这里将api请求的参数以json格式直接复制进来即可，作为请求参数的模板。注意：数据一定要经过https://www.json.cn/ 校验。
（2）json文件命名，必须保证和接口对应的方法名称一致。
```

### 2.2 commmon/apiCommon.py
##### 该文件将api请求的请求方法、header处理、request body的json模板处理等都存放在此文件中，直接调用即可
#### 2.2.1 pyget方法
```
url = CommonConfig.get_cf("config", "order_url", sys._getframe().f_code.co_name)
header = commonTask.getHeader(self.user.muctoken)

res = self.pyget(url=url, headers=header, customerId=self.customerId)
# 将customerId作为字典格式传给pyget方法进行处理
```
#### 2.2.2 pypost方法
```
用json传参
```
#### 2.2.3 pypostd方法
```
用data传参
```
#### 2.2.4 getHeader方法
```
定义header模板，关键传参替换并返回整个header，不同的token对应不同用户
```
#### 2.2.5 getApiJson方法
```
说明:
    一次性修改嵌套 JSON 数据中的多个字段，支持列表的增删操作
    :param data: 解析后的 JSON 数据（Python 字典或列表）
    :param changes: 包含修改信息的字典，键为路径，值为新值或操作指令
    :return: 修改后的 JSON 数据
```
```
实例:
    changes = {
        "buyerName": "张三",
        "itemBoList.__append__": {
            "id": None,
            "weight": 5,
            "title": "新商品",
            "skuId": 00000000000,
            "skuName": "新商品名称",
            "quantity": 1,
            "encPrice": "5000",
            "cost": 0,
            "image": "https://example.com/new_image.jpg"
        },
        "itemBoList.__delete__": 0,
        "itemBoList.0.quantity": 2
    }
    modified_data = commonTask.getApiJson("addOrder", changes)
    
# 根据changes的传参，getApiJson实现功能如下：
## （1）修改第一层级的buyerName，改为"张三"
## （2）在（1）基础上，itemBoList列表增加一个dict类型元素，并放置最后
## （3）在（2）基础上，itemBoList列表删除第一个dict类型元素
## （4）在（3）基础上，itemBoList列表的第一个dict类型元素的quantity参数值修改为2
```
### 2.3 commmon/dataHandle.py
动态逻辑方法，支持对api请求的逻辑处理

### 2.4 config/config.ini
全局配置文件，非常重要！
#### 2.4.1 env
```
环境域名，连接数据库
```
#### 2.4.2 url
```
定义各api的url，可以分类
```

### 2.5 locustService
```
每个.py文件分别对应一种场景或流程
```

### 2.6 cleanUp.py
```
清理Redis中保存的执行实例，用分布式压测时才会执行
```

# 3.脚本编写
```
编写脚本只需3步:
（1）/locustService下创建场景，py场景文件内添加实现api请求的方法
（2）在/config/config.ini下添加api的url，实现可配置化
（3）每个请求方式为POST的api，body传参时，都需要在/apiJson路径下建立一个json文件，形成传参模板
Warning: 这3步，名称必须要保持一致。
如: 
api请求的方法      def orderPageList(self):
api的url             orderPageList = /api/v3/order/pageList.json
/apiJson的json文件    orderPageList.json
```