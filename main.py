# coding=utf-8
import requests
import json
import threading
import time
import secrets
import string
import hashlib
import ntplib
import configparser


# 定义一个全局锁用于线程同步
thread_dict = {}
cookie_file_path = 'cookie.txt'
config_file_path = 'config.txt'
headers = {
            'authority': 'www.allcpp.cn',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://cp.allcpp.cn',
            'referer': 'https://cp.allcpp.cn/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }


# 读取配置文件
def getConfig(filename, section, option):
    conf = configparser.ConfigParser()
    conf.read(filename)
    config = conf.get(section, option)
    return config


def timeconvey(ntp):
    chec = ntplib.NTPClient() 
    response = chec.request(ntp) 
    timestamp = response.tx_time
    timestamp_local = time.time()
    #print(timestamp_local)
    #print(timestamp)
    differ= timestamp - timestamp_local
    return differ


def sign_for_post(ticketid):
    timestamp = str(int(time.time())) ##"1682074579"
    ## 貌似并不校验 sign: a()(t + r + i + e + n)
    # nonce="jcFFFK4pPz2eNGBND3xDxTEyZ7PGCyzm" ## 32位随机值即可
    n = string.ascii_letters + string.digits
    nonce = ''.join(secrets.choice(n) for i in range(32))
    sign=hashlib.md5(f"2x052A0A1u222{timestamp}{nonce}{ticketid}2sFRs".encode('utf-8')).hexdigest()
    # print(f"ticket_type_id={ticket_type_id}")
    # print(f"nonce={nonce}")
    # print(f"timestamp={timestamp}")
    # print(f"sign={sign}")
    vital='nonce='+nonce+'&timeStamp='+timestamp+'&sign='+sign
    return vital


def cookie_string_to_dict(cookie_string):
    cookies = {}
    cookie_pairs = cookie_string.split("; ")
    
    for pair in cookie_pairs:
        key, value = pair.split("=", 1)
        cookies[key] = value
    
    return cookies


def read_cookies_and_tickets_from_file():
    cookies = []
    ticket_id = []
    ticket_ids = []
    try:
        with open(cookie_file_path, 'r',encoding='utf-8') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                cookies.append(lines[i].strip())  # 使用append方法将元素添加到列表
                i += 1
                if i < len(lines):
                    ticket_id.append(lines[i].strip())  # 使用append方法将元素添加到列表
                    i += 1
    except FileNotFoundError:
        print(f"File '{cookie_file_path}' not found.")
    for item in ticket_id:
    # 使用逗号分割字符串并添加到输出列表
        ticket_ids.append(item.split(','))
    return cookies, ticket_ids  # 返回两个列表作为一个元组


def getpurser(cookie_str):
    cookies = cookie_string_to_dict(cookie_str)
    pur = requests.get(
        url='https://www.allcpp.cn/allcpp/user/purchaser/getList.do',
        cookies=cookies,
        headers=headers,
    )
    purrer = pur.content.decode("utf-8")
    purrer_data = json.loads(purrer)
    return purrer_data


def check_success(cookies,ticketid):
    url = 'https://www.allcpp.cn/allcpp/user/getMyOrderList.do?pageindex=1&pagesize=10&enabled=0&orderby=0'
    list = requests.get(
        url=url,
        cookies=cookies,
        headers=headers,
    )
    listing = list.content.decode("utf-8")
    data = json.loads(listing)
    # 遍历订单信息
    for order in data['result']['list']:
        if order['ticketTypeId'] == ticketid:
            return True
        else:
            return False


def process_thread(ticketid,cookie_str):
    try:
        cookies = cookie_string_to_dict(cookie_str)
        try:
            pur = requests.get(
                url='https://www.allcpp.cn/allcpp/user/purchaser/getList.do',
                cookies=cookies,
                headers=headers,
            )

            purrer = pur.content.decode("utf-8")
            purrer_data = json.loads(purrer)
            print(purrer_data)
        except json.decoder.JSONDecodeError as e:
            pass
        ids = [str(item["id"]) for item in purrer_data]
        ids_str = ",".join(ids)
        id_count = len(ids)
        print(f"IDs for ticket {ticketid}: {ids_str}")
        json_data = {}


        retn_params = sign_for_post(ticketid)
        url = 'https://www.allcpp.cn/allcpp/ticket/buyTicketAliWapPay.do?ticketTypeId=' + str(ticketid) + '&count=' + str(
                id_count) + '&' + retn_params + '&purchaserIds=' + ids_str
        print(url)
        try:
            response = requests.post(
                    url=url,
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
            )
            resp = response.content.decode("utf-8")
            parsed_resp = json.loads(resp)
        except json.decoder.JSONDecodeError as e:
            pass
        print(parsed_resp)
    except:
        pass
    
    i = 0
    if parsed_resp.get("isSuccess") == True:
        print(f"Thread for ticket {ticketid} succeeded")
        with open(f"output_ticket_{ticketid}_{ids_str}.txt", "a") as output_file:
            output_file.write(resp)
        print(f"Thread for ticket {ticketid} with cookies {cookies} succeeded, closing other two threads of the same type.")
        threads =[]
        threads_to_close = [thread for thread in threads if thread._target == process_thread and thread._args[0] == ticketid and thread._args[1] == cookies]
        for thread_to_close in threads_to_close[:2]:  # 关闭同类型的前两个线程
            thread_to_close.join()
        return True
    else:
        while i < 2:
            try:
                with open(f"output_ticket_{ticketid}_{ids_str}_attempt_{i}.txt", "a") as output_file:
                    output_file.write(resp)
                retn_params = sign_for_post(ticketid)
                url = 'https://www.allcpp.cn/allcpp/ticket/buyTicketAliWapPay.do?ticketTypeId=' + str(ticketid) + '&count=' + str(
                    id_count) + '&' + retn_params +'&purchaserIds=' + ids_str
                print(url)
                try:
                    response = requests.post(
                        url=url,
                        cookies=cookies,
                        headers=headers,
                        json=json_data,
                    )
                    resp = response.content.decode("utf-8")
                    parsed_resp = json.loads(resp)
                except json.decoder.JSONDecodeError as e:
                    pass
                print(parsed_resp)
                is_success = parsed_resp["isSuccess"]
                if is_success == True:
                    i = 3
                    print(f"Thread for ticket {ticketid} succeeded")
                    with open(f"output_ticket_{ticketid}_{ids_str}.txt", "a") as output_file:
                        output_file.write(resp)
                    threads_to_close = [thread for thread in threads if thread._target == process_thread and thread._args[0] == ticketid and thread._args[1] == cookies]
                    for thread_to_close in threads_to_close[:2]:  # 关闭同类型的前两个线程
                        thread_to_close.join()
                    return True
                else:
                    with open(f"output_ticket_{ticketid}_{ids_str}_attempt.txt", "a") as output_file:
                        output_file.write(resp)
                        url = 'https://www.allcpp.cn/allcpp/ticket/buyTicketAliWapPay.do?ticketTypeId=' + str(ticketid) + '&count=' + str(
                    id_count) + '&' + retn_params +'&purchaserIds=' + ids_str
                    print(url)
                    try:
                        response = requests.post(
                            url=url,
                            cookies=cookies,
                            headers=headers,
                            json=json_data,
                        )
                        resp = response.content.decode("utf-8")
                        parsed_resp = json.loads(resp)
                        is_success = parsed_resp["isSuccess"]
                    except json.decoder.JSONDecodeError as e:
                        pass
                    if is_success == True:
                            i = 3
                            print(f"Thread for ticket {ticketid} succeeded")
                            with open(f"output_ticket_{ticketid}_{ids_str}.txt", "a") as output_file:
                                output_file.write(resp)
                            threads_to_close = [thread for thread in threads if thread._target == process_thread and thread._args[0] == ticketid and thread._args[1] == cookies]
                            for thread_to_close in threads_to_close[:2]:  # 关闭同类型的前两个线程
                                thread_to_close.join()
                            return True
                    else:
                        with open(f"output_ticket_{ticketid}_{ids_str}_attempt.txt", "a") as output_file:
                            output_file.write(resp)
                        print(resp)
                        print(type(resp))
                        time.sleep(sleep_time)
            except:
                pass


def start(cookies, ticket_ids):
    thread_dict = {}

    for i in range(len(cookies)):
        for j in range(len(ticket_ids[i])):
             for _ in range(num_thread):
                ticket = ticket_ids[i][j]
                cook = cookies[i]
                thread = threading.Thread(target=process_thread, args=(ticket, cook))
                thread.start()


def schedule_script_at_timestamp(target_timestamp_ms,cookies, ticket_ids):
    current_timestamp_ms = int(time.time() * 1000)
    time_difference_ms = target_timestamp_ms - current_timestamp_ms

    if time_difference_ms <= 0:
        print("时间已经过去了主人")
    else:
        print(f"还有 {time_difference_ms / 1000} 秒喵~.")

        def delayed_execution():
            time.sleep(time_difference_ms / 1000)
            start(cookies, ticket_ids)
        t = threading.Thread(target=delayed_execution)
        t.start()


def main():
    ntp = getConfig("config.txt", 'time', 'ntp')
    global sleep_time
    sleep_time = float(getConfig("config.txt", 'ticket', 'sleep'))
    global num_thread
    num_thread = int(getConfig("config.txt", 'ticket', 'num_thread'))

    differ = timeconvey(ntp)
    if differ > 0 :
        print(f"\033[1;31;47m主人你的时间慢了{abs(differ)}秒\033[0m")
        print("\033[1;31;47m主人你的时间滞后了哦，请同步时间\033[0m")
    else:
        print(f"\033[1;31;47m主人你的时间快了{abs(differ)}秒\033[0m")
    cookies, ticket_ids = read_cookies_and_tickets_from_file()
    print(ticket_ids)
    i=0
    while i<len(cookies):
        ifn = getpurser(cookies[i])
        print(ifn)
        print(ticket_ids[i])
        i+=1
    if input('正确(回复T) or 错误(回复F) \n') == 'T':
        print("1.定时 2.捡漏\n")
        if input()== '1':
            target_timestamp_ms = int(input('输入开始时间戳(毫秒):'))
            schedule_script_at_timestamp(target_timestamp_ms,cookies, ticket_ids)
        else:
            start(cookies, ticket_ids)
    else: 
        exit


if __name__ == "__main__":
    main()
