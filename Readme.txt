检查站说明
系统基于Django, Redis


#启动redis
nohup redis-server &

#启动Django， 脚本自动开启x个Django线程 
sh startup.sh

配置文件
wenzhou/settings.py 服务器生产环境配置
wenzhou/basic_setting.py 基础配置

手动切换bing key
cd cohost
python bing.py -key
python bing.py -set 0-4(数字为key的序号)

手动执行动作获取ip-host
python tool.py

设定计划任务在basic_setting.py
每月2日执行查询操作


Ip需要手动添加到cohost/new_bing.py文件中result列表中
