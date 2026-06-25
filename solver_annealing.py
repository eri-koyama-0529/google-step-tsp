# import sys
# import math
# import random

# # commonモジュールがない環境でもエラーにならないようフォールバックを設定
# try:
#     from common import print_tour, read_input, format_tour
# except ImportError:
#     # テスト用にダミーの関数を定義（環境に合わせて適宜削除してください）
#     def read_input(filename): return [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(200)]
#     def format_tour(tour): return "\n".join(map(str, tour))

# # citiesの各位置情報にインデックスを付与する関数
# def give_index_cities(cities):
#     index_cities = [] # 各要素：(index, [x,y])
#     for i in range(len(cities)):
#         index_cities.append((i, list(cities[i])))
#     return index_cities


# # 2点間のユークリッド距離を求める関数
# def calurate_euclidean_distance(city1, city2):
#     return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)


# # 各都市の距離を求める関数と、高速化用の隣接リストを作成する関数
# def calcurate_distance(cities):
#     num_cities = len(cities)
#     distance_matrix = [[0]*num_cities for _ in range(num_cities)] 

#     for i in range(num_cities):
#         for j in range(i+1, num_cities):
#             distance = calurate_euclidean_distance(cities[i], cities[j])
#             distance_matrix[i][j] = distance_matrix[j][i] = distance
            
#     # 【高速化のキモ】各都市から距離が近い順に都市のインデックスをソートしたリストを作成
#     nearest_neighbors = []
#     for i in range(num_cities):
#         # (距離, 都市インデックス) のリストを作ってソート
#         neighbors = sorted([(distance_matrix[i][j], j) for j in range(num_cities) if i != j])
#         # 都市インデックスだけを抽出
#         nearest_neighbors.append([dummy_idx for dist, dummy_idx in neighbors])

#     return distance_matrix, nearest_neighbors


# # 🌟 高速化した貪欲法（隣接リストを利用）
# def greedy(cities, dist, nearest_neighbors, start_city):
#     num_cities = len(cities)
#     visited = [False] * num_cities
    
#     current_city = start_city
#     visited[current_city] = True
#     path_indexes = [current_city]

#     # 全都市を訪問するまでループ
#     while len(path_indexes) < num_cities:
#         next_city = None
#         # 近い順にソートされたリストをスキャンして、未訪問の都市を即座に見つける
#         for neighbor in nearest_neighbors[current_city]:
#             if not visited[neighbor]:
#                 next_city = neighbor
#                 break
        
#         # 万が一見つからなかった場合の安全策（基本は通らない）
#         if next_city == None:
#             for i in range(num_cities):
#                 if not visited[i]:
#                     next_city = i
#                     break

#         visited[next_city] = True
#         path_indexes.append(next_city)
#         current_city = next_city

#     # 元のコードの形式 [(idx, [x,y]), ...] に変換して返す
#     return [(idx, list(cities[idx])) for idx in path_indexes]


# # 現在の経路の総距離を計算する関数（評価関数）
# def get_total_distance(path, dist):
#     total = 0
#     num_cities = len(path)
#     for i in range(num_cities):
#         c1 = path[i][0]
#         c2 = path[(i + 1) % num_cities][0]
#         total += dist[c1][c2]
#     return total


# # 焼きなまし法（Simulated Annealing）
# def simulated_annealing(init_path, dist, steps=100000, init_temp=100.0, cool_rate=0.9999):
#     current_path = list(init_path)
#     current_dist = get_total_distance(current_path, dist)
    
#     best_path = list(current_path)
#     best_dist = current_dist
    
#     num_cities = len(current_path)
#     T = init_temp

#     print("--- Simulated Annealing Start ---")
#     for step in range(steps):
#         i = random.randint(0, num_cities - 2)
#         j = random.randint(i + 1, num_cities - 1)
        
#         if i == 0 and j == num_cities - 1:
#             continue

#         c_i = current_path[i][0]
#         c_i1 = current_path[i+1][0]
#         c_j = current_path[j][0]
#         c_j1 = current_path[(j+1) % num_cities][0]

#         before = dist[c_i][c_i1] + dist[c_j][c_j1]
#         after = dist[c_i][c_j] + dist[c_i1][c_j1]
        
#         diff = after - before
        
#         if diff < 0 or random.random() < math.exp(-diff / T):
#             current_path[i+1:j+1] = reversed(current_path[i+1:j+1])
#             current_dist += diff
            
#             if current_dist < best_dist:
#                 best_dist = current_dist
#                 best_path = list(current_path)
                
#         T *= cool_rate

#         if step % 200000 == 0:
#             print(f"Step: {step:6d} | Temp: {T:8.3f} | Current Dist: {current_dist:.2f} | Best Dist: {best_dist:.2f}")

#     print(f"Initial Distance (Greedy): {get_total_distance(init_path, dist):.2f}")
#     print(f"Optimized Distance (SA): {best_dist:.2f}")
#     return best_path


# # 🌟 高速化した2-opt（改善しても即breakせずループを継続）
# def local_search_2opt(init_path, dist):
#     current_path = list(init_path)
#     num_cities = len(current_path)
#     improved = True
    
#     print("--- Post-processing 2-opt Start ---")
#     while improved:
#         improved = False
#         for i in range(num_cities - 2):
#             for j in range(i + 2, num_cities):
#                 if i == 0 and j == num_cities - 1:
#                     continue
                
#                 c_i = current_path[i][0]
#                 c_i1 = current_path[i+1][0]
#                 c_j = current_path[j][0]
#                 c_j1 = current_path[(j+1) % num_cities][0]

#                 before = dist[c_i][c_i1] + dist[c_j][c_j1]
#                 after = dist[c_i][c_j] + dist[c_i1][c_j1]
                
#                 if after < before:
#                     current_path[i+1:j+1] = reversed(current_path[i+1:j+1])
#                     improved = True
#                     # 💡 ここにあった break を削除し、1周の探索で直せる場所を全て直す
                    
#     print(f"Final Distance (After 2-opt): {get_total_distance(current_path, dist):.2f}")
#     return current_path

# def local_search_2opt_fast(init_path, dist, nearest_neighbors):
#     """
#     全探索ではなく、各都市の近傍（上位20台）のみをターゲットにして2-optを行う超高速版
#     """
#     current_path = list(init_path)
#     num_cities = len(current_path)
    
#     # 都市番号から、現在のpath内でのインデックス（位置）を逆引きできる配列
#     pos = [0] * num_cities
#     for idx, (city_idx, _) in enumerate(current_path):
#         pos[city_idx] = idx

#     improved = True
#     print("--- Fast Post-processing 2-opt Start ---")
    
#     # 近傍サイズ（近くの何件を候補にするか）。20〜50程度がバランスが良い
#     K = min(30, num_cities - 1)
    
#     while improved:
#         improved = False
#         for i in range(num_cities):
#             c_i = current_path[i][0]
#             c_i1 = current_path[(i + 1) % num_cities][0]
            
#             # 全都市を回るのではなく、c_i から本当に近い都市だけを相手にする
#             for count, c_j in enumerate(nearest_neighbors[c_i]):
#                 if count >= K: 
#                     break
                
#                 # c_j が現在の経路のどこにいるかを取得
#                 j = pos[c_j]
                
#                 # 2-optが成立する位置関係かチェック
#                 if i == j or (i + 1) % num_cities == j or (j + 1) % num_cities == i:
#                     continue
                
#                 c_j1 = current_path[(j + 1) % num_cities][0]
                
#                 # インデックスの順序を揃える (i < j になるように調整)
#                 idx_i, idx_j = i, j
#                 if idx_i > idx_j:
#                     # ラップアラウンドを考慮する必要があるが、簡易的にスキップするか順序を考慮
#                     continue 

#                 before = dist[c_i][c_i1] + dist[c_j][c_j1]
#                 after = dist[c_i][c_j] + dist[c_i1][c_j1]
                
#                 if after < before:
#                     # 経路の反転
#                     current_path[idx_i+1:idx_j+1] = reversed(current_path[idx_i+1:idx_j+1])
                    
#                     # 逆引き位置テーブル（pos）の更新
#                     for k in range(idx_i + 1, idx_j + 1):
#                         pos[current_path[k][0]] = k
                        
#                     improved = True
#                     c_i1 = current_path[(idx_i + 1) % num_cities][0] # 次のために更新
                    
#     return current_path


# def solve_tsp(cities):
#     # 距離行列と隣接リストの計算
#     dist, nearest_neighbors = calcurate_distance(cities)
#     index_cities = give_index_cities(cities)
#     num_cities = len(cities)
    
#     best_overall_path = None
#     best_overall_dist = float('inf')
    
#     # ==================================================
#     # 🏁【予選フェーズ】すべての都市からGreedyのスコアを計測（高速化済み）
#     # ==================================================
#     print(f"⏱️ ====== Running Preliminary Greedy Filter for All {num_cities} Cities ======")
#     greedy_results = []
    
#     for idx in range(num_cities):
#         # 高速化したgreedyにスタート都市のインデックスを直接渡す
#         temp_path = greedy(cities, dist, nearest_neighbors, idx)
#         temp_dist = get_total_distance(temp_path, dist)
#         greedy_results.append((temp_dist, idx))
    
#     greedy_results.sort()
#     num_starts = min(5, num_cities)
#     # best_candidates = [idx for score, idx in greedy_results[:num_starts]]
#     # 上位2件＋ランダムに選んだ3件 を候補にする
#     best_candidates = [idx for score, idx in greedy_results[:50]]
#     # while len(best_candidates) < 10:
#     #     rand_idx = random.randint(0, num_cities - 1)
#     #     if rand_idx not in best_candidates:
#     #         best_candidates.append(rand_idx)
    
#     print(f"🎯 Elite Candidates Selected (Start City Indexes): {best_candidates}")
#     print(f"🚀 ====== Start Multi-Start Optimization (Total Starts: {num_starts}) ======")
    
#     for start_idx in best_candidates:
#         print(f"\n==================================================")
#         print(f"▶️ Launching Search from Start City Index: {start_idx}")
#         print(f"==================================================")
        
#         # 1. 貪欲法で初期解を作成
#         current_path = greedy(cities, dist, nearest_neighbors, start_idx)
        
#         total_cycles = 3
        
#         print(f"======= Start Iterative Optimization (Total Cycles: {total_cycles}) =======")
#         for cycle in range(total_cycles):
#             print(f"\n--- [Start {start_idx} / Cycle {cycle + 1} / {total_cycles}] ---")
            
#             cycle_init_temp = 500.0 if cycle == 0 else 2.0
            
#             # ① 焼きなまし法を実行
#             current_path = simulated_annealing(
#                 current_path, 
#                 dist, 
#                 steps=1000000, 
#                 init_temp=cycle_init_temp, 
#                 cool_rate=0.999995
#             )
            
#             # ② 2-optで完全に詰め切る（都市数に応じてアルゴリズムを自動切り替え）
#             if num_cities < 3000:
#                 # 都市数が短い（1500未満）時は精度の高い全探索2-opt
#                 current_path = local_search_2opt(current_path, dist)
#             else:
#                 # 都市数が長い（1500以上）時は近傍制限をかけた超高速2-opt
#                 current_path = local_search_2opt_fast(current_path, dist, nearest_neighbors)
            
#             cycle_dist = get_total_distance(current_path, dist)
            
#             if cycle_dist < best_overall_dist:
#                 best_overall_dist = cycle_dist
#                 best_overall_path = list(current_path)
#                 print(f"✨ Global Best Updated! New Best Distance: {best_overall_dist:.2f}")

#     print(f"\n======= All Starts and Cycles Completed =======")
#     print(f"Absolute Best Distance: {best_overall_dist:.2f}")

#     path = []          
#     for c in best_overall_path:
#         path.append(c[0])
#     return path
    

# if __name__ == '__main__':
#     # コマンドライン引数がない場合、テスト実行できるように設定
#     if len(sys.argv) > 1:
#         input_data = read_input(sys.argv[1])
#         output_filename = sys.argv[1].replace("input", "output")
#     else:
#         print("No input file specified. Running with dummy data for test.")
#         input_data = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(200)]
#         output_filename = "output_dummy.csv"

#     tour = solve_tsp(input_data)

#     with open(output_filename, "w") as f:
#         f.write(format_tour(tour))
#     print("Done")

import sys
import math
import random

try:
    from common import print_tour, read_input, format_tour
except ImportError:
    # commonモジュールがない場合のテスト用ダミー
    def read_input(filename): return [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(200)]
    def format_tour(tour): return "\n".join(map(str, tour))

# citiesの各位置情報にインデックスを付与する関数
def give_index_cities(cities):
    index_cities = []
    for i in range(len(cities)):
        index_cities.append((i, list(cities[i])))
    return index_cities


# 2点間のユークリッド距離を求める関数
def calurate_euclidean_distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)


# 各都市の距離を求める関数と、高速化用の隣接リストを作成する関数
def calcurate_distance(cities):
    num_cities = len(cities)
    distance_matrix = [[0]*num_cities for _ in range(num_cities)] 

    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = calurate_euclidean_distance(cities[i], cities[j])
            distance_matrix[i][j] = distance_matrix[j][i] = distance
            
    # 各都市から距離が近い順に都市のインデックスをソートしたリストを作成
    nearest_neighbors = []
    for i in range(num_cities):
        neighbors = sorted([(distance_matrix[i][j], j) for j in range(num_cities) if i != j])
        nearest_neighbors.append([dummy_idx for dist, dummy_idx in neighbors])

    return distance_matrix, nearest_neighbors


# 高速化した貪欲法（隣接リストを利用）
def greedy(cities, dist, nearest_neighbors, start_city):
    num_cities = len(cities)
    visited = [False] * num_cities
    
    current_city = start_city
    visited[current_city] = True
    path_indexes = [current_city]

    while len(path_indexes) < num_cities:
        next_city = None
        for neighbor in nearest_neighbors[current_city]:
            if not visited[neighbor]:
                next_city = neighbor
                break
        
        if next_city == None:
            for i in range(num_cities):
                if not visited[i]:
                    next_city = i
                    break

        visited[next_city] = True
        path_indexes.append(next_city)
        current_city = next_city

    return [(idx, list(cities[idx])) for idx in path_indexes]


# 現在の経路の総距離を計算する関数（評価関数）
def get_total_distance(path, dist):
    total = 0
    num_cities = len(path)
    for i in range(num_cities):
        c1 = path[i][0]
        c2 = path[(i + 1) % num_cities][0]
        total += dist[c1][c2]
    return total


# 焼きなまし法（Simulated Annealing）
def simulated_annealing(init_path, dist, steps=1000000, init_temp=100.0, cool_rate=0.999995):
    current_path = list(init_path)
    current_dist = get_total_distance(current_path, dist)
    
    best_path = list(current_path)
    best_dist = current_dist
    
    num_cities = len(current_path)
    T = init_temp

    print("--- Simulated Annealing Start ---")
    for step in range(steps):
        i = random.randint(0, num_cities - 2)
        j = random.randint(i + 1, num_cities - 1)
        
        if i == 0 and j == num_cities - 1:
            continue

        c_i = current_path[i][0]
        c_i1 = current_path[i+1][0]
        c_j = current_path[j][0]
        c_j1 = current_path[(j+1) % num_cities][0]

        before = dist[c_i][c_i1] + dist[c_j][c_j1]
        after = dist[c_i][c_j] + dist[c_i1][c_j1]
        
        diff = after - before
        
        if diff < 0 or random.random() < math.exp(-diff / T):
            current_path[i+1:j+1] = reversed(current_path[i+1:j+1])
            current_dist += diff
            
            if current_dist < best_dist:
                best_dist = current_dist
                best_path = list(current_path)
                
        T *= cool_rate

        if step % 200000 == 0:
            print(f"Step: {step:6d} | Temp: {T:8.3f} | Current Dist: {current_dist:.2f} | Best Dist: {best_dist:.2f}")

    print(f"Initial Distance: {get_total_distance(init_path, dist):.2f}")
    print(f"Optimized Distance (SA): {best_dist:.2f}")
    return best_path


# ① 通常の2-opt（全探索版：小〜中規模都市用）
def local_search_2opt(init_path, dist):
    current_path = list(init_path)
    num_cities = len(current_path)
    improved = True
    
    print("--- Post-processing 2-opt (Full Search) Start ---")
    while improved:
        improved = False
        for i in range(num_cities - 2):
            for j in range(i + 2, num_cities):
                if i == 0 and j == num_cities - 1:
                    continue
                
                c_i = current_path[i][0]
                c_i1 = current_path[i+1][0]
                c_j = current_path[j][0]
                c_j1 = current_path[(j+1) % num_cities][0]

                before = dist[c_i][c_i1] + dist[c_j][c_j1]
                after = dist[c_i][c_j] + dist[c_i1][c_j1]
                
                if after < before:
                    current_path[i+1:j+1] = reversed(current_path[i+1:j+1])
                    improved = True
                    
    print(f"Final Distance (After 2-opt): {get_total_distance(current_path, dist):.2f}")
    return current_path


# ② 【追加】超高速版2-opt（近傍制限版：8192都市などの大規模用）
def local_search_2opt_fast(init_path, dist, nearest_neighbors):
    current_path = list(init_path)
    num_cities = len(current_path)
    
    pos = [0] * num_cities
    for idx, (city_idx, _) in enumerate(current_path):
        pos[city_idx] = idx

    improved = True
    print("--- Fast Post-processing 2-opt (Nearest Neighbor) Start ---")
    
    K = min(30, num_cities - 1) # 近傍サイズ
    
    while improved:
        improved = False
        for i in range(num_cities):
            c_i = current_path[i][0]
            c_i1 = current_path[(i + 1) % num_cities][0]
            
            for count, c_j in enumerate(nearest_neighbors[c_i]):
                if count >= K: 
                    break
                
                j = pos[c_j]
                if i == j or (i + 1) % num_cities == j or (j + 1) % num_cities == i:
                    continue
                
                idx_i, idx_j = i, j
                if idx_i > idx_j:
                    continue 

                c_j1 = current_path[(idx_j + 1) % num_cities][0]

                before = dist[c_i][c_i1] + dist[c_j][c_j1]
                after = dist[c_i][c_j] + dist[c_i1][c_j1]
                
                if after < before:
                    current_path[idx_i+1:idx_j+1] = reversed(current_path[idx_i+1:idx_j+1])
                    for k in range(idx_i + 1, idx_j + 1):
                        pos[current_path[k][0]] = k
                    improved = True
                    c_i1 = current_path[(idx_i + 1) % num_cities][0]
                    
    print(f"Final Distance (After Fast 2-opt): {get_total_distance(current_path, dist):.2f}")
    return current_path


def solve_tsp(cities):
    dist, nearest_neighbors = calcurate_distance(cities)
    index_cities = give_index_cities(cities)
    num_cities = len(cities)
    
    best_overall_path = None
    best_overall_dist = float('inf')
    
    # ==================================================
    # 🏁【予選フェーズ】
    # ==================================================
    print(f"⏱️ ====== Running Preliminary Greedy Filter ======")
    greedy_results = []
    
    # 【修正点1】都市数が多い場合はランダムに30件だけサンプリングしてフリーズを防ぐ
    if num_cities < 1000:
        search_targets = range(num_cities)
    else:
        search_targets = random.sample(range(num_cities), 30)
    
    for idx in search_targets:
        temp_path = greedy(cities, dist, nearest_neighbors, idx)
        temp_dist = get_total_distance(temp_path, dist)
        greedy_results.append((temp_dist, idx))
    
    greedy_results.sort()
    
    # 🌟【マルチスタート件数の自動調整】
    # 小さい時は上位50件、8192都市など大きい時は上位20件にする（時間短縮のため）
    max_candidates = 50 if num_cities < 2049 else 20
    num_starts = min(max_candidates, len(greedy_results))
    best_candidates = [idx for score, idx in greedy_results[:num_starts]]
    
    print(f"🎯 Elite Candidates Selected: {best_candidates}")
    print(f"🚀 ====== Start Multi-Start Optimization (Total Starts: {num_starts}) ======")
    
    for start_idx in best_candidates:
        print(f"\n==================================================")
        print(f"▶️ Launching Search from Start City Index: {start_idx}")
        print(f"==================================================")
        
        current_path = greedy(cities, dist, nearest_neighbors, start_idx)
        total_cycles = 3
        
        for cycle in range(total_cycles):
            print(f"\n--- [Start {start_idx} / Cycle {cycle + 1} / {total_cycles}] ---")
            
            # 【検証成功設定】1回目は大破壊(500度)、2回目以降は微調整(2.0度)
            cycle_init_temp = 500.0 if cycle == 0 else 2.0
            
            # ① 焼きなまし法を実行
            current_path = simulated_annealing(
                current_path, 
                dist, 
                steps=1000000, 
                init_temp=cycle_init_temp, 
                cool_rate=0.999995
            )
            
            # ② 【修正点2】都市数に応じて、通常2-optと高速2-optを自動切り替え
            if num_cities < 1500:
                current_path = local_search_2opt(current_path, dist)
            else:
                current_path = local_search_2opt_fast(current_path, dist, nearest_neighbors)
            
            cycle_dist = get_total_distance(current_path, dist)
            
            if cycle_dist < best_overall_dist:
                best_overall_dist = cycle_dist
                best_overall_path = list(current_path)
                print(f"✨ Global Best Updated! New Best Distance: {best_overall_dist:.2f}")

    print(f"\n======= All Starts and Cycles Completed =======")
    print(f"Absolute Best Distance: {best_overall_dist:.2f}")

    path = []          
    for c in best_overall_path:
        path.append(c[0])
    return path
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_data = read_input(sys.argv[1])
        output_filename = sys.argv[1].replace("input", "output")
    else:
        print("No input file specified. Running with dummy data for test.")
        input_data = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(8192)] # 8192都市テスト
        output_filename = "output_dummy.csv"

    tour = solve_tsp(input_data)

    with open(output_filename, "w") as f:
        f.write(format_tour(tour))
    print("Done")