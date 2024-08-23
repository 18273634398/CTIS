import heapq

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
    campus.add_spot('Bt', '图书馆', '藏书丰富的图书馆')
    campus.add_spot('Bx', '湘江楼', '辅助的教学场所，5层以上为教师办公室专用')
    campus.add_spot('Bs', '实验楼', '主要实验室分布场所，共6层')
    campus.add_spot('Cc', '萃雅食堂', '主要的就餐场所')
    campus.add_spot('Pcy', '萃雅园区', '学生宿舍楼群')
    campus.add_spot('Pxd', '贤德园区', '学生宿舍楼群')
    campus.add_spot('Br', '日新楼', '主要的教学场所')
    campus.add_spot('Bz', '至诚楼', '主要的教学场所')
    campus.add_spot('Bl', '乐知楼', '主要的教学场所')
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
    campus.add_path()

    return campus




# 主程序启动
campus = init()
print(campus.query_spot_info('B'))

# 查询最短路径
path, length = campus.shortest_path('A', 'E')
print(f"最短路径: {' -> '.join(path)}, 路径长度: {length}")



