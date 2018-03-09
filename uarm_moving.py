# -*- coding: utf-8 -*
import pyuarm
import time

#读取数据点
def read_data():
    #首先读取下面路径中的文件，得到要写字的点
    filename = unicode(r'd:\zqj\UarmWritng.txt', 'utf-8')
    with open(filename, "r") as f0:
        filepath = f0.readline().strip()
    f0.close
    p = [['0', '120']]
    #首先加入一个起始点
    points = [[0, 140, 140]]
    points.append([100, 140, 140])
    points.append([100, 140, 100])
    points.append([100, 140, 140])
    points.append([100, 140, 100])
    points.append([100, 140, 140])
    point1 = [1, 1, 1]
    point2 = [0, 0, 0]
    #获得要写的字的点集合的路径，读取这些点到一个list中
    with open(filepath, "r") as f:
        for line in f.readlines():
            if line:
                a = line.split()[0:2]
                point1 = [int(-60 + 0.4 * int(a[0:1][0])), int(260 - 0.4 * int(a[1:2][0])), 140]
                # 这里判断该起点是否为上一个终点，如果是同一个点，则删除最后一个点
                if (point1[0] == point2[0] and point1[1] == point2[1]):
                    points.pop()
                #如果不是同一点，则继续读入
                else:
                    points.append(point1)
                    #这里(60 - 0.4 * int(a[0:1][0])是将得到的点转换到机械臂坐标下，
                    # 机械臂坐标左上角起点为（60,140），右下角为（-60,260）
                    point1 = [int(-60 + 0.4 * int(a[0:1][0])), int(260 - 0.4 * int(a[1:2][0])), 100]
                    points.append(point1)
                b = line.split()[2:4]
                point2 = [int(-60 + 0.4 * int(b[0:1][0])), int(260 - 0.4 * int(b[1:2][0])), 100]
                points.append(point2)
                point2 = [int(-60 + 0.4 * int(b[0:1][0])), int(260 - 0.4 * int(b[1:2][0])), 140]
                points.append(point2)
                # print points
    f.close()
    #最后机械臂回到起始点位置
    points.append([0, 140, 140])
    return points

#根据读取数据移动机械臂
def moving():
    #获取读入的点集合
    poionts = read_data()
    for each_point in poionts:
        print  each_point
    #机械臂初始化
    uarm = pyuarm.UArm()
    time.sleep(1)
    #写每个点
    for each_point in poionts:
        print each_point
        #蘸墨水
        if (each_point[0] >60):
            uarm.set_position(each_point[0], each_point[1], each_point[2], 40)
            time.sleep(1.2)
        #写字
        else:
            uarm.set_position(each_point[0], each_point[1], each_point[2], 100)
            time.sleep(1)
    #释放机械臂并断开连接；如果上面移动出错，无法执行uarm.set_servo_detach()语句
    uarm.set_servo_detach()
    uarm.disconnect()
    return

#测试
if __name__ == '__main__':
    moving()
