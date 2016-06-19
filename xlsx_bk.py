# -*- coding: utf-8 -*-
"""
更新twse_list.csv方法
下載http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php#
用記事本移除頭尾
另外儲存UTF-8

vi 搜尋到的行 整行刪除
:g/[要搜尋的字串]/d
刪除F 相關大陸股票


@author: tim
"""

import urllib, re
import requests
import xlsxwriter
import csv 
import time



"""
抓取http://mops.twse.com.tw/mops/web/t05st10_ifrs公開資訊觀測站
各股累積營運情況
2013.01後採用IFRSs後之月營業收入資訊

@author: tim
"""


def cumulative_revenues(co_id, yearmonth, year, month):
    """
	輸入:
	co_id = '8383' 股票代碼
	yearmonth = '10312'
	year = 103
	month = '01'
	http://mops.twse.com.tw/mops/web/t05st10_ifrs
	回傳list:['目前累積營收增減百分比']

	"""
    r=requests.post("http://mops.twse.com.tw/mops/web/t05st10_ifrs")



	#選歷史資料後按搜尋
    payload = {
    'encodeURIComponent':'1',
	'run':'	Y',
	'step':'0',
	'yearmonth':yearmonth,
	'TYPEK':'sii',
	'co_id':co_id,
	'off':'1',
	'year':year,
	'month':month,
	'firstin':'true'}

    r = requests.get("http://mops.twse.com.tw/mops/web/t05st10_ifrs", params=payload)
           
 
    optionUrl = r.url
    html = urllib.urlopen(optionUrl)  #open file-like object
    regexp = re.compile(r"<TD class='even' style='text-align:right !important;'>&nbsp;(?P<file>.*)</TD></TR>")
    print r.url

    i = 0 #只抓第四筆符合資料
    for line in html.readlines():
        result = regexp.search(line)
        if result != None:
            money = result.group('file')
            i+=1
        if i==2:
            last_year_revenues = money.split()
			
        if i==4:
            this_year_cumulative_revenues= money.split()
            time.sleep(20)
            return (last_year_revenues,this_year_cumulative_revenues)
            




if __name__ == "__main__":
    #testa = cumulative_revenues('6462','10505','105','05')
    

        
    """
    with open('twse_list.csv', 'rb') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=',')
         for row in spamreader:
             print row[0] ,row[1]
    """


    workbook = xlsxwriter.Workbook('Stock_A.xlsx')

    bold = workbook.add_format({'bold': 1})


    worksheet = workbook.add_worksheet()

    worksheet.write('A1', '代號')
    worksheet.write('B1', '股票')
    worksheet.write('C1', '比較去年當月營收')
    worksheet.write('D1', '今年累積營收')


    with open('twse_list.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i=1
        for row in spamreader:
            if row[1][0] == 'F':
                time.sleep(20)
                pass
            else:
                price = cumulative_revenues(row[0],'10505','105','05')
                worksheet.write(i,0,row[0])
                worksheet.write(i,1,row[1])
                try:
                    worksheet.write(i,2,price[0][0])
                except:
                    worksheet.write(i,2,"ERROR")
                try:
                    worksheet.write(i,3,price[1][0])
                except:
                    worksheet.write(i,3,"ERROR")
            i+=1
            print row[0],row[1]
     #worksheet.write(2, 0, 123)

    workbook.close()
     
    #print testa[0]

	
