import pymysql
import pymongo


# insert data from spider-object
def get_connector_mongo0():
    client = pymongo.MongoClient('localhost', 27017)
    book_weather = client['stock']  # 创建名为 "stock" 的数据库
    sheet_weather = book_weather['sheet_party']  # 在"weather"数据库中建表"sheet_weather"
    return sheet_weather

def get_connector_mongo1():
    client = pymongo.MongoClient('localhost', 27017)
    book_weather = client['stock']  # 创建名为 "stock" 的数据库
    sheet_weather = book_weather['sheet_info']  # 在"weather"数据库中建表"sheet_weather"
    return sheet_weather

def get_connector_mysql():
    db = pymysql.connect("localhost", "root", "123456", "stock")
    cursor = db.cursor()
    return cursor
