import requests
from bs4 import BeautifulSoup
import sys
from urllib import parse
import csv

url1 = 'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station='
url2 = '&stname='
url3 = '&datepicker=2020-'
stations = {'基隆': '466940', '臺北': '466920', '竹子湖': '466930', '淡水': '466900', '板橋': '466880',
            '蘇澳': '467060', '宜蘭': '467080', '新屋': '467050', '新竹': '467571', '梧棲': '467770',
            '臺中': '467490', '日月潭': '467650', '玉山': '467550', '嘉義': '467480', '阿里山': '467530',
            '永康': '467420', '臺南': '467410', '高雄': '467440', '恆春': '467590', '大武': '467540',
            '臺東': '467660', '花蓮': '466990'
            }
'''
'基隆': '466940', '臺北': '466920', '竹子湖': '466930', '淡水': '466900', '板橋': '466880',
            '蘇澳': '467060', '宜蘭': '467080', '新屋': '467050', '新竹': '467571', '梧棲': '467770',
            '臺中': '467490', '日月潭': '467650', '玉山': '467550', '嘉義': '467480', '阿里山': '467530',
            '永康': '467420', '臺南': '467410', '高雄': '467440', '恆春': '467590', '大武': '467540',
            '臺東': '467660', '花蓮': '466990'
            '''
weather = {}
# 各測站
for key in stations.keys():
    loc = {}
		##網址編碼
    stationName = parse.quote(str(parse.quote(key)))
    value = stations.get(key)
		#12個月分
    for month in range(1, 13):
        # range(1, 13)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
				#爬取網址
        url = url1 + value + url2 + str(stationName) + url3 + str(month)
        response = requests.get(url)
        htmlFile = BeautifulSoup(response.text, 'html.parser')
        dates = htmlFile.find('tbody').find_all('tr')
				# 抓取當月份每日均溫
        for i in range(3, len(dates)):
            date = '2020' + month + dates[i].find('td').text
						## 去除文字空格編碼\xa0
            temperature = str(dates[i].find_all('td')[7].text).replace(u'\xa0', '')
						## X值(空值)去除，以前一日均溫替換
            if 'X' in temperature:
                temp_date = '2020' + month + dates[i-1].find('td').text
                temperature = loc[temp_date]
            loc[date] = temperature
    weather[key] = loc
# 寫入CSV
rows = list(weather.values())
fieldnames = rows[0].keys()# 日期
with open('weather_loc_clean.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)