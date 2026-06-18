#================================
# TSPを貪欲法+2optで実装したコード
# python3 greedy.py input_0.csv > output_0.csv
#================================

from operator import index
from pickletools import optimize
import sys
import math

from common import print_tour, read_input, format_tour

# citiesの各位置情報にインデックスを付与する関数
def give_index_cities(cities):
    index_cities = [] # 各要素：(index, [x,y])
    for i in range(len(cities)):
        index_cities.append((i, list(cities[i])))
    return index_cities


# 2点間のユーグリッド距離を求める関数
def calurate_euclidean_distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)


# 各都市の距離を求める関数
def calcurate_distance(cities):
    num_cities = len(cities)
    # n×nの行列の初期化: i行j列はiからjへのユーグリッド距離を表す
    distance_matrix = [[0]*num_cities for _ in range(num_cities)] 

    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = calurate_euclidean_distance(cities[i], cities[j]) # ユーグリッド距離を求める
            distance_matrix[i][j] = distance_matrix[j][i] = distance # iからj、jからiの距離を記録
    return distance_matrix

# 貪欲法で経路を求める関数
def greedy(cities):
    # Build a trivial solution.
    # Visit the cities in the order they appear in the input.
    dist = calcurate_distance(cities) # 都市間のユーグリッド距離を求める
    index_cities = give_index_cities(cities) #都市の位置と元のインデックスを対応付ける
    current_city = 0 #スタートを設定
    unvisited = set(range(1, len(cities))) # 訪れていない都市のインデックスを格納
    path = [index_cities[0]] # どのような経路で回るか格納（インデックスを格納する）

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        unvisited.remove(next_city)
        path.append(index_cities[next_city])
        current_city = next_city

    return path

def two_opt(cities): #入力：(元のindex, [x,y])で回る順に格納されている
    # path = [cities[0][0]] # この関数から導いた経路
    len_cities = len(cities)

    for i in range(len_cities-1):
        for j in range(i+1, len_cities-1):
            if (i == cities[j+1][0]) | (j == cities[i+1][0]):
                continue
            # 入れ替える前の距離
            before = calurate_euclidean_distance(cities[i][1], cities[i+1][1]) + calurate_euclidean_distance(cities[j][1], cities[j+1][1])
            # 入れ替えた後の距離
            after = calurate_euclidean_distance(cities[i][1], cities[j][1]) + calurate_euclidean_distance(cities[i+1][1], cities[j+1][1])

            if before > after: #入れ替えたほうが距離が短くなる時
            #i+1番目からj番目までの間のノードを逆順にする必要がある
                start, goal = i+1, j
                cities[start:goal+1] = cities[goal:start-1:-1]
                
        # path = []          
        # for c in cities:
        #     path.append(c[0])
    
    return cities

def solve_tsp(cities):
    optimized_cities = greedy(cities)
    # 2optを三回繰り返すことで交差する点を減らす
    for _ in range(5):
        optimized_cities = two_opt(optimized_cities)

        path = []          
        for c in optimized_cities:
            path.append(c[0])
    return path
    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    # tour = greedy(read_input(sys.argv[1])) #貪欲法でけいろをもとめる
    # optimized_tour = two_opt(tour) #2-optで最適化する
    tour = solve_tsp(read_input(sys.argv[1]))
    # print_tour(tour)

    #csvファイルに出力する
    output_filename = sys.argv[1].replace("input", "output")

    with open(output_filename, "w") as f:
        f.write(format_tour(tour))
    print("Done")