# Asch Python SDK
## 运行坏境搭建

```
python 2.7及其依赖安装
sudo apt-get install python pip
pip install requests
```

## Asch monitor
监控排名前101受托人的丢块和余额不足情况，如果发现则发送邮件通知相关人  
TODO:区块高度对比  
lib/mail.py中配置发邮件的用户名和密码  
python monitor.py  


## 一键投票
回投（给投了我的票人投票）、取消投票（我投了，但他没投我）  
python voteback_for_voteme.py  
按照提示输入你的受托人密码（保存在内存中，不会记录到文件或者发送给他人）  
