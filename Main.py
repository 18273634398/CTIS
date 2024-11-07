import heapq
import time
import pymysql


# 定义景点类
class Spot:
    def __init__(self, code, name, description):
        self.code = code  # 景点代号
        self.name = name  # 景点名称
        self.description = description  # 景点简介

# 定义无向图类
class CampusMap:
    def __init__(self):
        self.spots = {}  # 景点字典（存储的是景点的代号）
        self.paths = {}  # 路径字典

    # 添加景点
    def add_spot(self, code, name, description):
        spot = Spot(code, name, description)
        self.spots[code] = spot

    # 添加路径
    def add_path(self, code1, code2, length):
        if code1 not in self.paths:   # 初始化该景点的路径字典为列表 用于存储该景点到其他景点的距离（以元组形式）
            self.paths[code1] = []
        if code2 not in self.paths:
            self.paths[code2] = []
        self.paths[code1].append((code2, length))
        self.paths[code2].append((code1, length))

    # 查询景点信息
    def query_spot_info(self, code):
        if code in self.spots:
            spot = self.spots[code]
            return f"景点名称: {spot.name}, 代号: {spot.code}, 简介: {spot.description}"
        return "景点不存在"

    # 根据景点名查询景点ID
    def query_spot_id(self, name):
        for code in self.spots:
            if self.spots[code].name == name:
                return code

    # 根据景点ID查询景点名
    def query_spot_name(self, code):
        if code in self.spots:
            spot = self.spots[code]
            return spot.name


    def shortest_path(self, start, end):
        # 首先检查输入的起点和终点是否存在于路径图中
        if start not in self.paths or end not in self.paths:
            return "无效的景点代号"  # 如果起点或终点不在图中，返回错误信息

        # 初始化距离表，每个景点的初始距离都设置为无穷大（表示不可达）
        distances = {spot: float('inf') for spot in self.spots}
        distances[start] = 0  # 起点的距离为0，因为从自己到自己距离为0

        # 创建一个优先队列，初始时将起点放入队列，优先级为0（即距离）
        priority_queue = [(0, start)]

        # 初始化前驱节点表，用于存储每个节点的最优前驱节点
        previous_nodes = {spot: None for spot in self.spots}

        # 当优先队列不为空时，执行循环
        while priority_queue:
            # 从优先队列中取出当前距离最小的节点
            current_distance, current_spot = heapq.heappop(priority_queue)

            # 如果当前节点的距离大于已经记录的距离，说明它不是最优路径，跳过
            if current_distance > distances[current_spot]:
                continue

            # 遍历当前节点的邻居节点
            for neighbor, weight in self.paths[current_spot]:
                # 计算从当前节点到邻居节点的距离
                distance = current_distance + weight

                # 如果新的距离比之前记录的距离小，更新距离表和前驱节点表
                if distance < distances[neighbor]:
                    distances[neighbor] = distance  # 更新距离
                    previous_nodes[neighbor] = current_spot  # 记录前驱节点
                    # 将邻居节点加入优先队列中，按照新的距离排序
                    heapq.heappush(priority_queue, (distance, neighbor))

        # 构建从终点到起点的路径
        path = []
        current = end
        while current is not None:  # 从终点回溯到起点
            path.append(current)
            current = previous_nodes[current]
        path = path[::-1]  # 将路径反转为从起点到终点

        # 如果终点距离仍然是无穷大，说明没有可达路径
        if distances[end] == float('inf'):
            return "无可达路径"

        # 返回最短路径和对应的距离
        return path, distances[end]




def init(db,campus):
    # 添加景点
    # 连接数据库
    cursor = db.cursor()
    # 查询景点信息
    sql = "SELECT code, name, description FROM ctis_info"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        code, name, description = row
        campus.add_spot(code, name, description)
    # 查询路径信息
    sql = "SELECT code_from, code_to, distance FROM ctis_distance"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        code1, code2, length = row
        campus.add_path(code1, code2, length)



# 主程序启动
db = pymysql.connect(host='localhost', user='root', password='lushangwu;2004', db='app', charset='utf8')
campus = CampusMap()
init(db,campus)
while True:
    print("\n\n\n=====================")
    print("欢迎使用校园导游系统CTIS\n1.查询最短路径\n2.查询景点信息\n3.添加景点信息\n4.退出系统\n输入数字编号进入功能")
    try:
        function = int(input("--------------------------\n请输入功能:"))
    except ValueError:
        print("输入非数值信息，请重试")
        continue
    if function == 1:
        # 信息输入
        start = input("请输入起点：")
        end = input("请输入终点：")
        # 信息有效性检测
        startID = campus.query_spot_id(start)
        endID = campus.query_spot_id(end)
        if startID in campus.spots and endID in campus.spots:
            path, length = campus.shortest_path(startID, endID)
            print(f"最短路径: {' -> '.join(path)}, 路径长度: {length}")
            for i in range(len(path)):
                if i==0:
                    print(f"【起点】{campus.query_spot_name(path[i])} -> ",end='')
                elif i<len(path)-1:
                    print(f"{campus.query_spot_name(path[i])} -> ",end='')
                else:
                    print(f"【终点】{campus.query_spot_name(path[i])}")
            time.sleep(1)
        else:
            print("输入景点名不在数据库中，程序重启，请重试")
    elif function == 2:
        place = input("请输入景点名：")
        placeID = campus.query_spot_id(place)
        print(campus.query_spot_info(placeID))
        time.sleep(1)
    elif function == 3:
        code = input("请输入景点代号：")
        name = input("请输入景点名称：")
        description = input("请输入景点简介：")
        campus.add_spot(code, name, description)
        # 写入数据库
        cursor = db.cursor()
        sql = "insert into ctis_info ( code, name, description ) values (%s, %s, %s)"
        cursor.execute(sql, (code, name, description))
        print(f"景点{name}({code})添加成功")
        print("是否需要添加路径？(y/n)")
        path = input()
        if path == 'y' or path == 'Y':
            while True:
                code1 = input("请输入起点代号：")
                code2 = input("请输入终点代号：")
                length = eval(input("请输入路径长度："))
                campus.add_path(code1, code2, length)
                # 写入数据库
                cursor = db.cursor()
                sql = "insert into ctis_distance (code_from, code_to, distance) values(%s, %s, %s)"
                cursor.execute(sql, (code1, code2, length))
                sql = "insert into ctis_distance (code_from, code_to, distance) values(%s, %s, %s)"
                cursor.execute(sql, (code2, code1, length))
                print(f"路径{code1} -> {code2} 长度：{length} \n路径{code2} -> {code1} 长度：{length} \n添加成功")
                print("是否继续添加路径？(y/n)")
                path = input()
                if path == 'n':
                    db.commit()
                    campus = None
                    campus = CampusMap()
                    init(db,campus) # 重新载入数据
                    break
        else:
            db.commit()
            campus = None
            campus = CampusMap()
            init(db,campus) # 重新载入数据
    elif function == 4:
        print("程序结束")
        break
    else:
        print("输入的功能数字选项异常，程序终止")
        exit(0)





