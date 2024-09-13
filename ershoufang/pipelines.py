# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql

class ErshoufangPipeline:
    def process_item(self, item, spider):
        return item
class ExcelPipeline:
    def __init__(self) -> None:
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = 'ershoufang'
        self.ws.append(['title', 'location', 'price', 'house_type', 'beike_id'])
    def close_spider(self, spider):
        self.wb.save('ershoufang.xlsx')
    def process_item(self, item, spider):
        title = item.get('title', '')
        location = item.get('location', '')
        price = item.get('price', '')
        house_type = item.get('house_type', '')
        beike_id = item.get('beike_id', '')
        self.ws.append([title, location, price, house_type, beike_id])
        return item
    
    
class DbPipeline:
    def __init__(self) -> None:
        self.conn = pymysql.connect(
            host='',
            user='',
            port=3306,
            password='',
            database='',
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()
        self.data=[]
    def close_spider(self, spider):
        if len(self.data)>0:
            self.cursor.executemany("insert into ershoufang(title, location, price, house_type, beike_id) values(%s, %s, %s, %s, %s)", self.data)
        self.conn.commit()
        self.conn.close()
    def process_item(self, item, spider):
        title = item.get('title', '')
        location = item.get('location', '')
        price = item.get('price', '')
        house_type = item.get('house_type', '')
        beike_id = item.get('beike_id', '')
        self.data.append([title, location, price, house_type, beike_id])
        if len(self.data) == 25:
            self.cursor.executemany("insert into ershoufang(title, location, price, house_type, beike_id) values(%s, %s, %s, %s, %s)", self.data)
            self.data.clear()
        return item