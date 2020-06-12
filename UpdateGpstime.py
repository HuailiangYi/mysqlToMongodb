from dbClient.mongoClient import MongoClient
from record.record import  Record

mongoConn = {
    'host': '10.0.1.186',
    'port':8635 ,
    'db': 'gpshisdata',
    'authDb': 'gpshisdata',
    'userName': 'gphis',
    'password': 'Openstack#2020'
}

# local
# mongoConn = {
#     'host': '192.168.10.41',
#     'port': 27017,
#     'db': 'gpshisdata',
#     'authDb': 'admin',
#     'userName': 'admin',
#     'password': 'openstack'
# }



# 每次处理的数据量
everyCount = 10000

# 存储处理数据历史记录的文件地址
recordPath = 'index.db'

if __name__ == '__main__':
    mongoDb = MongoClient(mongoConn)
    record = Record(recordPath)

    collection_names = mongoDb.getDocument("tb_vehicle_status_his")
    print("all collections: {}".format(collection_names))

    for name in  collection_names:
        if name in collection_names:
            if name != "tb_vehicle_status_his_20_06_12":
                print("更新表格：", name)
                mongoDb.updateTime(name)


