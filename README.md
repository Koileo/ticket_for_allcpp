# ticket_for_allcpp
开源免费，简单易用，多线程暴力抢票工具<br>
本程序仅供学习交流, 不得用于商业用途<br>
使用本程序进行违法操作产生的法律责任由操作者自行承担

## 安装教程
Windows 直接下载最新的release文件 [下载地址](https://github.com/Koileo/ticket_for_allcpp/releases/)<br>
Linux 和 Macos 请下载源码 使用Python运行

## 使用说明
cookie.txt为配置地址，第一行为账号cookie值，直接F12全部复制就可以<br>
第二行为ticketid，同样也是F12查看 https://www.allcpp.cn/allcpp/ticket/getTicketTypeList.do?eventMainId=xxxx 的响应 一般为4位数字<br>
以此类推，第三行第四行也是这样<br>
config.txt 是配置文件 包括ntp服务器，间隔时长，线程数
本程序支持多线程 多账户 （默认三线程）<br>
默认实名票全部按照购票人设置数量购买，你绑定几个人买几份票，即默认全选<br>
同一账号支持同时购买不同票类，在第二行用“,"分开
## 其他可用脚本

| 链接                                                       | 主要特色                |
| --------------------------------------------------------- | ---------------------- |
| https://github.com/mikumifa/cppTickerBuy                      |图形化，对小白友好         |


## 未来功能
- [ ] 微信通知
- [x] 程序外部配置空隔时间和线程数
- [ ] linux 和mac 打包
- [x] 时间校准


## 项目问题
反馈程序BUG或者提新功能建议： [点此链接向项目提出反馈BUG](https://github.com/Koileo/ticket_for_allcpp/issues)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Koileo/ticket_for_allcpp&type=Date)](https://star-history.com/#Koileo/ticket_for_allcpp&Date)
