import xlwt as xlwt

from pharmacy.mongoclient import MongoClient
import requests

def run(outputpath):
    client = MongoClient()
    data = client.find_many()
    title = ['商品名称', '通用名称', '厂家名称', '规格', '批准文号', '实际价格', '参考价', '网址', '药店名称'];
    list = []
    for d in data:
        v = {'商品名称': d['goodsName'], '通用名称': d['genericName'],
             "厂家名称": d['manufacturer'] if 'manufacturer' in d else '', "规格": d['specifications'], "批准文号": d['approvalNumber']
            , "实际价格": d['actualPrice'], "参考价": d['referencePrice'], "网址": d['url'], "药店名称": d['shopName']}
        list.append(v)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('商品数据', cell_overwrite_ok=True)
    for index in range(0, len(title)):
        sheet.write(0, index, title[index])
    for row in range(1, len(list) + 1):
        for col in range(0, len(title)):
            key = title[col]
            value = list[row - 1][key]
            sheet.write(row, col, value)
    workbook.save(outputpath)
    print('导出成功')


run('C:/Users/Administrator/Desktop/商品数据.xlsx')