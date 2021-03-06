from __future__ import print_function
from dbClient.mysqlClient import MysqlClient
from dbClient.mongoClient import MongoClient
from record.record import Record

# mysql 连接信息
mysqlConn = {
    'host': '139.159.198.104',
    'port': 3306,
    'db': 'gpshisdata',
    'userName': 'root',
    'password': 'Cesiumai-2018@#'
}

# mongodb 连接信息
# mongoConn = {
#     'host': '121.37.247.7',
#     'port': 27017,
#     'db': 'gpshisdata',
#     'authDb': 'gpshisdata',
#     'userName': 'gpshisdata2',
#     'password': 'gpshisdata2'
# }

# local
mongoConn = {
    'host': '192.168.10.41',
    'port': 27017,
    'db': 'gpshisdata',
    'authDb': 'admin',
    'userName': 'admin',
    'password': 'openstack'
}


# production
# mongoConn = {
#     'host': '10.0.1.186',
#     'port': 8635,
#     'db': 'gpshisdata',
#     'authDb': 'gpshisdata',
#     'userName': 'gphis',
#     'password': 'Openstack#2020'
# }

# 每次处理的数据量
everyCount = 10000

# 存储处理数据历史记录的文件地址
recordPath = 'six.db'

if __name__ == '__main__':
    sqlDb = MysqlClient(mysqlConn)
    mongoDb = MongoClient(mongoConn)
    record = Record(recordPath)

    # 获取tableName
    tableNameList = sqlDb.getAllTableName('tb_vehicle_status_his_20_06_12')
    print(tableNameList)

    for tableName in tableNameList:
        print("开始迁移表：%s" % tableName)
        total = sqlDb.getAllRowCount(tableName)
        print("%s数据总量：%d" % (tableName, total))

        # 计数
        startIndex = 0
        sum = 0

        # 后期记录表中的记录
        if record.findKeyExist(tableName.replace('_', '')):
            # 存在该记录, 取出处理的数据量
            handleNum = record.getHandledNum(tableName.replace('_', ''))
            if handleNum == total:
                # 全部数据已处理
                continue
            else:
                startIndex = handleNum
                sum = handleNum

        print("%s startIndex= %d, sum = %d" % (tableName, startIndex, sum))

        while startIndex < total:
            limit = everyCount
            if startIndex + limit > total:
                limit = total - startIndex
            # 获取数据
            count, data = sqlDb.getDataFromTable(tableName, startIndex, limit)
            print(count)
            for item in data:
                # print(item['f_time'], item['id_terminal'], item['gps_time'])
                # 更新mongodb 库
                mongoDb.updateTimeByCondition(tableName,
                                              {"f_time": item["f_time"], "id_terminal": item['id_terminal']},
                                              item['gps_time'])

            sum += count
            print("表%s插入数据量sum=%d" % (tableName, sum))
            # 更新处理数据入库
            record.updateHandledNum(tableName.replace('_', ''), sum)
            startIndex += limit

        if sum != total:
            print("获取数据总量不正确")
        else:
            print("%s插入全部数据" % tableName)

