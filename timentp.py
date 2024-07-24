import ntplib
import time
def timeconvey():
    chec = ntplib.NTPClient() 
    response = chec.request('ntp.aliyun.com') 
    timestamp = response.tx_time
    timestamp_local = time.time()
    #print(timestamp_local)
    #print(timestamp)
    differ= timestamp - timestamp_local
    return differ