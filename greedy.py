#================================
# TSPを貪欲法+2optで実装したコード
# python3 greedy.py input_0.csv
#================================

import sys
import math

from common import print_tour, read_input

# citiesの各位置情報にインデックスを付与する関数
def give_index_cities(cities):
    index_cities = [] # 各要素：(index, [x,y])
    for i in range(len(cities)):
        index_cities.append((i, cities[i]))
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
        for j in range(i, num_cities):
            distance = calurate_euclidean_distance(cities[i], cities[j]) # ユーグリッド距離を求める
            distance_matrix[i][j] = distance_matrix[j][i] = distance # iからj、jからiの距離を記録
    return distance_matrix


def greedy(cities):
    # Build a trivial solution.
    # Visit the cities in the order they appear in the input.
    print("入力確認")
    print(cities)
    # print("情報確認")
    dist = calcurate_distance(cities) # 都市間のユーグリッド距離を求める
    # print(dist) OK
    # index_cities = give_index_cities(cities) #都市の位置とインデックスを対応付ける
    # print(index_cities)
    current_city = 0 #スタートを設定
    unvisited = set(range(1, len(cities))) # 訪れていない都市のインデックスを格納
    path = [] # どのような経路で回るか格納（インデックスを格納する）

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        unvisited.remove(next_city)
        path.append(next_city)

    return path


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = greedy(read_input(sys.argv[1]))
    print_tour(tour)