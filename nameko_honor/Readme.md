nameko示例代码

MicroFlask/
	flask工程
	app.py 在内部使用了Nameko所提供的服务
	config.py 配置了nameko的地址 目前为本地
Nameko/
	nameko 微服务
	需要预先安装 pymysql DBUtils nameko和软件rabbitmq
	终端运行 为 nameko run schoolservice

	db.py 数据库连接池，待更新，将就着用。
	config.py 数据库配置
	schoolservice.py 微服务，school类提供了三个外部可访问的函数。
