 # mongodb数据保存到excel
import pymongo
import pandas as pd

# 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
db = client['stock']
jobs = db['sheet_stock']

# 加载数据到pandas
data = pd.DataFrame(list(jobs.find()))

# 删除_id字段
del data['_id']

# 选择要显示的字段
data = data[['sid', 'year', 'key1', 'key2', 'key3']]
# print(data)

# Dataframe写入到excel
file_path = r'./output_data.xlsx'
writer = pd.ExcelWriter(file_path)
data.to_excel(writer, columns=['sid', 'year', 'key1', 'key2', 'key3'],
              index=False, encoding='utf-8', sheet_name='Sheet')
writer.save()