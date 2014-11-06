#!/usr/bin/python3

import urllib.request
import json
"""
    query 12306 to get train D info
"""


def main():
    date = input('日期：')
    if len(date) != 0:
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={0}&leftTicketDTO.from_station=NGH&leftTicketDTO.to_station=HGH&purpose_codes=ADULT'.format(date)

        res = urllib.request.urlopen(url)

        res_str = res.read().decode('utf-8')

        res_json = json.JSONDecoder().decode(res_str)
        if 'data' in res_json:
            res_data = res_json['data']
            print(res_data)
        else:
            print('该日期无数据\n')

        main()

if __name__ == '__main__':
        main()
