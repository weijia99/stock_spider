import pymysql
import pymongo


# insert data from spider-object
def get_connector_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    book_weather = client['stock']  # 创建名为 "stock" 的数据库
    sheet_weather = book_weather['sheet_stock']  # 在"weather"数据库中建表"sheet_weather"
    return sheet_weather


def get_connector_mysql():
    db = pymysql.connect("localhost", "root", "123456", "stock")
    cursor = db.cursor()
    return cursor
