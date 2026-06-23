#================================
# TSPを貪欲法+2optで実装したコード（閉路対応・改善ループ版）
# python3 greedy.py input_0.csv 
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

    return path, dist # 2-optでも使い回すために距離行列(dist)も返す

def two_opt(cities, dist_matrix): # 入力に距離行列を追加
    len_cities = len(cities)
    improved = True

    # 改善が完全になくなるまで（1周してもどこも入れ替わらなくなるまで）ループ
    while improved:
        improved = False
        
        for i in range(len_cities):
            # 閉路（末尾から先頭への繋がり）を考慮するため、jの範囲を末尾まで広げる
            for j in range(i + 2, len_cities + (1 if i > 0 else 0)):
                
                idx_i = i
                idx_i_next = (i + 1) % len_cities
                idx_j = j % len_cities
                idx_j_next = (j + 1) % len_cities
                
                # 元の都市インデックスを取得
                city_a = cities[idx_i][0]
                city_b = cities[idx_i_next][0]
                city_c = cities[idx_j][0]
                city_d = cities[idx_j_next][0]

                # 事前に計算した距離行列から距離を取得（計算の高速化）
                before = dist_matrix[city_a][city_b] + dist_matrix[city_c][city_d]
                after = dist_matrix[city_a][city_c] + dist_matrix[city_b][city_d]

                if before > after: # 入れ替えたほうが距離が短くなる時
                    # idx_i_next から idx_j までの要素を反転させる
                    start = i + 1
                    end = j
                    while start < end:
                        cities[start % len_cities], cities[end % len_cities] = cities[end % len_cities], cities[start % len_cities]
                        start += 1
                        end -= 1
                    
                    improved = True # 改善があったフラグを立てる
    
    return cities

def solve_tsp(cities):
    # まず貪欲法で経路を出す（距離行列も一緒に受け取る）
    optimized_cities, dist_matrix = greedy(cities)
    
    # 改善がなくなるまで徹底的に2optを回す（引数に距離行列を渡す）
    optimized_cities = two_opt(optimized_cities, dist_matrix)

    path = []          
    for c in optimized_cities:
        path.append(c[0])

    total_dist = 0
    num_cities = len(path)
    for i in range(num_cities):
        city_current = path[i]
        city_next = path[(i + 1) % num_cities] # % を使うことで、最後は自動的に0番目に戻る
        total_dist += dist_matrix[city_current][city_next]
    
    print(f"Total Distance: {total_dist:.2f}") # 小数点2桁まで画面に出力

    return path
    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve_tsp(read_input(sys.argv[1]))

    #csvファイルに出力する
    output_filename = sys.argv[1].replace("input", "output")

    with open(output_filename, "w") as f:
        f.write(format_tour(tour))
    print("Done")