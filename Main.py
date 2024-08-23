import heapq
import time


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


    # Dijkstra算法求最短路径
    def shortest_path(self, start, end):
        if start not in self.paths or end not in self.paths:
            return "无效的景点代号"

        # 初始化距离表
        distances = {spot: float('inf') for spot in self.spots}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous_nodes = {spot: None for spot in self.spots}

        while priority_queue:
            current_distance, current_spot = heapq.heappop(priority_queue)

            if current_distance > distances[current_spot]:
                continue

            for neighbor, weight in self.paths[current_spot]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_spot
                    heapq.heappush(priority_queue, (distance, neighbor))

        # 构建路径
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path = path[::-1]  # 逆序

        if distances[end] == float('inf'):
            return "无可达路径"
        return path, distances[end]

def init():
    campus = CampusMap()
    # 添加景点
    campus.add_spot('Dx', '西门', '学校的西门')
    campus.add_spot('Btsg', '图书馆', '藏书丰富的图书馆')
    campus.add_spot('Bxj', '湘江楼', '辅助的教学场所，5层以上为教师办公室专用')
    campus.add_spot('Bsy', '实验楼', '主要实验室分布场所，共6层')
    campus.add_spot('Ccy', '萃雅食堂', '主要的就餐场所')
    campus.add_spot('Pcy', '萃雅园区', '学生宿舍楼群')
    campus.add_spot('Pxd', '贤德园区', '学生宿舍楼群')
    campus.add_spot('Brx', '日新楼', '主要的教学场所')
    campus.add_spot('Bzc', '至诚楼', '主要的教学场所')
    campus.add_spot('Blz', '乐知楼', '主要的教学场所')
    campus.add_spot('B2', '二办公楼', '学校行政部门办公场所')
    campus.add_spot('Q', '两桥', '启真桥与楚枫桥，作为连接湖南工商大学南校区北区与南区的通道')
    campus.add_spot('By', '阳光服务大厅', '学校提供的为学生服务的中心')
    campus.add_spot('Db', '北门', '学校最靠近地铁的地方，一般在新生季将在此处设置迎新广场')
    campus.add_spot('Dd', '东门', '学校东门，外面有很多小吃、饭店')
    campus.add_spot('Plhl', '老虎岭', '学校景点之一')
    campus.add_spot('Pxj', '咸嘉园区', '学生宿舍楼群')
    campus.add_spot('Pln', '岭南园区', '学生宿舍楼群')
    campus.add_spot('Ddn', '东南门', '学校东南门')

    # 添加路径
    campus.add_path('Ddn','Pln',0.5)
    campus.add_path('Pln','Pxj',3)
    campus.add_path('Pln','Plhl',1.5)
    campus.add_path('Pxj','Plhl',2)
    campus.add_path('Pxj','Dd',0.5)
    campus.add_path('Dd','Blz',1)
    campus.add_path('Blz','Db',1)
    campus.add_path('Blz','B2',1)
    campus.add_path('B2','Db',0.5)
    campus.add_path('B2','By',0.7)
    campus.add_path('Blz','By',1.5)
    campus.add_path('B2','Q',1)
    campus.add_path('By','Q',1)
    campus.add_path('Q','Bzc',0.5)
    campus.add_path('Q','Bxj',0.5)
    campus.add_path('Bxj','Dx',0.5)
    campus.add_path('Bxj','Bsy',3)
    campus.add_path('Bxj','Ccy',3)
    campus.add_path('Bxj','Pcy',3)
    campus.add_path('Bsy','Ccy',1)
    campus.add_path('Pcy','Ccy',1)
    campus.add_path('Pcy','Pxd',7)
    campus.add_path('Pcy','Brx',0.5)
    campus.add_path('Brx','Bxj',1.2)
    campus.add_path('Btsg','Bxj',0.9)
    campus.add_path('Bzc','Bxj',0.8)
    campus.add_path('Bzc','Btsg',0.5)
    campus.add_path('Brx','Btsg',0.5)
    campus.add_path('Brx','Pxd',4)

    return campus




# 主程序启动
campus = init()
print("湖南工商大学南校区景点一览表\n"
      "--------------------------\n"
      "1，东南门\n"
      "2.岭南园区\n"
      "3.老虎岭\n"
      "4.贤德园区\n"
      "5.东门\n"
      "6.乐知楼\n"
      "7.阳光服务大厅\n"
      "8.北门\n"
      "9.二办公室\n"
      "10.两桥\n"
      "11.至诚楼\n"
      "12.湘江楼\n"
      "13.图书馆\n"
      "14.西门\n"
      "15.日新楼\n"
      "16.萃雅园区\n"
      "17.萃雅食堂\n"
      "18.实验楼\n"
      "19.贤德园区")
print("--------------------------\n8秒后进入主程序")
time.sleep(8)
while True:
    print("\n\n\n=====================")
    print("欢迎使用校园导游系统CTIS\n1.查询最短路径\n2.查询景点信息\n3.退出系统\n输入数字编号进入功能")
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
            time.sleep(5)
        else:
            print("输入景点名不再数据库中，程序重启，请重试")
            time.sleep(5)
    elif function == 2:
        place = input("请输入景点名：")
        placeID = campus.query_spot_id(place)
        print(campus.query_spot_info(placeID))
        time.sleep(5)
    elif function == 3:
        print("程序结束")
        break
    else:
        print("输入的功能数字选项异常，程序终止")
        exit(0)





