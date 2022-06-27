import requests
import json



def main():
    url = 'https://weatherquery.api.bdymkt.com/weather/query/by-area'
    params = {}
    params['area'] = '长沙'
    params['areaId'] = ''

    headers = {

        'Content-Type': 'application/json;charset=UTF-8',
        'X-Bce-Signature': 'AppCode/0f08817485414350b13d8e724cdca59c'
    }
    r = requests.request("POST", url, params=params, headers=headers)
    r = json.loads(r.text)
    if(r['code'] == 200):
        print('获取成功')
        weather = r['data']
        message = '明日天气：%s,温度%s-%s' % (weather['dayWeathers']
                                       [1]['day_weather'], weather['dayWeathers']
                                       [1]['night_low_temperature'], weather['dayWeathers']
                                       [1]['day_high_temperature'])
        return message

