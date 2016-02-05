## how to run

./ops.sh start # 启动服务

然后[访问这儿](http://127.0.0.1:8081/dumpeek/a/b/c)

./ops.sh stop # 退出程序

## what to do

这个小程序本来是访问elasticsearch(搜索引擎)用的

你可能没安装elasticsearch, 所以我把访问es得到数据的接口给mock掉了(在basic.py的search函数)
