import requests
import datetime
import time
import json
import sys
import urllib3
urllib3.disable_warnings()

page_json ={
    'djh':
         {
             'seatid':'1349', #1309
            'start':'480',#8点
            'end':'1320',#22点
         },
    'cjl':
        {
            'studentNum':'201801007',
            'password':'808541',
             'seatid':'1448',
            'start':'840',
            'end':'1320',
        },
    'cyc':
         {
             'studentNum':'201801006',
            'password':'310010',
             'seatid':'1349',
            'start':'450',
            'end':'480',

         },
    'lyz':
        {
             'seatid':'2683',
            'start':'480',
            'end':'1320',
        },
    'lly':
        {
             'seatid':'1701',
            'start':'480',
            'end':'1320',
        },
    'xj':
        {
             'seatid':'1702',
            'start':'480',
            'end':'1320',
        }
}

login_headers = {
    'Host': 'leosys.cn',
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'doSingle/11 CFNetwork/811.5.4 Darwin/16.6.0',
    'Accept-Language': 'zh-cn',
    'token': 'SUSMZ48PYE09144246',
    'Accept-Encoding': 'gzip',
    #'X-Forwarded-For': '10.167.159.118'
}


date = datetime.date.today()
date += datetime.timedelta(days=1)
strdate = date.strftime('%Y-%m-%d')
headers = {
    'Host': 'leosys.cn',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'doSingle/11 CFNetwork/811.5.4 Darwin/16.6.0',
    'Accept-Language': 'zh-cn',
    # 'X-Forwarded-For': '10.167.159.118'
}

def save(name):
        getTokenURL='https://leosys.cn/yangtzeu/rest/auth?username='+page_json[name]['studentNum']+'&password='+page_json[name]['password']
        tokenResponse=requests.get(getTokenURL,headers=login_headers,verify=False)
        login_json = json.loads(tokenResponse.text)
        token=login_json['data']['token']
        headers['token']=token
        postdata={
            'startTime':page_json[name]['start'],
            'endTime':page_json[name]['end'],
            'date':strdate,
            'seat':page_json[name]['seatid'],
        }
        mainURL='https://leosys.cn/yangtzeu/rest/v2/freeBook'
        s=requests.post(mainURL,data=postdata,headers=headers,verify=False)
        result = json.loads(s.content.decode())
        if (result['status'] == 'success'):
            print(name, '预订成功!')
        else:
            print(name, '失败!该阶段座位已被预订或该用户已有预定!')

if __name__ == '__main__':
    names=['cjl']
    while int(time.strftime("%H%M%S")) < 90000: pass

    start = time.perf_counter()  # 返回系统运行时间
    for name in names:
        if name in page_json.keys():
            save(name)
        else:
            print("用户",name,"未注册！")
    end = time.perf_counter()
    print('用时：{:.4f}s'.format(end - start))