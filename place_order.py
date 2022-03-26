# -*-coding:utf-8-*-
import requests
import datetime
import json
from retrying import retry
import threading
# import re
# import pandas as pd
# import getopt
# import sys
import time


header={
'Host': 'seat.yangtzeu.edu.cn',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532)',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
}

account={
    'djh':
         {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=1D8oS4&openid=1D808DE184573E16CFC5367D35B96E5797182038D540151BDCA1D2D34FAC7B32&account=E6416BFA349FD12974D78499DF32EA99&upass=0656E66F8A10879CA5DA0B3479ACF455D4B2CB7714C5A1AE0356ED69FC6A8EBC&headimgurl=&nickname=&sign=2ea51f1ef3090476eaa7c591bc95bb11',
            'roomid':'3',#社科阅览室
             'buildid':'1',
             'seatid':'1708',
            'start':'480',#8点
            'end':'1290',#22点
         },
    'cjl':
        {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=373oS4&openid=373145D851109991C00A66CA578BCFCAA3CB8C56FC61E67FF47FF1E4D4AF0A06&account=BCAB731E1AB878EBB60AF12957839F6F&upass=93AE05FAD004ABC90D992637C92A27C46D72972AE64DD20CFD3C8A1DFA0301CC&headimgurl=&nickname=&sign=27c34d203139330e3e9bbbed22da63d2',
            'roomid':'7',
             'buildid':'1',
             'seatid':'7577',
            'start':'480',
            'end':'1290',
        },
    'cyc':
         {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=EC9oS4&openid=EC9DBE12B05D6A7EB55D6C613F4FE1D431179966B23C7A656467CC1485B1EA4E&account=A5939A469A1CA88EC1050B8573AFCAE3&upass=7910610B07185DD2DFB18095E71488180E03C05D07A4CD397E7FF22017E17275&headimgurl=&nickname=&sign=0d3f8838fafa1f3a53512abfd6c3137a',
            'roomid':'3',
             'buildid':'1',
             'seatid':'1713',
            'start':'480',
            'end':'1290',

         },
    'lyz':
        {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=806oS4&openid=806D917103CB62E5414A41D90C840A6B7371F6BBFCD326F05E7DD74C44E5F47A&account=3F066DC0AEFD1DA642968168F8913BF5&upass=920260512644CA0BD834D702944DC95427727C62767EFFB014A985F8E1FE0B41&headimgurl=&nickname=&sign=4592ab5045faf6209ddf1543d395da48',
            'roomid':'6',
             'buildid':'1',
             'seatid':'2683',
            'start':'450',
            'end':'1290',
        },
    'lly':
        {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=73DoS4&openid=73D4EBD871300041B30F5BE3D71B07E59110D20E853355375CB15028303E16B8&account=8E613393E67F62493A8A3245621E228B&upass=B2750EB5021B904ADA2B33381F16C111D45CFA8181C02DDE1BCEBC64F5A324C7&headimgurl=&nickname=&sign=e345d1d49f676f08bd99790b550cbd22',
            'roomid':'3',
             'buildid':'1',
             'seatid':'1701',
            'start':'480',
            'end':'1290',
        },
    'xj':
        {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=D97oS4&openid=D97F32A71F6DF1C0E875697BD001DCDF58D7360D9D4989D58FBA7F93B8A30CD2&account=F80DC71AA78C6DEB7C5B058D6B6279F7&upass=FE76972CB82EE3FCEF3CD6B334FC90110E03C05D07A4CD397E7FF22017E17275&headimgurl=&nickname=&sign=169398e4bddda9a1d5536345b37d8dd5',
            'roomid':'3',
             'buildid':'1',
             'seatid':'1702',
            'start':'480',
            'end':'1290',
        },
    'wt':
        {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=ED5oS4&openid=ED5A373B5D99A0524944007D8245D2D216D3429874CA85BB2841D65F0E04A905&account=2497EFFBC436F14F09466FCBB6E5F91D&upass=DE7062073D73BD51A8DB3399289E5FA8D45CFA8181C02DDE1BCEBC64F5A324C7&headimgurl=&nickname=&sign=a89c3937f6b2dcf8363dca87853e1875',
            'roomid':'10',
             'buildid':'1',
             'seatid':'5684',
            'start':'480',
            'end':'1290',
        },
    'syq':
        {
            'address':'http://seat.yangtzeu.edu.cn/libseat-ibeacon/wechatIndex?type=currentBook&isFlag=373oS4&openid=373145D851109991C00A66CA578BCFCAA3CB8C56FC61E67FF47FF1E4D4AF0A06&account=27ED935CBF2EF6F955AE64FCF3C1819C&upass=3689F3B2B5A4A08FE545AFC75C3D0F1BD09599D0C281490FBB6C6D5E314D5B12&headimgurl=&nickname=&sign=e3aa08f1f4726038a05513428aa82326',
            'roomid':'10',
             'buildid':'1',
             'seatid':'5647',
            'start':'480',
            'end':'1290',
        },
}

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
date = tomorrow.strftime('%Y-%m-%d')

# @retry(wait_fixed=600000)
def order(name):
    address=account[name]['address']
    seatid=account[name]['seatid']
    start=account[name]['start']
    end=account[name]['end']
    result='fail'
    book = 'http://seat.yangtzeu.edu.cn/libseat-ibeacon/saveBook?seatId=' + seatid + '&date=' + date + '&start=' + start + '&end=' + end + '&type=1'
    while int(time.strftime("%H%M%S")) < 214000: pass
    while result=='fail':
        try:
            s = requests.session()
            s.get(address,headers=header,allow_redirects=False)
            # cookie=res.cookies.values()
            # headert['Cookie']='JSESSIONID='+cookie[0]
            # violation_url='http: // seat.yangtzeu.edu.cn / libseat - ibeacon / getUserViolations'
            # headers['Referer']=new
            # violation=s.get(violation_url,headers=headers)
            # headers['Referer']='http://seat.yangtzeu.edu.cn/libseat-ibeacon/activitySeat'
            # roominfo='http://seat.yangtzeu.edu.cn/libseat-ibeacon/seatdetail?linkSign=activitySeat&roomId='+roomid+'&date='+date+'&buildId='+buildid
            # act='http://seat.yangtzeu.edu.cn/libseat-ibeacon/nowActivity'
            # headert['Referer']=act
            # history='http://seat.yangtzeu.edu.cn/libseat-ibeacon/getUserBookHistory'
            # h=s.get(history,headers=headert)
            # detail='http://seat.yangtzeu.edu.cn/libseat-ibeacon/seats?roomId=3&date=2021-03-28&linkSign=activitySeat&endTime='
            # seats=s.get(detail, headers=headers)
            # content=json.loads(seats.content.decode())
            # gg=content['params']['seats']
            # df=pd.DataFrame(gg)
            # df=df.dropna()
            # free=df[df['status']=='FREE']
            # print('空余座位：',free['name'])

            # seatname=input('输入预约座位号:')
            # seatid=df[df['name']==seatname]['seatid']

            # stime='http://seat.yangtzeu.edu.cn/libseat-ibeacon/loadStartTime?seatId=1209&date=2021-03-28'
            # freetime=s.get(stime,headers=headers)
            # freetime=json.loads(freetime.content.decode())

            # cancle='http://seat.yangtzeu.edu.cn/libseat-ibeacon/cancleBook?bookId=153546'
            # headers['Accept']='*/*'
            # headers['X-Requested-With']= 'XMLHttpRequest'
            save=s.get(book)
            result=json.loads(eval(save.text))['status']
        except:
            continue
    print(name,result)

if __name__ == '__main__':
    names=['xj','wt','djh','lyz','lly','syq','cjl']
    # start = time.perf_counter()  # 返回系统运行时间
    for name in names:
        # order(name)
        threading.Thread(target=order,args=(name,)).start()

    # end = time.perf_counter()
    # print('用时：{:.4f}s'.format(end - start))