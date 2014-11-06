#!/usr/local/bin/python3

import urllib.request
import json
import time
import webbrowser
"""
    query 12306 to get train D info
"""

start_time = '17:00'
end_time = '19:00'
date = '2014-11-09'

def main():
    print(time.ctime(time.time()))

    if len(date) != 0:
        queryInfo(date)

        time.sleep(60)
        main()

def filterDtrainByTimeAndSeat(train):
    traininfo = train.get('queryLeftNewDTO')
    trainType = traininfo.get('station_train_code')
    ctime = time.strptime(traininfo.get('start_time'), '%H:%M')
    stime = time.strptime(start_time, '%H:%M')
    etime = time.strptime(end_time, '%H:%M')
    seat = traininfo.get('ze_num')
    if stime < ctime < etime and trainType[0] == 'D' and (seat != '无' and seat != '--'):
        return True
    return False

def showInfo(train_list):
    print('符合条件的车次共{0}条'.format(len(train_list)))
    if train_list:
        for train in train_list:
            traininfo = train.get('queryLeftNewDTO')
            print(traininfo.get('station_train_code') + ' ' + traininfo.get('start_time'))

        # open browser if match, and stop query
        webbrowser.open('https://kyfw.12306.cn/otn/leftTicket/init')
    else:
        print('没有匹配的车次')
    print('\n')

def queryInfo(date):
    """
        根据日期查询12306列车数据
    """
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={0}&leftTicketDTO.from_station=NGH&leftTicketDTO.to_station=HGH&purpose_codes=ADULT'.format(date)


    res = urllib.request.urlopen(url)

    res_str = res.read().decode('utf-8')

    res_json = json.JSONDecoder().decode(res_str)
    if 'data' in res_json:
        train_list = res_json['data']

        if train_list:
            dtrain_list = list(filter(filterDtrainByTimeAndSeat, train_list))
            showInfo(dtrain_list)
        else:
            print('无匹配数据')
    else:
        print('无匹配数据')

def parseConfig():
    configFile = open('config.txt')
    content = configFile.read()
    configJson = json.JSONDecoder().decode(content)
    configFile.close()
    return configJson

if __name__ == '__main__':
    config = parseConfig()
    start_time = config.get('start')
    end_time = config.get('end')
    date = config.get('date')
    main()
