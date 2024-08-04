# ticket_for_allcpp

开源免费，简单易用，多线程暴力 CPP 抢票工具。

> [!NOTE]
> 本程序仅供学习交流, 不得用于商业用途
> 使用本程序进行违法操作产生的法律责任由操作者自行承担

## 安装教程

### 1. 快速安装

前往 [Releases](https://github.com/Koileo/ticket_for_allcpp/releases) 下载最新可执行文件直接命令行运行。

### 2. 源码运行

```shell
git clone https://github.com/Koileo/ticket_for_allcpp.git
cd ticket_for_allcpp
pip install -r requirements.txt
python main.py
```

## 使用说明

### cookie.txt 配置

- 第一行为账号`cookie`值，浏览器登入CPP直接F12获取并全部复制即可。
- 第二行为`ticketid`，同样也是F12查看 https://www.allcpp.cn/allcpp/ticket/getTicketTypeList.do?eventMainId=xxxx 的响应 一般为4位数字
- 以此类推，第三行第四行也是这样

### config.txt 配置文件：包括ntp服务器，间隔时长，线程数

- 本程序支持多线程，多账户（默认三线程）。
- 默认实名票全部按照购票人设置数量购买，你绑定几个人买几份票，即默认全选
- 同一账号支持同时购买不同票类，在第二行用“,"分开

## 其他可用脚本

| 链接                                                       | 主要特色                |
| --------------------------------------------------------- | ---------------------- |
| https://github.com/mikumifa/cppTickerBuy                      |图形化，对小白友好         |

## 未来功能

- [ ] 微信通知
- [x] 程序外部配置空隔时间和线程数
- [x] Linux 和 MacOS 打包
- [x] 时间校准

## 项目问题

反馈程序BUG或者提新功能建议：[点此链接向项目提出反馈BUG](https://github.com/Koileo/ticket_for_allcpp/issues)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Koileo/ticket_for_allcpp&type=Date)](https://star-history.com/#Koileo/ticket_for_allcpp&Date)
