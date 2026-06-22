import sys
import math
import random

from common import print_tour, read_input, format_tour

# citiesの各位置情報にインデックスを付与する関数
def give_index_cities(cities):
    index_cities = [] # 各要素：(index, [x,y])
    for i in range(len(cities)):
        index_cities.append((i, list(cities[i])))
    return index_cities


# 2点間のユークリッド距離を求める関数
def calurate_euclidean_distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)


# 各都市の距離を求める関数
def calcurate_distance(cities):
    num_cities = len(cities)
    distance_matrix = [[0]*num_cities for _ in range(num_cities)] 

    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = calurate_euclidean_distance(cities[i], cities[j])
            distance_matrix[i][j] = distance_matrix[j][i] = distance
    return distance_matrix


# 貪欲法で初期経路を求める関数
def greedy(cities, dist, index_cities):
    current_city = 0
    unvisited = set(range(1, len(cities)))
    path = [index_cities[0]]

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        unvisited.remove(next_city)
        path.append(index_cities[next_city])
        current_city = next_city

    return path


# 現在の経路の総距離を計算する関数（評価関数）
def get_total_distance(path, dist):
    total = 0
    num_cities = len(path)
    for i in range(num_cities):
        # path[i][0] は元の都市のインデックス
        c1 = path[i][0]
        c2 = path[(i + 1) % num_cities][0] # 最後の都市から最初の都市へ戻る
        total += dist[c1][c2]
    return total


# 焼きなまし法（Simulated Annealing）
def simulated_annealing(init_path, dist, steps=100000, init_temp=100.0, cool_rate=0.9999):
    """
    init_path: 貪欲法などで作った初期解 [(idx, [x,y]), ...]
    dist: 距離行列
    steps: ループ回数
    init_temp: 初期温度
    cool_rate: 冷却率（1に近いほどゆっくり冷える）
    """
    current_path = list(init_path)
    current_dist = get_total_distance(current_path, dist)
    
    # 探索中の一番良い解を保持する変数
    best_path = list(current_path)
    best_dist = current_dist
    
    num_cities = len(current_path)
    T = init_temp

    for step in range(steps):
        # 2-opt近傍からランダムに2つの位置を選択（経路を反転させる範囲 [i+1, j]）
        i = random.randint(0, num_cities - 2)
        j = random.randint(i + 1, num_cities - 1)
        
        if i == 0 and j == num_cities - 1:
            continue # 経路全体を反転させても結果が変わらないためスキップ

        # 差分だけを計算して高速化
        c_i = current_path[i][0]
        c_i1 = current_path[i+1][0]
        c_j = current_path[j][0]
        c_j1 = current_path[(j+1) % num_cities][0]

        # 入れ替え前のエッジの長さ
        before = dist[c_i][c_i1] + dist[c_j][c_j1]
        # 入れ替え後のエッジの長さ
        after = dist[c_i][c_j] + dist[c_i1][c_j1]
        
        # 距離の変動量（負なら改善、正なら改悪）
        diff = after - before
        
        # 受け入れ判定
        # 改善（diff < 0）しているか、確率（メトロポリス基準）をパスした場合
        if diff < 0 or random.random() < math.exp(-diff / T):
            # 実際に経路を反転
            current_path[i+1:j+1] = reversed(current_path[i+1:j+1])
            current_dist += diff
            
            # 最良解の更新
            if current_dist < best_dist:
                best_dist = current_dist
                best_path = list(current_path)
                
        # 温度の更新（指数冷却）
        T *= cool_rate

    print(f"Initial Distance (Greedy): {get_total_distance(init_path, dist):.2f}")
    print(f"Optimized Distance (SA): {best_dist:.2f}")
    return best_path


def solve_tsp(cities):
    # 距離行列の計算
    dist = calcurate_distance(cities)
    index_cities = give_index_cities(cities)
    
    # 1. 貪欲法で初期解を作成
    init_path = greedy(cities, dist, index_cities)
    
    # 2. 焼きなまし法で最適化 (都市数や実行時間に応じてstepsやcool_rateを調整してください)
    # 都市数が数百程度であれば、steps=100000〜500000程度で高速かつ綺麗に解けます
    optimized_cities = simulated_annealing(init_path, dist, steps=200000, init_temp=50.0, cool_rate=0.99995)

    path = []          
    for c in optimized_cities:
        path.append(c[0])
    return path
    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve_tsp(read_input(sys.argv[1]))

    # csvファイルに出力する
    output_filename = sys.argv[1].replace("input", "output")

    with open(output_filename, "w") as f:
        f.write(format_tour(tour))
    print("Done")